import random
value = random.randint(1, 100)
print("welcome to rock paper scissor")
human_answer=input("if 🏔️  enter 1 \n if 📃 enter 2 \n if ✂️  enter 3 \n enter your choice: ")
if human_answer == "1":
    human_answer="🏔️  "
elif human_answer == "2":
    human_answer="📃  "
elif human_answer == "3":
    human_answer="✂️  "
else:
    print("enter valid answer first")
if value in [2, 4, 6, 10, 13, 14, 17, 18, 20, 23, 27, 29, 31, 34, 37, 41, 44, 45, 47, 49, 51, 55, 56, 58, 60, 63, 67, 68, 72, 74, 75, 78, 81, 84]:
    machine_answer="🏔️  "
elif value in [1, 3, 5, 7, 9, 11, 15, 19, 21, 25, 26, 28, 30, 32, 35, 38, 40, 42, 46, 50, 52, 54, 57, 61, 64, 69, 71, 76, 79, 82, 86, 90, 92]:
    machine_answer="📃  "
elif value in [8, 12, 16, 22, 24, 33, 36, 39, 43, 48, 53, 59, 62, 65, 66, 70, 73, 77, 80, 83, 85, 87, 88, 89, 91, 93, 94, 95, 96, 97, 98, 99, 100]:
    machine_answer="✂️  "
else:
    print("un excepted error")
print(f"You have given {human_answer} while machine answer was {machine_answer}.")
if human_answer == machine_answer:
    print("match tied")
elif human_answer is "🏔️  " and machine_answer is "✂️  ":
    print("Human wins")
elif human_answer is "📃  " and machine_answer is "✂️  ":
    print("Machine wins")
elif human_answer is "✂️  " and machine_answer is "📃  ":
    print("Human wins")
elif human_answer is "✂️  " and machine_answer is "🏔️  ":
    print("Machine wins")
elif human_answer is "📃  " and machine_answer is "🏔️  ":
    print("Human wins")
elif human_answer is "🏔️  " and machine_answer is "📃  ":
    print("Human wins")
else:
    print("unexcepted error")
