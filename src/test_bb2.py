from bb2 import BB2_CONFIG, Bb2


def test_hello():
    bb = Bb2(BB2_CONFIG)
    assert bb.hello() == "Hello from BB2 SDK Class method!!!"
