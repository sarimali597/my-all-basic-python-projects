choice = input("Enter your choice (rectangle/square/circle/triangle): ").lower()
if choice == "rectangle":
    class Rectangle:
        def Intro(self,length,height,area):
            self.length=length
            self.height=height
            self.area=area
            print(f"The length of the rectangle is: {length}.\nThe height of the rectangle is: {height}.\nThe area of the rectangle is: {area}.")
    a = Rectangle()
    length = input("Enter length of rectangle: ")
    height = input("Enter height of rectangle: ")
    area = int(length) * int(height)
    a.Intro(length,height,area)
elif choice == "square":
    class Square:
        def Intro(self,side,area):
            self.side=side
            self.area=area
            print(f"The side of the square is: {side}.\nThe area of the square is: {area}.")
    a = Square()
    side = input("Enter side of square: ")
    area = int(side) * int(side)
    a.Intro(side,area)
elif choice == "circle":
    class Circle:
        def Intro(self,radius,area):
            self.radius=radius
            self.area=area
            print(f"The radius of the circle is: {radius}.\nThe area of the circle is: {area}.")
    a = Circle()
    radius = input("Enter radius of circle: ")
    area = 3.14 * int(radius) * int(radius)
    a.Intro(radius,area)
elif choice == "triangle":
    class Triangle:
        def Intro(self,base,height,area):
            self.base=base
            self.height=height
            self.area=area
            print(f"The base of the triangle is: {base}.\nThe height of the triangle is: {height}.\nThe area of the triangle is: {area}.")
    a = Triangle()
    base = input("Enter base of triangle: ")
    height = input("Enter height of triangle: ")
    area = 0.5 * int(base) * int(height)
    a.Intro(base,height,area)
else:
    print("Invalid choice.")