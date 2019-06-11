from pytest import *
from unittest.mock import Mock, call


def test_wheel():
    import code
    assert [0, 255, 0] == code.wheel(0)
    assert [189, 66, 0] == code.wheel(63)
    assert [129, 0, 126] == code.wheel(127)
    assert [0, 63, 192] == code.wheel(191)

def test_morse(monkeypatch):
    import code
    mock_time = Mock(sleep=Mock())
    monkeypatch.setattr(code, 'time', mock_time)

    m = code.Morse("... --- ...")
    m.start()
    for i in range(11):
        m.next()

    from pprint import pprint
    pprint(mock_time.sleep.mock_calls)
    assert mock_time.sleep.mock_calls == 6*[call(0.2)] + [call(0.4)] + 3*[call(0.2), call(approx(0.6))] + [call(0.2), call(0.4)] + 7*[call(0.2)]
