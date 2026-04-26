def contains_purple(*args):
    if 'purple' in args:
        return True
    return False


colors = ['black', 'orange', 'blue', 'purple']
print(contains_purple(*colors))

# or

print(contains_purple('black', 'orange', 'blue', 'purple'))

def combine_words(word, **kwargs):
    if 'prefix' in kwargs:
        return kwargs['prefix'] + word
    elif 'suffix' in kwargs:
        return word + kwargs['suffix']
    else:
        return word
    
    
print(combine_words("child", suffix="ish"))    