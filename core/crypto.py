# 10-DH logic, AES-GCM, and PSK masking

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import hmac
import hashlib

from config import MSG_COUNTER, PSK


def derive_keys(psk: str, counter: int, num_chunks: int = 10) -> list[bytes]:
    keys = []
    for i in range(num_chunks):
        # Every chunk gets a unique key based on PSK + Counter + Chunk ID
        keys.append(
            HKDF(
                algorithm=hashes.SHA256(),
                length=32,
                salt=str(counter).encode(),
                info=f"chunk-{i}".encode(),
            ).derive(psk.encode())
        )
    return keys


def derive_nonce(psk: str, counter: int, chunk_id: int) -> bytes:
    # Nonce is derived from PSK + Counter + Chunk ID to ensure uniqueness without storing it
    return hmac.new(
        psk.encode(), f"{counter}-nonce-{chunk_id}".encode(), hashlib.sha256
    ).digest()[:12]


def encrypt_message(shredded_text: list[str]) -> list[dict[str, str]]:
    keys = derive_keys(PSK, MSG_COUNTER)
    encrypted_chunks = []

    for i in range(10):
        # blind tagging to avoid leaking chunk ID
        tag = hmac.new(
            PSK.encode(), f"{MSG_COUNTER}-tag-{i}".encode(), hashlib.sha256
        ).hexdigest()[:8]

        aesgcm = AESGCM(keys[i])
        nonce = derive_nonce(PSK, MSG_COUNTER, i)  # Utility function recommended

        data_cipher = aesgcm.encrypt(nonce, shredded_text[i].encode(), None)

        # We store the tag instead of an encrypted ID
        encrypted_chunks.append({"tag": tag, "data": data_cipher.hex()})

    return encrypted_chunks


def decrypt_message(received_chunks: list[dict[str, str]]) -> list[str]:
    keys = derive_keys(PSK, MSG_COUNTER)
    decrypted_map = {}

    # 1. Map the expected tags to their IDs (0-9)
    tag_to_id = {}
    for i in range(10):
        t = hmac.new(
            PSK.encode(), f"{MSG_COUNTER}-tag-{i}".encode(), hashlib.sha256
        ).hexdigest()[:8]
        tag_to_id[t] = i

    # 2. Process chunks
    for item in received_chunks:
        tag = item["tag"]
        if tag not in tag_to_id:
            continue  # Skip decoy or corrupted chunks

        chunk_id = tag_to_id[tag]
        cipher_bytes = bytes.fromhex(item["data"])

        aesgcm = AESGCM(keys[chunk_id])
        nonce = derive_nonce(PSK, MSG_COUNTER, chunk_id)

        plain = aesgcm.decrypt(nonce, cipher_bytes, None)
        decrypted_map[chunk_id] = plain.decode()

    # 3. Handle missing chunks gracefully
    return [decrypted_map.get(i, "[LOST]") for i in range(10)]
