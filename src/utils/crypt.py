import bcrypt


class PSW2HASH:
    @staticmethod
    def crypt_psw(password: str) -> bytes:

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hashed

    @staticmethod
    def check_psw(password: str, token: bytes) -> bool:
        is_check = bcrypt.checkpw(password.encode(), token)
        return is_check
