using System;
using System.Collections.Generic;
using System.Text;

namespace Haaper2Hebrew
{
	class MainClass
	{
		public static void Main (string[] args)
		{
			//string inputFile = args[0];
			//string outputFile = args[1];
			//StreamReader reader = new StreamReader(inputFile);
			//string content = reader.ReadToEnd();
			//reader.Close();
			//StreamWriter writer = new StreamWriter(outputFile);

			Console.OutputEncoding = Encoding.UTF8;
			string input = "hatiqwah";
			Console.WriteLine("input: "+input);

			Tiqwah2Unicode tiqwah2hebrew = new Tiqwah2Unicode();
			Unicode2Tiqwah hebrew2tiqwah = new Unicode2Tiqwah();
			Tiqwah2SAMPA tiqwah2phonetic = new Tiqwah2SAMPA();

			string output = tiqwah2hebrew.xlat(input);
			Console.WriteLine("tiqwah2hebrew: "+output);

			string output2 = hebrew2tiqwah.xlat(output);
			Console.WriteLine("hebrew2tiqwah: "+output2);

			string output3 = tiqwah2phonetic.xlat(input);
			Console.WriteLine("tiqwah2SAMPA: "+output3);
		}
	}
}
