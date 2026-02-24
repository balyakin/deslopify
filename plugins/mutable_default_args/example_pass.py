def valid_function(items=None, config=None):
    if items is None:
        items = []
    if config is None:
        config = {}
    return items

def function_with_strings(name="default", active=True, count=0):
    return name

def function_with_tuple(data=(1, 2, 3)):
    return data

async def async_valid(data=None):
    pass
