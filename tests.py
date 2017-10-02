import dispatch
from dispatch import Case


def test_ratsignal():
    ret = dispatch.Parser.parse(data=dispatch.debug_constant_B)
    assert type(ret) is Case
    assert ret.client == "Potato"
    return True


def init():
    assert test_ratsignal()


if __name__ == '__main__':  # this prevents script code from being executed on import. (bad!)
    init()
