class PlayFairCipher:
    def __init__(self) -> None:
        pass

    def create_playfair_matrix(self, key):
        key = key.replace("J", "I") 
        key = key.upper()
        # Filter duplicates from the key while preserving order
        unique_key = []
        for char in key:
            if char.isalpha() and char not in unique_key:
                unique_key.append(char)
        
        key_set = set(unique_key)
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        remaining_letters = [
            letter for letter in alphabet if letter not in key_set
        ]
        
        matrix = list(unique_key)
        for letter in remaining_letters:
            matrix.append(letter)
            if len(matrix) == 25:
                break
        
        playfair_matrix = [matrix[i:i+5] for i in range(0, len(matrix), 5)]
        return playfair_matrix

    def find_letter_coords(self, matrix, letter):
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == letter:
                    return row, col
        return None
    # =========================================================
    def split_pairs(self, text): # he lx lo yo ux
        text = text.upper().replace("J", "I").replace(" ", "")
        pairs = []
        i = 0
        
        while i < len(text):
            a = text[i]
            if i + 1 < len(text):
                b = text[i+1]
                if a == b:
                    pairs.append(a + "X")
                    i += 1
                else:
                    pairs.append(a + b)
                    i += 2
            else:
                pairs.append(a + "X")
                i += 1
        return pairs

    # =========================================================
    # 2. HÀM ENCRYPT GỌI HÀM SPLIT_PAIRS THEO ẢNH GIẢNG VIÊN
    # =========================================================
    def playfair_encrypt(self, plain_text, matrix):
        pairs = self.split_pairs(plain_text)
        encrypted_text = ""
        
        for pair in pairs:
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])
            
            if row1 == row2:
                encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:
                encrypted_text += matrix[row1][col2] + matrix[row2][col1]
        return encrypted_text

    def playfair_decrypt(self, cipher_text, matrix):
        cipher_text = cipher_text.upper()
        cipher_text = "".join([c for c in cipher_text if c.isalpha()])
        decrypted_text = ""
        if not cipher_text:
            return ""
        
        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i:i+2]
            if len(pair) == 1:
                pair += "X"
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])
            if row1 == row2:
                decrypted_text += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                decrypted_text += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
            else:
                decrypted_text += matrix[row1][col2] + matrix[row2][col1]

        if not decrypted_text:
            return ""

        banro = ""
        for i in range(0, len(decrypted_text) - 2, 2):
            if decrypted_text[i+1] == "X" and decrypted_text[i] == decrypted_text[i+2]:
                banro += decrypted_text[i]
            else:
                banro += decrypted_text[i] + decrypted_text[i+1]

        if decrypted_text[-1] == "X":
            banro += decrypted_text[-2]
        else:
            banro += decrypted_text[-2]
            banro += decrypted_text[-1]
        return banro