#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: haaper.py

version = 0.2
import re 
import sys
import codecs
import argparse

# single-pass multiple string substitution using a dictionary:
# by Xavier Defrang
# from code.activestate.com/recipes/81330/
#
# You may combine both the dictionnary and search-and-replace
# into a single object using a 'callable' dictionary wrapper
# which can be directly used as a callback object.
# released under Python Software Foundation License

# In Python 2.2+ you may extend the 'dictionary' built-in class
from UserDict import UserDict 
class Xlator(UserDict):

  """ An all-in-one multiple string substitution class """ 

  def _make_regex(self): 

    """ Build a regular expression object 
     based on the keys of the current dictionary sorted by length"""
    keys = self.keys()
    keys.sort(lambda a,b: len(b)-len(a))
    return re.compile("(%s)" % "|".join(map(re.escape, keys))) 

  def __call__(self, mo): 
    
    """ This handler will be invoked for each regex match """

    # Count substitutions
    self.count += 1 # Look-up string

    return self[mo.string[mo.start():mo.end()]]

  def xlat(self, text): 

    """ Translate text, returns the modified text. """ 

    # Reset substitution counter
    self.count = 0 

    # Process text
    return self._make_regex().sub(self, text)

# End of Xlator

# Unicode Hebrew characters (UTF-16)
#  From Unicode Hebrew, Version 5.0.

# special Unicode stuff
WOJ =  u"\u206D"  # Word Joiner (WJ)
ZWJ =  u"\u200D"  # Zero-Width Joiner (ZWJ)
ZWNJ = u"\u200C"  # Zero-Width Non-Joiner (ZWJ)
ZWS =  u"\u200B"  # Zero-Width Space (ZWS)
CGJ =  u"\u034F"  # Combining Grapheme Joiner
SPC =  u"\u0020"  # Space
SHY =  u"\u00AD"  # Soft-hyphen (shy)
NHY =  u"\u00AD"  # Non-breaking Hyphen (shy)

RTL = u"\u203D"   # Right To Left marker
LTR = u"\u202D"   # Right To Left marker
BDI = u"\u202C"   # Return to Normal Bi-Di text mode

# Letters"  = Consonants
tiqwah2unicode_dict = {
	"'"  :       u"\u05d0", # aleph
	"b"  :       u"\u05d1", # bet / vet
	"g"  :       u"\u05d2", # gimel
	"d"  :       u"\u05d3", # daleth
	"h"  :       u"\u05d4", # hey
	"w"  :       u"\u05d5", # vav / waw
	"z"  :       u"\u05d6", # zayin
	"x"  :       u"\u05d7", # khet
	"T"  :       u"\u05d8", # tet
	"y"  :       u"\u05d9", # yodh / yud
	"k$":        u"\u05dA", # final kaf-sofit 
	"k"  :       u"\u05dB", # kaf / kaph
	"l"  :       u"\u05dC", # lamedh
	"m$":        u"\u05dD", # final mem-sofit 
	"m"  :       u"\u05dE", # mem
	"n$":        u"\u05dF", # final nun-sofit 
	"n"  :       u"\u05e0", # nun
	"s"  :       u"\u05e1", # samekh
	"\`" :       u"\u05e2", # ayin
	"p$":        u"\u05e3", # final pe-sofit 
	"p"  :       u"\u05e4", # peh / pey
	"Y$":        u"\u05e5", # final tsadi-sofit
	"Y"  :       u"\u05e6", # tsadi
	"q"  :       u"\u05e7", # quf / qof
	"r"  :       u"\u05e8", # resh
	"S"  :       u"\u05e9\u05c1", # shin w/dot
	"W"  :       u"\u05e9\u05c2", # sin w/dot
	"W/" :       u"\u05e9", # shin no dot
	"t"  :       u"\u05eA", # taf / tav

# Points and punctuation
	'"'     :      u"\u05b0", # sh'va / shewa (schwa)
	"{SWA}" :      u"\u05b0", # sh'va / shewa (schwa)
	"@"     :      u"\u05b0", # sh'va / shewa (schwa)
	"{HSE}" :      u"\u05b1", # hateph-segol
	"{HPA}" :      u"\u05b2", # hateph-patakh
	"{HQA}" :      u"\u05b3", # hateph-qamats
	"i"     :      u"\u05b4", # hiriq
	"{HIR}" :      u"\u05b4", # hiriq
	"e"     :      u"\u05b5", # tsere
	"{SER}" :      u"\u05b5", # tsere
	"E"     :      u"\u05b6", # segol
	"{SEG}" :      u"\u05b6", # segol
	"a"     :      u"\u05b7", # patakh
	"{PAT}" :      u"\u05b7", # patakh
	"A"     :      u"\u05b8", # qamats
	"{QAM}" :      u"\u05b8", # qamats
	"o"     :      u"\u05b9", # holam
	"{HOL}" :      u"\u05b9", # holam
	"w^o"   :      u"\u05ba", # holam haser (Unicode 5.0)
#	"w^o"   :      u"\u05ba\u05d5", # holam haser (Unicode 4.1)
	"u"     :      u"\u05bb", # qubuts / qibbuts
	"{QIB}" :      u"\u05bb", # qubuts / qibbuts
	"*"     :      u"\u05bc", # dagesh
	"{DAGESH}" :   u"\u05bc", # dagesh / BeGaD KeFaT ??
	"{SIL}" :      u"\u05bd", # meteg -- encode as silluq
	"="     :      u"\u05be", # maqaf / maqqeph
	"{RAF}" :      u"\u05bf", # rafe
	"{LIN}" :      u"\u05c0", # paseq / lineola
	":"     :      u"\u05c3", # sof pasuq
	"upperdot" :   u"\u05c4", # upper dot
	"lowerdot" :   u"\u05c5", # lower dot
	"n/"    :      u"\u05c6", # reversed nun
	"n//"   :      u"\u05e0", # raised nun () -- not supported, convert to regular
	"{PCR}" :      u"\u0307", # punctum-extraordinarium / circellus / masora-number-dot

	"{SET}" :      "<SAMEKH/>", # parsha marker Setuma
	"{PET}" :      "<PEH/>",    # parsha marker Petukha
	"{SHI}" :      "<SHIN/>",   # parsha marker Shir?

# Accents
	"{ATN}" :      u"\u0591", # aetnakhta / atnakh
	"{AST}" :      u"\u0592", # accent segol
	"{SHP}" :      u"\u0593", # shalshelet
	"{ZQP}" :      u"\u0594", # zaqef katan
	"{ZQM}" :      u"\u0595", # zaqef gadol
	"{TIP}" :      u"\u0596", # tipeha / tif'kha
	"{RBM}" :      u"\u0597", # revia (magnum) / gadol
	"{ZAR}" :      u"\u0598", # zarqa / (t)zinor ??
	"{PAS}" :      u"\u0599", # pashta
	"{YET}" :      u"\u059a", # yetiv / yetib
	"{TEB}" :      u"\u059b", # tevir / tebir
	"{GER}" :      u"\u059c", # geresh
	"{GRM}" :      u"\u059d", # geresh-muqdam ?? -- add
	"{GAR}" :      u"\u059e", # gershayim
	"{PZM}" :      u"\u059f", # qarney-para / pazer gadol (magnum)
	"{TLM}" :      u"\u05a0", # telisha-gedola (magnum)
	"{PAZ}" :      u"\u05a1", # pazer
	"{ATH}" :      u"\u05a2", # atnakh hafukh (Unicode 4.1) / yerah-ben-yomo / galgal
	"{MUN}" :      u"\u05a3", # munah
	"{MEH}" :      u"\u05a4", # mahapakh
	"{MER}" :      u"\u05a5", # merkha
	"{MEK}" :      u"\u05a6", # merkha-kefula
	"{DAR}" :      u"\u05a7", # darga
	"{AZL}" :      u"\u05a8", # azla / qadma
	"{TLP}" :      u"\u05a9", # telisha-qetana (parvum)
	"{GAL}" :      u"\u05aa", # yerah-ben-yomo / galgal
	"{OLE}" :      u"\u05ab", # ole / we-yored
	"{ILL}" :      u"\u05ac", # iluy
	"{DEH}" :      u"\u05ad", # dehi
	"{ZIN}" :      u"\u05ae", # tzinor == zarqa??
	"{CIR}" :      u"\u05af", # masora-circle / circellus?

# Yiddish ligatures just in case...
	"ww"    :      u"\u05f0", # double-vav
	"wy"    :      u"\u05f1", # vav-yod
	"yy"    :      u"\u05f2", # double-yod

# Added punctuation
	"!"     :      u"\u05f3", # punctuation-geresh ( ' )
	"!!"    :      u"\u05f4", # punctuation-gershayim ( '' )
	"{MUL}" :      u'\xd7'  # multiplication symbol &times;
}


# Letters"  = Consonants
unicode2tiqwah_dict = {
	u"\u05d0"   :   "'",  # aleph
	u"\u05d1"   :   "b",  # bet    
	u"\u05d2"   :   "g",  # gimel    
	u"\u05d3"   :   "d",  # dalet    
	u"\u05d4"   :   "h",  # hey    
	u"\u05d5"   :   "w",  # waw / vav    
	u"\u05d6"   :   "z",  # zayin    
	u"\u05d7"   :   "x",  # khet
	u"\u05d8"   :   "T",  # tet
	u"\u05d9"   :   "y",  # yud    
	u"\u05dA"   :   "k",  # final-kaf
	u"\u05dB"   :   "k",  # kaf    
	u"\u05dC"   :   "l",  # lamed    
	u"\u05dD"   :   "m",  # final-mem
	u"\u05dE"   :   "m",  # mem    
	u"\u05dF"   :   "n",  # final-nun
	u"\u05e0"   :   "n",  # nun    
	u"\u05e1"   :   "s",  # samekh    
	u"\u05e2"   :   "`",  # ayin
	u"\u05e3"   :   "p",  # final-pe 
	u"\u05e4"   :   "p",  # pe
	u"\u05e5"   :   "Y",  # final-tsadi
	u"\u05e6"   :   "Y",  # tsadi
	u"\u05e7"   :   "q",  # quf    
	u"\u05e8"   :   "r",  # resh    
	u"\u05e9\u05c1": "S", # shin w/dot
	u"\u05e9\u05c2": "W", # sin  w/dot
	u"\u05e9"   :    "W/", # shin / no dot
	u"\u05eA"   :    "t", # tav    
	u"\ufb4f"   :  "'/l", # aleph-lamed ligature

# Points and punctuation

	"/"         :       '_',      # gramatic-word break (and/of/in/possessive)
#	u"\u05b0"   :       '{SWA}',  # sh'va / shewa (schwa)
	u"\u05b0"   :       '@',      # sh'va / shewa (schwa)
	u"\u05b1"   :       '{HSE}',  # hateph-segol  '"E' (sh'va-E)
	u"\u05b2"   :       '{HPA}',  # hateph-patakh '"a' (sh'va-a)
	u"\u05b3"   :       '{HQA}',  # hateph-qamats '"A' (sh'va-A)
	u"\u05b4"   :       'i',      # hiriq
#	u"\u05b4"   :       "{HIR}",  # hiriq
	u"\u05b5"   :       'e',      # tsere
#	u"\u05b5"   :       "{SER}",  # tsere
	u"\u05b6"   :       'E',      # segol
#	u"\u05b6"   :       "{SEG}",  # segol
	u"\u05b7"   :       'a',      # patakh
#	u"\u05b7"   :       "{PAT}",  # patakh
	u"\u05b8"   :       'A',      # qamats
#	u"\u05b8"   :       "{QAM}",  # qamats
	u"\u05b9"   :       'o',      # holam
#	u"\u05b9"   :       "{HOL}",  # holam
	u"\u05ba"   :       "w^o",    # holam haser (Unicode 5.0)
	u"\u05d5\u05b9"  :  "w^o",    # holam haser (Unicode 4.1)
	u"\u05bb"   :       "u",      # qubuts / qibbuts
#	u"\u05bb"   :       "{QIB}",  # qubuts / qibbuts
	u"\u05bc"   :       "*",      # dagesh / mapiq / shuruq
#	u"\u05bc"   :       "{DAGESH}", # dagesh
	u"\u05bd"   :       "{SIL}",  # meteg -- encode as silluq
	u"\u05be"   :       "=",      # maqaf / maqqeph
	u"\u05bf"   :       "{RAF}",  # rafe
#	u"\u05bc"   :       "{LIN}",  # lineola / paseq
	u"\u05c0"   :       "|",      # lineola / paseq
	u"\u05c1"   :       ".",      # shin-dot
	u"\u05c3"   :       ":",      # sof pasuq
	u"\u05c4"   :       "upper-dot", # upper dot
	u"\u05c5"   :       "lower-dot", # lower dot
	u"\u05c6"   :  	    "n/",     # reversed nun (hafukha) - punctuation Numbers 10:35–36
#	u"\u05e0"   :  	    "n//",    # raised nun ()
	u"\u0307"   :       "{PCR}",  # punctum-extraordinarium / circellus / masora-number-dot

# Accents
	u"\u0591"   :       "{ATN}",  # aetnachta ? atnakh
	u"\u0592"   :       "{AST}",  # accent-segol ??
	u"\u0593"   :       "{SHP}",  # shalshelet
	u"\u0594"   :       "{ZQP}",  # zaqef-qatan (parvum)
	u"\u0595"   :       "{ZQM}",  # zaqef-gadol (magnum)
	u"\u0596"   :       "{TIP}",  # tipeha / tif'kha
	u"\u0597"   :       "{RBM}",  # revia (magnum) / gadol
	u"\u0598"   :       "{ZAR}",  # zarqa / (t)zinor ??
	u"\u0599"   :       "{PAS}",  # pashta
	u"\u059a"   :       "{YET}",  # yetiv / yetib
	u"\u059b"   :       "{TEB}",  # tevir / tebir
	u"\u059c"   :       "{GER}",  # geresh
	u"\u059d"   :       "{GRM}",  # geresh-muqdam ??
	u"\u059e"   :       "{GAR}",  # gershayim
	u"\u059f"   :       "{PZM}",  # qarney-para / pazer gadol (magnum)
	u"\u05a0"   :       "{TLM}",  # telisha-gedola (magnum)
	u"\u05a1"   :       "{PAZ}",  # pazer
	u"\u05a2"   :       "{GAL}",  # atnakh hafukh (Unicode 4.0) / yerah-ben-yomo / galgal
#	u"\u05a2"   :       "{ATH}",  # atnakh hafukh (Unicode 4.1) / yerah-ben-yomo / galgal
	u"\u05a3"   :       "{MUN}",  # munah
	u"\u05a4"   :       "{MEH}",  # mahapakh
	u"\u05a5"   :       "{MER}",  # merkha
	u"\u05a6"   :       "{MEK}",  # merkha-kefula
	u"\u05a7"   :       "{DAR}",  # darga
	u"\u05a8"   :       "{AZL}",  # azla / qadma
	u"\u05a9"   :       "{TLP}",  # telisha-qetana (parvum)
	u"\u05aa"   :       "{GAL}",  # yerah-ben-yomo / galgal
	u"\u05ab"   :       "{OLE}",  # ole / we-yored
	u"\u05ac"   :       "{ILL}",  # iluy
	u"\u05ad"   :       "{DEH}",  # dehi
	u"\u05ae"   :       "{ZIN}",  # tzinor == zarqa?

	u"\u05af"   :       "{CIR}",  # masora-circle / circellus?

# Yiddish ligatures just in case...
	u"\u05f0"   :       "ww",    # double-vav
	u"\u05f1"   :       "wy",    # vav-yod
	u"\u05f2"   :       "yy",    # double-yod

# Added punctuation
	u"\u05f3"   :       "!",     # punctuation-geresh ( ' )
	u"\u05f4"   :       "!!",    # punctuation-gershayim ( '' )
	"<SAMEKH/>" :       "{SET}", # parsha marker Setuma
	"<PEH/>"    :       "{PET}", # parsha marker Petukha
	"<SHIN/>"   :       "{SHI}", # parsha marker Shir?
	u'\xd7'     :       "{MUL}"  # multiplication symbol &times;
}

# SAMPA for Hebrew
# description: SAMPA for Hebrew, an ASCII representation of phonetic symbols for Hebrew
# w^o => o
# http://www.phon.ucl.ac.uk/home/sampa/hebrew.htm
# Established on the initiative of the http://www.orientel.org - OrienTel project
# Maintained by j.wells@phon.ucl.ac.uk - J.C. Wells - Created 2002 07 12
tiqwah2SAMPA_dict = {
	# Consonants
	#   Plosives
	"p*" :  "p", # peh
	"b*" :  "b", # beit
	"t*" :  "t", # tav
	"T"  :  "t", # tet
	"d"  :  "d", # dhalet
	"d*" :  "d", # dalet
	"k*" :  "k", # kaf
	"q"  :  "k", # quf
	"q*" :  "k", # quf w/dagesh?
	"g"  :  "g", # gimel
	"g*" :  "g", # gimel-dagesh
#	"\"" :  "?", # sh`va
	"\"" :  "@", # sh`va
#	"_"  :  "",  # grammatic word-break
#	"\'" :  "@", # aleph
	"'"  :  "",  # aleph
#	"`"  :  "@", # ayin
	"`"  :  "",  # ayin

	#   Fricatives
	"p"   :  "f", # phe
	"b"   :  "v", # veit
	"w"   :  "v", # waw
	"W"   :  "s", # sin
	"W*"  :  "s", # sin w/dagesh
	"W/"  :  "s", # sin w/out dot
	"s"   :  "s", # samekh
	"z"   :  "z", # zayin
	"S"   :  "S", # shin
	"S*"  :  "S", # shin w/dagesh
	"x"   :  "X", # khet
	"k"   :  "X", # khaf
	"h"   :  "h", # hey
	"&RAF;" : "", # raphe -- indicates fricative

	#   Affricate
#	"Y"   :  "ts", # tsadi
	"Y"   :  "Z", # tsadi

	#   Nasals
	"m"   :  "m", # mem
	"m*"  :  "m", # mem-dagesh
	"n"   :  "n", # nun
	"n*"  :  "n", # nun-dagesh

	#   Liquids
	"l"   :  "l", # lamed
	"l*"  :  "l", # lamed-dagesh
	"r"   :  "R", # resh

	#   Semi-vowel
#	"y"   :  "j",
	"y"   :  "y",
	"y*"  :  "y", # yud w/dagesh

	#   Vowels
	"i"      :  "i",
	"e"      :  "e",
	"E"      :  "e",
	"{HSE}" :  "e", # hateph-segol sh'va-E
	"a"      :  "a",
	"A"      :  "a",
	"{HPA}" :  "a", # hateph-patakh sh'va-a
	"{HQA}" :  "a", # hateph-qamats sh'va-A
	"o"      :  "o",
	"w^o"    :  "o", # holam-haser
	"u"      :  "u",
	"w*"     :  "u", # holam-waw?

	#   common strange cases
	"kal="   :  "kol-", # holam-waw?

	# Rare, dialectal or marginal phonemes
#	""   :  "Z",
#	""   :  "X\\",
#	""   :  "tS",
#	""   :  "dZ",
#	""   :  "?\\",

	# Stress mark
	"\$"   :  "\""
}



def unicode2tiqwah(hebrew_unicode):
    xlator = Xlator(unicode2tiqwah_dict)
    tiqwah_text = xlator.xlat(hebrew_unicode)
    #print "Changed %d thing(s)" % xlat.count 
    return tiqwah_text


def tiqwah2unicode(hebrew_tiqwah):
    xlator = Xlator(tiqwah2unicode_dict)
    unicode_text = xlator.xlat(hebrew_tiqwah)
    #print "Changed %d thing(s)" % xlat.count 
    return unicode_text
 
def tiqwah2phonetic(hebrew_tiqwah):
    xlator = Xlator(tiqwah2SAMPA_dict)
    sampa_text = xlator.xlat(hebrew_tiqwah)
    #print "Changed %d thing(s)" % xlat.count 
    return sampa_text

#
# command line
# 
if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='haaper: Convert one Hebrew encoding to another')
    parser.add_argument("-v", "--verbosity",
        action="store_true",
        help="verbosity flag", default=False)
    parser.add_argument("-t", "--tiqwah", "--tiqwah2unicode",
        action="store_true",
        help="Convert Tiqwah format to Unicode Hebrew", default=True)
    parser.add_argument("-u", "--unicode", "--unicode2tiqwah",
        action="store_true",
        help="Convert Unicode Hebrew to Tiqwah ASCII", default=False)
    parser.add_argument("-s", "--sampa", "--tiqwah2sampa",
        action="store_true", 
        help="Convert Tiqwah ASCII to SAMPA phonetic ASCII", default=False)
    parser.add_argument('input_file_name',
        help="file to be processed")
    parser.add_argument('output_file_name',
        help="result file")
    args = parser.parse_args()

    input_file = codecs.open(args.input_file_name, 'r', encoding = 'utf-8')
    output_file = codecs.open(args.output_file_name, 'w+', encoding = 'utf-8')

    for line in input_file:
        line = line.rstrip('\n')
        if args.sampa:
            output_file.write( tiqwah2phonetic(line) + '\n' )
        elif args.unicode:
            output_file.write( unicode2tiqwah(line) + '\n' )
        else:
            output_file.write( tiqwah2unicode(line) + '\n' )

# End of haaper.py

