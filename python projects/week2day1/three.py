# i = 1
# while i <= 5:
#     j = 1
#     while j <= 5:
#         print(i * j)
#         j += 1
#     print()
#     i += 1
flag = True
counter = 0
while flag:
    print(f"Counter: {counter}")
    counter += 1
    if counter > 5:
        flag = False
else:
    print("loop finished successfully")
