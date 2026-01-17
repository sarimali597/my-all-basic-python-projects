correct_pin = 92004
balance = 10000
attempts = 3  # total tries allowed

# Step 1: Ask for PIN, allow only 3 tries
while attempts > 0:
    try:
        pin = int(input("Enter your PIN to access account: "))
    except ValueError:
        print("Invalid input. Only numbers allowed.")
        continue

    if pin == correct_pin:
        print("Correct PIN.")
        break  # PIN accepted, move forward
    else:
        attempts -= 1  # decrease remaining tries
        print("Incorrect PIN. Tries left:", attempts)

        if attempts == 0:
            print("Too many wrong attempts. Account locked.")
            exit()  # stop the program completely

# Step 2: Ask if user wants to access account
while True:
    menu_choice = (
        input("Do you want to access your account? (yes/no): ").strip().lower()
    )

    if menu_choice == "yes":
        print("Access granted.")
        break
    elif menu_choice == "no":
        print("Goodbye.")
        exit()
    else:
        print("Please answer yes or no.")

# Step 3: Account menu
while True:
    print("\n--- Main Menu ---")
    print("1. Check Balance")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Exit")

    choice = input("Choose an option (1-4): ")

    if choice == "1":
        print("Your current balance is:", balance)

    elif choice == "2":
        try:
            deposit = float(input("Enter amount to deposit: "))
            if deposit > 0:
                balance += deposit
                print("Deposited successfully. New balance:", balance)
            else:
                print("Enter a positive amount.")
        except ValueError:
            print("Invalid amount.")

    elif choice == "3":
        try:
            withdraw = float(input("Enter amount to withdraw: "))
            if withdraw > balance:
                print("Insufficient balance.")
            elif withdraw > 0:
                balance -= withdraw
                print("Withdrawal successful. New balance:", balance)
            else:
                print("Enter a positive amount.")
        except ValueError:
            print("Invalid amount.")

    elif choice == "4":
        print("Thank you for using the ATM.")
        break

    else:
        print("Invalid option. Choose between 1 and 4.")
