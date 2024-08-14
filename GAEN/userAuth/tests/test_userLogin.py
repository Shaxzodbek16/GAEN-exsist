def user() -> bool:
    return True


def test_user():
    res: bool = user()
    assert False == res
