# Time Capsule Cloud Decryptor

## Overview
The provided code is a FastAPI-based cloud decryptor for time capsules. It receives encrypted time capsule data, verifies the integrity of the time capsule, and decrypts the message if the specified reveal time has passed.

## Algorithm
The cloud decryptor follows these steps to decrypt the time capsule:

1. Receive the encrypted time capsule data as a base64-encoded string.
2. Decode the base64 string and parse the data into a dictionary.
3. Extract the relevant information from the dictionary, including the encrypted message, creation time, reveal time, locked by user, encryption method, and user key.
4. Calculate the difference between the reveal time and creation time in seconds.
5. Verify that the time difference matches one of the allowed intervals (10 days, 100 days, or 1000 days). If not, return a warning message indicating that the time capsule has been tampered with.
6. Check if the current time is greater than or equal to the reveal time. If yes, proceed with decryption; otherwise, return the encrypted message along with other time capsule details.
7. If the encryption method is "vigenere", combine the user key with the secret key (stored in the environment variable `MASTER_KEY`) and use the Vigenère cipher to decrypt the message.
8. Return the decrypted message along with other time capsule details.

## Key Combination
The cloud decryptor combines the user key provided by the user and the secret key stored on the server to enhance security. The `combine_keys` function interleaves the characters of the user key and the secret key to create a combined key. This combined key is then used for encryption and decryption.

## Vigenère Cipher
The Vigenère cipher is used for encrypting and decrypting the time capsule messages. The `vigenere_encrypt` function takes the message and the combined key as input and performs the following steps:

1. Initialize an empty string to store the encrypted message.
2. Iterate over each character in the message.
3. If the character is alphabetic, determine the ASCII offset (65 for uppercase, 97 for lowercase).
4. Calculate the shift based on the corresponding character in the key (A=0, B=1, ..., Z=25).
5. Apply the shift to the character's ASCII value and wrap around the alphabet if necessary.
6. Append the encrypted character to the encrypted message.
7. If the character is non-alphabetic, append it to the encrypted message as is.
8. Return the encrypted message.

The `vigenere_decrypt` function follows a similar process but subtracts the shift instead of adding it to decrypt the message.

## Usage
To use the cloud decryptor, send a POST request to the `/submit-capsule` endpoint with the encrypted time capsule data as the request body. The data should be in the following format:

```
{
    "data": "base64_encoded_time_capsule_data"
}
```

The decryptor will process the time capsule and return the decrypted message along with other time capsule details if the reveal time has passed. If the reveal time has not passed, it will return the encrypted message.

Note: The secret key (`MASTER_KEY`) should be stored securely in the environment variables of the server running the cloud decryptor.