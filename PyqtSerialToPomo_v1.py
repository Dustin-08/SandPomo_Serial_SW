import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLabel, QComboBox, QPushButton, QLineEdit, 
                             QFrame, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import serial
import serial.tools.list_ports
import time

class SandPomoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ser = None
        self.BAUD_RATE = 115200
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("SandPomo")
        self.setFixedSize(400, 300)
        
        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 타이틀 라벨
        title_label = QLabel("SandPomo")
        title_font = QFont("Arial", 18, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 포트 선택 섹션
        port_layout = QHBoxLayout()
        port_label = QLabel("포트 선택")
        self.port_combo = QComboBox()
        self.port_combo.setMinimumWidth(250)
        # refresh_ports() 호출을 여기서 제거
        
        refresh_button = QPushButton("새로고침")
        refresh_button.clicked.connect(self.refresh_ports)
        
        port_layout.addWidget(port_label)
        port_layout.addWidget(self.port_combo)
        port_layout.addWidget(refresh_button)
        main_layout.addLayout(port_layout)
        
        # 연결 버튼
        self.connect_button = QPushButton("연결")
        self.connect_button.clicked.connect(self.connect_serial)
        main_layout.addWidget(self.connect_button)
        
        # 입력 프레임
        input_frame = QFrame()
        input_layout = QGridLayout()
        input_frame.setLayout(input_layout)
        
        # Session 입력
        session_label = QLabel("Session 시간 입력:")
        self.session_entry = QLineEdit()
        self.session_entry.setMaximumWidth(100)
        self.session_entry.setAlignment(Qt.AlignCenter)
        self.session_entry.textChanged.connect(self.validate_entries)
        
        input_layout.addWidget(session_label, 0, 0)
        input_layout.addWidget(self.session_entry, 0, 1)
        
        # Break 입력
        break_label = QLabel("Break 시간 입력:")
        self.break_entry = QLineEdit()
        self.break_entry.setMaximumWidth(100)
        self.break_entry.setAlignment(Qt.AlignCenter)
        self.break_entry.textChanged.connect(self.validate_entries)
        
        input_layout.addWidget(break_label, 1, 0)
        input_layout.addWidget(self.break_entry, 1, 1)
        
        # 전송 버튼
        self.send_button = QPushButton("전송")
        self.send_button.setEnabled(False)
        self.send_button.clicked.connect(self.send_time)
        input_layout.addWidget(self.send_button, 2, 0, 1, 2)
        
        main_layout.addWidget(input_frame)
        
        # 상태 라벨 (UI 구성 마지막에 생성)
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # 여백 추가
        main_layout.addStretch()
        
        # UI가 모두 생성된 후에 포트 새로고침 실행
        self.refresh_ports()
    
    def list_serial_ports(self):
        ports = serial.tools.list_ports.comports()
        port_list = []
        for port in ports:
            label = f"{port.device} ({port.description})"
            port_list.append(label)
        return port_list
    
    def get_device_from_label(self, label):
        return label.split(' ')[0]
    
    def refresh_ports(self):
        self.port_combo.clear()
        ports = self.list_serial_ports()
        self.port_combo.addItems(ports)
        self.status_label.setText("포트 목록 갱신")
        self.status_label.setStyleSheet("color: black;")
    
    def connect_serial(self):
        selected_label = self.port_combo.currentText()
        if not selected_label:
            self.status_label.setText("포트를 선택하세요.")
            self.status_label.setStyleSheet("color: red;")
            return
        
        port = self.get_device_from_label(selected_label)
        try:
            self.ser = serial.Serial(port, self.BAUD_RATE, timeout=1)
            time.sleep(2)
            self.status_label.setText(f"{port} 연결 성공")
            self.status_label.setStyleSheet("color: green;")
        except Exception as e:
            self.ser = None
            self.status_label.setText(f"연결 실패: {e}")
            self.status_label.setStyleSheet("color: red;")
    
    def send_time(self):
        if self.ser is None or not self.ser.is_open:
            self.status_label.setText("시리얼 연결 안 됨")
            self.status_label.setStyleSheet("color: red;")
            return
        
        session = self.session_entry.text()
        brk = self.break_entry.text()
        
        if not (session.isdigit() and brk.isdigit()):
            self.status_label.setText("숫자를 입력하세요.")
            self.status_label.setStyleSheet("color: red;")
            return
        
        try:
            # "Session,Break\n" 형식으로 전송
            self.ser.write(f"{session},{brk}\n".encode())
            self.status_label.setText(f"Session: {session}분, Break: {brk}분 전송 완료")
            self.status_label.setStyleSheet("color: orange;")
        except Exception as e:
            self.status_label.setText(f"전송 실패: {e}")
            self.status_label.setStyleSheet("color: red;")
    
    def validate_entries(self):
        session = self.session_entry.text()
        brk = self.break_entry.text()
        
        if (session.isdigit() and brk.isdigit() and 
            int(session) > 0 and int(brk) > 0):
            self.send_button.setEnabled(True)
        else:
            self.send_button.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SandPomoApp()
    window.show()
    sys.exit(app.exec_())
