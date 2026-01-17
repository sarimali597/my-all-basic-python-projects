while True:
    print("Simple calculator")
    print("Enter (q) to quite")
    num1 = input("Enter first value to calculate: ")
    if num1 == "q":
        break
    operation = input("Enter the opperation you want to perform (+) (*) (/) (-): ")
    num2 = input("enter the second value you want to calculate: ")
    if operation == "+":
        print(f"the calculated value is {float(num1) + float(num2)}")
    elif operation == "-":
        print(f"the calculated value is {float(num1) - float(num2)}")
    elif operation == "*":
        print(f"the calculated value is {float(num1) * float(num2)}")
    elif operation == "/":
        if float(num2) != 0:
            print(f"the calculated value is {float(num1) / float(num2)}")
        else:
            print("enter the number instead 0 to calculate")
    else:
        print("Enter valid operation to perform")
