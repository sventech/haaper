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
			Console.WriteLine(input);

			Tiqwah2Unicode tiqwah2hebrew = new Tiqwah2Unicode();

			string output = tiqwah2hebrew.xlat(input);
			Console.WriteLine(output);
		}
	}
}
