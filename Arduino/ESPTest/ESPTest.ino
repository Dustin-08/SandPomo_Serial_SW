// ESP32 C3 보드용 간단한 시리얼 수신 확인 코드
//#define LED_PIN 2  // ESP32 C3의 내장 LED 핀

String receivedData = "";
bool dataComplete = false;

void setup() {
  // 시리얼 통신 초기화
  Serial.begin(115200);
  
  // LED 핀 설정
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  
  // 준비 완료 신호 (LED 1번 길게 깜빡임)
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
}

void loop() {
  // 시리얼 데이터 수신 처리
  while (Serial.available() > 0) {
    char incomingChar = Serial.read();
    
    if (incomingChar == '\n') {
      // 데이터 수신 완료
      dataComplete = true;
    } else if (incomingChar != '\r') {
      // 캐리지 리턴 제외하고 데이터 누적
      receivedData += incomingChar;
    }
  }
  
  // 완전한 데이터를 받았을 때 처리
  if (dataComplete) {
    processReceivedData();
    dataComplete = false;
    receivedData = "";
  }
}

void processReceivedData() {
  // 쉼표가 있는지 확인 (Session,Break 형식)
  int commaIndex = receivedData.indexOf(',');
  
  if (commaIndex > 0) {
    String sessionStr = receivedData.substring(0, commaIndex);
    String breakStr = receivedData.substring(commaIndex + 1);
    
    // 문자열을 정수로 변환
    int sessionTime = sessionStr.toInt();
    int breakTime = breakStr.toInt();
    
    // 유효한 데이터인지 확인 (둘 다 0보다 큰 숫자)
    if (sessionTime > 0 && breakTime > 0) {
      // ✅ 올바른 데이터 수신! LED 2번 깜빡임
      blinkLED(2, 300);
    } else {
      // ❌ 잘못된 숫자 데이터 - LED 5번 빠르게 깜빡임
      blinkLED(5, 100);
    }
  } else {
    // ❌ 쉼표가 없는 잘못된 형식 - LED 3번 깜빡임
    blinkLED(3, 200);
  }
}

void blinkLED(int times, int delayMs) {
  for (int i = 0; i < times; i++) {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(delayMs);
    digitalWrite(LED_BUILTIN, LOW);
    delay(delayMs);
  }
}
