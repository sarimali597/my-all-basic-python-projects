shopping_list=[]
while True:
    print("choose options")
    print("1. Add Item")
    print("2. Remove Item")
    print("3. View Shopping List")
    print("4. Exit")
    choice=input("Choose an option to perform")
    if choice == "1":
        item = input("Enter the item to add: ")
        shopping_list.append(item)
        print(f"{item} added to the list.")
    elif choice == "2":
        item = input("Enter the item to remove: ")
        if item in shopping_list:
            shopping_list.remove(item)
            print(f"{item} removed from the list.")
        else:
            print("Item not found in the list.")
    elif choice == "3":
        print("Shopping List:", shopping_list)
    elif choice == "4":
        break
    else:
        print("Invalid choice")