# # # # # # # # # # # # # # # # file=open('example.txt','w')
# # # # # # # # # # # # # # # # file.write('Hello world')
# # # # # # # # # # # # # # # # file.close()
# # # # # # # # # # # # # # # file = open('example.txt', 'r')
# # # # # # # # # # # # # # # content = file.read()
# # # # # # # # # # # # # # # print(content)
# # # # # # # # # # # # # # # file.close()
# # # # # # # # # # # # # # line= ['line 1\n','line 2\n','line 3\n','line 4\n','line 5\n']
# # # # # # # # # # # # # # file=open('example.txt','w')
# # # # # # # # # # # # # # file.writelines(line)
# # # # # # # # # # # # # # file.close()
# # # # # # # # # # # # # file=open('example.txt', 'r')
# # # # # # # # # # # # # for line in file:
# # # # # # # # # # # # #     print(line.strip())
# # # # # # # # # # # # # file.close()
# # # # # # # # # # # # file=open('example.txt', 'a')
# # # # # # # # # # # # file.write('\nHow are you')
# # # # # # # # # # # # file.close()
# # # # # # # # # # # with open('example.txt', 'r') as file:
# # # # # # # # # # #     content = file.read()
# # # # # # # # # # #     print(content)
# # # # # # # # # # with open ('numbers.txt', 'w') as file:
# # # # # # # # # #     for num in range(1, 6):
# # # # # # # # # #         file.write(f"{num}\n")
# # # # # # # # # import os
# # # # # # # # # if os.path.exists('example.txt'):
# # # # # # # # #     with open('example.txt', 'r') as file:
# # # # # # # # #         print(file.read())
# # # # # # # # # else:
# # # # # # # # #     print("The file does not exists")
# # # # # # # # import os
# # # # # # # # try:
# # # # # # # #     with open('data.txt', 'r') as file:
# # # # # # # #         print(file.read())
# # # # # # # # except OSError:
# # # # # # # #     print("The file wasn't found")
# # # # # # # items = ['apple', 'banana', 'cherry']
# # # # # # # with open('items.txt', 'w') as file:
# # # # # # #     for item in items:
# # # # # # #         file.write(f'{item}\n')
# # # # # # # with open('items.txt', 'r') as file:
# # # # # # #     for line in file:
# # # # # # #         print(line.strip())
# # # # # # with open ('items.txt', 'r') as file:
# # # # # #     content = file.read()
# # # # # #     words = content.split()
# # # # # #     print(f'Number of words: {len(words)}')
# # # # # # with open('example.txt', 'r') as file1:
# # # # # #     content = file1.read()
# # # # # # with open('copy.txt', 'w') as file2:
# # # # # #     file2.write(content)
# # # # # # user_input= input("Enter some text: ")
# # # # # # with open('user_input.txt', 'w') as file:
# # # # # #     file.write(user_input)
# # # # # with open('example.txt', 'r') as file:
# # # # #     file.seek(10)
# # # # #     print(f'current position: {file.tell()}')
# # # # #     print(file.read())
# # # # import os
# # # # if os.path.exists('copy.txt'):
# # # #     os.remove('copy.txt')
# # # #     print('file deleted successfully')
# # # # else:
# # # #     print("File doesn't exists")
# # # name = input("Enter your name: ")
# # # age = input("Enter your age: ")
# # # with open('user_info.txt', 'a') as file:
# # #     file.write(f'Name: {name}, Age: {age}\n')
# # #     file.seek(0)
# # #     print(file.read)
# # with open('user_info.txt', 'r') as file:
# #     line_count = len(file.readlines())
# #     print(f'Total lines: {line_count}')
# lines = []
# for _ in range(3):
#     line = input("Enter a line of text: ")
#     lines.append(line)
# with open('user_input.txt', 'a') as file:
#     for line in lines:
#         file.write(line + '\n')
with open('user_input.txt', 'r') as file:
    content = file.read()
updated_content = content.replace('foo', 'bar')
with open('user_input.txt', 'w') as file:
    file.write(updated_content)
