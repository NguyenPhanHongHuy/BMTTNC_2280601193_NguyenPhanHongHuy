from block import Block # Import lớp Block từ tệp block.py
import hashlib
import time

class Blockchain:
    """
    Đại diện cho một chuỗi khối.
    Quản lý việc tạo khối, thêm giao dịch, bằng chứng công việc và xác thực chuỗi.
    """
    def __init__(self):
        self.chain = [] # Danh sách lưu trữ các khối trong chuỗi
        self.current_transactions = [] # Danh sách lưu trữ các giao dịch chưa được thêm vào khối
        # Tạo khối khởi nguồn (Genesis block) khi khởi tạo blockchain
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        """
        Tạo một khối mới và thêm nó vào chuỗi.
        """
        block = Block(
            len(self.chain) + 1, # Chỉ số của khối mới
            previous_hash,       # Hash của khối trước đó
            time.time(),         # Dấu thời gian hiện tại
            self.current_transactions, # Các giao dịch hiện tại
            proof                # Bằng chứng công việc
        )
        self.current_transactions = [] # Đặt lại danh sách giao dịch sau khi thêm vào khối
        self.chain.append(block)     # Thêm khối vào chuỗi
        return block

    def get_previous_block(self):
        """
        Trả về khối cuối cùng trong chuỗi.
        """
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        """
        Thuật toán Bằng chứng công việc để tìm một số `new_proof`
        sao cho hash của `(new_proof**2 - previous_proof**2)` bắt đầu bằng '0000'.
        """
        new_proof = 1
        check_proof = False
        while not check_proof:
            # Tạo chuỗi dữ liệu cho hash bằng cách trừ bình phương của hai bằng chứng
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            # Kiểm tra xem hash có bắt đầu bằng '0000' không
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1 # Tăng new_proof và thử lại
        return new_proof

    def add_transaction(self, sender, receiver, amount):
        """
        Thêm một giao dịch mới vào danh sách các giao dịch chờ xử lý.
        """
        self.current_transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        # Trả về chỉ số của khối mà giao dịch này sẽ được thêm vào
        return self.get_previous_block().index + 1

    def is_chain_valid(self, chain):
        """
        Kiểm tra xem toàn bộ chuỗi khối có hợp lệ không.
        Kiểm tra tính liên kết của hash và bằng chứng công việc.
        """
        previous_block = chain[0] # Bắt đầu từ khối đầu tiên
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            # 1. Kiểm tra hash của khối trước đó có khớp không
            if block.previous_hash != previous_block.hash:
                return False

            # 2. Kiểm tra bằng chứng công việc có hợp lệ không
            previous_proof = previous_block.proof
            proof = block.proof
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000': # Hash của bằng chứng phải bắt đầu bằng '0000'
                return False

            previous_block = block # Di chuyển đến khối tiếp theo
            block_index += 1
        return True # Nếu tất cả các kiểm tra đều thành công