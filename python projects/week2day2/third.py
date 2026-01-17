age = int(input("Enter your age to claim discount: "))
price=float(input("Dear customer please enter the amount of total bill on which you want to claim discount: "))
if age>0<110 and price>1:
    if age <= 11:
        print("congradulations you have achieved 50%")
        print(price-(price*0.5))
    elif age >= 12 and age <= 18:
        print("congradulations you have achieved 25%")
        print(price-(price*0.25))
    elif age >= 60:
        print("congradulations you have achieved 30%")
        print(price-(price*0.30))
    else:
        print("dear user you are not eligible for discount")
else:
    print("enter valid inputs")
