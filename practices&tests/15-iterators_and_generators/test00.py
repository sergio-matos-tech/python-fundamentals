

def custom_for_loop(iterable):
    
    iterator = iter(iterable)
    
    while True:
        try:
            print(next(iterator))
        except StopIteration as si:
            break
        
        
        
custom_for_loop('Hello')
custom_for_loop([1234, 43, 32, 322, 43])
