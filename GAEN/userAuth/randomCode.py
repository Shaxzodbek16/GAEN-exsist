from random import randint


def get_random_code() -> str:
    random_code = randint(100000, 999999)
    return str(random_code)



