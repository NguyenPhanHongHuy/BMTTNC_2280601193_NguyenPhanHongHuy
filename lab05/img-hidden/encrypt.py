import sys
from PIL import Image

def encode_image(image_path, message):
    """
    Mã hóa một thông điệp vào hình ảnh bằng cách thay đổi bit cuối cùng của các kênh màu.

    Args:
        image_path (str): Đường dẫn đến tệp hình ảnh gốc.
        message (str): Thông điệp cần mã hóa.
    """
    # Mở hình ảnh
    img = Image.open(image_path)
    width, height = img.size

    # Chuyển đổi thông điệp thành chuỗi bit nhị phân
    # Mỗi ký tự được chuyển thành 8 bit (vd: 'A' -> '01000001')
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    # Thêm một chuỗi đánh dấu kết thúc thông điệp (end-of-message marker)
    # '1111111111111110' là một chuỗi 16 bit ít có khả năng xuất hiện tự nhiên
    binary_message += '1111111111111110'

    data_index = 0
    # Lặp qua từng hàng (row) của hình ảnh
    for row in range(height):
        # Lặp qua từng cột (column) trong hàng
        for col in range(width):
            # Lấy giá trị pixel (R, G, B) tại vị trí (col, row)
            pixel = list(img.getpixel((col, row)))

            # Lặp qua 3 kênh màu (R, G, B) của pixel
            for color_channel in range(3):
                # Kiểm tra xem còn bit thông điệp để mã hóa không
                if data_index < len(binary_message):
                    # Lấy giá trị kênh màu hiện tại, chuyển sang nhị phân 8 bit
                    # '[:-1]' loại bỏ bit cuối cùng của kênh màu gốc
                    # Sau đó, nối bit thông điệp vào vị trí cuối cùng
                    # và chuyển đổi lại thành số nguyên
                    pixel[color_channel] = int(format(pixel[color_channel], '08b')[:-1] + binary_message[data_index], 2)
                    data_index += 1
                else:
                    # Nếu đã mã hóa hết thông điệp, thoát khỏi vòng lặp các kênh màu
                    break
            
            # Đặt lại pixel đã thay đổi vào hình ảnh
            img.putpixel((col, row), tuple(pixel))

            # Nếu đã mã hóa hết thông điệp, thoát khỏi vòng lặp cột
            if data_index >= len(binary_message):
                break
        
        # Nếu đã mã hóa hết thông điệp, thoát khỏi vòng lặp hàng
        if data_index >= len(binary_message):
            break

    # Lưu hình ảnh đã mã hóa
    encoded_image_path = 'encoded_image.png'
    img.save(encoded_image_path)
    print("Steganography complete. Encoded image saved as", encoded_image_path)

def main():
    """
    Hàm chính để xử lý đối số dòng lệnh và gọi hàm mã hóa.
    """
    # Kiểm tra số lượng đối số dòng lệnh
    # Cần 3 đối số: tên script, đường dẫn ảnh, thông điệp
    if len(sys.argv) != 3:
        print("Usage: python encrypt.py <image_path> <message>")
        return

    image_path = sys.argv[1] # Đối số thứ nhất là đường dẫn ảnh
    message = sys.argv[2]    # Đối số thứ hai là thông điệp
    
    encode_image(image_path, message)

if __name__ == "__main__":
    main()