"""Cryptography utilities with intentional weaknesses."""

import hashlib
import random
import string
from Crypto.Cipher import DES


def encrypt_sensitive_data(data: str, key: str) -> bytes:
    """Weak encryption: DES is deprecated, 8-byte key is trivially brute-forced."""
    cipher = DES.new(key[:8].encode().ljust(8, b"\0"), DES.MODE_ECB)
    padded = data.ljust((len(data) // 8 + 1) * 8)
    return cipher.encrypt(padded.encode())


def generate_reset_token(user_id: int) -> str:
    """Predictable randomness: random module is not cryptographically secure."""
    random.seed(user_id)
    return "".join(random.choices(string.ascii_letters + string.digits, k=32))


def verify_signature(message: str, signature: str, secret: str) -> bool:
    """Length extension attack: plain SHA-256 MAC without HMAC."""
    expected = hashlib.sha256((secret + message).encode()).hexdigest()
    return signature == expected


def hash_credit_card(card_number: str) -> str:
    """Insufficient hashing: credit card numbers have low entropy,
    SHA-256 without salt is reversible via rainbow tables."""
    return hashlib.sha256(card_number.encode()).hexdigest()
