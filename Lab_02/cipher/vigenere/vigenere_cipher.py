class VigenereCipher:
    def encrypt_text(self, text: str, key: str) -> str:
        """
        Encrypts plaintext using the Vigenere cipher with the specified string key.
        """
        if not key:
            return text
        
        # Clean the key to keep only alphabetic characters
        key_cleaned = "".join([c for c in key if c.isalpha()]).upper()
        if not key_cleaned:
            return text
        
        encrypted_chars = []
        key_len = len(key_cleaned)
        key_index = 0
        
        for char in text:
            if char.isalpha():
                shift = ord(key_cleaned[key_index % key_len]) - ord('A')
                if char.isupper():
                    new_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                else:
                    new_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
                encrypted_chars.append(new_char)
                key_index += 1
            else:
                encrypted_chars.append(char)
                
        return "".join(encrypted_chars)

    def decrypt_text(self, text: str, key: str) -> str:
        """
        Decrypts ciphertext using the Vigenere cipher with the specified string key.
        """
        if not key:
            return text
        
        key_cleaned = "".join([c for c in key if c.isalpha()]).upper()
        if not key_cleaned:
            return text
        
        decrypted_chars = []
        key_len = len(key_cleaned)
        key_index = 0
        
        for char in text:
            if char.isalpha():
                shift = ord(key_cleaned[key_index % key_len]) - ord('A')
                if char.isupper():
                    new_char = chr((ord(char) - ord('A') - shift + 26) % 26 + ord('A'))
                else:
                    new_char = chr((ord(char) - ord('a') - shift + 26) % 26 + ord('a'))
                decrypted_chars.append(new_char)
                key_index += 1
            else:
                decrypted_chars.append(char)
                
        return "".join(decrypted_chars)
