from mathss import Mean,Median

def processFile():

    lyst=[]
    bananas=[]
    straberry=[]
    all_lyst=[]

    for line in data[1:]:  
        data2 = line.strip().split()
        all_lyst.append(int(data2[2]))
        if data2[1]=='apple':
            lyst.append(int(data2[2])) 
        elif data2[1]=='banana':
            bananas.append(int(data2[2])) 
        if data2[1]=='strawberry':
            straberry.append(int(data2[2])) 

    vm= Mean(lyst)
    Mn= Median(lyst)
    ban1=Mean(bananas)
    ban2=Median(bananas)
    stra=Mean(straberry)
    stra2=Median(straberry)
    print("Check output.txt for result\n")
    print(f"Numbers of attempts is {attempt}")
    file_name= "output.txt"
    with open(file_name,'w') as file:

        file.write(f'The mean of apples eaten {vm}\n')
        file.write(f'The median of apples eaten {Mn}\n')
        file.write(f'The mean of bananas eaten {ban1}\n')
        file.write(f'The median of bananas eaten {ban2}\n')
        file.write(f'The mean of strabery eaten {stra}\n')
        file.write(f'The median of straberry eaten {stra2}\n')


done=False
attempt=1
while not done:
    try:
        file= input("Enter the file name")
        my_files= open(file,'r')
        data= my_files.readlines()
        processFile()
        attempt+=1
        done = True

    except FileNotFoundError as x:
        print(f"{x} You want to try again")
        again= input("Try another file (y/N)")
        if again=='y':
                done=False
        if again == 'N':
            done=True
        attempt+=1


