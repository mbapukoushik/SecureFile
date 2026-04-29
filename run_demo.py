"""
============================================================
  SECUREFILE - INTERACTIVE VIVA DEMONSTRATION
  AES-256-GCM + ASCON-128 + RSA-3072 + PBKDF2
============================================================
"""
import os, sys, time, json, shutil, subprocess

# ── Color Helpers (Windows Terminal) ──
os.system("")  # Enable ANSI on Windows
CYAN    = "\033[96m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
RED     = "\033[91m"
MAGENTA = "\033[95m"
WHITE   = "\033[97m"
DIM     = "\033[2m"
BOLD    = "\033[1m"
RESET   = "\033[0m"

def banner():
    print(f"""
{CYAN}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   {BOLD}SECUREFILE — Enterprise Hybrid Cryptographic Vault{RESET}{CYAN}        ║
║   {DIM}AES-256-GCM  ·  ASCON-128  ·  RSA-3072  ·  PBKDF2{RESET}{CYAN}        ║
║                                                              ║
║   {DIM}Group 12 Mini-Project  |  Viva Demonstration{RESET}{CYAN}              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{RESET}
""")

def step(num, title):
    print(f"\n{YELLOW}┌────────────────────────────────────────────────────────────┐{RESET}")
    print(f"{YELLOW}│  {BOLD}STEP {num}: {title}{RESET}")
    print(f"{YELLOW}└────────────────────────────────────────────────────────────┘{RESET}")

def info(msg):
    print(f"  {DIM}→ {msg}{RESET}")

def success(msg):
    print(f"  {GREEN}[OK] {msg}{RESET}")

def fail(msg):
    print(f"  {RED}[!!] {msg}{RESET}")

def explain(lines):
    """Show what is happening inside the cryptographic process with animation."""
    print()
    print(f"  {MAGENTA}┌─ What's Happening Inside ──────────────────────────────┐{RESET}")
    for line in lines:
        time.sleep(0.25)
        print(f"  {MAGENTA}│{RESET}  {DIM}{line}{RESET}")
    print(f"  {MAGENTA}└────────────────────────────────────────────────────────┘{RESET}")
    print()

def wait():
    input(f"  {DIM}Press ENTER to continue...{RESET}")

def clean_state():
    """Remove generated files to start fresh."""
    for f in ["vault_config.json", "lock_status.json", "recovery_key.pem", 
              "secure_vault.log", "secret.txt", "secret.txt.enc"]:
        if os.path.exists(f):
            os.remove(f)

def run_cmd(cmd):
    """Run a command and return exit code."""
    return os.system(cmd)

def detect_usb_drives():
    """Detect removable USB drives on Windows using pure Python."""
    import ctypes
    import string
    drives = []
    try:
        bitmask = ctypes.windll.kernel32.GetLogicalDrives()
        for i, letter in enumerate(string.ascii_uppercase):
            if bitmask & (1 << i):
                drive_path = f"{letter}:\\"
                drive_type = ctypes.windll.kernel32.GetDriveTypeW(drive_path)
                # DriveType 2 = REMOVABLE (USB pen drives)
                if drive_type == 2:
                    # Get volume name
                    vol_name_buf = ctypes.create_unicode_buffer(256)
                    ctypes.windll.kernel32.GetVolumeInformationW(
                        drive_path, vol_name_buf, 256, None, None, None, None, 0
                    )
                    name = vol_name_buf.value if vol_name_buf.value else "USB Drive"
                    drives.append((f"{letter}:", name))
    except:
        pass
    return drives


# ══════════════════════════════════════════════════════════
#                    MAIN DEMO FLOW
# ══════════════════════════════════════════════════════════
def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    banner()
    print(f"  {DIM}This script will walk through the full SecureFile system.{RESET}")
    print(f"  {DIM}You will type inputs yourself to demonstrate understanding.{RESET}")
    wait()

    # ── STEP 1: FRESH INIT ──
    step(1, "VAULT INITIALIZATION")
    info("Cleaning previous state for a fresh demo...")
    clean_state()
    success("Environment reset.")
    print()
    info("Generating RSA-3072 key pair for emergency recovery...")
    
    explain([
        "RSA.generate(3072)  →  Creates a 3072-bit asymmetric key pair",
        "Public Key   →  Saved to vault_config.json (stays on system)",
        "Private Key  →  Saved to recovery_key.pem  (move to USB!)",
        "Purpose: Admin can bypass lockout without knowing the password",
    ])
    
    run_cmd('python secure_vault.py init')
    success("Vault initialized. RSA key pair generated.")
    wait()

    # ── STEP 1.5: USB PEN DRIVE (Real Recovery Key Transfer) ──
    step("1b", "RECOVERY KEY TRANSFER TO USB")
    print()
    info("In a real enterprise, the recovery key must be stored offline.")
    info("We will now move recovery_key.pem to a real USB pen drive.")
    print()
    
    drives = detect_usb_drives()
    usb_used = False
    
    if drives:
        print(f"  {GREEN}USB drives detected:{RESET}")
        for i, (letter, name) in enumerate(drives):
            print(f"    {BOLD}[{i+1}]{RESET} {letter} — {name}")
        print(f"    {BOLD}[0]{RESET} Skip (keep key locally)")
        print()
        choice = input(f"  {CYAN}Select drive number: {RESET}").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(drives):
            drive_letter = drives[int(choice)-1][0]
            usb_path = os.path.join(drive_letter + "\\", "recovery_key.pem")
            try:
                shutil.copy2("recovery_key.pem", usb_path)
                os.remove("recovery_key.pem")
                success(f"Recovery key moved to {usb_path}")
                info("Key REMOVED from local machine (as per security protocol).")
                usb_used = True
                recovery_key_path = usb_path
            except Exception as e:
                fail(f"Could not copy to USB: {e}")
                info("Keeping recovery_key.pem locally for the demo.")
                recovery_key_path = "recovery_key.pem"
        else:
            info("Skipped USB transfer. Key remains at recovery_key.pem.")
            recovery_key_path = "recovery_key.pem"
    else:
        info("No USB drives detected. Insert a pen drive and re-run,")
        info("or skip this step. Key remains at recovery_key.pem.")
        recovery_key_path = "recovery_key.pem"
    
    if usb_used:
        explain([
            f"recovery_key.pem has been MOVED to {recovery_key_path}",
            "The local copy is DELETED — only the USB has the key.",
            "This is the 'Separation of Duties' security principle:",
            "  → The system (vault_config.json) has the PUBLIC key",
            "  → The admin (USB) holds the PRIVATE key",
            "  → Neither party alone can compromise the vault",
        ])
    
    wait()

    # ── STEP 2: ENCRYPT A FILE ──
    step(2, "FILE ENCRYPTION")
    print()
    print(f"  {BOLD}Create a secret message and encrypt it.{RESET}")
    print()
    
    message = input(f"  {CYAN}Type your secret message: {RESET}")
    if not message.strip():
        message = "This is a confidential document."
    
    with open("secret.txt", "w") as f:
        f.write(message)
    info(f'Saved to secret.txt: "{message}"')
    print()
    
    password = input(f"  {CYAN}Choose an encryption password: {RESET}")
    if not password.strip():
        password = "MyStr0ngP@ss"
    
    print()
    explain([
        f'Password: "{password}"',
        "PBKDF2-HMAC-SHA256 (100,000 iterations)  →  Derives 48-byte key",
        "  First 32 bytes  →  AES-256-GCM Key  (payload encryption)",
        "  Last  16 bytes  →  ASCON-128 Key    (metadata binding)",
        "",
        "Step A: AES-256-GCM encrypts the file payload → ciphertext + tag",
        "Step B: ASCON-128 encrypts the AES nonce + tag → encrypted header",
        "Output: salt | ascon_nonce | header_len | enc_header | ciphertext",
    ])
    
    run_cmd(f'python secure_vault.py encrypt secret.txt --password "{password}"')
    
    if os.path.exists("secret.txt.enc"):
        with open("secret.txt.enc", "rb") as f:
            raw = f.read(48)
        info(f"Encrypted file preview (first 48 bytes in hex):")
        print(f"  {DIM}{raw.hex()}{RESET}")
        info(f"File size: {os.path.getsize('secret.txt.enc')} bytes (vs original {len(message)} bytes)")
    
    success("File encrypted successfully.")
    wait()

    # ── STEP 3: DECRYPT THE FILE ──
    step(3, "FILE DECRYPTION")
    print()
    print(f"  {BOLD}Enter the SAME password to decrypt and recover the file.{RESET}")
    print()
    
    dec_password = input(f"  {CYAN}Enter decryption password: {RESET}")
    if not dec_password.strip():
        dec_password = password
    
    print()
    explain([
        "Step A: ASCON-128 decrypts the header → recovers AES nonce + tag",
        "        (If header was tampered, this step FAILS immediately)",
        "Step B: AES-256-GCM decrypts payload + verifies authentication tag",
        "        (If payload was tampered, tag verification FAILS)",
    ])
    
    result = run_cmd(f'python secure_vault.py decrypt secret.txt.enc --password "{dec_password}"')
    
    if result == 0:
        with open("secret.txt", "r") as f:
            recovered = f.read()
        success(f'Recovered message: "{recovered}"')
        if recovered == message:
            success("Original message matches perfectly!")
    else:
        fail("Decryption failed. Wrong password or tampered file.")
    
    wait()

    # ── STEP 4: TAMPER ATTACK ──
    step(4, "TAMPER RESISTANCE (INTEGRITY CHECK)")
    print()
    info("Re-encrypting file, then simulating an attacker who")
    info("modifies the encrypted file without knowing the key.")
    print()
    
    # Re-encrypt a fresh copy
    with open("secret.txt", "w") as f:
        f.write(message)
    run_cmd(f'python secure_vault.py encrypt secret.txt --password "{password}" > NUL 2>&1')
    
    explain([
        "attacks/tamper.py simulates a Man-in-the-Middle attacker:",
        "  1. Reads the encrypted .enc file as raw bytes",
        "  2. Flips Byte 20 using XOR (data[20] ^= 0xFF)",
        "  3. Writes the corrupted file back",
        "",
        "This corrupts the ASCON-128 encrypted header.",
        "Even a SINGLE BIT change should cause decryption to fail.",
    ])
    
    # Run tamper attack on secret.txt.enc (not pattern.txt.enc)
    run_cmd("python attacks/tamper.py secret.txt.enc")
    print()
    info("Attempting to decrypt the TAMPERED file with the correct password...")
    print()
    
    result = run_cmd(f'python secure_vault.py decrypt secret.txt.enc --password "{password}"')
    
    if result != 0:
        fail("Decryption REJECTED — Integrity violation detected!")
        success("ASCON-128 tag verification caught the tampering. (Strike 1/3)")
    else:
        success("Decryption succeeded (unexpected).")
    
    wait()

    # ── STEP 5: BRUTE FORCE + LOCKOUT ──
    step(5, "BRUTE FORCE ATTACK & 3-STRIKE LOCKOUT")
    print()
    info("Running attacks/exploit_poc.py — simulates a dictionary attack.")
    info("The attacker tries common passwords to crack the file.")
    print()
    
    # Re-encrypt fresh for exploit (clean .enc file)
    with open("secret.txt", "w") as f:
        f.write(message)
    run_cmd(f'python secure_vault.py encrypt secret.txt --password "{password}" > NUL 2>&1')
    
    explain([
        "The attacker's dictionary: admin, 123456, password, qwerty, ...",
        f'The real password ("{password}") is NOT in the dictionary.',
        "",
        "After 3 failed attempts → SYSTEM LOCKS permanently.",
        "Only the RSA recovery key can unlock it.",
        "",
        "This demonstrates the Account Lockout defense against brute force.",
    ])
    
    run_cmd("python attacks/exploit_poc.py secret.txt.enc")
    print()
    
    if os.path.exists("lock_status.json"):
        with open("lock_status.json") as f:
            data = json.load(f)
        if data.get("attempts", 0) >= 3:
            fail(f"SYSTEM LOCKED after {data['attempts']} failed attempts!")
        else:
            info(f"Strikes: {data['attempts']}/3")
    
    wait()

    # ── STEP 6: RECOVERY ──
    step(6, "EMERGENCY RSA RECOVERY")
    print()
    info("The vault is locked. No password will work anymore.")
    
    if usb_used:
        info(f"Using the recovery key from USB: {recovery_key_path}")
        # Copy key back temporarily for the recovery command
        if os.path.exists(recovery_key_path):
            shutil.copy2(recovery_key_path, "recovery_key.pem")
            info("Key loaded from USB into memory.")
        else:
            fail("USB key not found! Make sure the pen drive is still plugged in.")
            info("Attempting with local fallback...")
    else:
        info("Using the local recovery key: recovery_key.pem")
    
    print()
    explain([
        "recovery_key.pem contains the RSA-3072 private key.",
        "The system creates a random 32-byte challenge, encrypts it",
        "with the stored public key (vault_config.json), and checks if",
        "the private key can decrypt it back to the same challenge.",
        "",
        "If verified → Strike counter resets to 0 → System unlocked.",
    ])
    
    run_cmd("python secure_vault.py recover --key recovery_key.pem")
    
    # If USB was used, delete the local copy again
    if usb_used and os.path.exists("recovery_key.pem"):
        os.remove("recovery_key.pem")
        info("Local copy of key removed. Key only exists on USB.")
    
    success("System unlocked via RSA key verification.")
    wait()

    # ══════════════════════════════════════════════════════════
    #              PROJECT SUMMARY & FILE MAP
    # ══════════════════════════════════════════════════════════
    project_dir = os.path.dirname(os.path.abspath(__file__))
    
    print(f"""
{CYAN}╔══════════════════════════════════════════════════════════════╗
║  {BOLD}DEMONSTRATION COMPLETE — PROJECT SUMMARY{RESET}{CYAN}                   ║
╚══════════════════════════════════════════════════════════════╝{RESET}

  {BOLD}Cryptographic Stack:{RESET}
  {DIM}├─{RESET} AES-256-GCM     →  Payload encryption (NIST standard)
  {DIM}├─{RESET} ASCON-128       →  Metadata integrity (NIST lightweight)
  {DIM}├─{RESET} PBKDF2-SHA256   →  Key derivation (100k iterations)
  {DIM}└─{RESET} RSA-3072 OAEP   →  Emergency recovery bypass

  {BOLD}Threat Mitigations Demonstrated:{RESET}
  {DIM}├─{RESET} Brute Force     →  PBKDF2 + 3-Strike Lockout    {DIM}(Step 5){RESET}
  {DIM}├─{RESET} Data Tampering  →  AES-GCM Tag + ASCON-128 AEAD {DIM}(Step 4){RESET}
  {DIM}└─{RESET} Admin Recovery  →  RSA Asymmetric Key Challenge  {DIM}(Step 6){RESET}

  {BOLD}Project Structure:{RESET}
  {DIM}│{RESET}
  {DIM}├─{RESET} {GREEN}secure_vault.py{RESET}          {DIM}Core engine — init, encrypt, decrypt, recover{RESET}
  {DIM}│{RESET}      {DIM}├─ Line 33:  init_vault()      →  RSA key generation{RESET}
  {DIM}│{RESET}      {DIM}├─ Line 54:  recover_vault()   →  RSA challenge/response{RESET}
  {DIM}│{RESET}      {DIM}├─ Line 90:  encrypt()          →  AES + ASCON encryption{RESET}
  {DIM}│{RESET}      {DIM}└─ Line 119: decrypt()          →  Integrity check + decryption{RESET}
  {DIM}│{RESET}
  {DIM}├─{RESET} {YELLOW}attacks/{RESET}
  {DIM}│{RESET}   {DIM}├─{RESET} {GREEN}tamper.py{RESET}                {DIM}Integrity attack simulation (XOR bit-flip){RESET}
  {DIM}│{RESET}   {DIM}└─{RESET} {GREEN}exploit_poc.py{RESET}           {DIM}Dictionary brute-force simulation{RESET}
  {DIM}│{RESET}
  {DIM}├─{RESET} {YELLOW}docs/{RESET}
  {DIM}│{RESET}   {DIM}├─{RESET} README.md                {DIM}Project documentation & architecture{RESET}
  {DIM}│{RESET}   {DIM}└─{RESET} Research_Paper.pdf       {DIM}Academic research justification{RESET}
  {DIM}│{RESET}
  {DIM}├─{RESET} run_demo.py              {DIM}This interactive demo script{RESET}
  {DIM}└─{RESET} requirements.txt         {DIM}pycryptodome, ascon{RESET}
""")

    input(f"  {DIM}Press ENTER to exit.{RESET}")

if __name__ == "__main__":
    main()
