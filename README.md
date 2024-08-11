haaper (håper)
======

Convert Hebrew between standard Unicode UTF-8 encoding and Tiqwah* ASCII representation, also phonetic SAMPA IPA

Håper is Norwegian for 'hope,' equivalent to Hebrew תִקְוָה /tiqwah/ or &ldquo;tikvah.&rdquo;

* Tiqwah is an encoding developed by Yannis Haralambous for LaTeX editing of scholarly versions of ancient Hebrew and Aramaic documents. This is not yet a complete implementation. Also, the three letter codes for [te'amim](https://en.wikipedia.org/wiki/Hebrew_cantillation) and other symbols are surrounded by angle brackets `<XXX>` -- previously they were in curly braces `{XXX}` instead for use in HTML/XML. I don't expect them to be often embedded directly in markup.

* The inspiration for this project was part of another quest; testing 
the hypothesis that [Suzanne Haïk-Vantoura's musicological interpretation](https://en.wikipedia.org/wiki/Suzanne_Ha%C3%AFk-Vantoura) that the te'amim, Hebrew Bible symbols for cantillation, could be understood as individual notes and decorations rather than patterns.

<pre>
usage: transliterate.py [-h] [-v] [-t] [-u] [-s] input_file_name output_file_name

haaper: Convert one Hebrew encoding to another

positional arguments:
  input_file_name       file to be processed
  output_file_name      result file

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         verbose flag
  -t, --tiqwah, --tiqwah2unicode
                        Convert Tiqwah ASCII format to unicode Hebrew
  -u, --unicode, --unicode2tiqwah
                        Convert unicode Hebrew to Tiqwah ASCII
  -s, --sampa, --tiqwah2sampa
                        Convert Tiqwah ASCII to SAMPA phonetic ASCII
</pre>
