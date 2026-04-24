# CS134 Machine Problem 2 (MP2)

This project demonstrates **authenticated encryption** using an **encrypt-then-sign** construction with **RSA-OAEP** (for confidentiality) and **RSA-PSS** (for authenticity/integrity).

All cryptographic operations are provided by the [`cryptography`](https://cryptography.io/) Python library—no cryptographic algorithms are implemented manually.

## What the program does

The code is in `mp2.py` and implements the following roles and components:

- **Separate keypairs for encryption and signing**
  - The **receiver** generates an RSA keypair used for **encryption/decryption**.
  - The **sender** generates an RSA keypair used for **signing/verification**.

- **Trusted directory service (in-memory)**
  - A Python dictionary named `keyDirectory` stores the public keys that are safe to distribute:
    - `Receiver_Encryption_Public_Key` (used by anyone to encrypt to the receiver)
    - `Sender_Signing_Public_Key` (used by anyone to verify the sender’s signatures)

- **Encrypt-then-sign**
  - `encrypt(message, receiverPublicKey, senderSignPrivateKey)`:
    - Encrypts the ASCII plaintext using **RSA-OAEP with SHA-256** and the receiver’s public encryption key.
    - Signs the resulting ciphertext using **RSA-PSS with SHA-256** and the sender’s private signing key.
    - Returns `(ciphertext, signature)`.

- **Verify-then-decrypt**
  - `verify(ciphertext, signature, senderPublicKey, receiverPrivateKey)`:
    - Verifies the signature on the ciphertext using the sender’s public signing key.
    - Only if verification succeeds, decrypts the ciphertext using the receiver’s private decryption key.
    - Returns the recovered plaintext string.

## Why the message length is limited (RSA is not for “big” plaintext)

RSA-OAEP can only encrypt a limited number of bytes per operation. With:

- RSA modulus size = **2048 bits** (\(256\) bytes)
- Hash = **SHA-256** (\(hLen = 32\) bytes)

the OAEP maximum plaintext length is:

\[
256 - 2 \cdot 32 - 2 = 190 \text{ bytes}
\]

This project further restricts the input to **at most 140 ASCII characters** (`encrypt()` checks this) to stay comfortably under the OAEP limit and to match the machine problem requirement.

## Files

- `mp2.py`: main program demonstrating key generation, directory service, encrypt-then-sign, verify-then-decrypt.

## Requirements

- Python 3.x
- `cryptography` library

Install the dependency:

```bash
pip install cryptography
```

## How to run

Run the script from the project folder:

```bash
python mp2.py
```

By default, `main()` encrypts the message:

- `Hello Sample Message.`

and prints:

- **Original message**
- **Ciphertext** (hex)
- **Signature** (hex)
- **Decrypted message** (should match the original)

## How to use / modify

To encrypt a different message, edit the `message` variable in `main()`:

```python
message = "Your ASCII message here"
```

Constraints:

- The message must be **ASCII** (the code uses `encode("ascii")` / `decode("ascii")`).
- The message must be **≤ 140 characters** (enforced by `encrypt()`).

## Notes on authenticity

Authenticity/integrity is provided by the **signature over the ciphertext** (encrypt-then-sign):

- Any modification of the ciphertext will cause `senderPublicKey.verify(...)` to fail.
- Decryption happens only after successful verification (verify-then-decrypt), which is the intended safe order of operations for this construction.
