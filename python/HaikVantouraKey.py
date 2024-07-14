#!/usr/bin/env python
# Filename: HaikVantouraKey.py

ProsePattern_dict = {
	# Upper Accents (relative to the previous note)
	"<PAS>"   :  "[+1]",       # pashta
	"<AZL>"   :  "[+1]",       # azla / qadma / (pashta late)
	"<GER>"   :  "[+2]",       # geresh
	"<GRM>"   :  "[+2]",       # geresh-muqdam ??
	"<GAR>"   :  "[+2+0+2]",   # garshayim
	"<PAZ>"   :  "[+2-1]",     # pazer
	"<ZQP>"   :  "[-1]",       # zaqef-qatan (parvum)
	"<ZQM>"   :  "[-1-2]",     # zaqef-gadol (magnum)
	"<RBM>"   :  "[+0]",       # revia (magnum) / gadol
	"<AST>"   :  "[-1+0-1]",   # accent-segol ??
	"<ZAR>"   :  "[-1+1]",     # zarqa / (t)zinor / tzinorit?
	"<TLP>"   :  "[+1+2+3]",   # telisha-qetana (parvum)
	"<TLM>"   :  "[+3+2+1]",   # telisha-gedola (magnum)
	"<PZM>"   :  "[+1+2+3+3+2+1]", # qarney-para / pazer gadol (magnum) /(telisha-qetana,gedola)
	"<OLE>"   :  "[+3+0]",     # ole / we-yored
	"<ILL>"   :  "[+4]|[-3]",  # iluy
	"<SHP>"   :  "[-2-1-%]",   # shalshelet

	# Basic degrees (notes)
	"<YET>"   :  "0",    # [C] yetiv / yetib (mahapakh early) TODO: timing
	"<MEH>"   :  "6",    # [C] mahapakh
	"<MUN>"   :  "5",    # [B] munah / munakh / logarmeh
	"<ATN>"   :  "4",    # [A] aetnachta ? atnakh
	"<TIP>"   :  "3",    # [G] tipeha / tif'kha
	"<DEH>"   :  "9",    # [G] dehi / tif'kha early
	"<MER>"   :  "2",    # [F/F#] merkha
	"<MEK>"   :  "22",   # [FF] merkha-kefula (double merkha)?
	"<SIL>"   :  "1",    # [E] silluq / meteg / ga`ya
	"<GAL>"   :  "8",    # [D#] yerah-ben-yomo / galgal
	"<TEB>"   :  "7",    # [D,] tevir / tebir
	"<DAR>"   :  "6",    # [C,] darga -- FIXME: check octave

	# End of a Parsha
	"<SET>"   :  "", # parsha marker Setuma (Samekh)
	"<PET>"   :  "", # parsha marker Petukha (Pe)
	"<RST>"   :  "r" # rest inside verse (comma)
}
PsalmPattern_dict = ProsePattern_dict.copy()
# alternate meaning of revia for Psalmodic
PsalmPattern_dict["<RBM>"] = "[-1]" # revia (magnum) / gadol


# codes to allow separation of text and music information
CodeTable_dict = {
	# Upper Accents
	"100":	"<PAS>",   # pashta
	"101":	"<AZL>",   # azla / qadma / (pashta late)
	"102":	"<GER>",   # geresh
	"103":	"<GRM>",   # geresh-muqdam ??
	"104":	"<GAR>",   # garshayim
	"105":	"<PAZ>",   # pazer
	"106":	"<ZQP>",   # zaqef-qatan (parvum)
	"107":	"<ZQM>",   # zaqef-gadol (magnum)
	"108":	"<RBM>",   # revia (magnum) / gadol
	"109":	"<AST>",   # accent-segol ??
	"110":	"<ZAR>",   # zarqa / (t)zinor / tzinorit?
	"111":	"<TLP>",   # telisha-qetana (parvum)
	"112":	"<TLM>",   # telisha-gedola (magnum)
	"113":	"<PZM>",   # qarney-para / pazer gadol (magnum) /(telisha-qetana,gedola)
	"114":	"<OLE>",   # ole / we-yored
	"115":	"<ILL>",   # iluy
	"116":	"<SHP>",   # shalshelet

	# Basic degrees (notes)
	"011":	"<YET>",   # [C] yetiv / yetib (mahapakh early)
	"010":	"<MEH>",   # [C] mahapakh
	"009":	"<MUN>",   # [B] munah / munakh / logarmeh
	"008":	"<ATN>",   # [A] aetnachta ? atnakh
	"007":	"<TIP>",   # [G] tipeha / tif'kha
	"006":	"<DEH>",   # [G] dehi / tif'kha early
	"005":	"<MER>",   # [F/F#] merkha
	"004":	"<MEK>",   # [FF] merkha-kefula (double merkha)?
	"003":	"<SIL>",   # [E] silluq / meteg / ga`ya
	"002":	"<GAL>",   # [D#] yerah-ben-yomo / galgal
	"001":	"<TEB>",   # [D,] tevir / tebir
	"000":	"<DAR>",   # [C,] darga -- FIXME

	# End of a Parsha
	"200":	"<SET>",   # parsha marker Setuma (Samekh)
	"201":	"<PET>",   # parsha marker Petukha (Pe)
	"999":	"<RST>"    # rest inside verse (comma)
}

# reverse the dictionary for easy lookup restoring the original code
CodePattern_dict = {tikva: f"[{numeric}]" for numeric, tikva in CodeTable_dict.items()}

# End HaikVantouraKey.py
