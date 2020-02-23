import string
import random
import names

def netid_generator(number_of_numbers, number_of_letters):
    characters = string.ascii_lowercase
    digits = string.digits
    chars = []
    while(number_of_letters > 0):
        chars.append(random.choice(characters))
        number_of_letters = number_of_letters -1
    nums = []
    while(number_of_numbers > 0):
        nums.append(random.choice(digits))
        number_of_numbers = number_of_numbers-1
    charchars = ''.join(chars)
    numnums = ''.join(nums)
    return charchars +numnums
        

def female_names():
    return names.get_full_name(gender = 'female')
    
def male_names():
    return names.get_full_name(gender = 'male')

