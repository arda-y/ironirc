import random
import os
import json

import time

from core.crypto import encrypt_message, decrypt_message
from core.shredder import shred, unshred

os.remove("logs.txt") if os.path.exists("logs.txt") else None
start = time.time()

message = """
the internet is a vast, vast place. 
it is full of wonders and horrors, and everything in between."""

print(f"Original: {message}\n----\n", file=open("logs.txt", "w"))

shredded_chunks = shred(message)
# shred the message into 10 chunks, each chunk is a string of characters
print(f"Shredded: {shredded_chunks}\n----\n", file=open("logs.txt", "a"))


e_msg_chunks = encrypt_message(shredded_chunks)
# encrypt each chunk with a unique key derived from PSK + Counter + Chunk ID
print(f"Encrypted: {e_msg_chunks}\n----\n", file=open("logs.txt", "a"))

random.shuffle(e_msg_chunks)
# shuffle chunks intentionally to simulate out-of-order delivery, and make tracking harder for adversaries
print(f"Shuffled: {e_msg_chunks}\n----\n", file=open("logs.txt", "a"))

d_msg_chunks = decrypt_message(e_msg_chunks)
# decrypt chunks with the same keys derived from PSK + Counter + Chunk ID, regardless of order
print(f"Decrypted Chunks: {d_msg_chunks}\n----\n", file=open("logs.txt", "a"))

final_msg = unshred(d_msg_chunks)
# reconstruct the original message from decrypted chunks, ensuring correct order based on frame tags
print(f"Unshredded: {final_msg}\n----\n", file=open("logs.txt", "a"))

finish = time.time()
print(f"Time taken: {finish - start:.4f} seconds", file=open("logs.txt", "a"))
print(f"time taken: {finish - start:.4f} seconds")
