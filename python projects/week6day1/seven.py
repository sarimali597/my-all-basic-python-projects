class A:
    def Intro(self,name,county):
        self.name=name
        print(f"Hello my name is: {name}.\nI am from {county}.")
a = A()
name = input("Enter your name: ")
country = input("Enter your country: ")
a.Intro(name,country)