import importlib.util
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('wcag_contrast_check', ROOT / 'scripts' / 'wcag_contrast_check.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_black_white_is_maximum_contrast():
    assert MODULE.ratio('#000000', '#FFFFFF') == pytest.approx(21.0)


def test_mid_gray_on_white_fails_normal_text_threshold():
    assert MODULE.ratio('#777777', '#FFFFFF') < 4.5


def test_contrast_ratio_is_order_independent():
    assert MODULE.ratio('#FFFFFF', '#000000') == pytest.approx(MODULE.ratio('#000000', '#FFFFFF'))


def test_rejects_invalid_hex_colors():
    with pytest.raises(ValueError):
        MODULE.ratio('white', '#FFFFFF')
