from Crypto.Cipher import AES
from Crypto import Random

# AES supports multiple key sizes: 16 (AES128), 24 (AES192), or 32 (AES256).

class AESCipher:
    def __init__(self):
        # set your own key
        self.key = 'A'*32
        self.BS = 32
        self.pad = lambda s: s + (self.BS - len(s) %
                                  self.BS) * chr(self.BS - len(s) % self.BS)
        self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    def encrypt(self, raw):
        raw = self.pad(raw).encode()
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key.encode(), AES.MODE_CBC, iv)
        return (iv + cipher.encrypt(raw)).hex()

    def decrypt(self, enc):
        enc = bytes.fromhex(enc)
        iv = enc[:16]
        cipher = AES.new(self.key.encode(), AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(enc[16:]).decode())
