import serial
import time
import serial.tools.list_ports

# Hàm tìm kiếm cổng COM của Arduino
def find_arduino_port():
    """
    Tìm kiếm cổng COM mà Arduino đang được kết nối.  Hàm này kiểm tra cả mô tả 
    cổng (description) và ID phần cứng (Hardware ID) để tăng độ chính xác.
    """
    ports = serial.tools.list_ports.comports()  # Lấy danh sách các cổng COM
    for port, desc, hwid in sorted(ports): # Duyệt qua từng cổng
        if "Arduino" in desc:  # Kiểm tra xem mô tả cổng có chứa từ "Arduino" không
            return port  # Trả về cổng COM nếu tìm thấy
        # Kiểm tra HWID cho độ chính xác cao hơn.  Bạn cần thay thế các VID:PID 
        # sau đây bằng ID của Arduino bạn đang dùng. Bạn có thể tìm thấy ID này trong 
        # Device Manager (Windows) hoặc System Information (macOS/Linux).
        if "VID:PID=2341:0043" in hwid.upper():  # ID của Arduino Uno
            return port
        if "VID:PID=2A03:0043" in hwid.upper(): # ID cho một số Arduino khác (ví dụ Nano)
            return port
    return None  # Trả về None nếu không tìm thấy cổng Arduino


# Hàm chính điều khiển đèn LED
def main():
    """
    Hàm chính điều khiển đèn LED trên Arduino qua cổng Serial.  Chương trình 
    cho phép người dùng chọn chế độ hoạt động của đèn và gửi lệnh đến Arduino.
    """
    port = find_arduino_port()  # Tìm cổng COM của Arduino
    if not port:
        print("Không tìm thấy cổng COM của Arduino. Hãy chắc chắn rằng Arduino đã được kết nối và driver đã được cài đặt.")
        return  # Kết thúc chương trình nếu không tìm thấy cổng

    try:
        # Mở cổng Serial. timeout=1 đặt thời gian chờ là 1 giây.  Nếu không nhận 
        # được dữ liệu trong 1 giây, hàm sẽ trả về lỗi timeout
        ser = serial.Serial(port, 9600, timeout=1) 
        time.sleep(2)  # Chờ Arduino khởi động (khoảng thời gian cần thiết để Arduino khởi chạy)

        while True:  # Vòng lặp chính
            try:
                # Nhận đầu vào từ người dùng để chọn chế độ
                mode = input("Chọn chế độ (0: Tắt, 1: Sáng, 2: Nhấp nháy, 3: Nối đuôi, q để thoát): ")

                if mode.lower() == 'q':  # Thoát chương trình nếu người dùng nhập 'q' hoặc 'Q'
                    break

                mode = int(mode) # Chuyển đổi đầu vào thành số nguyên

                if 0 <= mode <= 3: # Kiểm tra xem đầu vào có hợp lệ (từ 0 đến 3) không.
                    ser.write(str(mode).encode())  # Gửi dữ liệu đến Arduino (chuyển đổi số thành bytes)
                    print(f"Chế độ {mode}: {'Tắt' if mode == 0 else 'Sáng' if mode == 1 else 'Nhấp nháy' if mode == 2 else 'Nối đuôi'}")

                else:
                    raise ValueError("Số không hợp lệ") # Ném lỗi nếu số nhập vào không hợp lệ

            except ValueError as e:  # Xử lý lỗi nếu đầu vào không phải là số
                print(f"Lỗi: {e}. Vui lòng nhập số từ 0 đến 3 hoặc 'q' để thoát.")
            except serial.SerialTimeoutException: # Xử lý lỗi timeout
                print("Lỗi: Timeout khi giao tiếp với Arduino. Kiểm tra kết nối.")
                break  # Thoát vòng lặp nếu xảy ra lỗi timeout

        ser.close()  # Đóng cổng Serial khi kết thúc

    except serial.SerialException as e:  # Xử lý lỗi kết nối Serial
        print(f"Lỗi kết nối Serial: {e}. Hãy chắc chắn rằng Arduino đã được kết nối đúng cách.")

if __name__ == "__main__":  # Chạy hàm main nếu file được chạy trực tiếp (không được import làm module)
    main()