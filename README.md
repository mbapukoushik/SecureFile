# SecureFile: Enterprise Hybrid Cryptographic Vault
**Group 12 Mini-Project**

## Overview
SecureFile is a NIST-compliant file encryption architecture that combines **AES-256-GCM** (for bulk data confidentiality) with **ASCON-128** (for lightweight metadata binding and integrity). It prevents offline tampering and brute-force dictionary attacks.

## Security Architecture
1. **Outer Layer (ASCON-128):** Protects the AES metadata and attempt limits.
2. **Inner Layer (AES-256-GCM):** Encrypts the payload.
3. **Recovery Layer (RSA-3072):** Asymmetric challenge-response for Admin recovery.

## Installation
```bash
pip install pycryptodome ascon
