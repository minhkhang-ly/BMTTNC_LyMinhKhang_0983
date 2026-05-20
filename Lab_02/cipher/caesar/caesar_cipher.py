class CaesarCipher:
    def encrypt_text(self, text: str, key: int) -> str:
        """
        Encrypts plaintext using the Caesar cipher with the specified key (shift).
        """
        try:
            shift = int(key)
        except (ValueError, TypeError):
            return text
        
        encrypted_chars = []
        for char in text:
            if char.isalpha():
                if char.isupper():
                    new_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                else:
                    new_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
                encrypted_chars.append(new_char)
            else:
                encrypted_chars.append(char)
        return "".join(encrypted_chars)

    def decrypt_text(self, text: str, key: int) -> str:
        """
        Decrypts ciphertext using the Caesar cipher with the specified key (shift).
        """
        try:
            shift = int(key)
        except (ValueError, TypeError):
            return text
        
        return self.encrypt_text(text, -shift)
