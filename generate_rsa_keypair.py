from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

BITS = 1024


def keypair_gen():
    private_key = rsa.generate_private_key(public_exponent=65537,  key_size=BITS)
    public_key = private_key.public_key()

    public_pem = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                         format=serialization.PublicFormat.SubjectPublicKeyInfo)

    return public_pem
