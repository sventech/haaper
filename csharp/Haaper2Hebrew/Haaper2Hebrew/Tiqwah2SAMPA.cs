using System;
using System.Collections.Generic;

namespace Haaper2Hebrew
{
	public class Tiqwah2SAMPA : Xlator
	{
		// SAMPA for Hebrew
		// description, SAMPA for Hebrew, an ASCII representation of phonetic symbols for Hebrew
		
		// w^o => o
		
		public static Dictionary<string,string> tiqva2SAMPA_dict = new Dictionary<string, string> {
			// Consonants
			//   Plosives
			{ "p*" ,  "p" }, // peh
			{ "b*" ,  "b" }, // beit
			{ "t*" ,  "t" }, // tav
			{ "T"  ,  "t" }, // tet
			{ "d"  ,  "d" }, // dhalet
			{ "d*" ,  "d" }, // dalet
			{ "k*" ,  "k" }, // kaf
			{ "q"  ,  "k" }, // quf
			{ "q*" ,  "k" }, // quf w/dagesh?
			{ "g"  ,  "g" }, // gimel
			{ "g*" ,  "g" }, // gimel-dagesh
		//	{ "\"" ,  "?" }, // sh`va
			{ "\"" ,  "@" }, // sh`va
		//	{ "_"  ,  "" },  // grammatic word-break
		//	{ "\'" ,  "@" }, // aleph
			{ "'"  ,  "" },  // aleph
		//	{ "`"  ,  "@" }, // ayin
			{ "`"  ,  "" },  // ayin
			
			//  Fricatives
			{ "p"   ,  "f" }, // phe
			{ "b"   ,  "v" }, // veit
			{ "w"   ,  "v" }, // waw
			{ "W"   ,  "s" }, // sin
			{ "W*"  ,  "s" }, // sin w/dagesh
			{ "W/"  ,  "s" }, // sin w/out dot
			{ "s"   ,  "s" }, // samekh
			{ "z"   ,  "z" }, // zayin
			{ "S"   ,  "S" }, // shin
			{ "S*"  ,  "S" }, // shin w/dagesh
			{ "x"   ,  "X" }, // khet
			{ "k"   ,  "X" }, // khaf
			{ "h"   ,  "h" }, // hey
			{ "&RAF;" , "" }, // raphe -- indicates fricative
			
			//   Affricate
		//	{ "Y"   ,  "ts" }, // tsadi
			{ "Y"   ,  "Z" }, // tsadi
			
			//   Nasals
			{ "m"   ,  "m" }, // mem
			{ "m*"  ,  "m" }, // mem-dagesh
			{ "n"   ,  "n" }, // nun
			{ "n*"  ,  "n" }, // nun-dagesh
			
			//   Liquids
			{ "l"   ,  "l" }, // lamed
			{ "l*"  ,  "l" }, // lamed-dagesh
			{ "r"   ,  "R" }, // resh
			
			//   Semi-vowel
		//	{ "y"   ,  "j" },
			{ "y"   ,  "y" },
			{ "y*"  ,  "y" }, // yud w/dagesh
			
			//   Vowels
			{ "i"      ,  "i" },
			{ "e"      ,  "e" },
			{ "E"      ,  "e" },
			{ "{HSE}" ,  "e" }, // hateph-segol sh'va-E
			{ "a"      ,  "a" },
			{ "A"      ,  "a" },
			{ "{HPA}" ,  "a" }, // hateph-patakh sh'va-a
			{ "{HQA}" ,  "a" }, // hateph-qamats sh'va-A
			{ "o"      ,  "o" },
			{ "w^o"    ,  "o" }, // holam-haser
			{ "u"      ,  "u" },
			{ "w*"     ,  "u" }, // holam-waw?
			
			//   common strange cases
			{ "kal="   ,  "kol-" }, // holam-waw?
			
			// Rare, dialectal or marginal phonemes
		//	{ ""   ,  "Z" },
		//	{ ""   ,  "X\\" },
		//	{ ""   ,  "tS" },
		//	{ ""   ,  "dZ" },
		//	{ ""   ,  "?\\" },
			
			// Stress mark
			{ "$"   ,  "\"" }
		};
		
		// http,//www.phon.ucl.ac.uk/home/sampa/hebrew.htm
		// Established on the initiative of the http,//www.orientel.org - OrienTel project
		// Maintained by j.wells@phon.ucl.ac.uk - J.C. Wells - Created 2002 07 12
		public Tiqwah2SAMPA () : base(tiqva2SAMPA_dict)
		{
		}
	}
}

