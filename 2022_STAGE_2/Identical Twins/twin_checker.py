book1 = open('WizardOfOz1.txt').read()
book2 = open('WizardOfOz2.txt').read()

print(len(book1))
print(len(book2))

flag =''

for i in range(0,len(book1)):
    if book1[i] != book2[i]:
        flag += book2[i]
print(flag)