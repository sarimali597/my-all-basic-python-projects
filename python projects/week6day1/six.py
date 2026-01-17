class A:    
    def Car(self,name):
        self.name = name
        print("I am method of class A. My name is ", self.name)
class B:
    def Car(self,name,model,city):
        self.name = name
        self.model = model
        self.city = city
        print("I am method of class B. My name is ", self.name, " and my model is ", self.model, " also the city is ", self.city)  
a=A()
a.Car("Audi")
b=B()
b.Car("BMW","2020","Karachi")