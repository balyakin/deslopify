def bad_list_func(items=[]):
    items.append(1)
    return items

def bad_dict_func(name="test", config={}):
    config[name] = True
    return config

def bad_set_func(cache=set()):
    pass

def bad_kwonly_func(data, *, options=list()):
    pass

async def bad_async_func(items=[]):
    pass
