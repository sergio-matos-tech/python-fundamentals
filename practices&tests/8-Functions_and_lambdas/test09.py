

'''
Interleaving Strings (kind of tough!)
This challenge is a bit more involved than the others in this section.  Do not worry if you can't get it!

Write a function interleave  that accepts two strings.  It should return a new string containing the 2 strings interwoven or zipped together. For example:

interleave('hi','ha')    # 'hhia'

interleave('aaa', 'zzz')  # 'azazaz'

interleave('lzr','iad') #  'lizard'

 This might seem like an easy task using zip , but in fact there are a couple intermediate steps to go from zip  back to a single string.  If you need help, I've written up a basic walkthrough of the steps:

suppose we call interleave('hi', 'no')  

zip  the two strings together, giving you a list of tuples (once you convert from the default zip_object) -  [('h','n'), ('i','o')]  

For each of the tuples in the list, join them together using "".join  resulting in ['hn', 'io']  - Easiest if you use a list comp.  You need to join EACH tuple.

Finally, join the items in the list together using "".join  again resulting in 'hnio'  

Don't stress if you don't get this one!


'''


def interleave(string1, string2):
    new_string = ''
    for a, b in zip(string1, string2):
        new_string += a + b
    return new_string



print(interleave('aaa', 'zzz'))
print(interleave('hi','ha'))
print(interleave('lzr','iad'))



def triple_and_filter():
    
    