import socket
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad

def generate_rsa_key_pair():
    """Tự sinh cặp khóa RSA 2048 của client"""
    key = RSA.generate(2048)
    private_key = key
    public_key = key.publickey()
    return private_key, public_key

def encrypt_message(key, message):
    """Mã hóa tin nhắn bằng AES MODE_CBC và pad dữ liệu"""
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    ciphertext = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
    return iv + ciphertext

def decrypt_message(key, encrypted_message):
    """Giải mã tin nhắn bằng AES MODE_CBC và unpad dữ liệu"""
    iv = encrypted_message[:AES.block_size]
    ciphertext = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return message.decode('utf-8')

def receive_messages(client_socket, aes_key):
    """Luồng riêng để liên tục lắng nghe và in tin nhắn từ server"""
    while True:
        try:
            encrypted_message = client_socket.recv(4096)
            if not encrypted_message:
                print("\n[!] Mất kết nối tới server.")
                break
            
            message = decrypt_message(aes_key, encrypted_message)
            print(f"\n[Server]: {message}\n> ", end="")
        except Exception as e:
            print(f"\n[!] Lỗi khi nhận tin nhắn: {e}")
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('192.168.88.158', 8080))
        print("[*] Đã kết nối tới server 192.168.88.158:8080")
    except Exception as e:
        print(f"[!] Không thể kết nối đến server: {e}")
        return

    try:
        # 3. Tự sinh cặp khóa RSA 2048 riêng của client
        print("[*] Đang sinh khóa RSA 2048 của Client...")
        private_key, public_key = generate_rsa_key_pair()

        # 4. Nhận Public Key của server và gửi Public Key của client sang cho server
        server_public_key_data = client_socket.recv(4096)
        print("[*] Đã nhận Public Key từ Server.")
        
        client_socket.sendall(public_key.export_key())
        print("[*] Đã gửi Public Key của Client cho Server.")

        # 5. Nhận khóa AES đã bị mã hóa từ server về, dùng Private Key RSA giải mã
        encrypted_aes_key = client_socket.recv(4096)
        cipher_rsa = PKCS1_OAEP.new(private_key)
        aes_key = cipher_rsa.decrypt(encrypted_aes_key)
        print("[*] Đã nhận và giải mã khóa AES thành công. Bắt đầu chat!")
        print("---------------------------------------------------------")

        # 7. Tạo luồng dữ liệu riêng để nhận tin nhắn
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket, aes_key))
        receive_thread.daemon = True
        receive_thread.start()

        # 8. Vòng lặp chính xử lý nhập thông điệp từ bàn phím
        while True:
            message = input("> ")
            if message.strip().lower() == "exit":
                print("[*] Đóng kết nối...")
                break
            
            if message:
                encrypted_msg = encrypt_message(aes_key, message)
                client_socket.sendall(encrypted_msg)
                
    except Exception as e:
        print(f"[!] Đã xảy ra lỗi: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
