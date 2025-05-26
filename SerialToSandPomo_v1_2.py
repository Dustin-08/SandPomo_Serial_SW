import tkinter as tk
import serial
import serial.tools.list_ports
import time

BAUD_RATE = 115200  # ESP32 기본 baudrate 예시

def find_esp32_port():
    # ESP32 계열 주요 VID/PID (필요시 추가)
    ESP32_IDS = [
        ('10C4', 'EA60'),  # CP210x (실리콘랩스, 자주 사용)
        ('1A86', '7523'),  # CH340 (클론)
        ('0403', '6001'),  # FTDI (일부)
        ('303A', '1001'),  # ESP32-S3 내장 CDC
        ('303A', '1002'),  # ESP32-C3 내장 CDC
        ('303A', '1003'),  # ESP32-S2 내장 CDC
    ]
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        vid = f"{port.vid:04X}" if port.vid else ""
        pid = f"{port.pid:04X}" if port.pid else ""
        if (vid, pid) in ESP32_IDS:
            return port.device
    # 못 찾으면 첫 번째 포트 반환(선택)
    if ports:
        return ports[0].device
    return None

def connect_serial():
    global ser
    port = find_esp32_port()
    if port:
        try:
            ser = serial.Serial(port, BAUD_RATE, timeout=1)
            time.sleep(2)
            status_label.config(text=f"{port} 연결 성공", fg="green")
        except Exception as e:
            ser = None
            status_label.config(text=f"연결 실패: {e}", fg="red")
    else:
        ser = None
        status_label.config(text="ESP32 포트 미감지", fg="red")

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

root = tk.Tk()
root.title("SandPomo")

title_label = tk.Label(root, text="SandPomo", font=("Arial", 18, "bold"))
title_label.grid(row=0, column=0, columnspan=3, pady=10)

session_label = tk.Label(root, text="Session 시간 입력")
session_label.grid(row=1, column=0, padx=5, pady=5)

entry = tk.Entry(root, width=10)
entry.grid(row=1, column=1, padx=5, pady=5)

send_button = tk.Button(root, text="전송", command=send_time)
send_button.grid(row=1, column=2, padx=5, pady=5)

status_label = tk.Label(root, text="", fg="blue")
status_label.grid(row=2, column=0, columnspan=3, pady=10)

ser = None
connect_serial()

root.mainloop()
