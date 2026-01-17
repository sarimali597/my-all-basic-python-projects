marks = float(input("Dear user enter your total you obtained markes out of 1100: "))
obtained_percentage = (marks / 1100) * 100
if obtained_percentage >= 80:
    print(
        f"congadulations you have obtained A+ grade with {obtained_percentage} % of marks"
    )
elif obtained_percentage >= 70:
    print(
        f"congadulations you have obtained A  grade with {obtained_percentage} % of marks"
    )
elif obtained_percentage >= 60:
    print(
        f"congadulations you have obtained B grade with {obtained_percentage} % of marks"
    )
elif obtained_percentage >= 50:
    print(
        f"congadulations you have obtained C grade with {obtained_percentage} % of marks"
    )
elif obtained_percentage >= 40:
    print(
        f"congadulations you have obtained D grade with {obtained_percentage} % of marks"
    )
else:
    print("Dear studend you have failed in you exam better luck  next time")
