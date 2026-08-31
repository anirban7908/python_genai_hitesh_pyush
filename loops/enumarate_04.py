# enumerate() is a built-in Python function that allows you to loop through an iterable (like a list, tuple, or string) while automatically keeping track of the index (position) of each item.
menu = ["Green", "Lemon", "Spiced", "Mint"]

for idx, item in enumerate(menu):
    print(f"The id is:{idx}, and the value is: {item}")