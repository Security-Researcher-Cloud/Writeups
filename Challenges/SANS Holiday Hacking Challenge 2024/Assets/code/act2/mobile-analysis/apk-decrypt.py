from base64 import b64decode  
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes  
from cryptography.hazmat.backends import default_backend  
from typing import Optional  
  
  
def add_base64_padding(data: str) -> str:  
    """  
    Ensure the Base64 string is properly padded.  
    Args:        data (str): Base64 encoded string that might be missing padding  
    Returns:        str: Properly padded Base64 string    """    return data + '=' * (-len(data) % 4)  
  
  
def decrypt_aes_gcm_no_padding(key_b64: str, iv_b64: str, ciphertext_b64: str) -> Optional[str]:  
    """  
    Decrypt data using AES-GCM mode with no padding.  
    Args:        key_b64 (str): Base64 encoded encryption key        iv_b64 (str): Base64 encoded initialization vector        ciphertext_b64 (str): Base64 encoded ciphertext with auth tag  
    Returns:        Optional[str]: Decrypted string or None if decryption fails    """    try:  
        # Ensure the Base64 strings are properly padded  
        key_b64 = add_base64_padding(key_b64)  
        iv_b64 = add_base64_padding(iv_b64)  
        ciphertext_b64 = add_base64_padding(ciphertext_b64)  
  
        # Decode the Base64-encoded inputs  
        key = b64decode(key_b64)  
        iv = b64decode(iv_b64)  
        ciphertext = b64decode(ciphertext_b64)  
  
        # Validate input lengths  
        if len(key) not in [16, 24, 32]:  # AES-128, AES-192, or AES-256  
            raise ValueError(f"Invalid key length: {len(key)}. Must be 16, 24, or 32 bytes.")  
        if len(iv) != 12:  # GCM mode requires 12-byte IV  
            raise ValueError(f"Invalid IV length: {len(iv)}. Must be 12 bytes.")  
        if len(ciphertext) < 16:  # Must at least contain the tag  
            raise ValueError("Ciphertext too short to contain authentication tag")  
  
        # Split the ciphertext and tag  
        tag_length = 16  # GCM tag is always 16 bytes  
        actual_ciphertext = ciphertext[:-tag_length]  
        tag = ciphertext[-tag_length:]  
  
        # Create and initialize cipher  
        cipher = Cipher(  
            algorithms.AES(key),  
            modes.GCM(iv, tag),  
            backend=default_backend()  
        )  
        decryptor = cipher.decryptor()  
  
        # Perform decryption  
        plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()  
        return plaintext.decode('utf-8')  
  
    except ValueError as ve:  
        print(f"Validation error: {ve}")  
        return None  
    except Exception as e:  
        print(f"Decryption failed: {e}")  
        return None

if __name__ == "__main__":  
    base64_key = 'rmDJ1wJ7ZtKy3lkLs6X9bZ2Jvpt6jL6YWiDsXtgjkXw'  
    base64_iv = 'Q2hlY2tNYXRlcml4'  
    base64_ciphertext = input("base64 encoded value: ")  
  
    decrypted = decrypt_aes_gcm_no_padding(base64_key, base64_iv, base64_ciphertext)  
    if decrypted:  
        print("Decrypted text:", decrypted)