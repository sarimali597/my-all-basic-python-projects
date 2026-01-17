class Mobile: 
    count=0
    def __init__(self):
        file=open('example.txt','a')
        file.write('\nobject has been created successfully')
        print("object has been created successfully")
        print(Mobile.count)
        Mobile.count+=1
m=Mobile()
k=Mobile()
n=Mobile()
