import tkinter as tk
import serial
import time

try:
    # Khởi tạo kết nối Serial
    ser = serial.Serial('COM3', 9600, timeout=1)  # Thay 'COM7' bằng cổng thực tế của Arduino
    time.sleep(2)  # Đợi cho Arduino reset
except serial.SerialException as e:
    ser = None  # Đặt ser thành None nếu không thể kết nối

def send_text():
    if ser is not None and ser.is_open:
        text_to_send = textbox1.get("1.0", tk.END).strip() + '\n'  # Lấy chuỗi từ textbox1 và thêm \n
        ser.write(text_to_send.encode('utf-8'))  # Gửi chuỗi đến Arduino dưới dạng UTF-8
        time.sleep(0.1)  # Chờ một khoảng thời gian nhỏ để tránh xung đột với buffer

def receive_text():
    if ser is not None and ser.is_open:
        textbox2.delete("1.0", tk.END)  # Xóa nội dung cũ của textbox2 trước khi hiển thị dữ liệu mới
        received_data = ""
        
        time.sleep(0.1)  # Chờ để đảm bảo dữ liệu vào buffer

        if ser.in_waiting > 0:  # Kiểm tra xem có dữ liệu nhận được không
            try:
                received_data = ser.read(ser.in_waiting).decode('utf-8', errors='replace').strip()
                print(f"Received data: {received_data}")  # In ra dữ liệu nhận được để kiểm tra
            except UnicodeDecodeError as e:
                print(f"Unicode decode error: {e}")  # Báo lỗi nếu có vấn đề khi giải mã
        
        if received_data:
            received_data += '$'  # Thêm ký tự $ vào cuối chuỗi
            textbox2.insert(tk.END, received_data)  # Hiển thị dữ liệu từ Arduino (đã được đảo và thêm $)
        else:
            textbox2.insert(tk.END, "No data received")


def on_closing():
    if ser is not None and ser.is_open:
        ser.close()  # Đóng kết nối Serial
    root.destroy()  # Đóng cửa sổ ứng dụng

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Simple App")
root.configure(bg="gray")  # Đổi màu nền của cửa sổ chính thành màu xám

# Tạo textbox1 (cho phép nhập nhiều dòng)
textbox1 = tk.Text(root, width=150, height=20, bg="lightyellow", fg="black")  # Tăng kích thước width và height, đổi màu nền
textbox1.grid(row=0, column=0, padx=10, pady=10)

# Tạo textbox2 (cho phép hiển thị nhiều dòng)
textbox2 = tk.Text(root, width=150, height=20, bg="lightblue", fg="black")  # Tăng kích thước width và height, đổi màu nền
textbox2.grid(row=1, column=0, padx=20, pady=20)

# Tạo nút Send
send_button = tk.Button(root, text="Send", command=send_text)
send_button.grid(row=0, column=1, padx=10, pady=10)

# Tạo nút Receive
receive_button = tk.Button(root, text="Receive", command=receive_text)
receive_button.grid(row=1, column=1, padx=10, pady=10)

# Đặt hàm on_closing khi đóng cửa sổ
root.protocol("WM_DELETE_WINDOW", on_closing)

# Chạy chương trình
root.mainloop()

# Đóng kết nối khi kết thúc chương trình
if ser is not None and ser.is_open:
    ser.close()
