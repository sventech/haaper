using System;
using System.Collections.Generic;
using System.Text;
using System.IO;

namespace Haaper2Hebrew
{
	class MainClass
	{
		public static void Main (string[] args)
		{
			string conversion = "tiqwah2unicode";
			//string inputFile = args[0];
			//string outputFile = args[1];
			//StreamReader reader = new StreamReader(inputFile);
			//string content = reader.ReadToEnd();
			//reader.Close();
			//StreamWriter writer = new StreamWriter(outputFile);

			string input_name = @"/Users/svenpedersen/code/haaper/ten_commandments.tiq";
			string output_name = @"/Users/svenpedersen/code/haaper/ten_commandments.txt";

			var tiqwah2hebrew = new Tiqwah2Unicode();
			var hebrew2tiqwah = new Unicode2Tiqwah();
			var tiqwah2phonetic = new Tiqwah2SAMPA();
			Xlator xlator;
			if(conversion == "tiqwah2unicode") {
				xlator = tiqwah2hebrew;
			} else if(conversion == "unicode2tiqwah") {
				xlator = hebrew2tiqwah;
			} else if(conversion == "tiqwah2SAMPA") {
				xlator = tiqwah2phonetic;
			}

			string line;
			using (System.IO.StreamWriter outFile = new System.IO.StreamWriter(output_name))
			{
				// Read the file and process it line by line.
				System.IO.StreamReader inFile = new System.IO.StreamReader(input_name);
				while((line = inFile.ReadLine()) != null)
				{
					line = xlator.xlat(line);
					outFile.WriteLine(line);
				}
				
				inFile.Close();
			}

			//Console.OutputEncoding = Encoding.UTF8;
			//string input = "hatiqwah";
			//Console.WriteLine("input: "+input);

			//string output = tiqwah2hebrew.xlat(input);
			//Console.WriteLine("tiqwah2hebrew: "+output);

			//string output2 = hebrew2tiqwah.xlat(output);
			//Console.WriteLine("hebrew2tiqwah: "+output2);

			//string output3 = tiqwah2phonetic.xlat(input);
			//Console.WriteLine("tiqwah2SAMPA: "+output3);
		}
	}
}
