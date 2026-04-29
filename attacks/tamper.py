"""
============================================================
INTEGRITY TAMPERING DEMONSTRATION
Simulates an attacker modifying an encrypted file in transit 
or offline, demonstrating ASCON-128 tag verification.
============================================================
Usage:
  python attacks/tamper.py                  (defaults to pattern.txt.enc)
  python attacks/tamper.py secret.txt.enc   (custom target)
"""
import sys

# Accept target file from command line, or default to pattern.txt.enc
target = sys.argv[1] if len(sys.argv) > 1 else "pattern.txt.enc"

print("--- STARTING INTEGRITY ATTACK ---")
print(f"[TARGET] {target}")

# Read the original encrypted file bytes into memory
with open(target, "rb") as f: 
    data = bytearray(f.read())

print("[ATTACK] Simulating Bit-Flip / Data Corruption on Byte 20 (Header)...")

# XOR the 20th byte to maliciously change the data without knowing the key
data[20] = data[20] ^ 0xFF

# Write the corrupted data back to the file
with open(target, "wb") as f: 
    f.write(data)

print("[ATTACK] Tampered file saved.")
print("The SecureVault Decryption should now detect this and FAIL.")
