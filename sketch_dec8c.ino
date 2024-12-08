const int led1 = 2; // Khai báo chân số 2 cho đèn LED 1
const int led2 = 3; // Khai báo chân số 3 cho đèn LED 2
const int led3 = 4; // Khai báo chân số 4 cho đèn LED 3
int mode = 0; // Khai báo biến mode để lưu chế độ hoạt động của đèn. 0: Tắt, 1: Sáng bình thường, 2: Nhấp nháy, 3: Chạy đuổi

void setup() {
  pinMode(led1, OUTPUT); // Cấu hình chân led1 là ngõ ra
  pinMode(led2, OUTPUT); // Cấu hình chân led2 là ngõ ra
  pinMode(led3, OUTPUT); // Cấu hình chân led3 là ngõ ra
  Serial.begin(9600); // Khởi tạo giao tiếp Serial với tốc độ baud 9600 để nhận dữ liệu từ máy tính
}

void loop() {
  if (Serial.available() > 0) { // Kiểm tra xem có dữ liệu từ Serial port hay không
    mode = Serial.parseInt(); // Đọc giá trị số nguyên từ Serial port và gán cho biến mode
  }

  switch (mode) { // Chọn chế độ hoạt động dựa trên giá trị của biến mode
    case 1: // Chế độ sáng bình thường (Normal)
      digitalWrite(led1, HIGH); // Bật đèn LED 1
      digitalWrite(led2, HIGH); // Bật đèn LED 2
      digitalWrite(led3, HIGH); // Bật đèn LED 3
      break;
    case 2: // Chế độ nhấp nháy (Blink)
      digitalWrite(led1, HIGH); // Bật tất cả đèn LED
      digitalWrite(led2, HIGH);
      digitalWrite(led3, HIGH);
      delay(500); // Đợi 500ms (0.5 giây)
      digitalWrite(led1, LOW); // Tắt tất cả đèn LED
      digitalWrite(led2, LOW);
      digitalWrite(led3, LOW);
      delay(500); // Đợi 500ms (0.5 giây)
      break;
    case 3: // Chế độ chạy đuổi (Chase)
      digitalWrite(led1, HIGH); // Bật đèn LED 1
      delay(250); // Đợi 250ms (0.25 giây)
      digitalWrite(led1, LOW); // Tắt đèn LED 1
      digitalWrite(led2, HIGH); // Bật đèn LED 2
      delay(250); // Đợi 250ms (0.25 giây)
      digitalWrite(led2, LOW); // Tắt đèn LED 2
      digitalWrite(led3, HIGH); // Bật đèn LED 3
      delay(250); // Đợi 250ms (0.25 giây)
      digitalWrite(led3, LOW); // Tắt đèn LED 3
      break;
    default: // Chế độ tắt (Off) - mặc định khi mode không phải 1, 2, hay 3
      digitalWrite(led1, LOW); // Tắt đèn LED 1
      digitalWrite(led2, LOW); // Tắt đèn LED 2
      digitalWrite(led3, LOW); // Tắt đèn LED 3
      break;
  }
}