# SecureFile: Enterprise Hybrid Cryptographic Vault
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![NIST Compliant](https://img.shields.io/badge/NIST-Compliant-green.svg)](https://csrc.nist.gov/publications/detail/sp/800-38d/final)

**Group 12 Mini-Project**  
*Academic Research Prototype — Not for Production Use*

## Overview
SecureFile is a high-assurance file encryption architecture designed to mitigate advanced persistent threats and offline tampering. By implementing a **nested hybrid cryptographic scheme**, it provides strong confidentiality through **AES-256-GCM** and lightweight metadata integrity through **ASCON-128**, an authenticated encryption cipher selected by NIST for lightweight applications.

## Technical Architecture

### Cryptographic Stack
1.  **Transport/Bulk Layer**: `AES-256-GCM` — High-performance authenticated encryption for file payloads.
2.  **Metadata Binding Layer**: `ASCON-128` — Protects bulk-layer nonces and tags from pre-computation or substitution attacks.
3.  **Key Derivation**: `PBKDF2-HMAC-SHA256` — 100,000 iterations to resist GPU-accelerated brute force.
4.  **Admin Recovery**: `RSA-3072` (OAEP Padding) — Asymmetric bypass mechanism for emergency access.

### System Flow
```mermaid
graph TD
    subgraph KDF [Key Derivation]
    PW[User Password] --> K[PBKDF2-SHA256]
    K --> AK[32B AES Key]
    K --> AS[16B ASCON Key]
    end

    subgraph Bulk [Payload Encryption]
    PL[Plaintext File] --> AES[AES-256-GCM]
    AK --> AES
    AES --> CT[Encrypted Payload]
    AES --> TG[Authentication Tag]
    end

    subgraph Meta [Metadata & Integrity]
    AS --> ASN[ASCON-128 AEAD]
    TG --> ASN
    AN[AES Nonce] --> ASN
    ASN --> HDR[Encrypted Header]
    end

    CT --> FIN[.enc File Output]
    HDR --> FIN
```

## Threat Model & Security Analysis

| Threat Segment | Targeted Mitigation | Effectiveness |
| :--- | :--- | :--- |
| **Brute-Force Attack** | PBKDF2 w/ 100k rounds + Account Lockout (3 attempts) | High (Prevents offline/online guessing) |
| **Metadata Forgery** | ASCON-128 Authenticated Encryption (AEAD) | High (Integrity bounds metadata to payload) |
| **Offline Tampering** | AES-GCM Tag Verification (Inner Layer) | Ultra (Detects even single-bit changes) |
| **Admin Key Theft** | RSA-3072 Asymmetric Recovery Logic | High (Separation of duties) |
| **Side-Channel Analysis** | Constant-time operation (Library-dependent) | Medium (Environment Dependent) |

## Quick Start

### Prerequisites
```powershell
pip install -r requirements.txt
```

### Interactive Demo (Recommended)
Run the full interactive demonstration that walks through all features step-by-step:
```powershell
python run_demo.py
```
Or simply double-click `run_demo.bat`.

The demo covers:
1. **Vault Initialization** — RSA-3072 key pair generation
2. **USB Key Transfer** — Moves recovery key to a real USB pen drive
3. **File Encryption** — You type your own message and password
4. **File Decryption** — Recovers the original file
5. **Tamper Resistance** — Simulates a bit-flip attack, shows ASCON-128 detection
6. **Brute Force & Lockout** — Dictionary attack triggers 3-strike lockout
7. **Emergency Recovery** — RSA key from USB unlocks the vault

### Manual Usage

#### 1. Initialization
Generate the RSA recovery pair. **Keep `recovery_key.pem` secure and offline.**
```powershell
python secure_vault.py init
```

#### 2. Encryption
Secure any file with a strong master password.
```powershell
python secure_vault.py encrypt secret_data.txt --password "MySUp3rS3cr3t"
```

#### 3. Decryption
Restore access to your encrypted vault.
```powershell
python secure_vault.py decrypt secret_data.txt.enc --password "MySUp3rS3cr3t"
```

#### 4. Emergency Recovery
Reset strike limits or regain access if the master password is lost using the RSA Private Key.
```powershell
python secure_vault.py recover --key recovery_key.pem
```

## Project Structure

```
SecureFile/
│
├── secure_vault.py          Core engine — init, encrypt, decrypt, recover
│   ├── Line 33:  init_vault()      →  RSA key generation
│   ├── Line 54:  recover_vault()   →  RSA challenge/response
│   ├── Line 90:  encrypt()         →  AES-256 + ASCON-128 encryption
│   └── Line 119: decrypt()         →  Integrity check + decryption
│
├── attacks/
│   ├── tamper.py                   Integrity attack simulation (XOR bit-flip)
│   └── exploit_poc.py              Dictionary brute-force simulation
│
├── docs/
│   ├── README.md                   Project documentation & architecture
│   └── SecureFile_Research_Paper.pdf.pdf   Academic research paper
│
├── run_demo.py                     Interactive viva demonstration script
├── run_demo.bat                    One-click demo launcher
├── pattern.txt                     Sample file for encryption
├── requirements.txt                Python dependencies (pycryptodome, ascon)
└── .gitignore
```

## Core Code Map

| Function | File | Line | Purpose |
| :--- | :--- | :--- | :--- |
| `init_vault()` | `secure_vault.py` | 33 | Generates RSA-3072 key pair for recovery |
| `recover_vault()` | `secure_vault.py` | 54 | RSA challenge-response to bypass lockout |
| `CryptoEngine.encrypt()` | `secure_vault.py` | 90 | AES-256-GCM + ASCON-128 encryption pipeline |
| `CryptoEngine.decrypt()` | `secure_vault.py` | 119 | ASCON integrity check → AES-GCM decryption |
| `tamper.py` | `attacks/` | — | XOR bit-flip on encrypted header |
| `exploit_poc.py` | `attacks/` | — | Dictionary attack with 7 common passwords |

---
*Developed for the Modern Cryptography course. All rights reserved.*
