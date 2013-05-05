using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.Linq;

namespace Haaper2Hebrew
{
	public class Xlator
	{
		protected Dictionary<string, string> _char_map;
		private Regex _xlat_regex;

		protected void setDictionary(Dictionary<string,string> dict)
		{
			_char_map = dict;
		}

		public Xlator()
		{
			if(_char_map.Keys.Count > 1)
			{
			   this.createRegex();
			}
		}

		public Xlator (Dictionary<string,string> dict)
		{
			_char_map = dict;
			/*
			// Loop over pairs with foreach
			foreach (KeyValuePair<string, string> pair in dict)
			{
				Console.WriteLine("{0}, {1}",
				                  pair.Key,
				                  pair.Value);
			}

			// Use var keyword to enumerate dictionary
			foreach (var pair in dict)
			{
				Console.WriteLine("{0}, {1}",
				                  pair.Key,
				                  pair.Value);
			}
			*/
			this.createRegex();
		}

		private void createRegex()
		{
			List<string> keyList = new List<string>(this._char_map.Keys);
			//string tmp = "(" + String.Join("|", keyList) + ")";
			//Console.WriteLine("list before sort: "+tmp);
			if(!IsNullOrEmpty(keyList)) {
				keyList =  new List<string>( SortByLength(keyList) );
				string xlat_regex_text = "";

				if(keyList.Count > 1) {
					xlat_regex_text = "(" + String.Join("|", keyList ) + ")";
					//Console.WriteLine("final: "+xlat_regex_text);
				}
				_xlat_regex = new Regex( xlat_regex_text );
			} else {
				_xlat_regex = new Regex(".");
			}
		}

		/// <summary>
		/// change text according to dictionary patterns
		/// </summary>
		public string xlat(string text)
		{
			return _xlat_regex.Replace(text, delegate(Match m) {
				if(this._char_map.ContainsKey(m.Value)) {
					return this._char_map[m.Value];
				} else {
					return m.Value;
				}
			});
		}
		/// <summary>
		/// Sorts the list of Regex matches by length and escapes strings for literal matching.
		/// </summary>
		/// <returns>Escaped strings in descending order of length</returns>
		/// <param name="e">enumerable (list or collection of keys)</param>
		static IEnumerable<string> SortByLength(IEnumerable<string> e)
		{
			if( ((ICollection<string>)e).Count > 1 ) {
				// Use LINQ to sort the array received and return a copy.
				var sorted = from s in e
					orderby s.Length descending
						select Regex.Escape(s);
				return sorted;
			} else {
				return e;
			}
		}

		/// <summary>
		/// Determines whether the collection is null or contains no elements.
		/// </summary>
		/// <typeparam name="T">The IEnumerable type.</typeparam>
		/// <param name="enumerable">The enumerable, which may be null or empty.</param>
		/// <returns>
		///     <c>true</c> if the IEnumerable is null or empty; otherwise, <c>false</c>.
		/// </returns>
		/// Written by Daniel Vaughan
		public static bool IsNullOrEmpty<T>(IEnumerable<T> enumerable)
		{
			if (enumerable == null)
			{
				return true;
			}
			/* If this is a list, use the Count property for efficiency. 
         	* The Count property is O(1) while IEnumerable.Count() is O(N). */
			var collection = enumerable as ICollection<T>;
			if (collection != null)
			{
				return collection.Count < 1;
			}
			return !enumerable.Any();
		}

	}
}

