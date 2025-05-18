import os

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from config import auth_jwt

os.makedirs(os.path.dirname(auth_jwt.private_key_path), exist_ok=True)

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)


with open(auth_jwt.private_key_path, "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

public_key = private_key.public_key()

with open(auth_jwt.public_key_path, "wb") as f:
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))
