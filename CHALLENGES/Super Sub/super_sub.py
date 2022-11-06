def perform_substitution(message):
    sub = {
    'a':'0', 'b':'1', 'c':'2',
    'd':'3', 'e':'&', 'f':'5',
    'g':'6', 'h':'7', 'i':'8',
    'j':'9', 'k':'k', 'l':'l',
    'm':'m', 'n':'a', 'o':'o',
    'p':'c', 'q':'$', 'r':'e',
    's':'#', 't':'@', 'u':'h',
    'v':'i', 'w':'w', 'x':'x',
    'y':'!', 'z':'m', ' ':'+', 
    '}':'.', '{':',', '_':']'}
    encrypted = ''
    for letter in message:
        if letter in sub:
            encrypted += sub[letter]
        else:
            encrypted += letter
    return encrypted
    

plaintext = input("Enter Plaintext: ")

ciphertext = perform_substitution(plaintext)

print(ciphertext)