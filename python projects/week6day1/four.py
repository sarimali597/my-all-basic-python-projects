class Mobile:
    def __init__(self,name=None ,city=None):
        if name and city:
            self.name=name
            self.city=city
            print(name, city)
        elif name:
            self.name=name
            print(self.name)
        elif city:
            self.city=city
            print(self.city)
        print("Mobile Name: ",self.name)
        print("City: ",self.city)