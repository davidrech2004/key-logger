def xor_decrypt(self, encrypt_text: str):
    return ''.join([chr(ord(c) ^ self.key) for c in encrypt_text])
