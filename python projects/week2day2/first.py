name = input("Dear user please input your good name: ")
age = input(f"Dear {name} please input your age: ")
qualification = input(f"Dear {name} can you briefly tell me your qualifiation: ")
qualification = qualification.lower()
skills = input(
    f"Dear {name} it will be honour for me to know what exactly my user have skills: "
)
print(
    f"Hello, {name} its a nice that you have completed your {qualification} at the age of {age} and having skill {skills} ."
)
if qualification == "matriculation":
    input(
        f"{name} its nice you have completed your matriculation but can you tell me your passing year of your matriculation"
    )
    input(
        f"dear {name} can you clearify the grades you have achieved in your matriculation "
    )
elif qualification == "enter":
    input(
        f"{name} its nice you have completed your enter but can you tell me your passing year of your enter"
    )
    input(f"dear {name} can you clearify the grades you have achieved in your enter ")
elif qualification == "batcholors":
    input(
        f"{name} its nice you have completed your batcholors but can you tell me your passing year of your batcholors"
    )
    input(
        f"dear {name} can you clearify the grades you have achieved in your batcholors "
    )

else:
    input(
        f"{name} its nice you have completed your {qualification} but can you tell me your passing year of your batcholors"
    )
    input(
        f"dear {name} can you clearify the grades you have achieved in your {qualification} "
    )
