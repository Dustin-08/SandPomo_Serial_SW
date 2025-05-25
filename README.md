# SandPomo_Serial_SW

## University of Ulsan OSS TermProject Back Up && Test Repo

### 사용 언어
- 파이썬
### 사용 패키지
- Tkinter
### 사용 툴킷
- Github, VS Code
### 전송 데이터 예시(현재 토글버전(v2)만 가능)
``` bash
25,5\n
```

## 01) 동작 예시 이미지

### 자동 포트 잡기 코드
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/66eb805d-5302-4067-8ed6-f3471aa3cf76" />
<img width="317" alt="Image" src="https://github.com/user-attachments/assets/e0ed59a1-85e3-47d7-bf50-c52f0e29c7f2" />

### 토글로 포트 확인 및 연결 코드
- 중앙 정렬로 이미지 변경 예정
<img width="576" alt="Image" src="https://github.com/user-attachments/assets/bab34f7b-ed27-4bfc-8d5e-e15930e3967d" />
<img width="570" alt="Image" src="https://github.com/user-attachments/assets/6970968d-7332-4e26-9826-9e322172a612" />

## 02) 사용법
1. 다운로드 후 관련 라이브러리 설치
``` bash
python -m pip install pyserial
```
2. 아래 명령어 입력 후 실행
``` bash
python SerialToSandPomo_v2_3.py
```
## 03) 애플리케이션 빌드화
1. PyInstaller 설치
먼저 명령 프롬프트(cmd)를 열고 다음 명령어로 PyInstaller를 설치하세요.
```bash
pip install pyinstaller
```
2. 파이썬 파일이 있는 폴더로 이동
예를 들어, 파일명이 myapp.py라면 해당 폴더에서 명령 프롬프트를 엽니다.

3. PyInstaller로 실행 파일 생성
아래 명령어를 입력
```bash
pyinstaller --onefile --windowed myapp.py
```
--onefile : 모든 파일을 하나의 실행 파일로 만듭니다.
--windowed : 콘솔 창 없이 GUI 창만 띄웁니다(Tkinter 앱에 필수).

4. 실행 파일 위치
변환이 끝나면, dist 폴더 안에 myapp.exe 파일이 생성됩니다.
이 파일을 더블 클릭하면 파이썬이 설치되어 있지 않은 PC에서도 바로 실행됩니다.

5. if Windows OS에서 빌드 후 에러가 날시
myapp.spec 파일 내에 hiddenimports에 라이브러리 추가
```spec
a = Analysis(
    ['myapp.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['serial', 'serial.tools', 'serial.tools.list_ports'],  # 이 줄 추가/수정
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
```
6. 후에 spec 파일 기반으로 앱 빌드
```bash
pyinstaller myapp.spec
```
