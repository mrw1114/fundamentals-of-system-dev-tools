def append_to(element, target=None):
    if target == None:
        target = []
    target.append(element)
    return target

print(append_to(1))
print(append_to(2))
