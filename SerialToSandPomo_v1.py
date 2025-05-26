import tkinter as tk
import serial
import time

# 시리얼 포트와 보드레이트를 환경에 맞게 수정하세요.
SERIAL_PORT = 'COM4'  # 예: Windows는 'COM4', 리눅스는 '/dev/ttyACM0'
BAUD_RATE = 9600

# 시리얼 연결
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # 아두이노 초기화 대기
except Exception as e:
    ser = None
    print(f"시리얼 연결 실패: {e}")

def send_time():
    if ser is None:
        status_label.config(text="시리얼 연결 실패")
        return
    minutes = entry.get()
    if not minutes.isdigit():
        status_label.config(text="숫자를 입력하세요.")
        return
    try:
        ser.write((minutes + '\n').encode())  # 아두이노로 데이터 전송
        status_label.config(text=f"{minutes}분 전송 완료")
    except Exception as e:
        status_label.config(text=f"전송 실패: {e}")

root = tk.Tk()
root.title("SandPomo")

# 제목
title_label = tk.Label(root, text="SandPomo", font=("Arial", 18, "bold"))
title_label.grid(row=0, column=0, columnspan=3, pady=10)

# Session 시간 입력 라벨
session_label = tk.Label(root, text="Session 시간 입력")
session_label.grid(row=1, column=0, padx=5, pady=5)

# 입력창
entry = tk.Entry(root, width=10)
entry.grid(row=1, column=1, padx=5, pady=5)

# 전송 버튼
send_button = tk.Button(root, text="전송", command=send_time)
send_button.grid(row=1, column=2, padx=5, pady=5)

# 상태 표시 라벨
status_label = tk.Label(root, text="", fg="blue")
status_label.grid(row=2, column=0, columnspan=3, pady=10)

root.mainloop()
