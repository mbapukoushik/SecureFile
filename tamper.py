import os
print("--- STARTING INTEGRITY ATTACK ---")
target = "pattern.txt.enc"
with open(target, "rb") as f: data = bytearray(f.read())

print(f"[ATTACK] Corrupting Byte 20 (Header Tamper)...")
data[20] = data[20] ^ 0xFF

with open(target, "wb") as f: f.write(data)
print("[ATTACK] Tampered file saved. Decryption should now fail.")
