import os
x,y=1,1
game_over=1
def game():
    global x,y
    for i in range(10):
        
        for j in range(20):
            
            if (i==0 or i==9 or j==0 or j==19):
                print("#", end ="")
            else:
                if (i==x and j==y):
                    print("@", end ="")
                elif (i==2 and j==4):
                    print("+", end ="")
                else:
                    print(" ", end ="")
        print("")

def move(val):
    global x,y,game_over
    os.system('cls')

    if val=="a":
        y-=1
    elif val=="d":
        y+=1
    elif val=="w":
        x-=1
    elif val=="s":
        x+=1
    elif val=="q":
        game_over=0

    if x==2 and y==4:
        print("Congrats you won")
        game_over=0

    if x==2 and y==19:
        print("""VCC{5N4K35_C0NQU3R3D}""")
        game_over=0
        
    if x<0 or x>9 or y<0 or y>19:
        game_over=0
    


def main():
    global game_over
    while(game_over !=0):
        
        game()
        move(str(input()))

if __name__=='__main__':
    main()