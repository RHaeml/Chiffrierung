#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 20:49:22 2023

@author: ramon
"""
import qrcode
import base64
import secrets


def decode_xor(byte_a: bytes, byte_b: bytes):
    #Wird zu bytearray Konvertiert:
    bytearray_a = bytearray(byte_a)
    bytearray_b = bytearray(byte_b)
    
    bytearray_c = bytearray()

    for a,b in zip(bytearray_a, bytearray_b):
        bytearray_c.append(a^b)
    byte_c = bytes(bytearray_c)
    return byte_c


def generate_password(len_of_passkey: int):
    password = secrets.token_bytes(len_of_passkey)
    return password


def generate_qrcode(data:str, output_path:str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
       
    # Bild speichern
    img.save(output_path)


def to_base64(data: str): 
    if type(data) == str:
       data = data.encode('utf-8')
    return base64.urlsafe_b64encode(data).decode('utf-8')


def base64_to_str(base64_as_str:str):
    return base64.urlsafe_b64decode(base64_as_str).decode('utf-8')


def str_to_byte(string :str):
    return string.encode('utf-8')


def encode_data(unencripted_data:str, byte_password:bytes):
    byte_unencripted_data = str_to_byte(unencripted_data)
    byte_encrypted_data = decode_xor(byte_password, byte_unencripted_data)
    
    #Translate to Base64 URL-Save
    b64_encrypted_data = to_base64(byte_encrypted_data)
    b64_password = to_base64(byte_password)
    return b64_encrypted_data, b64_password 
   

def decode_data(en1: str, pa1:str):
    r_encrypted_data = base64_to_str(en1)
    r_password = base64_to_str(pa1)
    
    r_byte_encrypted_data = str_to_byte(r_encrypted_data)
    r_byte_password = str_to_byte(r_password)
    
    r_byte_unencrypted_data = decode_xor(r_byte_encrypted_data, r_byte_password)
    r_unencrypted_data = r_byte_unencrypted_data.decode('utf-8')
    
    print(r_unencrypted_data)


#%% Beispiel verschlüsseln
a = 'Das ist ein sehr geheimer Test'
b = 'Passwort in utf-8 ohne umlaute'
byte_b = b.encode('utf-8')
b64_encrypted_data, b64_password = encode_data(a,byte_b)

#%% Encodieren einer txt-Datei mit drei verschiedenen Schlüsseln
split = 3
name_unencryption_data = 'Key'

with open(name_unencryption_data, 'r') as raw_file:
    unencryption_data = raw_file.read()

for i in range(split):
    password = generate_password(len(unencryption_data))
    b64_encrypted_data, b64_password = encode_data(unencryption_data, password)

    generate_qrcode(b64_encrypted_data, f'Encrypted_{i}.png')
    generate_qrcode(b64_password, f'Password_{i}.png')
    with open('Encrypted.txt', 'a') as f:
        f.write(b64_encrypted_data +'\n')
    with open('Password.txt', 'a') as f:
        f.write(b64_password +'\n')

#%% Beispiel Entschlüsseln
pa1 = 'U2xoT0tiZnpnZ09LdUVnYkJobnpzSGhmblpXQlBxQWdYeHB0T1RtZGtsd2Zpa0trcEtSenNwTGxGV2JnaVN2eVRBVmZ6RnlLUHZCanlLZWJodmxBQmROaWtrbXdqTHhlRFVEZXBYUGlwVUxtTlRRd1ZCQmNrR1BYTGt3bFl2Z056ZFJrWlRsQmt1Z0dXZ2FpQUxiWW9taHhLeWVac0tMelNmc2dmblpBQQ=='
en1 = 'Mg4JIS8NCHAGBSYnHDEeaCMKAh95KQoJGy5dIzIeNwJSGRIHKjoZbgoOBAkbCUEKEjgmCBITOGYnNRESGzd8GDY0JQNwJxooNQUxYBgoBgsMEwI1SAUtCgQeAwNgLRsGMSYhbxE7OAAVIylnLzc4E1wjIQweNCQxL2EWDygDDjwfbjMIKDsfMWEUBDNdBgIdKCMMUw4OHBc5cwQ5BzkpCSBsEgQSGzstSw=='
decode_data(en1, pa1)
