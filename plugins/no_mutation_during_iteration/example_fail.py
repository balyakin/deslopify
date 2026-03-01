# Плохо: удаление во время итерации
for key in my_dict:
    if condition(key):
        del my_dict[key]

# pop()
for item in my_list:
    if condition(item):
        my_list.pop()

# remove()
for val in items:
    if val == 0:
        items.remove(val)
