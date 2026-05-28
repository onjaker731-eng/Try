import socket
import cv2
import numpy as np
import time

# Список адрес для автоматичної перевірки
POSSIBLE_HOSTS = ['127.0.0.1', '192.168.1.8']
PORT = 9999

client_socket = None

print("Пошук сервера...")

# Цикл автоматичного підключення
for host in POSSIBLE_HOSTS:
    try:
        print(f"Спроба підключення до {host}:{PORT}...")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Встановлюємо таймаут 2 секунди, щоб довго не чекати на закритих адресах
        client_socket.settimeout(2.0) 
        client_socket.connect((host, PORT))
        
        # Якщо підключилися успішно, повертаємо нормальний режим роботи без таймаутів
        client_socket.settimeout(None)
        print(f"[УСПІХ] Підключено до сервера на адресі: {host}")
        print("Чекаємо натискання кнопки 'Старт' на сервері...")
        break
    except Exception:
        print(f"[ВІДХИЛЕНО] Сервер на {host} не відповідає.")
        client_socket.close()
        client_socket = None

# Якщо жодна адреса не підійшла
if client_socket is None:
    print("\n[ПОМИЛКА] Не вдалося знайти запущений сервер.")
    print("Перевірте, чи запущено server.py і чи не блокує його брандмауер.")
    input("\nНатисніть Enter для виходу...")
    exit()

# Головний цикл прийому відео (залишається без змін)
try:
    while True:
        raw_msg_len = client_socket.recv(4)
        if not raw_msg_len:
            print("Трансляцію завершено сервером або з'єднання розірвано.")
            break
        msg_len = int.from_bytes(raw_msg_len, byteorder='little')
        
        data = b''
        while len(data) < msg_len:
            packet = client_socket.recv(msg_len - len(data))
            if not packet:
                break
            data += packet
            
        narray = np.frombuffer(data, dtype=np.uint8)
        frame = cv2.imdecode(narray, cv2.IMREAD_COLOR)
        
        if frame is not None:
            cv2.imshow("Трансляція камери", frame)
            
        if cv2.waitKey(1) == ord('q'):
            print("Клієнт закрив вікно трансляції.")
            break
            
finally:
    cv2.destroyAllWindows()
    if client_socket:
        client_socket.close()
