age = int(input("Enter your age to claim discount: "))
if age <= 11:
    print("congradulations you have achieved 50%")
elif age >= 12 and age <= 18:
    print("congradulations you have achieved 25%")
elif age >= 60:
    print("congradulations you have achieved 30%")
else:
    print("dear user you are not eligible for discount")
