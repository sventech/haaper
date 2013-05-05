using System;
using System.Collections.Generic;

namespace Haaper2Hebrew
{
	public class Tiqwah2Unicode : Xlator
	{
		public static Dictionary<string,string> tiqwah2unicode_dict = new Dictionary<string, string> {
			// Letters  = Consonants
			{ @"'"  ,        "\u05d0" }, // aleph
			{ @"b"  ,        "\u05d1" }, // bet / vet
			{ @"g"  ,        "\u05d2" }, // gimel
			{ @"d"  ,        "\u05d3" }, // daleth
			{ @"h"  ,        "\u05d4" }, // hey
			{ @"w"  ,        "\u05d5" }, // vav / waw
			{ @"z"  ,        "\u05d6" }, // zayin
			{ @"x"  ,        "\u05d7" }, // khet
			{ @"T"  ,        "\u05d8" }, // tet
			{ @"y"  ,        "\u05d9" }, // yodh / yud
			{ @"k\b",        "\u05dA" }, // final kaf-sofit 
			{ @"k"  ,        "\u05dB" }, // kaf / kaph
			{ @"l"  ,        "\u05dC" }, // lamedh
			{ @"m\b",        "\u05dD" }, // final mem-sofit 
			{ @"m"  ,        "\u05dE" }, // mem
			{ @"n\b",        "\u05dF" }, // final nun-sofit 
			{ @"n"  ,        "\u05e0" }, // nun
			{ @"s"  ,        "\u05e1" }, // samekh
			{ "`"   ,        "\u05e2" }, // ayin
			{ @"p\b",        "\u05e3" }, // final pe-sofit 
			{ @"p"  ,        "\u05e4" }, // peh / pey
			{ @"Y\b",        "\u05e5" }, // final tsadi-sofit
			{ @"Y"  ,        "\u05e6" }, // tsadi
			{ @"q"  ,        "\u05e7" }, // quf / qof
			{ @"r"  ,        "\u05e8" }, // resh
			{ @"S"  ,  "\u05e9\u05c1" }, // shin w/dot
			{ @"W"  ,  "\u05e9\u05c2" }, // sin w/dot
			{ @"W/" ,        "\u05e9" }, // shin no dot
			{ @"t"  ,        "\u05eA" }, // taf / tav
			
			// Points and punctuation
			{ "\""    ,       "\u05b0" }, // sh'va / shewa (schwa)
			{ "{SWA}" ,       "\u05b0" }, // sh'va / shewa (schwa)
			{ "{HSE}" ,       "\u05b1" }, // hateph-segol
			{ "{HPA}" ,       "\u05b2" }, // hateph-patakh
			{ "{HQA}" ,       "\u05b3" }, // hateph-qamats
			{ "i"     ,       "\u05b4" }, // hiriq
			{ "{HIR}" ,       "\u05b4" }, // hiriq
			{ "e"     ,       "\u05b5" }, // tsere
			{ "{SER}" ,       "\u05b5" }, // tsere
			{ "E"     ,       "\u05b6" }, // segol
			{ "{SEG}" ,       "\u05b6" }, // segol
			{ "a"     ,       "\u05b7" }, // patakh
			{ "{PAT}" ,       "\u05b7" }, // patakh
			{ "A"     ,       "\u05b8" }, // qamats
			{ "{QAM}" ,       "\u05b8" }, // qamats
			{ "o"     ,       "\u05b9" }, // holam
			{ "{HOL}" ,       "\u05b9" }, // holam
			{ "w^o"   ,       "\u05ba" }, // holam haser (Unicode 5.0)
			//{ "w^o"   ,       "\u05ba\u05d5" }, // holam haser (Unicode 4.1)
			{ "u"     ,       "\u05bb" }, // qubuts / qibbuts
			{ "{QIB}" ,       "\u05bb" }, // qubuts / qibbuts
			{ "*"     ,       "\u05bc" }, // dagesh
			{ "{DAGESH}",     "\u05bc" }, // dagesh / BeGaD KeFaT ??
			{ "{SIL}" ,       "\u05bd" }, // meteg -- encode as silluq
			{ "="     ,       "\u05be" }, // maqaf / maqqeph
			{ "{RAF}" ,       "\u05bf" }, // rafe
			{ "{LIN}" ,       "\u05c0" }, // paseq / lineola
			{ ":"     ,       "\u05c3" }, // sof pasuq
			{ "upperdot" ,    "\u05c4" }, // upper dot
			{ "lowerdot" ,    "\u05c5" }, // lower dot
			{ "n/"    ,       "\u05c6" }, // reversed nun
			{ "n//"   ,       "\u05e0" }, // raised nun () -- not supported, convert to regular
			{ "{PCR}" ,       "\u0307" }, // punctum-extraordinarium / circellus / masora-number-dot
			
			{ "{SET}" ,    "<SAMEKH/>" }, // parsha marker Setuma
			{ "{PET}" ,       "<PEH/>" },    // parsha marker Petukha
			{ "{SHI}" ,      "<SHIN/>" },   // parsha marker Shir?
			
			// Accents
			{ "{ATN}" ,       "\u0591" }, // aetnakhta / atnakh
			{ "{AST}" ,       "\u0592" }, // accent segol
			{ "{SHP}" ,       "\u0593" }, // shalshelet
			{ "{ZQP}" ,       "\u0594" }, // zaqef katan
			{ "{ZQM}" ,       "\u0595" }, // zaqef gadol
			{ "{TIP}" ,       "\u0596" }, // tipeha / tif'kha
			{ "{RBM}" ,       "\u0597" }, // revia (magnum) / gadol
			{ "{ZAR}" ,       "\u0598" }, // zarqa / (t)zinor ??
			{ "{PAS}" ,       "\u0599" }, // pashta
			{ "{YET}" ,       "\u059a" }, // yetiv / yetib
			{ "{TEB}" ,       "\u059b" }, // tevir / tebir
			{ "{GER}" ,       "\u059c" }, // geresh
			{ "{GRM}" ,       "\u059d" }, // geresh-muqdam ?? -- addition
			{ "{GAR}" ,       "\u059e" }, // gershayim
			{ "{PZM}" ,       "\u059f" }, // qarney-para / pazer gadol (magnum)
			{ "{TLM}" ,       "\u05a0" }, // telisha-gedola (magnum)
			{ "{PAZ}" ,       "\u05a1" }, // pazer
			{ "{ATH}" ,       "\u05a2" }, // atnakh hafukh (Unicode 4.1) / yerah-ben-yomo / galgal
			{ "{MUN}" ,       "\u05a3" }, // munah
			{ "{MEH}" ,       "\u05a4" }, // mahapakh
			{ "{MER}" ,       "\u05a5" }, // merkha
			{ "{MEK}" ,       "\u05a6" }, // merkha-kefula
			{ "{DAR}" ,       "\u05a7" }, // darga
			{ "{AZL}" ,       "\u05a8" }, // azla / qadma
			{ "{TLP}" ,       "\u05a9" }, // telisha-qetana (parvum)
			{ "{GAL}" ,       "\u05aa" }, // yerah-ben-yomo / galgal
			{ "{OLE}" ,       "\u05ab" }, // ole / we-yored
			{ "{ILL}" ,       "\u05ac" }, // iluy
			{ "{DEH}" ,       "\u05ad" }, // dehi
			//{ "{ZIN}" ,       "\u05ae" }, // tzinor == zarqa?
			{ "{CIR}" ,       "\u05af" }, // masora-circle / circellus?
			
			// Yiddish ligatures just in case...
			{ "ww"    ,       "\u05f0" }, // double-vav
			{ "wy"    ,       "\u05f1" }, // vav-yod
			{ "yy"    ,       "\u05f2" }, // double-yod
			
			// Added punctuation
			{ "!"     ,       "\u05f3" }, // punctuation-geresh ( ' )
			{ "!!"    ,       "\u05f4" } // punctuation-gershayim ( '' )
		};

		public Tiqwah2Unicode () : base(tiqwah2unicode_dict)
		{
		}
	}
}

