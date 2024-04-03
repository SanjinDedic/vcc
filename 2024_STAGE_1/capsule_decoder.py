from fastapi import FastAPI, HTTPException, Request, status,APIRouter
from dotenv import load_dotenv
from pydantic import BaseModel
import base64
import time
import json
import os
from os.path import join, dirname
from dotenv import load_dotenv
import datetime

router = APIRouter()

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SECRET_KEY = os.environ.get("MASTER_KEY")

class TimeCapsuleRequest(BaseModel):
    data: str

class Encryption(BaseModel):
    message: str
    key: str

def combine_keys(user_key, my_key):
    combined_key = ""
    # Iterate over the length of the longer key
    for i in range(max(len(user_key), len(my_key))):
        if i < len(user_key):
            combined_key += user_key[i]  # Add character from user key
        if i < len(my_key):
            combined_key += my_key[i]    # Add character from your key
    return combined_key

def vigenere_decrypt(message, key):
    decrypted_message = ""
    key_length = len(key)
    key_index = 0
    for char in message:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            shift = ord(key[key_index % key_length].upper()) - 65
            decrypted_char = chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
            decrypted_message += decrypted_char
            key_index += 1
        else:
            decrypted_message += char
    return decrypted_message


def caesar_encrypt(message, user_key):
    key = combine_keys(user_key,SECRET_KEY)
    numeric_key = sum(ord(char) for char in key)
    encrypted_message = ""
    for char in message:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            encrypted_char = chr((ord(char) - ascii_offset + numeric_key) % 26 + ascii_offset)
            encrypted_message += encrypted_char
        else:
            encrypted_message += char
    return encrypted_message

def vigenere_encrypt(message, user_key):
    key = combine_keys(user_key,SECRET_KEY)
    encrypted_message = ""
    key_length = len(key)
    key_index = 0
    for char in message:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            shift = ord(key[key_index % key_length].upper()) - 65
            encrypted_char = chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            encrypted_message += encrypted_char
            key_index += 1
        else:
            encrypted_message += char
    return encrypted_message

@router.post("/submit-capsule")
async def process_time_capsule(request: TimeCapsuleRequest):
    try:
        decoded_data = base64.b64decode(request.data+"==").decode('utf-8')
        data_dict = dict(item.split(': ') for item in decoded_data.split(', '))

        message = data_dict['message']
        time_created = int(data_dict['time_created'])
        time_revealed = int(data_dict['time_revealed'])
        locked_by = data_dict['locked_by']
        encryption_method = data_dict['encryption_method']
        user_key = data_dict['user_key']
        dt_time_created = datetime.datetime.fromtimestamp(time_created)
        dt_time_revealed = datetime.datetime.fromtimestamp(time_revealed)

        difference_in_seconds = (dt_time_revealed - dt_time_created).total_seconds()

        allowed_intervals = [10 * 86400, 100 * 86400, 1000 * 86400]  # Convert days to seconds

        if difference_in_seconds not in allowed_intervals:
            return {
                "message": "WARNING! Time Capsule has been tampered",
                "time_created": time_created,
                "time_revealed": time_revealed,
                "locked_by": locked_by,
                "encryption_method": encryption_method,
                "user_key": user_key
            }
        else:
            current_time = int(time.time())

            if current_time >= time_revealed:
                if encryption_method == 'vigenere':
                   key=combine_keys(user_key,SECRET_KEY)
                   decrypted_message = vigenere_decrypt(message, key)
                   return {
                       "message": decrypted_message,
                       "time_created": time_created,
                       "time_revealed": time_revealed,
                       "locked_by": locked_by,
                       "encryption_method": encryption_method,
                       "user_key": user_key
                   }
                else:
                   raise HTTPException(status_code=400, detail="Unsupported encryption method")
            else:
               time_created_str = time.strftime('%d/%m/%Y %I:%M:%S %p', time.localtime(time_created))
               time_revealed_str = time.strftime('%d/%m/%Y %I:%M:%S %p', time.localtime(time_revealed))

               return {
                    "message": message,
                    "time_created": time_created_str,
                    "time_revealed": time_revealed_str,
                    "locked_by": locked_by,
                    "encryption_method": encryption_method,
                    "user_key": user_key
               }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/caesar_encrypt")
async def process_caesar_encription(request: Encryption):
    try:
        encrypted_message = caesar_encrypt(request.message,request.key)
        return { "encrypted_message" : encrypted_message }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/vigenere_encrypt")
async def process_vigenere_encription(request: Encryption):
    try:
        encrypted_message = vigenere_encrypt(request.message,request.key)
        return { "encrypted_message" : encrypted_message }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))