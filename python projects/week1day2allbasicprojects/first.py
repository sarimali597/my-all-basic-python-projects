name = input("Hello, user plese enter your name.")
day = input(f"{name} can you tell me what day is today? ")
day = day.title()

if day == "Monday":
    question = input(f"So {name} what is you plane to spend monday Tell in one word")
    question = question.title()
    if question == "Codding":
        print(f"{name} codding is a really nice way to spend monday ")
    elif question == "Gamming":
        print(
            f"{name} dont you think its not the waste of time on moday by playing games"
        )
    elif question == "Study":
        print(f"{name} its the most perfect way to spend your monday")
    else:
        print(f"{name} its nice to spend monday while doing {question}")
elif day == "Tuesday":
    question = input(f"So {name} what is you plane to spend Tuesday Tell in one word")
    question = question.title()
    if question == "Codding":
        print(f"{name} codding is a really nice way to spend Tuesday ")
    elif question == "Gamming":
        print(
            f"{name} dont you think its not the waste of time on Tuesday by playing games"
        )
    elif question == "Study":
        print(f"{name} its the most perfect way to spend your Tuesday")
    else:
        print(f"{name} its nice to spend Tuesday while doing {question}")
elif day == "Wednesday":
    question = input(f"So {name} what is you plane to spend Wednesday Tell in one word")
    question = question.title()
    if question == "Codding":
        print(f"{name} codding is a really nice way to spend Wednesday ")
    elif question == "Gamming":
        print(
            f"{name} dont you think its not the waste of time on Wednesday by playing games"
        )
    elif question == "Study":
        print(f"{name} its the most perfect way to spend your Wednesday")
    else:
        print(f"{name} its nice to spend Wednesday while doing {question}")
elif day == "Thursday":
    question = input(f"So {name} what is you plane to spend Thursday Tell in one word")
    question = question.title()
    if question == "Codding":
        print(f"{name} codding is a really nice way to spend Thursday ")
    elif question == "Gamming":
        print(
            f"{name} dont you think its not the waste of time on Thursday by playing games"
        )
    elif question == "Study":
        print(f"{name} its the most perfect way to spend your Thursday")
    else:
        print(f"{name} its nice to spend Thursday while doing {question}")
elif day == "Friday":
    question = input(f"So {name} what is you plane to spend Friday Tell in one word")
    question = question.title()
    if question == "Codding":
        print(f"{name} codding is a really nice way to spend Friday ")
    elif question == "Gamming":
        print(
            f"{name} dont you think its not the waste of time on Friday by playing games"
        )
    elif question == "Study":
        print(f"{name} its the most perfect way to spend your Friday")
    else:
        print(f"{name} its nice to spend Friday while doing {question}")
elif day == "Saturday":
    question = input(f"So {name} what is you plane to spend Saturday Tell in one word")
    question = question.title()
    if question == "Codding":
        print(f"{name} codding is a really nice way to spend Saturday ")
    elif question == "Gamming":
        print(
            f"{name} dont you think its not the waste of time on Saturday by playing games"
        )
    elif question == "Study":
        print(f"{name} its the most perfect way to spend your Saturday")
    else:
        print(f"{name} its nice to spend Saturday while doing {question}")
elif day == "Sunday":
    question = input(f"So {name} what is you plane to spend Sunday Tell in one word")
    question = question.title()
    if question == "Codding":
        print(f"{name} codding is a really nice way to spend Sunday ")
    elif question == "Gamming":
        print(
            f"{name} dont you think its not the waste of time on Sunday by playing games"
        )
    elif question == "Study":
        print(f"{name} its the most perfect way to spend your Sunday")
    else:
        print(f"{name} its nice to spend Sunday while doing {question}")
else:
    print("Enter Valid day name")
