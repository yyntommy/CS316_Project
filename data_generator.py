import string
import random
import names

STIMES = ['20:00', '21:00', '22:00', '23:00', '00:00', '01:00', '02:00', '03:00', '20:30', '21:30', '22:30', '23:30', '00:30', '01:30', '02:30', '03:30']
WTIMES = ['06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '06:30', '07:30', '08:30', '09:30', '10:30', '11:30', '12:30', '13:30']
TMAJORS = ['African and African American Studies', 'Air Force ROTC', 'Army ROTC', 'Art, Art History and Visual Studies', 'Arts of the Moving Image', 'Asian and Middle Eastern Studies', 'Biology', 'Chemistry', 'Classical Studies', 'Computer Science', 'Cultural Anthropology', 'Dance', 'Ecnomics', 'Education', 'English', 'Evolutionary Anthropology', 'Gender, Sexuality and Feminist Studies', 'Germanic Languages and Literature', 'Health, Wellness and Physical Education', 'History', 'International Comparative Studies', 'Linguistics', 'Literature', 'Mathematics', 'Music', 'Navy ROTC', 'Philosophy', 'Physics', 'Political Science', 'Psychology', 'Neuroscience', 'Religious Studies', 'Romance Studies', 'Slavic and Eurasian Studies', 'Sociology', 'Statistical Science', 'Theater Studies']
PMAJORS = ['Biomedical Engineering', 'Civil Engineering', 'Environmental Engineering', 'Electrical and Computer Engineering', 'Mechanical Engineering', 'Energy Engineering']
SCHOOLS = ['Trinity College of Arts and Sciences', 'Pratt School of Engineering']
HOUSEOPTIONS = [['Avalon','Kilgo'], ['Banham', 'Edens'], ['Bastille' ,'Edens'], ['Bel Air', 'Edens'], ['Blue Ridge', 'Keohane'], ['Farquaad' ,'Edens'], ['Gates', 'Crowell'], ['Griffin', 'Crowell'], ['Hart', 'Crowell'], ['House 3B', 'Edens'], ['Hun', 'Few'], ['Khaya', 'Edens'], ['Lumos', 'Craven'], ['Magnolia Commons', 'Crowell'], ['Marquis', 'Kilgo'], ['Montauk', 'Few'], ['Mt. Olympus' ,'Hollows'], ['Narnia', 'Hollows'], ['Ox' ,'Keohane'], ['Powerhouse' ,'Craven'], ['Pride Rock', 'Few'], ['Rabbit Hole' ,'Hollows'], ['Sherwood', 'Craven'], ['Shire', 'Keohane'], ['Sierra', '300 Swift'], ['Skylar', 'Hollows'], ['Stark' ,'Wannamaker'], ['Stonehenge' ,'Kilgo'], ['Styron' ,'Few'], ['Tortuga' ,'Hollows'], ['Windsor', 'Keohane']]

def g_netid(number_of_numbers, number_of_letters):
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


def fname():
    return names.get_full_name(gender = 'female')

def mname():
    return names.get_full_name(gender = 'male')

def get_new_users(num):
    users = []
    uids = []

    for i in range(num):
        nid = g_netid(random.randrange(2,4),random.randrange(2,4))
        uids.append(nid)

        user = "insert into Users values ('{netid}', '{name}', '{gender}', '{year}', '{smoke}', '{sleep}', '{wake}', '{utility}', '{campus}', 'default_profile.png', 'pbkdf2:sha256:150000$9kLJiurt$03f84eb4796f9497b08e5f58e9f14822795151ee4747a487ef5ecd0bf1d05c2d');".format(netid=nid, name=random.choice([fname(), mname()]), gender=random.choice(["M", "F", "O"]), year=random.choice([2021,2022,2023,2024]), smoke=random.choice(['Y', 'N']), sleep=random.choice(STIMES), wake=random.choice(WTIMES), utility=random.choice(["Study", "Social"]), campus=random.choice(['Y', 'N']))
        users.append(user)

    return users, uids

def get_new_usermajors(users):
    usermajor = []

    for user in users[0:int(len(users)*0.75)]:
        choice = "insert into UserMajor values ('{netid}', '{major}', '{school}');".format(netid=user, major=random.choice(TMAJORS), school=SCHOOLS[0])
        usermajor.append(choice)

    for user in users[int(len(users)*0.75):len(users)]:
        choice = "insert into UserMajor values ('{netid}', '{major}', '{school}');".format(netid=user, major=random.choice(PMAJORS), school=SCHOOLS[1])
        usermajor.append(choice)

    return usermajor

def get_new_userlikes(users):
    userlikes = []

    for user in users:
        for i in range(random.randrange(0,6)):
            housing = random.choice(HOUSEOPTIONS)
            likes = "insert into UserLikes values ('{netid}', '{name}', '{building}');".format(netid=user, name=housing[0], building=housing[1])
            userlikes.append(likes)

    return userlikes

def main():
    users, nids = get_new_users(500)
    usermajors = get_new_usermajors(nids)
    userlikes = get_new_userlikes(nids)

    aggregate = users + usermajors + userlikes

    f = open("load2.sql", "w+")
    for line in aggregate:
        insert = line + "\n"
        f.write(insert)

    f.close()

if __name__=="__main__":
    main()
