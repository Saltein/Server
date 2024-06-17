import random, string




def GenerateAlfNumStr(length, type_="all"):
    """Creating an alphanumeric, numeric, or alphanumeric string"""
    if type_ == "all":
        letters_and_digits = string.ascii_letters + string.digits
        rand_string = ''.join(random.sample(letters_and_digits, length))
        return rand_string
    elif type_ == "int":
        letters_and_digits = string.digits
        rand_string = ''.join(random.sample(letters_and_digits, length))
        return rand_string
    elif type_ == "str":
        letters_and_digits = string.ascii_letters
        rand_string = ''.join(random.sample(letters_and_digits, length))
        return rand_string
    else:
        return False


def creatDictfromLists(lis):
    resDict = {}
    try:
        for i in range(len(lis)):
            resDict[i] = lis[i]
        return resDict
    except Exception as e:
        return []

