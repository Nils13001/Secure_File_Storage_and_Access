from PIL import Image
import rsa
from cryptography.fernet import Fernet
from base64 import b64decode

def img_decode(len1, lp):
    
    # Taking the Stegged Image name and readying it
    # Remember, no JPEG/JPG image
    img = input("Enter the name of image downloaded from email (with extension) : ")
    image = Image.open(img, 'r')
    imgdata = iter(image.getdata())
    
    # Extracting Symmetric Key
    data = ''
    ct = 0
    ls = []
    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
								imgdata.__next__()[:3] +
								imgdata.__next__()[:3]]
        ct+=1
        
        # Strings of binary data
        binstr = ''
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
        d = int(binstr, 2)
        data += chr(d)
        if (pixels[-1] % 2 != 0 or ct==len1):
            ls.append(data)
            break
    
    # Extracting Private Key
    priv = ''
    ct = 0
    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
								imgdata.__next__()[:3] +
								imgdata.__next__()[:3]]
        ct+=1
        # Strings of binary data
        binstr = ''
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
        d = int(binstr, 2)
        priv += chr(d)
        if (pixels[-1] % 2 != 0 or ct==lp):
            ls.append(priv)
            break
    
    # First is Symmetric key and 2nd is Private Key
    return ls[0], ls[1]

def dec_main():
    # Provide the lengths of Symmetric key and Private key received on mail
    leng = int(input("Enter the length of key received on mail: "))
    lenp = int(input("Enter the length of private key received on mail: "))

    # Provide the length parameters to retrieve the encrypted symmetric key and private key
    k, pkp = img_decode(leng, lenp)

    # Convert private key from string back to key object
    privkey = rsa.PrivateKey.load_pkcs1(pkp.encode('utf8'))
    
    # Decode the encrypted symmetric key from base64
    enc_symmetricKey = b64decode(k)

    # Provide the name of the encoded/encrypted file and read its content
    enc_file = input("Enter the name of encoded file (with extension): ")
    with open (enc_file, 'rb') as file:
                d = file.read()

    # Decode the read data from base64
    enc_data = b64decode(d)

    # Decrypt the symmetric key with private key
    symmetricKey = rsa.decrypt(enc_symmetricKey, privkey)

    # Decrypt the data
    f = Fernet(symmetricKey)
    data = f.decrypt(enc_data)

    # Provide a new file name and write the decrypted content to it
    dec_file = input("Provide new name for decoded file (with extension): ")
    with open(dec_file, 'wb') as file:
        file.write(data)