import base64
import time
import os
import requests

caesar_url = 'https://vccfinal.net/time_capsule/caesar_encrypt'
vigenere_url = 'https://vccfinal.net/time_capsule/vigenere_encrypt'

def create_time_capsule():
    print("Time Capsule Builder")
    print("--------------------")

    message = input("Enter your message: ")
    user_key = input("Enter the key: ")
    print("\nLocking Options:")
    print("1. 10 days")
    print("2. 100 days")
    print("3. 1000 days")
    lock_option = input("Choose the locking option (1-3): ")

    if lock_option == "1":
        lock_duration = 10 * 24 * 60 * 60  # 10 days in seconds
    elif lock_option == "2":
        lock_duration = 100 * 24 * 60 * 60  # 100 days in seconds
    elif lock_option == "3":
        lock_duration = 1000 * 24 * 60 * 60  # 1000 days in seconds
    else:
        print("Invalid locking option. Defaulting to 10 days.")
        lock_duration = 10 * 24 * 60 * 60  # 10 days in seconds

    print("\nEncryption Methods:")
    print("1. Caesar Cipher")
    print("2. Vigenère Cipher")
    encryption_option = input("Choose the encryption method (1-2): ")

    if encryption_option == "1":
        data = {
            'message': message,
            'key': user_key
        }
        response = requests.post(caesar_url, json=data)
        if response.status_code == 200:
            encrypted_message = response.json()['encrypted_message']
        else:
            print("An error occurred.")
        encryption_method = "caesar"
    elif encryption_option == "2":
        data = {
            'message': message,
            'key': user_key
        }
        response = requests.post(vigenere_url, json=data)
        if response.status_code == 200:
            encrypted_message = response.json()['encrypted_message']
        else:
            print("An error occurred.")

        encryption_method = "vigenere"
    else:
        print("Invalid encryption option. Defaulting to Caesar Cipher.")
        data = {
            'message': message,
            'key': user_key
        }
        response = requests.post(caesar_url, json=data)
        if response.status_code == 200:
            encrypted_message = response.json()['encrypted_message']
        else:
            print("An error occurred.")
        encryption_method = "caesar"

    time_created = int(time.time())
    time_revealed = time_created + lock_duration
    locked_by = input("Enter your name: ")

    time_capsule_data =(
        f"message: {encrypted_message}, "
        f"time_created: {time_created}, "
        f"time_revealed: {time_revealed}, "
        f"locked_by: {locked_by}, "
        f"encryption_method: {encryption_method}, "
        f"user_key: {user_key}"
    )
    encoded_data = base64.b64encode(time_capsule_data.encode('utf-8')).decode('utf-8')

    print("\nYour digital time capsule:")
    print(encoded_data)

# Run the time capsule builder
create_time_capsule()