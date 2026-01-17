def bank_system():
    balance = 5
    while True:
        print("\nOptions:")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            print(f"Your balance is: ${balance}")
        elif choice == "2":
            amount = float(input("Enter amount to deposit: "))
            balance += amount
            print(f"${amount} deposited. New balance: ${balance}")
        elif choice == "3":
            amount = float(input("Enter amount to withdraw: "))
        if amount > balance:
            print("Insufficient funds!")
        else:
            balance -= amount
            print(f"${amount} withdrawn. New balance:${balance}")
        elif choice == "4":
        break
        else:
            print("Invalid choice")
            bank_system()