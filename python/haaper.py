#!/usr/bin/env python
# Filename: haaper.py

version = 0.3
import re
import sys
import codecs
from collections import UserDict
import argparse

# single-pass multiple string substitution using a dictionary:
# by Xavier Defrang
# from code.activestate.com/recipes/81330/
#
# You may combine both the dictionnary and search-and-replace
# into a single object using a 'callable' dictionary wrapper
# which can be directly used as a callback object.
# released under Python Software Foundation License

class Xlator(UserDict):
    """ An all-in-one multiple string substitution class """

    def _make_regex(self):
        ''' Build a regular expression object
         based on the keys of the current dictionary sorted by length'''
        keys = sorted(self.keys(), key=len, reverse=True)
        return re.compile("(%s)" % "|".join(map(re.escape, keys)))

    def __call__(self, mo):
        ''' This handler will be invoked for each regex match '''
        # Count substitutions
        self.count += 1  # Look-up string

        return self[mo.string[mo.start():mo.end()]]

    def xlat(self, text):
        ''' Translate text, returns the modified text. '''
        # Reset substitution counter
        self.count = 0

        # Process text
        return self._make_regex().sub(self, text)

# End of Xlator

# Unicode Hebrew characters (UTF-16)
#  From Unicode Hebrew, Version 5.0.

# special Unicode stuff
WOJ = "\u206D"   # Word Joiner (WJ)
ZWJ = "\u200D"   # Zero-Width Joiner (ZWJ)
ZWNJ = "\u200C"  # Zero-Width Non-Joiner (ZWJ)
ZWS = "\u200B"   # Zero-Width Space (ZWS)
CGJ = "\u034F"   # Combining Grapheme Joiner
SPC = "\u0020"   # Space
SHY = "\u00AD"   # Soft-hyphen (SHY)
NHY = "\u00AD"   # Non-breaking Hyphen (NHY)

# https://www.oxygenxml.com/doc/versions/25.0/ug-editor/topics/control-text-direction-dfc.html
LRM = "\u200E"   # Left to right mark (zero-width) single "word"
RLM = "\u200F"   # Right To Left mark (zero-width) single "word"
LRE = "\u202A"   # Left to right embedding (following text)
RLE = "\u202B"   # Right To Left embedding (following text)
PDF = "\u202C"   # Return to normal Bidirectional text mode (pop directional formatting)
LRO = "\u202D"   # Left To Right override
RLO = "\u202E"   # Right To Left override

# Letters"  = Consonants
tiqwah2unicode_dict = {
    r"'": "\u05d0",   # aleph
    r"b": "\u05d1",   # bet / vet
    r"g": "\u05d2",   # gimel
    r"d": "\u05d3",   # daleth
    r"h": "\u05d4",   # hey
    r"w": "\u05d5",   # vav / waw
    r"z": "\u05d6",   # zayin
    r"x": "\u05d7",   # khet
    r"T": "\u05d8",   # tet
    r"y": "\u05d9",   # yodh / yud
    r"k$": "\u05dA",  # final kaf-sofit
    r"k": "\u05dB",   # kaf / kaph
    r"l": "\u05dC",   # lamedh
    r"m$": "\u05dD",  # final mem-sofit
    r"m": "\u05dE",   # mem
    r"n$": "\u05dF",  # final nun-sofit
    r"n": "\u05e0",   # nun
    r"s": "\u05e1",   # samekh
    r"\`": "\u05e2",  # ayin
    r"p$": "\u05e3",  # final pe-sofit
    r"p": "\u05e4",   # peh / pey
    r"Y$": "\u05e5",  # final tsadi-sofit
    r"Y": "\u05e6",   # tsadi
    r"q": "\u05e7",   # quf / qof
    r"r": "\u05e8",   # resh
    r"S": "\u05e9\u05c1",  # shin w/dot
    r"W": "\u05e9\u05c2",  # sin w/dot
    r"W/": "\u05e9",  # shin no dot
    r"t": "\u05eA",   # taf / tav

    # Points and punctuation
    r'"': "\u05b0",      # sh'va / shewa (schwa)
    r"{SWA}": "\u05b0",  # sh'va / shewa (schwa)
    r"@": "\u05b0",      # sh'va / shewa (schwa)
    r"{HSE}": "\u05b1",  # hateph-segol
    r"{HPA}": "\u05b2",  # hateph-patakh
    r"{HQA}": "\u05b3",  # hateph-qamats
    r"i": "\u05b4",      # hiriq
    r"{HIR}": "\u05b4",  # hiriq
    r"e": "\u05b5",      # tsere
    r"{SER}": "\u05b5",  # tsere
    r"E": "\u05b6",      # segol
    r"{SEG}": "\u05b6",  # segol
    r"a": "\u05b7",      # patakh
    r"{PAT}": "\u05b7",  # patakh
    r"A": "\u05b8",      # qamats
    r"{QAM}": "\u05b8",  # qamats
    r"o": "\u05b9",      # holam
    r"{HOL}": "\u05b9",  # holam
    r"w^o": "\u05ba",    # holam haser (Unicode 5.0)
    #    r"w^o":      "\u05ba\u05d5",  # holam haser (Unicode 4.1)
    r"u": "\u05bb",      # qubuts / qibbuts
    r"{QIB}": "\u05bb",  # qubuts / qibbuts
    r"*": "\u05bc",      # dagesh
    r"{DAGESH}": "\u05bc",  # dagesh / BeGaD KeFaT ??
    r"{SIL}": "\u05bd",  # meteg -- encode as silluq
    r"=": "\u05be",      # maqaf / maqqeph
    r"{RAF}": "\u05bf",  # rafe
    r"{LIN}": "\u05c0",  # paseq / lineola
    r":": "\u05c3",      # sof pasuq
    r"{upperdot}": "\u05c4",  # upper dot
    r"{lowerdot}": "\u05c5",  # lower dot
    r"n/": "\u05c6",     # reversed nun / nun hafukha
    r"n//": "\u05e0",    # raised-nun (hafukh) -- not supported, convert to regular
    r"{PCR}": "\u0307",  # punctum-extraordinarium / circellus/masora-number-dot

    # Accents
    "{ATN}": "\u0591",  # aetnakhta / atnakh
    "{AST}": "\u0592",  # accent segol
    "{SHP}": "\u0593",  # shalshelet
    "{ZQP}": "\u0594",  # zaqef katan
    "{ZQM}": "\u0595",  # zaqef gadol
    "{TIP}": "\u0596",  # tipeha / tif'kha
    "{RBM}": "\u0597",  # revia (magnum) / gadol
    "{ZAR}": "\u0598",  # zarqa / (t)zinor ??
    "{PAS}": "\u0599",  # pashta
    "{YET}": "\u059a",  # yetiv / yetib
    "{TEB}": "\u059b",  # tevir / tebir
    "{GER}": "\u059c",  # geresh
    "{GRM}": "\u059d",  # geresh-muqdam ?? -- add
    "{GAR}": "\u059e",  # gershayim
    "{PZM}": "\u059f",  # qarney-para / pazer gadol (magnum)
    "{TLM}": "\u05a0",  # telisha-gedola (magnum)
    "{PAZ}": "\u05a1",  # pazer
    "{ATH}": "\u05a2",  # atnakh hafukh (Unicode 4.1) / yerah-ben-yomo / galgal
    "{MUN}": "\u05a3",  # munah
    "{MEH}": "\u05a4",  # mahapakh
    "{MER}": "\u05a5",  # merkha
    "{MEK}": "\u05a6",  # merkha-kefula
    "{DAR}": "\u05a7",  # darga
    "{AZL}": "\u05a8",  # azla / qadma
    "{TLP}": "\u05a9",  # telisha-qetana (parvum)
    "{GAL}": "\u05aa",  # yerah-ben-yomo / galgal
    "{OLE}": "\u05ab",  # ole / we-yored
    "{ILL}": "\u05ac",  # iluy
    "{DEH}": "\u05ad",  # dehi
    "{ZIN}": "\u05ae",  # tzinor == zarqa??
    "{CIR}": "\u05af",  # masora-circle / circellus?

    # Yiddish ligatures just in case...
    "ww": "\u05f0",     # double-vav
    "wy": "\u05f1",     # vav-yod
    "yy": "\u05f2",     # double-yod

    # Added punctuation
    r"!": "\u05f3",      # punctuation-geresh ( ' )
    r"!!": "\u05f4",     # punctuation-gershayim ( '' )
    r"{MUL}": '\xd7'     # multiplication symbol &times;
}


# Letters"  = Consonants
unicode2tiqwah_dict = {
    "\u05d0": "'",  # aleph
    "\u05d1": "b",  # bet
    "\u05d2": "g",  # gimel
    "\u05d3": "d",  # dalet
    "\u05d4": "h",  # hey
    "\u05d5": "w",  # waw / vav
    "\u05d6": "z",  # zayin
    "\u05d7": "x",  # khet
    "\u05d8": "T",  # tet
    "\u05d9": "y",  # yud
    "\u05dA": "k",  # final-kaf
    "\u05dB": "k",  # kaf
    "\u05dC": "l",  # lamed
    "\u05dD": "m",  # final-mem
    "\u05dE": "m",  # mem
    "\u05dF": "n",  # final-nun
    "\u05e0": "n",  # nun
    "\u05e1": "s",  # samekh
    "\u05e2": "`",  # ayin
    "\u05e3": "p",  # final-pe
    "\u05e4": "p",  # pe
    "\u05e5": "Y",  # final-tsadi
    "\u05e6": "Y",  # tsadi
    "\u05e7": "q",  # quf
    "\u05e8": "r",  # resh
    "\u05e9\u05c1": "S",  # shin w/dot
    "\u05e9\u05c2": "W",  # sin  w/dot
    "\u05e9": "W/",  # shin / no dot
    "\u05ea": "t",   # tav
    "\ufb4f": "'/l",  # aleph-lamed ligature

    # combined
    "\ufb40": "n*",  # nun with dagesh
    "\ufb30": "'*",  # aleph with dagesh
    "\ufb31": "b*",  # bet with dagesh
    "\ufb32": "g*",  # aleph with dagesh
    "\ufb33": "d*",  # aleph with dagesh
    "\ufb34": "h*",  # hey with dagesh
    "\ufb35": "w*",  # waw / vav with dagesh
    "\ufb36": "z*",  # zayin with dagesh
    "\ufb38": "T*",  # tet with dagesh
    "\ufb39": "y*",  # yud with dagesh
    "\ufb3a": "k*",  # final-kaf with dagesh
    "\ufb3b": "k*",  # kaf with dagesh
    "\ufb3c": "l*",  # lamed with dagesh
    #"\ufb3e": "m*",  # final-mem with dagesh
    "\ufb3e": "m*",  # mem with dagesh
    #"\ufb40": "n*",  # final-nun with dagesh
    "\ufb40": "n*",  # nun with dagesh
    "\ufb43": "p*",  # final-pe with dagesh
    "\ufb44": "p*",  # pe with dagesh
    #"\ufb40": "Y*",  # final-tsadi with dagesh
    "\ufb46": "Y*",  # tsadi with dagesh
    "\ufb47": "q*",  # quf with dagesh
    "\ufb48": "r*",  # resh with dagesh
    "\ufb49\u05c1": "S*",  # shin w/dot with dagesh
    "\ufb49\u05c2": "W*",  # sin  w/dot with dagesh
    "\ufb49": "W/*",  # shin / no dot with dagesh
    "\ufb4a": "t*",   # tav with dagesh
    

    # Points and punctuation
    "/": '_',  # gramatic-word break (and/of/in/possessive)
    # "\u05b0": '{SWA}',  # sh'va / shewa (schwa)
    "\u05b0": '@',      # sh'va / shewa (schwa)
    "\u05b1": "{HSE}",  # hateph-segol  '"E' (sh'va-E)
    "\u05b2": "{HPA}",  # hateph-patakh '"a' (sh'va-a)
    "\u05b3": "{HQA}",  # hateph-qamats '"A' (sh'va-A)
    "\u05b4": 'i',      # hiriq
    # "\u05b4": "{HIR}",  # hiriq
    "\u05b5": 'e',      # tsere
    # "\u05b5": "{SER}",  # tsere
    "\u05b6": 'E',      # segol
    # "\u05b6": "{SEG}",  # segol
    "\u05b7": 'a',      # patakh
    # "\u05b7": "{PAT}",  # patakh
    "\u05b8": 'A',      # qamats
    # "\u05b8": "{QAM}",  # qamats
    "\u05b9": 'o',      # holam
    # "\u05b9": "{HOL}",  # holam
    "\u05ba": "w^o",    # holam haser (Unicode 5.0)
    "\u05d5\u05b9": "w^o",    # holam haser (Unicode 4.1)
    "\u05bb": "u",      # qubuts / qibbuts
    #  "\u05bb": "{QIB}",  # qubuts / qibbuts
    "\u05bc": "*",      # dagesh / mapiq / shuruq
    # "\u05bc": "{DAGESH}",  # dagesh
    "\u05bd": "{SIL}",  # meteg -- encode as silluq
    "\u05be": "=",      # maqaf / maqqeph
    "\u05bf": "{RAF}",  # rafe
    # "\u05bc": "{LIN}",  # lineola / paseq
    "\u05c0": "|",      # lineola / paseq
    "\u05c1": ".",      # shin-dot
    "\u05c3": ":",      # sof pasuq
    "\u05c4": "{UPPERDOT}",  # upper dot
    "\u05c5": "{LOWERDOT}",  # lower dot
    "\u05c6": "n/",     # reversed nun (hafukha) - punctuation Numbers 10:35–36
    # "\u05e0": "n//",  # raised nun ()
    "\u0307": "{PCR}",  # punctum-extraordinarium / circellus/masora-number-dot

    # Accents
    "\u0591": "{ATN}",  # aetnachta ? atnakh
    "\u0592": "{AST}",  # accent-segol ??
    "\u0593": "{SHP}",  # shalshelet
    "\u0594": "{ZQP}",  # zaqef-qatan (parvum)
    "\u0595": "{ZQM}",  # zaqef-gadol (magnum)
    "\u0596": "{TIP}",  # tipeha / tif'kha
    "\u0597": "{RBM}",  # revia (magnum) / gadol
    "\u0598": "{ZAR}",  # zarqa / (t)zinor ??
    "\u0599": "{PAS}",  # pashta
    "\u059a": "{YET}",  # yetiv / yetib
    "\u059b": "{TEB}",  # tevir / tebir
    "\u059c": "{GER}",  # geresh
    "\u059d": "{GRM}",  # geresh-muqdam ??
    "\u059e": "{GAR}",  # gershayim
    "\u059f": "{PZM}",  # qarney-para / pazer gadol (magnum)
    "\u05a0": "{TLM}",  # telisha-gedola (magnum)
    "\u05a1": "{PAZ}",  # pazer
    "\u05a2": "{GAL}",  # atnakh hafukh (Unicode 4.0) / yerah-ben-yomo / galgal
    # "\u05a2": "{ATH}",  # atnakh hafukh (Unicode 4.1) / yerah-ben-yomo/galgal
    "\u05a3": "{MUN}",  # munah
    "\u05a4": "{MEH}",  # mahapakh
    "\u05a5": "{MER}",  # merkha
    "\u05a6": "{MEK}",  # merkha-kefula
    "\u05a7": "{DAR}",  # darga
    "\u05a8": "{AZL}",  # azla / qadma
    "\u05a9": "{TLP}",  # telisha-qetana (parvum)
    "\u05aa": "{GAL}",  # yerah-ben-yomo / galgal
    "\u05ab": "{OLE}",  # ole / we-yored
    "\u05ac": "{ILL}",  # iluy
    "\u05ad": "{DEH}",  # dehi
    "\u05ae": "{ZIN}",  # tzinor == zarqa?

    "\u05af": "{CIR}",  # masora-circle / circellus?

    # Yiddish ligatures just in case...
    "\u05ef": "yyy",    # yod triangle
    "\u05f0": "ww",    # double-vav
    "\u05f1": "wy",    # vav-yod
    "\u05f2": "yy",    # double-yod

    # Added punctuation
    "\u05f3": "!",     # punctuation-geresh ( ' )
    "\u05f4": "!!",    # punctuation-gershayim ( '' )
    '\xd7': "{MUL}"    # multiplication symbol &times;
}

# SAMPA for Hebrew
# description: SAMPA for Hebrew, an ASCII representation of phonetic symbols
# for Hebrew w^o =} o
# http://www.phon.ucl.ac.uk/home/sampa/hebrew.htm
# Established by initiative of the http://www.orientel.org -OrienTel project
# Maintained by j.wells@phon.ucl.ac.uk - J.C. Wells - Created 2002-07-12
tiqwah2SAMPA_dict = {
    # Consonants
    #   Plosives
    "p*": "p",  # peh
    "b*": "b",  # beit
    "t*": "t",  # tav
    "T": "t",  # tet
    "d": "d",  # dhalet
    "d*": "d",  # dalet
    "k*": "k",  # kaf
    "q": "k",  # quf
    "q*": "k",  # quf w/dagesh?
    "g": "g",  # gimel
    "g*": "g",  # gimel-dagesh
    # "\"" :  "?",  # sh`va
    "\"": "@",  # sh`va
    # "_": "",  # grammatic word-break
    # "\'": "@",  # aleph
    "'": "",  # aleph
    # "`": "@",  # ayin
    "`": "",  # ayin

    #   Fricatives
    "p": "f",  # phe
    "b": "v",  # veit
    "w": "v",  # waw
    "W": "s",  # sin
    "W*": "s",  # sin w/dagesh
    "W/": "s",  # sin w/out dot
    "s": "s",  # samekh
    "z": "z",  # zayin
    "S": "S",  # shin
    "S*": "S",  # shin w/dagesh
    "x": "X",  # khet
    "k": "X",  # khaf
    "h": "h",  # hey
    "{RAF}": "",  # raphe -- indicates fricative

    #   Affricate
    # "Y": "ts",  # tsadi
    "Y": "Z",  # tsadi

    #   Nasals
    "m": "m",  # mem
    "m*": "m",  # mem-dagesh
    "n": "n",  # nun
    "n*": "n",  # nun-dagesh

    #   Liquids
    "l": "l",  # lamed
    "l*": "l",  # lamed-dagesh
    "r": "R",  # resh

    #   Semi-vowel
    # "y": "j",
    "y": "y",
    "y*": "y",  # yud w/dagesh

    #   Vowels
    "i": "i",
    "e": "e",
    "E": "e",
    "{HSE}": "e",  # hateph-segol sh'va-E
    "a": "a",
    "A": "a",
    "{HPA}": "a",  # hateph-patakh sh'va-a
    "{HQA}": "a",  # hateph-qamats sh'va-A
    "o": "o",
    "w^o": "o",  # holam-haser
    "u": "u",
    "w*": "u",  # holam-waw?

    #   common strange cases
    "kal=": "kol-",  # holam-waw?

    # Rare, dialectal or marginal phonemes
    #    "": "Z",
    #    "": "X\\",
    #    "": "tS",
    #    "": "dZ",
    #    "": "?\\",

    # Stress mark
    "\$": "\""
}


def custom2xlat(custom_text: str, match_dict: dict, rtl=False) -> str:
    """ convert from a custom format based on a regex dict"""
    xlator = Xlator(match_dict)
    xlat_text = xlator.xlat(custom_text)
    if rtl:
        return f"{RLM}{xlat_text}{PDF}"
    else:
        return xlat_text


def unicode2tiqwah(hebrew_unicode):
    xlator = Xlator(unicode2tiqwah_dict)
    tiqwah_text = xlator.xlat(hebrew_unicode)
    # remove text direction markers (because output is plain ASCII)
    text_direction_marker = fr"{LRM}|{RLM}|{LRE}|{RLE}|{LRO}|{RLO}|{PDF}"
    tiqwah_text = re.sub(text_direction_marker, '', tiqwah_text)
    return tiqwah_text


def tiqwah2unicode(hebrew_tiqwah):
    xlator = Xlator(tiqwah2unicode_dict)
    unicode_text = xlator.xlat(hebrew_tiqwah)
    return f"{RLM}{unicode_text}{PDF}"


def tiqwah2phonetic(hebrew_tiqwah):
    xlator = Xlator(tiqwah2SAMPA_dict)
    sampa_text = xlator.xlat(hebrew_tiqwah)
    return sampa_text


def main(input_file, output_file, mode='tiqwah'):
    input_file = codecs.open(args.input_file_name, 'r', encoding='utf-8')
    output_file = codecs.open(args.output_file_name, 'w+', encoding='utf-8')

    for line in input_file:
        line = line.rstrip('\n')
        if 'sampa' == mode:
            output_file.write(tiqwah2phonetic(line) + '\n')
        elif 'unicode' == mode:
            output_file.write(unicode2tiqwah(line) + '\n')
        else:
            output_file.write(tiqwah2unicode(line) + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='haaper: Convert one Hebrew encoding to another')
    parser.add_argument("-t", "--tiqwah", "--tiqwah2unicode", action="store_true",
                        help="Convert Tiqwah format to Unicode Hebrew (default)", default=True)
    parser.add_argument("-u", "--unicode", "--unicode2tiqwah", action="store_true",
                        help="Convert Unicode Hebrew to Tiqwah ASCII", default=False)
    parser.add_argument("-s", "--sampa", "--tiqwah2sampa", action="store_true",
                        help="Convert Tiqwah ASCII to SAMPA phonetic ASCII", default=False)
    parser.add_argument('input_file_name',
                        help="file to be processed")
    parser.add_argument('output_file_name',
                        help="result file")
    args = parser.parse_args()
    mode = 'tiqwah'
    if args.unicode:
        mode = 'unicode'
    elif args.sampa:
        mode = 'sampa'
    main(args.input_file_name, args.output_file_name, mode)
# End of haaper.py
