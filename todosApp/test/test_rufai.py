import pytest


def test_two_numbers():
    assert 3 == 3


class Rufai:

    def __init__(self, first_name: str, last_name: str, major: str, level: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.level = level


@pytest.fixture
def general_object():
    return Rufai('Abdul-Mumin', 'Rufai', 'Computer Science', 400)


def test_rufai(general_object):
    assert general_object.first_name == 'Abdul-Mumin'
    assert general_object.last_name == 'Rufai'
    assert general_object.major == 'Computer Science'
    assert general_object.level == 400
