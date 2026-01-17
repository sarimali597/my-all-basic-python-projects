correct_pin=92004
balance=25500
attempts=3
while attempts>0:
    try:
        pin=int(input("Dear user enter the pin to access account: "))
    except:
        print("only the numeric digits are allow.")
        continue
    
