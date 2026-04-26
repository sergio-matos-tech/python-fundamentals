def last_paremeter(list):
    if list:
        return list[-1]
    return None


print(f"Last parameter {last_paremeter([12, 32, 432, 31, 9])}")


def letter_count(word="Hello", letter='H'):
    count = 0
    for char in word:
        if char == letter:
            count += 1
    return count


print(letter_count("fwhqjflkjdsaçflkjdfsa", "a"))


def is_palindrome(word="ovo"):
    if word == ''.join(reversed(word)):
        return True
    return False


print(is_palindrome())
