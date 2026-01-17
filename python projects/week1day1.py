print("Python successully installed!")
print("I am 17 years old.")
print("i love to code")

name =  "sarim"
age = 17
favourite_food = input("what is your favourite food? :")
most_favourite_food = input("what is your most favourite food?:")
floating_value = 3.3

print("Name:" , name)
print("Age:" , age)
print("favourite food:" , favourite_food , "&" ,  most_favourite_food)
print("Hello , My name is " , name , "I am" , age , "Years old. my favourite food is" , favourite_food , "&" ,  most_favourite_food )
print("Type of name: " , type(name))
print("Type of age: " , type(age))
print("type of pre defined float value:" , type(floating_value))

num1 = float(input("Enter first number:"))
num2 = float(input("Enter Second number:"))
average = (num1+num2) / 2
print("Average of two numbers :" , average)
quotient = num1/num2
print("quotient (rounded) : " , round(quotient,2))
sum = num1 + num2
product = num1 * num2
div = num1 / num2
sub = num1 - num2


print(sum)
print(div)
print(product)
print(sub)


name = input("Enter your name : ")
age = int(input("Enter your age :"))
years_left = 100 - age
age_in_dog_life = age * 7
print("Hello! " + name +  " How are you? I hope you are fine.")
print("hello! "  + name +  " you will be 100 years old in "  + str(years_left) + " years.")
width = float(input("Enter width of the element to find its area :"))
height = float(input("Enter height of the element to find its area :"))
area = width * height
print("the area of the element is: " , area )
price =  float( input("enter the price of the item you have purchaced: "))
quantity = int(input("enter the quantity of the item you have purchaced: "))
discount = float(input("Enter discount percentage:"))
total_price = price*quantity
final_price  = total_price * (1 - discount)
print("final price after discount : " , final_price)
print('Hello {name} , you are {age} years old')
celcius = float(input("Enter the degree of celcius to convert: "))
farenheit_answer = (celcius*9/5)+32
print("The converted degree of celcius into farenheit is :  " , farenheit_answer)
farenheit = float(input("Enter the degree of farenheit to convert: "))
celcius_answer = (farenheit-32)*5/9
print("The converted degree of farenheit into celcius is :  " , celcius_answer )
num = int(input("enter a number: "))
print(f"number is even if answer is 0 else number is odd: . Answer = {num%2}")
radius = float(input("Enter the value of radius of the circle to find its Area: "))
area = 3.142*(radius*2)
print(f"Area of circle with radius {radius} is {area}." )
name = input("Enter your name: ")
profession = input("Enter your profession: ")
fun_fact = input("Enter your fun fact: ")
print(f" Hello {name} \n your profession is {profession} \n your fun fact is {fun_fact}")
height = float(input("Enter your height in meters: "))
weight = float(input("Enter your weight in Kilograms"))
bmi = weight/(height**2)
print(f"Your BMI is {bmi:.3f}")
sentence = input("Enter any sentence: ")
print("Uppercase: " , sentence.upper())
print("Lowercase: " , sentence.lower())
print("Titlecase: " , sentence.title())
movie = input("Enter your favourite movie: ")
city = input("Enter your favourite city: ")
print("your favourite movie is {} and your favourite city is {} . " .format(movie,city))
