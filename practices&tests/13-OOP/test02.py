class User:
    
    active_users = 0
    
    def __init__(self, first_name, second_name, email, age) -> None:
        self.first_name = first_name
        self.second_name = second_name
        self.email = email
        self._age = age
    
    def user_info(self):
        return f'Full name: {self.first_name + ' ' + self.second_name}, email: {self.email}, age: {self._age}'
    
    def activate_user(self):
        User.active_users += 1
    

user1 = User('Sergio', 'Matos', 'sm@gmail.com', 29)
print(user1.user_info())
print(user1._age)
