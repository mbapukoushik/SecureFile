#!/usr/bin/env python3
"""
============================================================
SECURE VAULT — Version 7.1 (Enterprise Gold)
NIST Compliant | AES-256-GCM + ASCON-128 + RSA-3072
============================================================
"""
import os, sys, json, logging, argparse
try:
    import ascon
    from Crypto.Cipher import AES, PKCS1_OAEP
    from Crypto.Random import get_random_bytes
    from Crypto.Protocol.KDF import PBKDF2
    from Crypto.PublicKey import RSA
    from Crypto.Hash import SHA256
except ImportError as e:
    sys.exit(f"[CRITICAL] Missing libraries: {e}")

MAX_ATTEMPTS = 3
LOCK_FILE = "lock_status.json"
VAULT_CONFIG = "vault_config.json"
RECOVERY_KEY = "recovery_key.pem"
LOG_FILE = "secure_vault.log"
RSA_KEY_SIZE = 3072

def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(levelname)-8s %(message)s", handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(LOG_FILE)])
    return logging.getLogger("SecureVault")

def init_vault(logger):
    if os.path.exists(VAULT_CONFIG): sys.exit("[!] Vault already initialized.")
    logger.info(f"Initializing Enterprise Vault (RSA-{RSA_KEY_SIZE})...")
    keypair = RSA.generate(RSA_KEY_SIZE)
    with open(VAULT_CONFIG, 'w') as f: json.dump({"public_key": keypair.publickey().export_key().decode()}, f)
    with open(RECOVERY_KEY, 'wb') as f: f.write(keypair.export_key())
    logger.info( "✔ Vault Configured. MOVE 'recovery_key.pem' TO USB STORAGE IMMEDIATELY." )

def recover_vault(logger, key_path):
    if not os.path.exists(VAULT_CONFIG): sys.exit("[!] Run 'init' first.")
    try:
        with open(VAULT_CONFIG) as f: pub_key = RSA.import_key(json.load(f)["public_key"])
        with open(key_path, 'rb') as f: priv_key = RSA.import_key(f.read())

        challenge = get_random_bytes(32)
        cipher_enc = PKCS1_OAEP.new(pub_key, hashAlgo=SHA256)
        cipher_dec = PKCS1_OAEP.new(priv_key, hashAlgo=SHA256)

        if challenge != cipher_dec.decrypt(cipher_enc.encrypt(challenge)): raise ValueError
        with open(LOCK_FILE, 'w') as f: json.dump({"attempts": 0}, f)
        logger.info( "✔ Identity Verified. System Unlocked." )
    except:
        logger.critical("SECURITY ALERT: Access Denied (Key Mismatch)")
        sys.exit(1)

class CryptoEngine:
    def __init__(self, logger): self.logger = logger
    def encrypt(self, file_path, password):
        salt, aes_nonce, ascon_nonce = get_random_bytes(16), get_random_bytes(12), get_random_bytes(16)
        keys = PBKDF2(password, salt, dkLen=48, count=100000)
        aes_key, ascon_key = keys[:32], keys[32:]

        with open(file_path, 'rb') as f: plaintext = f.read()
        ciphertext, tag = AES.new(aes_key, AES.MODE_GCM, nonce=aes_nonce).encrypt_and_digest(plaintext)

        metadata = f"{aes_nonce.hex()}:{tag.hex()}".encode()
        enc_header = ascon.encrypt(ascon_key, ascon_nonce, associateddata=salt, plaintext=metadata)

        with open(file_path + ".enc", 'wb') as f:
            f.write(salt + ascon_nonce + len(enc_header).to_bytes(4,'big') + enc_header + ciphertext)
        self.logger.info( f"✔ Secured:  {file_path}.enc")

    def decrypt(self, file_path, password):
        try:
            with open(file_path, 'rb') as f:
                salt, ascon_nonce = f.read(16), f.read(16)
                header_len = int.from_bytes(f.read(4), 'big')
                enc_header, body = f.read(header_len), f.read()

            keys = PBKDF2(password, salt, dkLen=48, count=100000)
            meta = ascon.decrypt(keys[32:], ascon_nonce, associateddata=salt, ciphertext=enc_header)
            aes_nonce_hex, tag_hex = meta.decode().split(':')

            plaintext = AES.new(keys[:32], AES.MODE_GCM, nonce=bytes.fromhex(aes_nonce_hex)).decrypt_and_verify(body, bytes.fromhex(tag_hex))
            with open(file_path.replace(".enc", ""), 'wb') as f: f.write(plaintext)
            self.logger.info( f"✔ Restored:  {file_path.replace('.enc', '')}")
            return True
        except: return False

def main():
    logger = setup_logging()
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    rec = sub.add_parser("recover"); rec.add_argument("--key", required=True)
    enc = sub.add_parser("encrypt"); enc.add_argument("file"); enc.add_argument("--password", required=True)
    dec = sub.add_parser("decrypt"); dec.add_argument("file"); dec.add_argument("--password", required=True)

    args = parser.parse_args()
    engine = CryptoEngine(logger)

    if args.command in ["encrypt", "decrypt"]:
        attempts = 0
        if os.path.exists(LOCK_FILE):
            try:
                with open(LOCK_FILE) as f: attempts = json.load(f).get("attempts", 0)
            except: pass
        if attempts >= MAX_ATTEMPTS: logger.critical("SYSTEM LOCKED."); sys.exit(1)

    if args.command == "init": init_vault(logger)
    elif args.command == "recover": recover_vault(logger, args.key)
    elif args.command == "encrypt": engine.encrypt(args.file, args.password)
    elif args.command == "decrypt":
        if not engine.decrypt(args.file, args.password):
            logger.warning(f"Strike {attempts+1}/{MAX_ATTEMPTS}")
            with open(LOCK_FILE, 'w') as f: json.dump({"attempts": attempts + 1}, f)
            sys.exit(1)

if __name__ == "__main__": main()
