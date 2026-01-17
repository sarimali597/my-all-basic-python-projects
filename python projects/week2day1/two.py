import random

number = random.randint(1, 100)
print("I have decided a number can you guest it: ")
print(number)
attempts = 3

while attempts > 0:
    guest = int(input("Enter the number you have guest: "))
    if guest < number:
        print(f"your guest number ({guest}) is too low.")
    elif guest > number:
        print(f"your guest number ({guest}) is too high.")
    elif guest == number:
        print(
            f"congradulations you have guest right number. The guested number is {number}"
        )
        break
    else:
        print(f"wrong! hou have {attempts-1} remaining.")
        attempts -= 1
else:
    print(f"sorry you are failed the correct number was {number}")
