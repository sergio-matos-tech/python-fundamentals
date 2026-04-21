def yell(string):
    new_string = string.upper()
    new_string += '! '
    return new_string


print(yell('go away'))


def count_dollar_signs(word):
    count = 0
    for char in word:
        if char == '$':
            count += 1
    return count


print(count_dollar_signs('$$$ 33345t55 $$ 444 $'))



def speak(animal='dog'):
    if animal == 'pig':
        return 'oink'
    elif animal == 'cat':
        return 'mial'
    

print(speak())
print(speak('cat'))
