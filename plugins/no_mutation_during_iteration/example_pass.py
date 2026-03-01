# Хорошая практика: итерация по копии
for key in list(my_dict.keys()):
    if should_delete(key):
        del my_dict[key]

# Запоминание ID для удаления
to_delete = []
for item in my_list:
    if condition(item):
        to_delete.append(item.id)

for item_id in to_delete:
    my_list.remove(item_id)
