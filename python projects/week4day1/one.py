# # # # # # dict={"Name":"Sarim","Age":"20","City":"Sukkur"}
# # # # # # print(dict)
# # # # # # for i in dict.items():
# # # # # #     print(i)
# # # # # try:
# # # # #     num = int(input('Enter a number: '))
# # # # #     result = 10 / num
# # # # # except ZeroDivisionError:
# # # # #     print('Cannot divide by zero.')
# # # # # except ValueError:
# # # # #     print('Invalid input. Please enter a number.')
# # # # try:
# # # #     num = int(input('Enter a number: '))
# # # #     result = 10 / num
# # # # except ZeroDivisionError:
# # # #     print('Cannot divide by zero.')
# # # # finally:
# # # #     print('End of program.')
# # # age=int(input("Enter a number"))
# # # def check_age(age):
# # #     if age < 18:
# # #         raise ValueError('Age must be at least 18.')
# # #     else:
# # #         print('Access granted.')
# # # try:
# # #     check_age(age)
# # # except ValueError as e:
# # #     print(e)
# # def multiply(a, b):
# #     print(f'a = {a}, b = {b}')
# #     result = a * b
# #     print(f'Result = {result}')
# #     return result
# # multiply(5, 10)
# # Contact Management System
# contacts = {}
# def add_contact(name, phone, email):
#     contacts[name] = {'phone': phone, 'email': email}
# def delete_contact(name):
#     if name in contacts:
#             del contacts[name]
#             print(f'{name} has been deleted.')
#     else:
#         print(f'{name} not found.')
# def search_contact(name):
#     if name in contacts:
#         print(f"Name: {name}, Phone: {contacts[name]['phone']}, Email: {contacts[name]['email']}")
#     else:
#         print(f'{name} not found.')
# # Example usage
# add_contact('Alice', '123-456', 'alice@example.com')
# add_contact('Bob', '789-012', 'bob@example.com')
# search_contact('Alice')
# delete_contact('Bob')
