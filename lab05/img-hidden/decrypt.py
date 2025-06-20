import sys
from PIL import Image

def decode_image(encoded_image_path):
    """
    Giải mã thông điệp được ẩn trong hình ảnh bằng cách trích xuất bit cuối cùng của các kênh màu.

    Args:
        encoded_image_path (str): Đường dẫn đến tệp hình ảnh đã mã hóa.

    Returns:
        str: Thông điệp đã giải mã.
    """
    # Mở hình ảnh đã mã hóa
    img = Image.open(encoded_image_path)
    width, height = img.size
    binary_message = "" # Chuỗi để lưu trữ các bit thông điệp trích xuất được

    # Lặp qua từng hàng và cột của hình ảnh
    for row in range(height):
        for col in range(width):
            # Lấy giá trị pixel (R, G, B)
            pixel = img.getpixel((col, row))

            # Lặp qua 3 kênh màu (R, G, B) của pixel
            for color_channel in range(3):
                # Lấy giá trị bit cuối cùng của kênh màu (LSB)
                # format(..., '08b') chuyển số nguyên thành chuỗi nhị phân 8 bit
                # '[-1]' lấy ký tự cuối cùng (bit cuối cùng)
                binary_message += format(pixel[color_channel], '08b')[-1]

    message = ""
    # Chuyển đổi chuỗi bit nhị phân trở lại thành các ký tự
    # Lặp qua chuỗi bit với bước nhảy 8 (vì mỗi ký tự là 8 bit)
    # LƯU Ý: Đoạn code gốc sử dụng '\0' làm dấu kết thúc.
    # Trong phần encode_image đã cung cấp trước đó, dấu kết thúc là '1111111111111110'.
    # Để tương thích, tôi sẽ sửa lại phần này để tìm dấu kết thúc thực tế đã dùng.

    # Tìm dấu kết thúc '1111111111111110'
    end_marker = '1111111111111110'
    # Tìm vị trí của dấu kết thúc trong chuỗi binary_message
    marker_index = binary_message.find(end_marker)

    if marker_index != -1:
        # Nếu tìm thấy dấu kết thúc, chỉ lấy phần dữ liệu trước đó
        binary_message_to_decode = binary_message[:marker_index]
    else:
        # Nếu không tìm thấy dấu kết thúc, cố gắng giải mã toàn bộ chuỗi (có thể sẽ có rác)
        binary_message_to_decode = binary_message

    # Chuyển đổi chuỗi bit thành ký tự
    for i in range(0, len(binary_message_to_decode), 8):
        # Đảm bảo có đủ 8 bit để tạo một ký tự
        if i + 8 <= len(binary_message_to_decode):
            byte_str = binary_message_to_decode[i:i+8]
            # Chuyển chuỗi 8 bit thành số nguyên, sau đó thành ký tự
            char = chr(int(byte_str, 2))
            message += char
        else:
            # Nếu không đủ 8 bit, bỏ qua phần còn lại
            break
            
    return message

def main():
    """
    Hàm chính để xử lý đối số dòng lệnh và gọi hàm giải mã.
    """
    # Kiểm tra số lượng đối số dòng lệnh
    # Cần 2 đối số: tên script và đường dẫn ảnh đã mã hóa
    if len(sys.argv) != 2:
        print("Usage: python decrypt.py <encoded_image_path>")
        return

    encoded_image_path = sys.argv[1] # Đối số là đường dẫn đến ảnh đã mã hóa
    decoded_message = decode_image(encoded_image_path)
    print("Decoded message:", decoded_message)

if __name__ == "__main__":
    main()