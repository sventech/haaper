haaper (håper)
======

Convert Hebrew between standard Unicode UTF-8 encoding and Tiqwah* ASCII representation, also phonetic SAMPA IPA

Håper is Norwegian for 'hope,' equivalent to Hebrew תִקְוָה /tiqwah/ or &ldquo;tikvah.&rdquo;

* Tiqwah is an encoding developed by Yannis Haralambous for LaTeX editing of scholarly versions of ancient Hebrew and Aramaic documents. This is not yet a complete implementation, but it covers most characters for a Bible text. Also, the three letter codes for teamim and other symbols are surrounded by curly braces {} instead of angle brackets &lt;&gt; for use in HTML/XML.

<pre>
usage: python/haaper.py [-h] [-v] [-t] [-u] [-s] input_file_name output_file_name

haaper: Convert one Hebrew encoding to another

positional arguments:
  input_file_name       file to be processed
  output_file_name      result file

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbosity       verbosity flag
  -t, --tiqwah, --tiqwah2unicode
                        Convert Tiqwah ASCII format to unicode Hebrew
  -u, --unicode, --unicode2tiqwah
                        Convert unicode Hebrew to Tiqwah ASCII
  -s, --sampa, --tiqwah2sampa
                        Convert Tiqwah ASCII to SAMPA phonetic ASCII
</pre>
