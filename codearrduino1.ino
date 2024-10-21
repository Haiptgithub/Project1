#include <EEPROM.h>

String receivedString = "";  // Biến chứa chuỗi nhận được
const int EEPROM_SIZE = 512;  // Giới hạn kích thước lưu trữ EEPROM cho chuỗi

void setup() {
  Serial.begin(9600);  // Khởi tạo giao tiếp Serial với tốc độ 9600
}

void loop() {
  // Kiểm tra xem có dữ liệu từ máy tính gửi đến Arduino qua Serial
  if (Serial.available() > 0) {
    char receivedChar = Serial.read();  // Đọc từng ký tự từ Serial

    // Kiểm tra nếu là ký tự kết thúc chuỗi (ký tự '\n')
    if (receivedChar == '\n') {
      // Ghi chuỗi vào EEPROM
      writeToEEPROM(receivedString);
      
      // Đọc chuỗi từ EEPROM và đảo ngược
      String reversedString = readAndReverseUTF8FromEEPROM();

      // Gửi chuỗi đảo ngược lại về máy tính
      Serial.println(reversedString);
      
      // Xóa chuỗi sau khi đã xử lý
      receivedString = "";
    } else {
      receivedString += receivedChar;  // Tích lũy các ký tự vào chuỗi
    }
  }
}

// Hàm lưu chuỗi vào EEPROM (lưu từng byte)
void writeToEEPROM(String data) {
  int addr = 0;
  
  // Đảm bảo không ghi quá giới hạn kích thước EEPROM
  for (int i = 0; i < data.length() && addr < EEPROM_SIZE - 1; i++) {
    EEPROM.write(addr++, data[i]);
  }

  // Ghi ký tự kết thúc chuỗi
  EEPROM.write(addr, '\0');
}

// Hàm đọc và đảo ngược chuỗi từ EEPROM
String readAndReverseUTF8FromEEPROM() {
  String data = "";
  int addr = 0;
  byte b;
  
  // Đọc chuỗi từ EEPROM cho đến khi gặp ký tự kết thúc chuỗi
  while ((b = EEPROM.read(addr++)) != '\0' && addr < EEPROM_SIZE) {
    data += (char)b;
  }

  // Đảo ngược chuỗi UTF-8
  return reverseUTF8String(data);
}

// Hàm đảo ngược chuỗi UTF-8
String reverseUTF8String(String str) {
  String reversed = "";
  int i = str.length() - 1;

  // Duyệt ngược chuỗi, xử lý các ký tự UTF-8 (1, 2, hoặc 3 byte)
  while (i >= 0) {
    char c = str[i];
    
    // Kiểm tra ký tự ASCII (1 byte)
    if ((c & 0x80) == 0) {
      reversed += c;
      i--;
    } 
    // Kiểm tra ký tự UTF-8 (2 byte)
    else if ((c & 0xE0) == 0xC0 && i >= 1) {
      reversed += str[i-1];
      reversed += c;
      i -= 2;
    } 
    // Kiểm tra ký tự UTF-8 (3 byte)
    else if ((c & 0xF0) == 0xE0 && i >= 2) {
      reversed += str[i-2];
      reversed += str[i-1];
      reversed += c;
      i -= 3;
    } 
    else {
      // Xử lý byte không hợp lệ
      i--;
    }
  }
  return reversed;
}
