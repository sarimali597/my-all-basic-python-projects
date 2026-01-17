sentence=input("Enter you sentence containing vowels: ")
if "a" or "o" or "u" or "e" or "i" in sentence:
    print(sum(1 for ch in sentence if ch in 'aeiou'))