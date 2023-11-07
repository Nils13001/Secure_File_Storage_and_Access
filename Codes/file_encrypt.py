from send_mail import mail
from img_stego import encode
import rsa
from cryptography.fernet import Fernet
from base64 import b64encode

def Encoding():
    # Generate public + private keypair
    publicKey, privateKey = rsa.newkeys(2048)

    # Generate a symmetric key
    symmetricKey = Fernet.generate_key()

    # Create a symmetric key object
    f = Fernet(symmetricKey)

    # Provide name of file to be encrypted and read its content
    filename = input("Enter name of the file to be encoded (with extension): ")
    with open(filename, 'rb') as file:
                data = file.read()

    # Encrypt data with symmetric key
    enc_data = f.encrypt(data)

    # Convert the encrypted data to base64 for sending over the network
    b64_enc_data = b64encode(enc_data)

    # Write this encoded/encrypted data to a new file and provide a new name for it
    new_filename = input("Provide new name for encoded file (with extension): ")
    with open (new_filename, 'wb') as file:
                file.write(b64_enc_data)

    # Encrypt the Symmetric key with Public Key
    enc_symmetricKey = rsa.encrypt(symmetricKey, publicKey)
    
    # Encode the encrypted key into base64
    b64_enc_symmetricKey = b64encode(enc_symmetricKey)

    # Decode the encrypted/encoded key into UTF-8 format
    b64_enc_symmetricKey = b64_enc_symmetricKey.decode('utf-8')


    # Convert private key to string
    pkr = privateKey.save_pkcs1().decode('utf-8')

    # Pass the encrypted/encoded symmetric key and encoded private key
    # for steganography and take their lengths and image name
    leng, imgname, lenp = encode(b64_enc_symmetricKey, pkr)

    # Passing the returned values to mail module to mail them via Mailtrap
    mail(leng, lenp, imgname)

    # Return the name of New Encrypted File
    return new_filename
