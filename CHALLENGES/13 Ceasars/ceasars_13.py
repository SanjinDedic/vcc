import random

def perform_substitution(message):
    sub = {
      'A':'/', 'B':'Z', 'C':'R',
      'D':'S', 'E':'T', 'F':'U',
      'G':'V', 'H':'W', 'I':'X',
      'J':'Y', 'K':'a', 'L':'b',
      'M':'c', 'N':'d', 'O':'e',
      'P':'f', 'Q':'g', 'R':'h',
      'S':'i', 'T':'j', 'U':'k',
      'V':'l', 'W':'m', 'X':'n',
      'Y':'o', 'Z':'p', ' ':'q' }
    
    encrypted = ''
    for letter in message:
        if letter in sub:
            encrypted += sub[letter]
        else:
            encrypted += letter
    return encrypted
    

def shift(message, shift_amount):
    shifted_message = ''
    for letter in message:
        current_num = ord(letter)
        shifted_num = current_num + shift_amount
        shifted_letter = chr(shifted_num)
        shifted_message += shifted_letter
    return shifted_message


message = input('ENTER MESSAGE USE ALL CAPS:')
print(message)

stage1 = perform_substitution(message)
stage2 = shift(stage1, random.randint(-5,5))
print("ENCRYPTED MESSAGE IS BELOW")
print(stage2)