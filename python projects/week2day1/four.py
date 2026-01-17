start = int(input("Enter the starting number: "))
skip_multiples_of_three = input("Skip numbers divisible by 3? (y/n): ")
while start >= 0:
    if skip_multiples_of_three == "y" and start % 3 == 0:
        start -=1
        continue
    print(start)

    if input("press 'q' to quite or enter to continue: ") == 'q':
        break
        start -= 1

print("countdown ended!")
