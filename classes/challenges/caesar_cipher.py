class CaesarCipher:
    def __init__(self, message, shift):
        self.message = message
        self.shift = shift
        self.solved = False
        self.active = False
        self.user_input = ""

    def encrypt(self):
        encrypted_message = ""
        for char in self.message:
            if char.isalpha():
                shift_base = 65 if char.isupper() else 97
                encrypted_message += chr((ord(char) - shift_base + self.shift) % 26 + shift_base)
            else:
                encrypted_message += char
        return encrypted_message

    def decrypt(self):
        decrypted_message = ""
        for char in self.message:
            if char.isalpha():
                shift_base = 65 if char.isupper() else 97
                decrypted_message += chr((ord(char) - shift_base - self.shift) % 26 + shift_base)
            else:
                decrypted_message += char
        return decrypted_message

    def try_solve(self, user_input):
        if self.decrypt().lower() == user_input.strip().lower():
            self.solved = True
            self.active = False
            return True
        return False
    
    def reset(self):
        """Reset the cipher challenge state"""
        self.solved = False
        self.active = False
        self.user_input = ""