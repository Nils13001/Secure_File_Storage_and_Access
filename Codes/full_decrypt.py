from PIL import Image

import rsa
from cryptography.fernet import Fernet
from base64 import b64decode

def img_decode(len1, lp):
    
    img = input("Enter image name(with extension) : ")
    image = Image.open(img, 'r')
    data = ''
    imgdata = iter(image.getdata())
    ct = 0
    ls = []
    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
								imgdata.__next__()[:3] +
								imgdata.__next__()[:3]]
        ct+=1
        #Strings of binary data
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
    
    priv = ''
    ct = 0
    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
								imgdata.__next__()[:3] +
								imgdata.__next__()[:3]]
        ct+=1
        #Strings of binary data
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
    
    return ls[0], ls[1]

def dec_main():
    leng = int(input("Enter the length of key received on mail: "))
    lenp = int(input("Enter the length of private key received on mail: "))
    k, pkp = img_decode(leng, lenp)
    privkey = rsa.PrivateKey.load_pkcs1(pkp.encode('utf8'))
    # Here we send payload over the network
    # And receive it somewhere at the client side

    # Decode the symmetric key from base64
    enc_symmetricKey = b64decode(k)

    enc_file = input("Enter name of encoded file: ")
    with open (enc_file, 'rb') as file:
                d = file.read()

    # Decode the data from base64
    enc_data = b64decode(d)

    # Decrypt the symmetric key
    symmetricKey = rsa.decrypt(enc_symmetricKey, privkey)

    # Decrypt the data
    f = Fernet(symmetricKey)
    data = f.decrypt(enc_data)

    dec_file = input("Enter name for decoded file: ")
    with open(dec_file, 'wb') as file:
        file.write(data)
    print("Decryption Successful!!!")