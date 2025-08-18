import os
import sys

# Make src/PlayGame importable
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src', 'PlayGame'))

import ascii_wheel


def test_parse_values_arg_mappings():
    raw = 'BK, LT, 500, 0, -1, LOSE, LOSETURN, LOSE_TURN, BANKRUPT, 250'
    out = ascii_wheel.parse_values_arg(raw)
    assert out == [-1, 0, 500, 0, -1, 0, 0, 0, -1, 250]


def test_parse_values_arg_invalid_raises():
    # Non-numeric and not a known token should raise ValueError
    try:
        ascii_wheel.parse_values_arg('X')
        raised = False
    except ValueError:
        raised = True
    assert raised


def test_draw_ascii_wheel_outputs_labels(capsys):
    # Small wheel and a few values. Ensure labels appear as expected.
    values = [0, -1, 100, 200]
    ascii_wheel.draw_ascii_wheel(values, radius=3, label_style='short')
    out_short = capsys.readouterr().out
    assert '0' in out_short
    assert 'BK' in out_short

    ascii_wheel.draw_ascii_wheel(values, radius=3, label_style='long')
    out_long = capsys.readouterr().out
    assert 'LOSE TURN' in out_long
    assert 'BANKRUPT' in out_long
