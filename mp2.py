from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# Generate Keypairs (sender | receiver)
def generateKeypair():
    privateKey = rsa.generate_private_key(
        public_exponent = 65537,
        key_size = 2048
    )
    publicKey = privateKey.public_key()
    return privateKey, publicKey

# Receiver and Sender keypairs:
receiverPrivateEnc, receiverPublicEnc = generateKeypair()
senderPrivateSign, senderPublicSign = generateKeypair()

# Key Directory
keyDirectory = {
    "Receiver_Encryption_Public_Key": receiverPublicEnc,
    "Sender_Signing_Public_Key": senderPublicSign
}

def encrypt(msg: str, receiverPublicKey, senderSignPrivateKey):
    if len(msg) > 140:
        raise ValueError("Message must be at most 140 characters long.")
    
    plaintext = msg.encode("ascii")

    ciphertext = receiverPublicKey.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    

    signature = sign(ciphertext, senderSignPrivateKey)

    return ciphertext, signature

def sign(ciphertext, senderSignPrivateKey):
    signature = senderSignPrivateKey.sign(
        ciphertext,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return signature

def verify(ciphertext, signature, senderPublicKey, receiverPrivateKey):
    senderPublicKey.verify(
        signature,
        ciphertext,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    plaintext = decrypt(ciphertext, receiverPrivateKey)

    return plaintext

def decrypt(ciphertext, receiverPrivateKey):
    plaintext = receiverPrivateKey.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return plaintext.decode("ascii")

# Main

def main():
    message = "Hello Sample Message."

    ciphertext, signature = encrypt(message, keyDirectory["Receiver_Encryption_Public_Key"], senderPrivateSign)

    decrypted = verify(ciphertext, signature, keyDirectory["Sender_Signing_Public_Key"], receiverPrivateEnc)

    print("Original message:", message)
    print("Ciphertext:", ciphertext.hex())
    print("Signature:", signature.hex())
    print("Decrypted message:", decrypted)



main()