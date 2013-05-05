using System;
using System.Collections.Generic;

namespace Haaper2Hebrew
{
	public class Unicode2Tiqwah : Xlator
	{
		// Letters"  = Consonants
		public static Dictionary<string,string> unicode2tiqwah_dict = new Dictionary<string, string> {
			{ "\u05d0"   ,  "'" },  // aleph
			{ "\u05d1"   ,   "b" },  // bet    
			{ "\u05d2"   ,   "g" },  // gimel    
			{ "\u05d3"   ,   "d" },  // dalet    
			{ "\u05d4"   ,   "h" },  // hey    
			{ "\u05d5"   ,   "w" },  // waw / vav    
			{ "\u05d6"   ,   "z" },  // zayin    
			{ "\u05d7"   ,   "x" },  // khet
			{ "\u05d8"   ,   "T" },  // tet
			{ "\u05d9"   ,   "y" },  // yud    
			{ "\u05dA"   ,   "k" },  // final-kaf
			{ "\u05dB"   ,   "k" },  // kaf    
			{ "\u05dC"   ,   "l" },  // lamed    
			{ "\u05dD"   ,   "m" },  // final-mem
			{ "\u05dE"   ,   "m" },  // mem    
			{ "\u05dF"   ,   "n" },  // final-nun
			{ "\u05e0"   ,   "n" },  // nun    
			{ "\u05e1"   ,   "s" },  // samekh    
			{ "\u05e2"   ,   "`" },  // ayin
			{ "\u05e3"   ,   "p" },  // final-pe 
			{ "\u05e4"   ,   "p" },  // pe
			{ "\u05e5"   ,   "Y" },  // final-tsadi
			{ "\u05e6"   ,   "Y" },  // tsadi
			{ "\u05e7"   ,   "q" },  // quf    
			{ "\u05e8"   ,   "r" },  // resh    
			{ "\u05e9\u05c1", "S" }, // shin w/dot
			{ "\u05e9\u05c2", "W" }, // sin  w/dot
			{ "\u05e9"   ,    "W/" }, // shin / no dot
			{ "\u05eA"   ,    "t" }, // tav    
			{ "\ufb4f"   ,  "'/l" }, // aleph-lamed ligature
				
			// Points and punctuation	
			{ "/"         ,      "_" },      // gramatic-word break (and/of/in/possessive)
		//	{ "\u05b0"   ,       "{SWA}" },  // shva / shewa (schwa)
			{ "\u05b0"   ,       "\"" },      // shva / shewa (schwa)
			{ "\u05b1"   ,       "{HSE}" },  // hateph-segol  '"E' (sh'va-E)
			{ "\u05b2"   ,       "{HPA}" },  // hateph-patakh '"a' (sh'va-a)
			{ "\u05b3"   ,       "{HQA}" },  // hateph-qamats '"A' (sh'va-A)
			{ "\u05b4"   ,       "i" },      // hiriq
		//	{ "\u05b4"   ,       "{HIR}" },  // hiriq
			{ "\u05b5"   ,       "e" },      // tsere
		//	{ "\u05b5"   ,       "{SER}" },  // tsere
			{ "\u05b6"   ,       "E" },      // segol
		//	{ "\u05b6"   ,       "{SEG}" },  // segol
			{ "\u05b7"   ,       "a" },      // patakh
		//	{ "\u05b7"   ,       "{PAT}" },  // patakh
			{ "\u05b8"   ,       "A" },      // qamats
		//	{ "\u05b8"   ,       "{QAM}" },  // qamats
			{ "\u05b9"   ,       "o" },      // holam
		//	{ "\u05b9"   ,       "{HOL}" },  // holam
			{ "\u05ba"   ,       "w^o" },    // holam haser (Unicode 5.0)
			{ "\u05d5\u05b9"  ,  "w^o" },    // holam haser (Unicode 4.1)
			{ "\u05bb"   ,       "{ " },      // qubuts / qibbuts
		//	{ "\u05bb"   ,       "{QIB}" },  // qubuts / qibbuts
			{ "\u05bc"   ,       "*" },      // dagesh / mapiq / shuruq
		//	{ "\u05bc"   ,       "{DAGESH}" }, // dagesh
			{ "\u05bd"   ,       "{SIL}" },  // meteg -- encode as silluq
			{ "\u05be"   ,       "=" },      // maqaf / maqqeph
			{ "\u05bf"   ,       "{RAF}" },  // rafe
		//	{ "\u05bc"   ,       "{LIN}" },  // lineola / paseq
			{ "\u05c0"   ,       "|" },      // lineola / paseq
			{ "\u05c1"   ,       "." },      // shin-dot
			{ "\u05c3"   ,       ":" },      // sof pasuq
			{ "\u05c4"   ,       "upper-dot" }, // upper dot
			{ "\u05c5"   ,       "lower-dot" }, // lower dot
			{ "\u05c6"   , 		"n/" },     // reversed nun (hafukha) - punctuation Numbers 10:35–36
		//	{ "\u05e0"   ,  	"n//" },    // raised nun ()
			{ "\u0307"   ,       "{PCR}" },  // punctum-extraordinarium / circellus / masora-number-dot
								
			// Accents
			{ "\u0591"   ,       "{ATN}" },  // aetnachta ? atnakh
			{ "\u0592"   ,       "{AST}" },  // accent-segol ??
			{ "\u0593"   ,       "{SHP}" },  // shalshelet
			{ "\u0594"   ,       "{ZQP}" },  // zaqef-qatan (parvum)
			{ "\u0595"   ,       "{ZQM}" },  // zaqef-gadol (magnum)
			{ "\u0596"   ,       "{TIP}" },  // tipeha / tif'kha
			{ "\u0597"   ,       "{RBM}" },  // revia (magnum) / gadol
			{ "\u0598"   ,       "{ZAR}" },  // zarqa / (t)zinor ??
			{ "\u0599"   ,       "{PAS}" },  // pashta
			{ "\u059a"   ,       "{YET}" },  // yetiv / yetib
			{ "\u059b"   ,       "{TEB}" },  // tevir / tebir
			{ "\u059c"   ,       "{GER}" },  // geresh
			{ "\u059d"   ,       "{GRM}" },  // geresh-muqdam ??
			{ "\u059e"   ,       "{GAR}" },  // gershayim
			{ "\u059f"   ,       "{PZM}" },  // qarney-para / pazer gadol (magnum)
			{ "\u05a0"   ,       "{TLM}" },  // telisha-gedola (magnum)
			{ "\u05a1"   ,       "{PAZ}" },  // pazer
			{ "\u05a2"   ,       "{GAL}" },  // atnakh hafukh (Unicode 4.0) / yerah-ben-yomo / galgal
		//	{ "\u05a2"   ,       "{ATH}" },  // atnakh hafukh (Unicode 4.1) / yerah-ben-yomo / galgal
			{ "\u05a3"   ,       "{MUN}" },  // munah
			{ "\u05a4"   ,       "{MEH}" },  // mahapakh
			{ "\u05a5"   ,       "{MER}" },  // merkha
			{ "\u05a6"   ,       "{MEK}" },  // merkha-kefula
			{ "\u05a7"   ,       "{DAR}" },  // darga
			{ "\u05a8"   ,       "{AZL}" },  // azla / qadma
			{ "\u05a9"   ,       "{TLP}" },  // telisha-qetana (parvum)
			{ "\u05aa"   ,       "{GAL}" },  // yerah-ben-yomo / galgal
			{ "\u05ab"   ,       "{OLE}" },  // ole / we-yored
			{ "\u05ac"   ,       "{ILL}" },  // iluy
			{ "\u05ad"   ,       "{DEH}" },  // dehi
			{ "\u05ae"   ,       "{ZIN}" },  // tzinor == zarqa?
				
			{ "\u05af"   ,       "{CIR}" },  // masora-circle / circellus?
				
			// Yiddish ligatures just in case...
			{ "\u05f0"   ,       "ww" },    // double-vav
			{ "\u05f1"   ,       "wy" },    // vav-yod
			{ "\u05f2"   ,       "yy" },    // double-yod
				
			// Added punctuation
			{ "\u05f3"   ,       "!" },     // punctuation-geresh ( ' )
			{ "\u05f4"   ,       "!!" },    // punctuation-gershayim ( '' )
			{ "<SAMEKH/>" ,      "{SET}" }, // parsha marker Setuma
			{ "<PEH/>"    ,      "{PET}" }, // parsha marker Petukha
			{ "<SHIN/>"   ,      "{SHI}" }  // parsha marker Shir?
		};

		public Unicode2Tiqwah () : base(unicode2tiqwah_dict)
		{
		}
	}
}

