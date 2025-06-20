import socket
import ssl
import threading

# Thông tin server
server_address = ('localhost', 12345)

# Danh sách các client đã kết nối
clients = []

def handle_client(client_socket):
    # Thêm client vào danh sách
    clients.append(client_socket)

    print("Đã kết nối với:", client_socket.getpeername())

    try:
        # Nhận và gửi dữ liệu
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print("Nhận:", data.decode('utf-8'))

            # Gửi dữ liệu đến tất cả các client khác
            for client in clients:
                if client != client_socket:
                    try:
                        client.send(data)
                    except: # Bắt lỗi khi gửi, có thể client đã ngắt kết nối
                        clients.remove(client)

    except: # Bắt lỗi tổng quát khi xử lý client_socket
        clients.remove(client_socket)
    finally: # Luôn thực hiện khi kết thúc hàm, dù có lỗi hay không
        print("Đã ngắt kết nối:", client_socket.getpeername())
        clients.remove(client_socket)
        client_socket.close()

# Tạo socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5) # Nghe tối đa 5 kết nối đang chờ

print("Server đang chờ kết nối...")

# Lắng nghe các kết nối
while True:
    client_socket, client_address = server_socket.accept() # Chấp nhận kết nối mới

    # Tạo SSL context
    # ssl.PROTOCOL_TLS chọn phiên bản TLS phù hợp nhất (ví dụ: TLSv1.2 hoặc TLSv1.3)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)

    # Tải chứng chỉ server và khóa riêng tư
    # Các file này phải nằm trong thư mục 'certificates' cùng cấp với script
    context.load_cert_chain(certfile="./certificates/server-cert.crt",
                            keyfile="./certificates/server-key.key")

    # Thiết lập kết nối SSL
    # 'server_side=True' chỉ định đây là phía server
    ssl_socket = context.wrap_socket(client_socket, server_side=True)

    # Bắt đầu một luồng xử lý riêng cho mỗi client đã kết nối
    # 'args=(ssl_socket,)' truyền socket SSL đã được bọc vào hàm handle_client
    client_thread = threading.Thread(target=handle_client, args=(
        ssl_socket,))
    client_thread.start()