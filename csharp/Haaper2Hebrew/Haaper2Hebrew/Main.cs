using System;
using System.Collections.Generic;
using System.Text;

namespace Haaper2Hebrew
{
	class MainClass
	{
		public static void Main (string[] args)
		{
			//StreamReader reader = new StreamReader(filename);
			//string content = reader.ReadToEnd();
			//reader.Close();

			Console.OutputEncoding = Encoding.UTF8;
			//Console.WriteLine ("Hello World!");
			string input = "hatiqwah";
			Console.WriteLine("input: "+input);

			Tiqwah2Unicode tiqwah2hebrew = new Tiqwah2Unicode();
			Unicode2Tiqwah hebrew2tiqwah = new Unicode2Tiqwah();

			string output = tiqwah2hebrew.xlat(input);
			Console.WriteLine("tiqwah2hebrew: "+output);

			string output2 = hebrew2tiqwah.xlat(output);
			Console.WriteLine("hebrew2tiqwah: "+output2);
		}
	}
}
