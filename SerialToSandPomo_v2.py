import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports
import time

BAUD_RATE = 115200  # 긱블 미니(ESP32-C3) 기준, 필요시 변경

def list_serial_ports():
    # 포트와 기기명(설명) 함께 반환
    ports = serial.tools.list_ports.comports()
    port_list = []
    for port in ports:
        # 예: 'COM3 (Silicon Labs CP210x USB to UART Bridge)'
        label = f"{port.device} ({port.description})"
        port_list.append(label)
    return port_list

def get_device_from_label(label):
    # 'COM3 (설명)' 중 'COM3'만 추출
    return label.split(' ')[0]

def connect_serial():
    global ser
    selected_label = port_combo.get()
    if not selected_label:
        status_label.config(text="포트를 선택하세요.", fg="red")
        return
    port = get_device_from_label(selected_label)
    try:
        ser = serial.Serial(port, BAUD_RATE, timeout=1)
        time.sleep(2)
        status_label.config(text=f"{port} 연결 성공", fg="green")
    except Exception as e:
        ser = None
        status_label.config(text=f"연결 실패: {e}", fg="red")

def send_time():
    if ser is None or not ser.is_open:
        status_label.config(text="시리얼 연결 안 됨", fg="red")
        return
    minutes = entry.get()
    if not minutes.isdigit():
        status_label.config(text="숫자를 입력하세요.", fg="red")
        return
    try:
        ser.write((minutes + '\n').encode())
        status_label.config(text=f"{minutes}분 전송 완료", fg="blue")
    except Exception as e:
        status_label.config(text=f"전송 실패: {e}", fg="red")

def refresh_ports():
    port_combo['values'] = list_serial_ports()
    status_label.config(text="포트 목록 갱신", fg="black")

root = tk.Tk()
root.title("SandPomo")

title_label = tk.Label(root, text="SandPomo", font=("Arial", 18, "bold"))
title_label.grid(row=0, column=0, columnspan=4, pady=10)

# 포트 선택 콤보박스
tk.Label(root, text="포트 선택").grid(row=1, column=0, padx=5, pady=5)
port_combo = ttk.Combobox(root, width=35, state="readonly")
port_combo['values'] = list_serial_ports()
port_combo.grid(row=1, column=1, padx=5, pady=5, columnspan=2)
refresh_button = tk.Button(root, text="새로고침", command=refresh_ports)
refresh_button.grid(row=1, column=3, padx=5, pady=5)

connect_button = tk.Button(root, text="연결", command=connect_serial)
connect_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew", columnspan=2)

session_label = tk.Label(root, text="Session 시간 입력")
session_label.grid(row=3, column=0, padx=5, pady=5)
entry = tk.Entry(root, width=10)
entry.grid(row=3, column=1, padx=5, pady=5)
send_button = tk.Button(root, text="전송", command=send_time)
send_button.grid(row=3, column=2, padx=5, pady=5)

status_label = tk.Label(root, text="", fg="blue")
status_label.grid(row=4, column=0, columnspan=4, pady=10)

ser = None

root.mainloop()
