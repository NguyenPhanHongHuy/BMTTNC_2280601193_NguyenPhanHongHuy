import socket
import ssl
import threading

# Thông tin server mà client sẽ kết nối tới
server_address = ('localhost', 12345)

def receive_data(ssl_socket):
    """
    Hàm này được chạy trong một luồng riêng để liên tục nhận dữ liệu từ server.
    """
    try:
        while True:
            # Nhận tối đa 1024 byte dữ liệu
            data = ssl_socket.recv(1024)
            if not data: # Nếu không có dữ liệu, server đã đóng kết nối
                break
            # Giải mã dữ liệu và in ra màn hình
            print("Nhận:", data.decode('utf-8'))
    except Exception as e: # Bắt các ngoại lệ (ví dụ: mất kết nối đột ngột)
        print(f"Lỗi khi nhận dữ liệu: {e}")
        pass # Có thể xử lý lỗi chi tiết hơn nếu cần
    finally:
        # Đảm bảo socket được đóng khi luồng kết thúc
        ssl_socket.close()
        print("Kết nối đã đóng.")


# Tạo socket client
# socket.AF_INET cho địa chỉ IPv4, socket.SOCK_STREAM cho TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Tạo SSL context
# ssl.PROTOCOL_TLS chọn phiên bản TLS an toàn nhất được hỗ trợ
context = ssl.SSLContext(ssl.PROTOCOL_TLS)

# Cấu hình kiểm tra chứng chỉ server (thay đổi tùy theo nhu cầu bảo mật)
# ssl.CERT_NONE: Không kiểm tra chứng chỉ (ít an toàn, chỉ dùng cho dev/test)
# ssl.CERT_REQUIRED: Yêu cầu và xác minh chứng chỉ server
context.verify_mode = ssl.CERT_NONE # Thay đổi nếu bạn muốn xác thực chứng chỉ
context.check_hostname = False # Thay đổi nếu bạn muốn kiểm tra hostname của chứng chỉ

# Thiết lập kết nối SSL
# Bọc socket thông thường bằng SSL, chỉ định hostname của server để TLS có thể xác minh (nếu verify_mode không phải là CERT_NONE)
ssl_socket = context.wrap_socket(client_socket, server_hostname='localhost')

# Kết nối tới server
ssl_socket.connect(server_address)
print(f"Đã kết nối tới server {server_address}")

# Bắt đầu một luồng riêng để nhận dữ liệu từ server
# Điều này cho phép client vừa gửi tin nhắn vừa nhận tin nhắn cùng lúc
receive_thread = threading.Thread(target=receive_data, args=(ssl_socket,))
receive_thread.start()

# Gửi dữ liệu lên server
try:
    while True:
        # Lấy tin nhắn từ người dùng nhập vào
        message = input("Nhập tin nhắn: ")
        # Gửi tin nhắn sau khi mã hóa sang byte (UTF-8)
        ssl_socket.send(message.encode('utf-8'))
except KeyboardInterrupt:
    # Xử lý khi người dùng nhấn Ctrl+C để thoát
    print("\nNgười dùng đã ngắt kết nối.")
    pass
finally:
    # Đảm bảo socket được đóng khi chương trình chính kết thúc
    ssl_socket.close()
    # Chờ luồng nhận dữ liệu kết thúc (tùy chọn)
    receive_thread.join()