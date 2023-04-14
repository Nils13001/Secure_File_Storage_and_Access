from PIL import Image

#Converting data(key) to bytes
def genData(data):
    # list of binary codes of given data
    newd = []
    
    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd

# Pixels are modified according to the 8-bit binary data and finally returned
def modPix(pix, data):
    
    datalist = genData(data)
    lendata = len(datalist)
    
    imdata = iter(pix)
    for i in range(lendata):
        
        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
								imdata.__next__()[:3] +
								imdata.__next__()[:3]]
        # Pixel value should be made odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j]% 2 != 0):
                pix[j] -= 1
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
            
        # Eighth pixel of every set tells whether to stop ot read further.
		# 0 means keep reading; 1 means the message is over.
        if (i < (lendata-1)):
            if (pix[-1] % 2 != 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
        
        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

#Encoding modified pixel in new image opy
def encode_enc(newimg, data, private):
    
    w = newimg.size[0]
    (x, y) = (0, 0)
    d = newimg.getdata()
    ct = 1
    for pixel in modPix(d, data):
        # Putting modified pixels in the new image
        ct+=1
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

    for pixel in modPix(d, private):
        # Putting modified pixels in the new image
        ct+=1
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

# Main encode program
def encode(key, priv):
    
    img = input("Enter image name(with extension) : ")
    image = Image.open(img, 'r')
    data = key
    privat = priv
    len_key = len(data)
    len_priv = len(privat)
    
    if (len(data) == 0):
        raise ValueError('Data is empty')
    
    newimg = image.copy()
    encode_enc(newimg, data, privat)
    
    new_img_name = input("Enter the name of new image(with extension) : ")
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))
    return len_key, new_img_name, len_priv