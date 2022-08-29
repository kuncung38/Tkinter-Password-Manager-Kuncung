from random import choice, randint, shuffle
from tkinter import messagebox

END = 'end'

class GeneratePassword():
    def __init__(self):
        self.generated_password = ''
        self.generate_your_password()

    def generate_your_password(self):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        uppercase_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

        nr_letters = randint(4, 5)
        nr_symbols = randint(2, 4)
        nr_numbers = randint(2, 4)

        password_letter = [(choice(letters)+ choice(uppercase_letters)) for char in range(nr_letters)]
        password_symbol = [choice(symbols) for char in range(nr_symbols)]
        password_number = [choice(numbers) for char in range(nr_numbers)]

        password_list = password_letter + password_symbol + password_number
        
        shuffle(password_list)
        self.generated_password= "".join(password_list)

        