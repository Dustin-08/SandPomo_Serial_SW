import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports
import time

BAUD_RATE = 115200  # H/W 코드와 일치시켜야 함

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    port_list = []
    for port in ports:
        label = f"{port.device} ({port.description})"
        port_list.append(label)
    return port_list

def get_device_from_label(label):
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
    session = session_entry.get()
    brk = break_entry.get()
    if not (session.isdigit() and brk.isdigit()):
        status_label.config(text="숫자를 입력하세요.", fg="red")
        return
    try:
        # "Session,Break\n" 형식으로 전송
        ser.write(f"{session} {brk}\n".encode())
        status_label.config(text=f"Session: {session}분, Break: {brk}분 전송 완료", fg="yellow")
    except Exception as e:
        status_label.config(text=f"전송 실패: {e}", fg="red")

def refresh_ports():
    port_combo['values'] = list_serial_ports()
    status_label.config(text="포트 목록 갱신", fg="black")

def validate_entries(*args):
    session = session_var.get()
    brk = break_var.get()
    if session.isdigit() and brk.isdigit() and int(session) > 0 and int(brk) > 0:
        send_button.config(state="normal")
    else:
        send_button.config(state="disabled")

root = tk.Tk()
root.title("SandPomo")

title_label = tk.Label(root, text="SandPomo", font=("Arial", 18, "bold"))
title_label.grid(row=0, column=0, columnspan=4, pady=10)

tk.Label(root, text="포트 선택").grid(row=1, column=0, padx=5, pady=5)
port_combo = ttk.Combobox(root, width=35, state="readonly")
port_combo['values'] = list_serial_ports()
port_combo.grid(row=1, column=1, padx=5, pady=5, columnspan=2)
refresh_button = tk.Button(root, text="새로고침", command=refresh_ports)
refresh_button.grid(row=1, column=3, padx=5, pady=5)

connect_button = tk.Button(root, text="연결", command=connect_serial)
connect_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew", columnspan=2)

# Session과 Break 입력을 위한 중앙 Frame 생성
input_frame = tk.Frame(root)
input_frame.grid(row=3, column=0, columnspan=4, pady=20)

# Session 입력 (라벨과 Entry를 나란히 배치)
session_label = tk.Label(input_frame, text="Session 시간 입력:")
session_label.grid(row=0, column=0, padx=5, pady=5)
session_var = tk.StringVar()
session_var.trace_add('write', validate_entries)
session_entry = tk.Entry(input_frame, width=10, textvariable=session_var, justify="center")
session_entry.grid(row=0, column=1, padx=5, pady=5)

# Break 입력 (라벨과 Entry를 나란히 배치)
break_label = tk.Label(input_frame, text="Break 시간 입력:")
break_label.grid(row=1, column=0, padx=5, pady=5)
break_var = tk.StringVar()
break_var.trace_add('write', validate_entries)
break_entry = tk.Entry(input_frame, width=10, textvariable=break_var, justify="center")
break_entry.grid(row=1, column=1, padx=5, pady=5)

# 전송 버튼도 Frame 안에 중앙 배치
send_button = tk.Button(input_frame, text="전송", command=send_time, state="disabled")
send_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

# 상태 라벨
status_label = tk.Label(root, text="", fg="blue")
status_label.grid(row=4, column=0, columnspan=4, pady=10)

ser = None

root.mainloop()
