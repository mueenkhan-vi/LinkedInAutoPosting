"""
Encryption utilities for securing sensitive credentials
"""
from cryptography.fernet import Fernet
import os
import base64
import hashlib


class CredentialEncryptor:
    """Handles encryption and decryption of credentials"""

    def __init__(self, master_key: str = None):
        """
        Initialize the encryptor with a master key

        Args:
            master_key (str): Master key for encryption. If None, generates from machine ID
        """
        if master_key:
            # Derive a key from the provided master key
            self.key = base64.urlsafe_b64encode(
                hashlib.sha256(master_key.encode()).digest()
            )
        else:
            # Generate from environment or machine
            self.key = self._get_or_create_key()

        self.cipher = Fernet(self.key)

    def _get_or_create_key(self) -> bytes:
        """Get encryption key from environment or create one"""
        key_file = ".encryption.key"

        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(key)
            print(f"⚠️  Encryption key generated and saved to {key_file}")
            print("   Keep this file safe! Anyone with this file can decrypt your credentials.")
            return key

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt a string

        Args:
            plaintext (str): The text to encrypt

        Returns:
            str: Encrypted text (can be stored in .env)
        """
        encrypted = self.cipher.encrypt(plaintext.encode())
        return encrypted.decode()

    def decrypt(self, encrypted_text: str) -> str:
        """
        Decrypt a string

        Args:
            encrypted_text (str): Encrypted text from .env

        Returns:
            str: Decrypted plaintext
        """
        try:
            decrypted = self.cipher.decrypt(encrypted_text.encode())
            return decrypted.decode()
        except Exception as e:
            raise ValueError(f"Failed to decrypt credential: {str(e)}")


def encrypt_credential(value: str, master_key: str = None) -> str:
    """
    Helper function to encrypt a single credential

    Args:
        value (str): The credential to encrypt
        master_key (str): Optional master key

    Returns:
        str: Encrypted credential
    """
    encryptor = CredentialEncryptor(master_key)
    return encryptor.encrypt(value)


def decrypt_credential(encrypted_value: str, master_key: str = None) -> str:
    """
    Helper function to decrypt a single credential

    Args:
        encrypted_value (str): The encrypted credential
        master_key (str): Optional master key

    Returns:
        str: Decrypted credential
    """
    encryptor = CredentialEncryptor(master_key)
    return encryptor.decrypt(encrypted_value)
