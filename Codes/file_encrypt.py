
from mail import mail
from stego import encode
import rsa
from cryptography.fernet import Fernet
from base64 import b64encode

def Encoding():
    # Generate public + private keypair
    publicKey, privateKey = rsa.newkeys(2048)

    # Generate a symmetric key
    symmetricKey = Fernet.generate_key()

    f = Fernet(symmetricKey)

    # Sample data to encrypt

    filename = input("File to be encoded: ")
    with open(filename, 'rb') as file:
                data = file.read()

    # Encrypt data with symmetric key
    enc_data = f.encrypt(data)

    # Convert to base64 for sending over the network
    b64_enc_data = b64encode(enc_data)
    new_filename = input("Name for encoded file: ")
    with open (new_filename, 'wb') as file:
                file.write(b64_enc_data)

    enc_symmetricKey = rsa.encrypt(symmetricKey, publicKey)
    # Convert the symmetric key to base64 for sending
    # over the network

    b64_enc_symmetricKey = b64encode(enc_symmetricKey)

    b64_enc_symmetricKey = b64_enc_symmetricKey.decode('utf-8')

    #Private Key conversion to string and length
    pkr = privateKey.save_pkcs1().decode('utf-8')

    leng, imgname, lenp = encode(b64_enc_symmetricKey, pkr) #Taking length of key, to be sent with image

    mail(leng, lenp, imgname)
    return new_filename