haaper (håper)
======

Convert Hebrew between standard Unicode UTF-8 encoding and Tiqwah* ASCII representation, also phonetic SAMPA IPA

Håper is Norwegian for 'hope,' equivalent to Hebrew תִקְוָה /tiqwah/ or &ldquo;tikvah.&rdquo;

* Tiqwah is an encoding developed by Yannis Haralambous for LaTeX editing of scholarly versions of ancient Hebrew and Aramaic documents. This is not yet a complete implementation. Also, the three letter codes for [te'amim](https://en.wikipedia.org/wiki/Hebrew_cantillation) and other symbols are surrounded by angle brackets `<XXX>` -- previously they were in curly braces `{XXX}` instead for use in HTML/XML. I don't expect them to be often embedded directly in markup.

* The inspiration for this project was part of another quest; testing 
the hypothesis that [Suzanne Haïk-Vantoura's musicological interpretation](https://en.wikipedia.org/wiki/Suzanne_Ha%C3%AFk-Vantoura) that the te'amim, Hebrew Bible symbols for cantillation, could be understood as individual notes and decorations rather than patterns.

## Development Setup

This project uses UV for Python package management. To get started:

1. Install UV if you haven't already:
   https://docs.astral.sh/uv/getting-started/installation/

2. Create and activate a virtual environment:
   ```bash
   uv venv
   source .venv/bin/activate  # On Unix/macOS
   # or
   .venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

4. Install the project in development mode:
   ```bash
   uv tool install -e .
   ```

<pre>
usage: haaper [-h] [-v] [-t] [-u] [-s] input_file_name output_file_name

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

<pre>
usage: tunify [-h] [-p] [-i INSTRUMENT] [-o OCTAVE] [-m MODE] [--modes] [--csv] [--data-column DATA_COLUMN] input_file_name output_file_name

Bible text music ala Haik-Vantoura

positional arguments:
  input_file_name       file to be processed
  output_file_name      result file

options:
  -h, --help            show this help message and exit
  -p, --psalmodic       Use psalmody interpretation of notes
  -i INSTRUMENT, --instrument INSTRUMENT
                        Alda/midi instrument for score
  -o OCTAVE, --octave OCTAVE
                        Octave for score
  -m MODE, --mode MODE  Mode for score (default-prose: chromatic-dorian, default-psalm: dorian)
  --modes               List available musical modes
  --csv                 Extract from CSV/TSV file
  --data-column DATA_COLUMN
                        Specify column for text extraction: default 'text'
</pre>