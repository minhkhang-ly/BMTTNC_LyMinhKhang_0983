from flask import Flask, request, jsonify
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher

app = Flask(__name__)

# Khởi tạo các class thuật toán
caesar_cipher = CaesarCipher()
vigenere_cipher = VigenereCipher()

# ==========================================
# 1. CAESAR CIPHER APIs
# ==========================================
@app.route('/api/caesar/encrypt', methods=['POST'])
def caesar_encrypt():
    data = request.get_json()
    if not data or 'plain_text' not in data or 'key' not in data:
        return jsonify({'error': 'Invalid JSON body'}), 400
    
    plain_text = data['plain_text']
    key = int(data['key'])
    encrypted_text = caesar_cipher.encrypt_text(plain_text, key)
    return jsonify({'encrypted_message': encrypted_text})

@app.route('/api/caesar/decrypt', methods=['POST'])
def caesar_decrypt():
    data = request.get_json()
    if not data or 'cipher_text' not in data or 'key' not in data:
        return jsonify({'error': 'Invalid JSON body'}), 400
        
    cipher_text = data['cipher_text']
    key = int(data['key'])
    decrypted_text = caesar_cipher.decrypt_text(cipher_text, key)
    return jsonify({'decrypted_message': decrypted_text})


# ==========================================
# 2. VIGENERE CIPHER APIs
# ==========================================
@app.route('/api/vigenere/encrypt', methods=['POST'])
def vigenere_encrypt():
    data = request.get_json()
    if not data or 'plain_text' not in data or 'key' not in data:
        return jsonify({'error': 'Invalid JSON body'}), 400
        
    plain_text = data['plain_text']
    key = data['key'] # Đối với Vigenere, key là một chuỗi (str) chứ không phải số (int)
    encrypted_text = vigenere_cipher.encrypt_text(plain_text, key)
    return jsonify({'encrypted_message': encrypted_text})

@app.route('/api/vigenere/decrypt', methods=['POST'])
def vigenere_decrypt():
    data = request.get_json()
    if not data or 'cipher_text' not in data or 'key' not in data:
        return jsonify({'error': 'Invalid JSON body'}), 400
        
    cipher_text = data['cipher_text']
    key = data['key']
    decrypted_text = vigenere_cipher.decrypt_text(cipher_text, key)
    return jsonify({'decrypted_message': decrypted_text})


# Chạy server ứng dụng ngầm ở port 5000
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)