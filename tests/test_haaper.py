import pytest
from pathlib import Path
from haaper.haaper import custom2xlat, unicode2tiqwah, tiqwah2unicode, tiqwah2phonetic, \
    tiqwah2prose_pattern, tiqwah2psalm_pattern, DIRECTION_MARKERS

UNICODE_EXAMPLE = Path('tests/human_rights.txt').read_text()
TIQWAH_EXAMPLE = Path('tests/human_rights.tiq').read_text()

def test_custom2xlat():
    assert 1 == 1

def test_unicode2tiqwah():
    result = unicode2tiqwah(UNICODE_EXAMPLE)
    assert result == TIQWAH_EXAMPLE

def test_tiqwah2unicode():
    result = tiqwah2unicode(TIQWAH_EXAMPLE)
    result_unmarked = result
    for marker in DIRECTION_MARKERS:
        result_unmarked = result_unmarked.replace(marker, '')
    assert result_unmarked == UNICODE_EXAMPLE

def test_tiqwah2phonetic():
    result = tiqwah2phonetic(TIQWAH_EXAMPLE)
    assert len(result) > 0

def test_tiqwah2prose_pattern():
    result = tiqwah2prose_pattern(TIQWAH_EXAMPLE)
    assert len(result) > 0

def test_tiqwah2psalm_pattern():
    result = tiqwah2psalm_pattern(TIQWAH_EXAMPLE)
    assert len(result) > 0

