order = {"b": 1, "c": 2, "d": 3}

to_sort = ["cbd", "bc", "dc", "cd"]

def sort_key():
    return [order.get(char) for char in sort_key()]

print(to_sort.sort(key=sort_key())) 