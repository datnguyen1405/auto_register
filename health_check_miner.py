import socket

import requests

TELEGRAM_BOT_TOKEN = '7163368588:AAGqO6rMA-2CS'
TELEGRAM_GROUP_ID = '-41452'


def send_alert(host, port, key_name):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_GROUP_ID,
        'text': f"CẢNH BÁO: Không thể kết nối đến miner {host}:{port} - KEY: {key_name}. Vui lòng kiểm tra!"
    }
    response = requests.post(url, json=payload)
    return response.json()


def check_connection(host, port, key_name):
    max_attempts = 3  # Số lần thử tối đa
    attempt_count = 0  # Bắt đầu đếm từ 0
    while attempt_count < max_attempts:
        try:
        # Tạo một socket sử dụng IPv4 và TCP
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Thiết lập thời gian chờ cho kết nối
                s.settimeout(10)  # Thời gian chờ tối đa là 10 giây
                # Thử kết nối đến host và port
                s.connect((host, port))
                print(f"Kết nối thành công đến miner {host}:{port} - KEY: {key_name}")
                return True
        except socket.error as err:
            attempt_count += 1
            print(f"Không thể kết nối đến miner {host}:{port} - KEY: {key_name} - {err}")
            if attempt_count == max_attempts:
                send_alert(host, port, key_name)
    return False


# Địa chỉ IP và cổng cần kiểm tra
# Cần update ngay khi có thay đổi

# Gọi hàm kiểm tra kết nối
hosts_and_ports = [
    # sub32-long
    ("85.167.195.137", 41103, "sub32_longdh1_k1"),
]
for host, port, key_name in hosts_and_ports:
    is_connected = check_connection(host, port, key_name)
