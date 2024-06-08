import pytest
import next
import random


@pytest.fixture(scope="module")
def size():
    return random.randint(1, 1000)


def test_pick_first(size):
    index = next.pick(size, 1)
    assert index == 0


def test_pick_last(size):
    index = next.pick(size, -1)
    assert index == size -1


def test_pick_random(size):
    index1 = next.pick(size, None)
    index2 = next.pick(size, None)
    assert 0 <= index1 < size and 0 <= index2 < size and index1 != index2


def test_pick_second():
    index = next.pick(100, 2)
    assert index == 1


def test_pick_second_last():
    index = next.pick(100, -2)
    assert index == 98


def test_pick_zero(size):
    index1 = next.pick(size, 0)
    index2 = next.pick(size, 0)
    assert 0 <= index1 < size and 0 <= index2 < size and index1 != index2
