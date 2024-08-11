#!/usr/bin/env python
# Produce Alda song and Hebrew ASCII IPA text from Hebrew Bible text
import argparse
import codecs
import csv
import json
import re
import sys
from typing import Iterable
from haaper.haaper import tiqwah2codes, code2tiqwah, tiqwah2pattern, tiqwah2phonetic


def named_regex(p_name, pattern, optional=False):
    '''named pattern generator'''
    pat = r'(?P<' + p_name + r'>' + pattern
    if optional:
        pat += '|)'
    else:
        pat += ')'
    return pat


def strip_regex(stringSource, regexPattern) -> tuple:
    '''remove substrings defined by regex
        and return (newString, match(es) removed)'''
    matchesRemoved = []
    matches = regexPattern.findall(stringSource)
    matchesRemoved = matches
    newString = regexPattern.sub("", stringSource)
    return (newString, matchesRemoved)


# consonants + aleph & ayin, begadkefat
consonant = r'b\*|g\*|d\*|k\*|p\*|t\*|'  # begadkefat (w/dagesh)
consonant += r'l\*|S\*|'				 # lamed/shin/
consonant += r'[\'bgdhwzxTyklmns\`pYqrSWt]|(W\/)|'  # regular C's, sin w/out dot
C = named_regex("C", consonant, optional=False)

# vowels + schwa
vowel = r'[aeiouAE]|\"|\||'
vowel += r'w\^o|w\*|'			   # holem vowels
vowel += r'<HSE>|<HPA>|<HQA>'	   # hateph-{segol,patach,qamats}
V = named_regex("V", vowel, optional=False)

# vowel time for music
shwa_time = r'\"|<HSE>|<HPA>|<HQA>'  # schwa,hateph-{segol,patach,qamats}

# Musical Accents (te'amim -- ta'am, singular)
taAm = r'(?:\[(\d\d\d)\])'

# closed syllable code
C2 = named_regex("C2", consonant, optional=True)  # coda (2nd consonant)

onset = re.compile(C)  # onset = starting consonant of syllable
core = re.compile(V)   # core vowel
coda = re.compile(C2)  # coda  = final consonant

# lookahead assertion: only if followed by...
semivowel = re.compile(r"y(?=k|t)")
# we should do lookbehind for "iy", but our list makes that tough
#  or include the whole consonant class -- CC is not valid

music = re.compile(taAm)  # we only use numbers for music
shortvowel = re.compile(shwa_time)
end_passage = re.compile(r":")
text_pause = re.compile(r" \|")

# arpeggio patterns ('[+1+2+3]' or '[+0]')
relative_pattern = re.compile(r"\[(.+)\]")  # anything in square braces
relative_note = re.compile(r"([\+\-])(\d|\%)")

# translate overall music by mode
note_names = {
    #                     0    1    2    3    4     5    6    7    8    9
    'chromatic-dorian': ['c', 'd', 'e', 'f', 'g+', 'a', 'b', 'c', 'd', 'd+', 'g'],
          'hypodorian': ['c', 'd', 'e', 'f+', 'g', 'a', 'b', 'c'],
              'dorian': ['c', 'd', 'e', 'f', 'g', 'a', 'b', 'c'],
}
beat_unit = 4  # we assume 4/4 or 3/4 rhythm
# Basic degrees (notes)
#        "YET"   :  "0",    # [C] yetiv / yetib (mahapakh early): TODO: 'early onset' implementation
#        "MEH"   :  "6",    # [C] mahapakh
#        "MUN"   :  "5",    # [B] munah / munakh / logarmeh
#        "ATN"   :  "4",    # [A] aetnachta ? atnakh
#        "TIP"   :  "3",    # [G] tipeha / tif'kha
#        "DEH"   :  "9",    # [G] dehi / tif'kha early
#        "MER"   :  "2",    # [F/F#] merkha
#        "MEK"   :  "22",   # [FF] merkha-kefula (double merkha)?
#        "SIL"   :  "1",    # [E] silluq / meteg / ga`ya
#  psa   "GAL"   :  "8",    # [D#] yerah-ben-yomo / galgal
#        "TEB"   :  "7,",   # [D,] tevir / tebir
#        "DAR"   :  "6,",   # [C,] darga -- FIXME
natur = ['do', 're', 'mi', 'fa', 'sol', 'la', 'ti', 'do']
sharp = ['di', 'ri', 'mi', 'fa', 'sol', 'la', 'ti', 'di']
flatt = ['ti', 'ra', 'me', 'mi', 'se', 'le', 'ta', 'de']


def decode_note(tla_note: str, cur_note: str, is_psalmodic=False, mode='chromatic-dorian'):
    # get numeric version of single note (tla) in the scale
    prev_cur_note = cur_note
    num_note = tiqwah2pattern(tla_note, is_psalmodic)
    cur_note = tiqwah2pattern(cur_note, is_psalmodic)  # can only be absolute
    notes = []
    if num_note == 'r':
        notes.append('r')
        cur_note = prev_cur_note
    elif len(num_note) == 1:
        notes.append(note_names[mode][int(num_note)])
    elif len(num_note) == 2:
        # we have only 1 or 2 character note units (i.e. 22)
        notes.append(note_names[mode][int(num_note[0])])
        notes.append(note_names[mode][int(num_note[1])])
    elif relative_note.search(num_note) is not None:
        # FIXME: do we need alternation of down or up arpeggios?
        # check for two options: [-4]|[+3]
        # break out individual note(s) '[+1+2+3]' or '[+0]' -> '+1','+2','+3' or '+0'
        for operation, step_note in dict(relative_note.findall(num_note)).items():
            # handle flat/sharp half step
            accidental = True if step_note == '%' else False
            step_note = 0 if step_note == '%' else step_note
            if operation == '+':
                half_step = '+' if accidental else ''
                rel_num_note = int(cur_note) + int(step_note)
                notes.append(note_names[mode][rel_num_note])
            elif operation == '-':
                half_step = '-' if accidental else ''
                rel_num_note = int(cur_note) - int(step_note)
                notes.append(f"{note_names[mode][rel_num_note]}{half_step}")
            else:
                print(f"error decoding relative note: {num_note}")

    else:
        # FIXME: always empty
        pass
        # print(f'* {tla_note} -> {num_note} *')

    return notes


def decode_syl(tla_note, rhythm, cur_note="<SIL>", is_psalmodic=False, mode='chromatic-dorian'):
    ''' decode Three-Letter Acronym (tla) notes (per-syllable) into musical notation'''
    # check for multiple notes per syllable
    note_tuples = []
    if ' ' in tla_note:
        subnotes = tla_note.split(" ")
        subrhythm = float(rhythm) * len(subnotes)
        for subnote in subnotes:
            (subnote_tuples, cur_note) = decode_syl(subnote, subrhythm, cur_note, is_psalmodic)
            note_tuples.append(subnote_tuples[0])
    else:
        note_rhythm = float(rhythm) * beat_unit
        musicses = decode_note(tla_note, cur_note, is_psalmodic)
        for note in musicses:
            note_tuples.append((note, note_rhythm))
    return (note_tuples, cur_note)


def decode_verse(syllables, is_psalmodic=False, cur_note="<SIL>") -> list:
    ''' decode a list of music beats (syllables) -- per-stanza?'''
    notes = []
    for syl in syllables:
        # print(f'syl: {syl}')
        (syl_music, cur_note) = decode_syl(syl['music'], syl['rhythm'], cur_note, is_psalmodic)
        for item in syl_music:
            notes.append(item)
        # print(f" {syl['music']} {syl['rhythm']} -> {syl_music}")
    return notes


def get_syllable(phrase: str) -> list:
    # remove rafe -- fricative indicator
    phrase = re.sub('<RAF>', '', phrase)

    # remove grammatical break
    phrase = re.sub('_', '', phrase)

    # break down by syllables, notes and ornaments
    #  the core vowel is the heart of the syllable
    # syllable = onset + rime(nucleus+[coda])
    vowels = core.findall(phrase)
    parts = core.split(phrase)
    syllables = []

    # each syllable has a vowel
    for vowel in vowels:
        syl = {'text': None, 'music': '', 'rhythm': 0, 'ipa': None}
        if '|' in vowel:
            syl['music'] = '<RST>'
            syl['rhythm'] = 2
            syllables.append(syl)
            continue
        # syllables have up to 3 parts... CV/CVC - Onset, Nucleus [,Coda]
        cur_onset = parts.pop(0)  # dequeue
        cur_nucleus = parts.pop(0)  # dequeue
        # 1: check if we have a closed syllable, last letter is a consonant
        cur_coda = parts.pop(0) if len(parts) == 1 and coda.match(parts[0]) else ''  # dequeue

        # 2: next letter is a semi-vowel ("y")
        tmp_vowel = ""
        if len(parts) > 0 and semivowel.search(parts[0]):
            (parts[0], tmp_matches) = strip_regex(parts[0], semivowel)
            tmp_vowel = tmp_matches.pop(0)  # we assume only one found

        # Break off music parts
        syl_music = []

        # check START of syllable
        (cur_onset, tmp_music) = strip_regex(cur_onset, music)
        for mcode in tmp_music:
            # convert back to textual trope (ta'am)
            syl_music.append(code2tiqwah(mcode))

        # check END of syllable
        (cur_coda, tmp_music) = strip_regex(cur_coda, music)
        for mcode in tmp_music:
            # convert back to textual trope (ta'am)
            syl_music.append(code2tiqwah(mcode))

        # add a music element if music data is present
        if len(syl_music) > 0:
            syl['music'] = " ".join(syl_music)
        else:
            syl['music'] = ''

        # add semi-vowel if present
        if len(tmp_vowel) > 0:
            cur_nucleus = cur_nucleus + tmp_vowel
        # stick C + V together
        syl['text'] = cur_onset + cur_nucleus + cur_coda

        # add music timing (shared between notes)
        syl['rhythm'] = 1
        if shortvowel.match(cur_nucleus) is not None:
            syl['rhythm'] = 0.5

        # TODO: add indicated rests
        # add end of line rest
        # if end_passage.match(syl['text']) is not None:
        #     line = ET.SubElement(song_root, "line")

        # insert a rest if indicated
        # if text_pause.search(syl['text']) is not None:
        #     print('PAUSE')

        # convert to fonetik ASCII
        syl['ipa'] = tiqwah2phonetic(syl['text'])
        syllables.append(syl)
    return syllables


def to_alda(note_tuples: list, rest: str='r4') -> str:
    """Convert note tuples to Alda music notation"""
    notes = [note + str(int(dur)) for note, dur in note_tuples]
    return ' '.join(notes) + f' {rest}\n'


def get_alda(input_iterable, output_file, column='text', is_psalmodic=False, instrument='midi-sitar', mode='chromatic-dorian', octave=3):
    """Convert Hebrew Bible text to Alda music notation"""
    output_file.write(f'{instrument}: o{octave} #mode: {mode}\n')
    meta = {}
    for verse in input_iterable:
        syllables = []
        if 'name' in verse.keys() and column not in verse.keys():
            meta = verse
            continue
        assert column in verse.keys(), f"No text '{column}' found in input: {verse}"

        # get the Haik-Vantoura intermediate version
        phrase = tiqwah2codes(verse[column])
        for word in phrase.split(' '):
            syl = get_syllable(word)
            # FIXME: add hyphenation to indicate word connections
            syllables.extend(syl)
        music = decode_verse(syllables, is_psalmodic)
        #print(syllables)
        #print(music)
        alda_text = to_alda(music)
        output_file.write(alda_text)
        output_file.write(f"# {verse[column]}\n")
        try:
            output_file.write(f"# {' '.join([t['text'] for t in syllables if t['text'] is not None])}\n")
            output_file.write(f"# {' '.join([t['ipa'] for t in syllables if t['ipa'] is not None])}\n")
        except Exception as e:
            print(f"Failed text: {e}")
            print(f"{syllables}")
        output_file.write("\n")


if __name__ == '__main__':
    class ModesAction(argparse.Action):
        def __init__(self, option_strings, dest, nargs=None, **kwargs):
            super(ModesAction, self).__init__(option_strings, dest, nargs=0, **kwargs)
        def __call__(self, parser, namespace, values, option_string=None):
            print(f"Available modes: {', '.join(note_names.keys())}")
            sys.exit(0)
    parser = argparse.ArgumentParser(description='Bible text music ala Haik-Vantoura')
    parser.add_argument('input_file_name', help="file to be processed")
    parser.add_argument('output_file_name', help="result file")
    parser.add_argument("-p", "--psalmodic", action="store_true", help="Use psalmody interpretation of notes", default=False)
    parser.add_argument("-i", "--instrument", default="midi-pan-flute", help="Alda/midi instrument for score")
    parser.add_argument("-o", "--octave", default=3, help="Octave for score")
    parser.add_argument("-m", "--mode", default='', help="Mode for score (default-prose: chromatic-dorian, default-psalm: dorian)")
    parser.add_argument("--modes", default=False, action=ModesAction, help="List available musical modes")
    parser.add_argument("--csv", action="store_true", default=False, help="Extract from CSV file")
    parser.add_argument("--data-column", default='text', help="Specify column for text extraction: default 'text'")
    args = parser.parse_args()
    mode = args.mode if args.mode else 'dorian' if args.psalmodic else 'chromatic-dorian'
    if mode not in note_names.keys():
        print(f"ERROR: mode '{mode}' is not available")
        sys.exit(1)
    input_file = codecs.open(args.input_file_name, 'r', encoding='utf-8')
    output_file = codecs.open(args.output_file_name, 'w+', encoding='utf-8')
    print(f"Processing from column '{args.data_column}' of file: {args.input_file_name}")
    column = args.data_column
    if args.csv:
        delim = '\t' if args.input_file_name.endswith('.tsv') else ','
        data_reader = csv.DictReader(input_file, delimiter=delim)
        get_alda(data_reader, output_file, column, args.psalmodic, args.instrument, mode, args.octave)
    else:
        data = [json.loads(data) for data in input_file.readlines()]
        print(f"Processing {len(data)-1} rows of data")
        get_alda(data, output_file, column, args.psalmodic, args.instrument, mode, args.octave)
    
    input_file.close()
    output_file.close()
