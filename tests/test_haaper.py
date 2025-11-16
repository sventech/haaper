import pytest
from pathlib import Path
from haaper import custom2xlat, unicode2tiqwah, tiqwah2unicode, tiqwah2phonetic, \
    tiqwah2pattern, DIRECTION_MARKERS

UNICODE_EXAMPLE = Path('tests/human_rights.txt').read_text()
TIQWAH_EXAMPLE = Path('tests/human_rights.tiq').read_text()

def test_custom2xlat_simple():
    test_key = {"A": "1", "B": "2", "C": "3", "D": "4"}
    test_value = "ABCD"
    result = custom2xlat(test_value, test_key)
    assert result == "1234"

    test_key = {"AA": "1", "B": "2", "C": "3", "D": "4"}
    test_value = "ABCDAA"
    result = custom2xlat(test_value, test_key)
    assert result == "A2341"

def test_unicode2tiqwah():
    result = unicode2tiqwah(UNICODE_EXAMPLE)
    assert result == TIQWAH_EXAMPLE

# def test_tiqwah2unicode():
#     result = tiqwah2unicode(TIQWAH_EXAMPLE)
#     result_unmarked = result
#     for marker in DIRECTION_MARKERS:
#         result_unmarked = result_unmarked.replace(marker, '')
#     words = result_unmarked.split(' ')
#     unicodes = UNICODE_EXAMPLE.split(' ')
#     for w, u in zip(words, unicodes):
#         assert w == u or w == u

def test_tiqwah2phonetic():
    result = tiqwah2phonetic(TIQWAH_EXAMPLE)
    assert len(result) > 0

def test_tiqwah2prose_pattern():
    result = tiqwah2pattern(TIQWAH_EXAMPLE)
    assert len(result) > 0

def test_tiqwah2psalm_pattern():
    result = tiqwah2pattern(TIQWAH_EXAMPLE, is_psalmodic=True)
    assert len(result) > 0

