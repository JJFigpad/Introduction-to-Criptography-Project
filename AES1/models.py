# models.py
from django.db import models
from .utils import encode_aes_img_ECB, decode_aes_img_ECB, decode_aes_img_CBC,encode_aes_img_CBC, decode_aes_img_CFB,encode_aes_img_CFB, decode_aes_img_OFB,encode_aes_img_OFB, decode_aes_img_CTR,encode_aes_img_CTR,generate_aes_key_and_iv

class Image(models.Model):
    title = models.CharField(max_length=255)
    image_file = models.ImageField(upload_to='images/original/')
    encrypted_image = models.ImageField(upload_to='images/encrypted/')
    decrypted_image = models.ImageField(upload_to='images/decrypted/')
    is_encrypted = models.BooleanField(default=False)
    encryption_key = models.CharField(max_length=256, blank=True, null=True)
    decryption_key = models.CharField(max_length=256, blank=True, null=True)
    encryption_iv = models.CharField(max_length=256, blank=True, null=True)
    aes_mode = models.CharField(max_length=10, default='ecb')  # Agregamos el campo del modo de operación AES



    def encrypt_image(self, custom_key=None,custom_iv=None):
        #if not self.is_encrypted:
            key = custom_key or generate_aes_key_and_iv()[0]
            iv = custom_iv or generate_aes_key_and_iv()[1]

            original_file = self.image_file.path
            print(f"Original image path: {original_file}")
            original_path = self.image_file.path

            if self.aes_mode == "ecb":
                # Realiza la encriptación
                encode_aes_img_ECB(key, self)
#                print(f"Original image path original: {original_path}")
            elif self.aes_mode == "cbc":
                encode_aes_img_CBC(key,iv,self)
            elif self.aes_mode == "cfb":
                encode_aes_img_CFB(key,iv,self)
            elif self.aes_mode == "ofb":
                encode_aes_img_OFB(key,iv,self)
            elif self.aes_mode == "ctr":
                encode_aes_img_CTR(key,iv,self)
            # Guarda la clave utilizada y marca la imagen como encriptada
            self.encryption_key = key
            self.encryption_iv = iv
            self.is_encrypted = True
            self.save()

    def decrypt_image(self, custom_key,encrypted_image_iv):
            iv = encrypted_image_iv
            original_file = self.image_file.path
            print(f"Original image path: {original_file}")
            original_path = self.image_file.path
            print(self.is_encrypted,"????????????????????????????????")
        #if self.is_encrypted:
            print(f"Decrypting with key: {custom_key}")

            # Decodifica la imagen utilizando la clave proporcionada
            if self.aes_mode == "ecb":
                decode_aes_img_ECB(custom_key, self)
            elif self.aes_mode == "cbc":
                decode_aes_img_CBC(custom_key,iv,self)
            elif self.aes_mode =="cfb":
                 decode_aes_img_CFB(custom_key,iv,self)
            elif self.aes_mode == "ofb":
                decode_aes_img_OFB(custom_key,iv,self)
            elif self.aes_mode == "ctr":
                 decode_aes_img_CTR(custom_key,iv,self)
                 

            # Marca la imagen como desencriptada y guarda la clave
            self.is_encrypted = False
            self.decryption_key =custom_key
            self.encryption_key = custom_key
            self.encryption_iv = iv
            self.save()
