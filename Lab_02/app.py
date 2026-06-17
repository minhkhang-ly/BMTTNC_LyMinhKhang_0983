from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Khai báo địa chỉ gốc kết nối đến Backend Flask API (cổng 5000)
API_SERVER_URL = "http://127.0.0.1:5000/api"

# 1. Định tuyến trang chủ (index.html)
@app.route("/")
def home():
    return render_template('index.html')

# 2. Điều hướng tất cả thuật toán chung về file giao diện caesar.html
@app.route("/<algo_name>")
def show_cipher_page(algo_name):
    # Cấu hình tiêu đề và kiểu nhập Key cho từng thuật toán
    config = {
        "caesar": {"title": "Caesar Cipher", "key_type": "number"},
        "vigenere": {"title": "Vigenere Cipher", "key_type": "text"},
        "railfence": {"title": "Rail Fence Cipher", "key_type": "number"},
        "playfair": {"title": "Playfair Cipher", "key_type": "text"},
        "transposition": {"title": "Transposition Cipher", "key_type": "number"}
    }
    
    if algo_name not in config:
        return "Thuật toán không tồn tại!", 404
        
    cfg = config[algo_name]

    # Render trực tiếp file caesar.html sẵn có nhưng thay ruột cấu hình
    return render_template('caesar.html', 
                           title=cfg["title"], 
                           key_type=cfg["key_type"], 
                           algo_type=algo_name)


# 3. Xử lý sự kiện Mã hóa (Encrypt) gửi sang API cổng 5000
@app.route("/encrypt", methods=['POST'])
def handle_encrypt():
    algo = request.form['algo_type']
    text = request.form['inputPlainText']
    raw_key = request.form['inputKeyPlain']
    
    # Ép kiểu dữ liệu Key đúng chuẩn mà backend api.py yêu cầu
    key = int(raw_key) if algo in ["caesar", "railfence", "transposition"] else raw_key
    
    payload = {"plain_text": text, "key": key}
    
    try:
        response = requests.post(f"{API_SERVER_URL}/{algo}/encrypt", json=payload)
        res_data = response.json()
        
        # Bóc tách đúng từ khóa trả về của từng thuật toán từ file api.py
        out_key = 'encrypted_message' if algo in ["caesar", "vigenere"] else 'encrypted_text'
        encrypted_text = res_data.get(out_key, "Không tìm thấy kết quả")
        
    except Exception as e:
        return f"Lỗi kết nối Backend API (Port 5000): {e}"
        
    return f"text: {text}<br>key: {raw_key}<br>encrypted text: {encrypted_text}"


# 4. Xử lý sự kiện Giải mã (Decrypt) gửi sang API cổng 5000
@app.route("/decrypt", methods=['POST'])
def handle_decrypt():
    algo = request.form['algo_type']
    text = request.form['inputCipherText']
    raw_key = request.form['inputKeyCipher']
    
    key = int(raw_key) if algo in ["caesar", "railfence", "transposition"] else raw_key
    
    payload = {"cipher_text": text, "key": key}
    
    try:
        response = requests.post(f"{API_SERVER_URL}/{algo}/decrypt", json=payload)
        res_data = response.json()
        
        out_key = 'decrypted_message' if algo in ["caesar", "vigenere"] else 'decrypted_text'
        decrypted_text = res_data.get(out_key, "Không tìm thấy kết quả")
        
    except Exception as e:
        return f"Lỗi kết nối Backend API (Port 5000): {e}"
        
    return f"text: {text}<br>key: {raw_key}<br>decrypted text: {decrypted_text}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)