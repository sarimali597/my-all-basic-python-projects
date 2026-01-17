raining=input("I their raining outside today? yes/no : ")
homework=input("do you have any homework today? yes/no: ")
if raining=="yes" and homework=="yes":
    print("Its dangerouse to go outside i sugest stay at home and do your work from home")
elif raining=="yes" and homework=="no":
    print("Its nice you are free their is no work can be disturbed so watch your movie while stay at home.")
elif raining=="no" and homework=="yes":
    print("Go to office reponsively")
elif raining=="no" and homework=="no":
    print("Go to home spend time with family")
else:
    print("Dear user write your answer in yes or no")
