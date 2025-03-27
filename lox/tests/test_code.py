
# from 

# def _runner():

from lox.eng import Eng


def test_a():
    assert Eng().run("3 + 5;") == 8
    assert Eng().run("3 / 3;") == 1
    assert Eng().run("3 + 5 == 9 - 1;") == True

def test_print():
    assert Eng().run("print 3 + 5;") == None

