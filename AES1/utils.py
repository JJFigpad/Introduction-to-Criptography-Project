from re import A
from Crypto.Cipher import AES
from PIL import Image
import requests
from PIL import ImageOps
import codecs
from secrets import token_bytes
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image, ImageOps
from Crypto.Cipher import AES


def generate_aes_key_and_iv():
    # Genera una clave de 16 bytes (128 bits)
    key = token_bytes(16)
    # Convierte la clave de bytes a una cadena hexadecimal
    key_hex = key.hex().upper()

    # Genera un IV de 8 bytes (64 bits)
    iv = token_bytes(8)
    # Convierte el IV de bytes a una cadena hexadecimal
    iv_hex = iv.hex().upper()

    return key_hex, iv_hex

def DecimalToHex(l):
	result = ""
	for i in l:
		if len(hex(i).split('x')[-1]) != 1:
			result += hex(i).split('x')[-1]
		else:
			result += '0' + hex(i).split('x')[-1]
	return result.upper()

def HexToDecimal(s):
	result = []
	while len(s) != 32:
		s = '0' + s
	for i in range(0, 32, 8):
		pixel = []
		for j in range(i, i+8, 2):
			pixel.append(int(s[j]+s[j+1], base=16))
		result.append(tuple(pixel))
	return result

def encode_aes_img_ECB(key, image):
	cipher = AES.new(key.encode("utf8"), AES.MODE_ECB)
	img = Image.open(image.image_file)
	encryptedImg = img.convert("RGBA")

	if encryptedImg.width % 4 != 0:
		diff = 4 - (encryptedImg.width % 4)
		encryptedImg = ImageOps.expand(encryptedImg, border=(0,0, diff, 0), fill = 0)
	for y in range(0, encryptedImg.height):
		rowPixels = []
		for x in range(0, encryptedImg.width):
			if x % 4 == 0 and x > 0:
				# Transform the 4 pixels using AES cipher
				#print(hex(int.from_bytes(bytes(rowPixels), "big")))
				newRowPixels = cipher.encrypt(bytes(rowPixels))
				#print(hex(int.from_bytes(newRowPixels, "big")))
				newRowPixels = HexToDecimal(hex(int.from_bytes(newRowPixels, "big"))[2:])
				for i in range(x - 4, x):
					encryptedImg.putpixel((i,y), newRowPixels[i - (x-4)])
				rowPixels = []
			rowPixels += encryptedImg.getpixel((x,y))
			
	# Guarda la imagen en memoria
	output = BytesIO()
	encryptedImg.save(output, format='PNG')
	output.seek(0)
	# Actualiza la imagen en el modelo Image
	image.encrypted_image = InMemoryUploadedFile(output, 'ImageField', f"Encrypted_ECB.png", 'image/png', output.tell(), None)
	image.save()
	print(f"Ruta antes de la encriptación: {image.encrypted_image.path}")
	#return image.image_file.path

	#encryptedImg.show()
	#encryptedImg.save("criptosite/static/img/Encrypted_ECB.png")
	
	
def decode_aes_img_ECB(key,image):
	cipher = AES.new(key.encode("utf8"), AES.MODE_ECB)
	img = Image.open(image.image_file)
	decryptedImg = img

	for y in range(0, decryptedImg.height):
		rowPixels = []
		for x in range(0, decryptedImg.width):
			if x % 4 == 0 and x > 0:
				# Transform the 4 pixels using AES cipher
				#print(hex(int.from_bytes(bytes(rowPixels), "big")))
				newRowPixels = cipher.decrypt(bytes(rowPixels))
				#print(hex(int.from_bytes(newRowPixels, "big")))
				newRowPixels = HexToDecimal(hex(int.from_bytes(newRowPixels, "big"))[2:])
				for i in range(x - 4, x):
					decryptedImg.putpixel((i,y), newRowPixels[i - (x-4)])
				rowPixels = []
			
			rowPixels += decryptedImg.getpixel((x,y))
	# Guarda la imagen en memoria
	output = BytesIO()
	decryptedImg.save(output, format='PNG')
	output.seek(0)# Actualiza la imagen en el modelo Image
	image.decrypted_image = InMemoryUploadedFile(output, 'ImageField', f"Decrypted_ECB.png", 'image/png', output.tell(), None)
	image.save()
	#decryptedImg.show()
	#decryptedImg.save("criptosite/static/img/Decrypted_ECB.png")

    	
def encode_aes_img_CBC(key, iv,image):
    # Asegúrate de que el IV tenga la longitud correcta
    iv_bytes = bytes.fromhex(iv)
    iv_bytes = iv_bytes.ljust(16, b'\0')

    cipher = AES.new(key.encode("utf8"), AES.MODE_CBC, iv_bytes)
    img = Image.open(image.image_file)
    encryptedImg = img.convert("RGBA")

    if encryptedImg.width % 4 != 0:
        diff = 4 - (encryptedImg.width % 4)
        encryptedImg = ImageOps.expand(encryptedImg, border=(0, 0, diff, 0), fill=0)
    
    for y in range(0, encryptedImg.height):
        rowPixels = []
        for x in range(0, encryptedImg.width):
            if x % 4 == 0 and x > 0:
                # Transforma los 4 píxeles usando el cifrado AES
                newRowPixels = cipher.encrypt(bytes(rowPixels))
                newRowPixels = HexToDecimal(hex(int.from_bytes(newRowPixels, "big"))[2:])
                for i in range(x - 4, x):
                    encryptedImg.putpixel((i, y), newRowPixels[i - (x-4)])
                rowPixels = []

            rowPixels += encryptedImg.getpixel((x, y))

    #encryptedImg.show()
    #encryptedImg.save("criptosite/static/img/Encrypted_CBC.png")
	
    	# Guarda la imagen en memoria
    output = BytesIO()
    encryptedImg.save(output, format='PNG')
    output.seek(0)
	# Actualiza la imagen en el modelo Image
    image.encrypted_image = InMemoryUploadedFile(output, 'ImageField', f"Encrypted_CBC.png", 'image/png', output.tell(), None)
    image.save()
    print(f"Ruta antes de la encriptación: {image.encrypted_image.path}")

    return iv_bytes.hex()

def decode_aes_img_CBC(key, iv,image):
    # Asegúrate de que el IV tenga la longitud correcta
    iv_bytes = bytes.fromhex(iv)
    iv_bytes = iv_bytes.ljust(16, b'\0')

    cipher = AES.new(key.encode("utf8"), AES.MODE_CBC, iv_bytes)
    img = Image.open("criptosite/static/img/Encrypted_CBC.png")
    decryptedImg = img

    for y in range(0, decryptedImg.height):
        rowPixels = []
        for x in range(0, decryptedImg.width):
            if x % 4 == 0 and x > 0:
                # Transforma los 4 píxeles usando el cifrado AES
                newRowPixels = cipher.decrypt(bytes(rowPixels))
                newRowPixels = HexToDecimal(hex(int.from_bytes(newRowPixels, "big"))[2:])
                for i in range(x - 4, x):
                    decryptedImg.putpixel((i, y), newRowPixels[i - (x-4)])
                rowPixels = []

            rowPixels += decryptedImg.getpixel((x, y))

    #decryptedImg.show()
    #decryptedImg.save("criptosite/static/img/Decrypted_CBC.png")
		# Guarda la imagen en memoria
    output = BytesIO()
    decryptedImg.save(output, format='PNG')
    output.seek(0)# Actualiza la imagen en el modelo Image
    image.decrypted_image = InMemoryUploadedFile(output, 'ImageField', f"Decrypted_CBC.png", 'image/png', output.tell(), None)
    image.save()
	
#OFB
def encode_aes_img_OFB(key,iv,image):
	cipher = AES.new(key.encode("utf8"), AES.MODE_OFB, iv.encode("utf8"))
	img = Image.open(image.image_file)
	encryptedImg = img.convert("RGBA")

	if encryptedImg.width % 4 != 0:
		diff = 4 - (encryptedImg.width % 4)
		encryptedImg = ImageOps.expand(encryptedImg, border=(0,0, diff, 0), fill = 0)
	for y in range(0, encryptedImg.height):
		rowPixels = []
		for x in range(0, encryptedImg.width):
			if x % 4 == 0 and x > 0:
				# Transform the 4 pixels using AES cipher
				#print(hex(int.from_bytes(bytes(rowPixels), "big")))
				newRowPixels = cipher.encrypt(bytes(rowPixels))
				#print(hex(int.from_bytes(newRowPixels, "big")))
				newRowPixels = HexToDecimal(hex(int.from_bytes(newRowPixels, "big"))[2:])
				for i in range(x - 4, x):
					encryptedImg.putpixel((i,y), newRowPixels[i - (x-4)])
				rowPixels = []
			rowPixels += encryptedImg.getpixel((x,y))
	
	#encryptedImg.show()
	#encryptedImg.save("criptosite/static/img/Encrypted_OFB.png")
	# Guarda la imagen en memoria
	output = BytesIO()
	encryptedImg.save(output, format='PNG')
	output.seek(0)
	# Actualiza la imagen en el modelo Image
	image.encrypted_image = InMemoryUploadedFile(output, 'ImageField', f"Encrypted_OFB.png", 'image/png', output.tell(), None)
	image.save()
	print(f"Ruta antes de la encriptación: {image.encrypted_image.path}")

	return (cipher.iv).hex()

def decode_aes_img_OFB(key,iv,image):
	cipher = AES.new(key.encode("utf8"), AES.MODE_OFB, iv.encode("utf8"))
	img = Image.open("criptosite/static/img/Encrypted_OFB.png")
	decryptedImg = img

	for y in range(0, decryptedImg.height):
		rowPixels = []
		for x in range(0, decryptedImg.width):
			if x % 4 == 0 and x > 0:
				# Transform the 4 pixels using AES cipher
				#print(hex(int.from_bytes(bytes(rowPixels), "big")))
				newRowPixels = cipher.decrypt(bytes(rowPixels))
				#print(hex(int.from_bytes(newRowPixels, "big")))
				newRowPixels = HexToDecimal(hex(int.from_bytes(newRowPixels, "big"))[2:])
				for i in range(x - 4, x):
					decryptedImg.putpixel((i,y), newRowPixels[i - (x-4)])
				rowPixels = []
			
			rowPixels += decryptedImg.getpixel((x,y))
	
	#decryptedImg.show()
	#decryptedImg.save("criptosite/static/img/Decrypted_OFB.png")
	output = BytesIO()
	decryptedImg.save(output, format='PNG')
	output.seek(0)# Actualiza la imagen en el modelo Image
	image.decrypted_image = InMemoryUploadedFile(output, 'ImageField', f"Decrypted_OFB.png", 'image/png', output.tell(), None)
	image.save()



    #CFB
def encode_aes_img_CFB(key,iv,image):
	cipher = AES.new(key.encode("utf8"), AES.MODE_CFB, iv.encode("utf8"), segment_size=128)
	img = Image.open(image.image_file)
	encryptedImg = img.convert("RGBA")

	if encryptedImg.width % 4 != 0:
		diff = 4 - (encryptedImg.width % 4)
		encryptedImg = ImageOps.expand(encryptedImg, border=(0,0, diff, 0), fill = 0)
	for y in range(0, encryptedImg.height):
		rowPixels = []
		for x in range(0, encryptedImg.width):
			if x % 4 == 0 and x > 0:
				# Transform the 4 pixels using AES cipher
				#print(hex(int.from_bytes(bytes(rowPixels), "big")))
				newRowPixels = cipher.encrypt(bytes(rowPixels))
				#print(hex(int.from_bytes(newRowPixels, "big")))
				newRowPixels = HexToDecimal(hex(int.from_bytes(newRowPixels, "big"))[2:])
				for i in range(x - 4, x):
					encryptedImg.putpixel((i,y), newRowPixels[i - (x-4)])
				rowPixels = []
			rowPixels += encryptedImg.getpixel((x,y))
	#encryptedImg.show()
	#encryptedImg.save("criptosite/static/img/Encrypted_CFB.png")
	output = BytesIO()
	encryptedImg.save(output, format='PNG')
	output.seek(0)
	# Actualiza la imagen en el modelo Image
	image.encrypted_image = InMemoryUploadedFile(output, 'ImageField', f"Encrypted_CFB.png", 'image/png', output.tell(), None)
	image.save()
	print(f"Ruta antes de la encriptación: {image.encrypted_image.path}")

	return (cipher.iv).hex()

def decode_aes_img_CFB(key,iv,image):
	cipher = AES.new(key.encode("utf8"), AES.MODE_CFB, iv.encode("utf8"), segment_size=128)
	img = Image.open(image.image_file)
	decryptedImg = img

	for y in range(0, decryptedImg.height):
		rowPixels = []
		for x in range(0, decryptedImg.width):
			if x % 4 == 0 and x > 0:
				# Transform the 4 pixels using AES cipher
				#print(hex(int.from_bytes(bytes(rowPixels), "big")))
				newRowPixels = cipher.decrypt(bytes(rowPixels))
				#print(hex(int.from_bytes(newRowPixels, "big")))
				newRowPixels = HexToDecimal(hex(int.from_bytes(newRowPixels, "big"))[2:])
				for i in range(x - 4, x):
					decryptedImg.putpixel((i,y), newRowPixels[i - (x-4)])
				rowPixels = []
			
			rowPixels += decryptedImg.getpixel((x,y))
	
	output = BytesIO()
	decryptedImg.save(output, format='PNG')
	output.seek(0)# Actualiza la imagen en el modelo Image
	image.decrypted_image = InMemoryUploadedFile(output, 'ImageField', f"Decrypted_CFB.png", 'image/png', output.tell(), None)
	image.save()

#CTR
def encode_aes_img_CTR(key,iv,image):
    iv2 = b"00000000"
    cipher = AES.new(key.encode("utf8"),AES.MODE_CTR,nonce=iv2[:len(iv)//2])
    img = Image.open(image.image_file)
    encryptedImg = img.convert("RGBA")   

	# Resize image as needed, the image width must be a multiple
	# of 4
    if encryptedImg.width % 4 != 0:
        diff=4-(encryptedImg.width %4)
        encryptedImg = ImageOps.expand(encryptedImg, border=(0,0, diff, 0), fill = 0)
    for y in range(0, encryptedImg.height):
        rowPixels = []
        for x in range(0, encryptedImg.width):
            if x % 4 == 0 and x > 0:
                newRowPixels = cipher.encrypt(bytes(rowPixels))
                newRowPixels = HexToDecimal(hex(int.from_bytes(newRowPixels, "big"))[2:])
                for i in range(x - 4, x):
                    encryptedImg.putpixel((i,y), newRowPixels[i - (x-4)])
                rowPixels = []
            rowPixels += encryptedImg.getpixel((x,y))
	
    output = BytesIO()
    encryptedImg.save(output, format='PNG')
    output.seek(0)
	# Actualiza la imagen en el modelo Image
    image.encrypted_image = InMemoryUploadedFile(output, 'ImageField', f"Encrypted_CTR.png", 'image/png', output.tell(), None)
    image.save()
    print(f"Ruta antes de la encriptación: {image.encrypted_image.path}")
	

def decode_aes_img_CTR(key,iv,image):
    iv2 = b"00000000"
    cipher = AES.new(key.encode("utf8"),AES.MODE_CTR,nonce=iv2[:len(iv)//2])
    img = Image.open(image.image_file)
    decryptedImg = img

	# Iterate over each row of the image height taking at each step
	# 4 pixels to transform them into a new 4 pixels
    for y in range(0, decryptedImg.height):
        rowPixels = []
        for x in range(0, decryptedImg.width):
            if x % 4 == 0 and x > 0:
                newRowPixels = cipher.encrypt(bytes(rowPixels))
                newRowPixels = HexToDecimal(hex(int.from_bytes(newRowPixels, "big"))[2:])
                for i in range(x - 4, x):
                    decryptedImg.putpixel((i,y), newRowPixels[i - (x-4)])
                rowPixels = []
            rowPixels += decryptedImg.getpixel((x,y))
    output = BytesIO()
    decryptedImg.save(output, format='PNG')
    output.seek(0)# Actualiza la imagen en el modelo Image
    image.decrypted_image = InMemoryUploadedFile(output, 'ImageField', f"Decrypted_CTR.png", 'image/png', output.tell(), None)
    image.save()