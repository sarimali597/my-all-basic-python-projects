# # # # # # # # # def add_numbers(a, b):
# # # # # # # # #     print("added: ", a + b)
# # # # # # # # #     print("subtracted: ", a - b)
# # # # # # # # #     print("multipication: ", a * b)
# # # # # # # # #     print("division: ", a + b)
# # # # # # # # #     return a + b
# # # # # # # # # add_numbers(
# # # # # # # # #     a=int(input("Enter the value of a: ")), b=int(input("Enter the value of b: "))
# # # # # # # # # )
# # # # # # # # # def add_numbers(a, b):
# # # # # # # # #     return a + b
# # # # # # # # # result = add_numbers(3, 5)
# # # # # # # # # print(result)
# # # # # # # # # def greet_user(name, greeting="hello"):
# # # # # # # # #     print(f"{greeting} , {name} !")
# # # # # # # # # greet_user(input("Enter name: "))
# # # # # # # # # greet_user(input("Enter name: "), input("Enter greet: "))
# # # # # # # # # def describe_pet(animal="dog", name="buddy"):
# # # # # # # # #     print(f"I have a {animal} named {name}.")
# # # # # # # # # describe_pet(animal="cat", name="whisckers")
# # # # # # # # # describe_pet(name="whiskers", animal="cat")
# # # # # # # # # describe_pet("whiskers","cat")
# # # # # # # # # def math_operations(a,b):
# # # # # # # # #     return (a+b, a-b, a*b)
# # # # # # # # # a= math_operations(10,5)
# # # # # # # # # print(a,type(a))
# # # # # # # # def sum_all(*numbers):
# # # # # # # #     return sum(numbers)
# # # # # # # # print(sum_all(1,2,3,4))
# # # # # # # def sum_all(*numbers):
# # # # # # #     sum = 0
# # # # # # #     for num in numbers:
# # # # # # #         sum += num
# # # # # # #     return sum
# # # # # # # result = sum_all(1, 2, 3, 4)
# # # # # # # print(result)
# # # # # # def outer_function():
# # # # # #     def inner_function():
# # # # # #         print("This is the inner function. ")
# # # # # #     inner_function()
# # # # # # outer_function()
# # # # # def calculator(a, b, operator):
# # # # #     if operator == '+':
# # # # #         return a + b
# # # # #     elif operator == '-':
# # # # #         return a - b
# # # # #     elif operator == '*':
# # # # #         return a * b
# # # # #     elif operator == '/':
# # # # #         return a / b
# # # # #     else:
# # # # #         return 'Invalid operator'
# # # # # print(calculator(10, 2, '*'))
# # # # def print_items(items):
# # # #     for item in items:
# # # #         print(item)
# # # # fruits=["apples", "banana", "cherry"]
# # # # print_items(fruits)
# # # def find_max(a,b,c):
# # #     if a>=b and a>=c:
# # #         return a
# # #     elif b>=a and b>=c:
# # #         return a
# # #     else:
# # #         return c
# # # print(find_max(10,15,5))
# # # def factorial (n):
# # #     if n == 0:
# # #         return 1
# # #     else:
# # #         return n * factorial(n-1)
# # # # print(factorial(4))
# # # def fact(n):
# # #     result=1
# # #     for i in range(1,n+1):
# # #         result*=i
# # #     return result
# # # print(fact(4))
# # # print((lambda a,b:a+b) (1,2))
# # # a=lambda a,b:a+b
# # # print(a(1,2))
# # def is_even(n):
# #     return n % 2 == 0
# # print(is_even(4))
# # print(is_even(5))
# # number=[4,4,5,7,3,56,]
# # number.sort()
# # print(number)
# numbers= [10,20,30,40,50]
# numbers.insert(5,25)
# print(numbers)
# fruits=["apple", "banana" , "cherry"]
# if "banana" in fruits:
# print(fruits)
# squares=[x**2 for x in range (1, 10)]
# print(squares)
the_list=[[1,2],[3,4],[5,6]]
for sublist in the_list:
    print(sublist)
    for list in sublist:
        print(list)