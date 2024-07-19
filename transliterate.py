#!/usr/bin/env python

import argparse
import codecs

from haaper.haaper import unicode2tiqwah, tiqwah2unicode, tiqwah2phonetic

def main(input_file, output_file, mode='tiqwah', verbose=False):
    input_file = codecs.open(args.input_file_name, 'r', encoding='utf-8')
    output_file = codecs.open(args.output_file_name, 'w+', encoding='utf-8')

    for line in input_file:
        line = line.rstrip('\n')
        if 'sampa' == mode:
            output_file.write(tiqwah2phonetic(line, verbose) + '\n')
        elif 'unicode' == mode:
            output_file.write(unicode2tiqwah(line, verbose) + '\n')
        else:
            output_file.write(tiqwah2unicode(line, verbose) + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='haaper: Convert one Hebrew encoding to another')
    parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")
    parser.add_argument("-t", "--tiqwah", "--tiqwah2unicode", action="store_true",
                        help="Convert Tiqwah format to Unicode Hebrew (default)", default=True)
    parser.add_argument("-u", "--unicode", "--unicode2tiqwah", action="store_true",
                        help="Convert Unicode Hebrew to Tiqwah ASCII", default=False)
    parser.add_argument("-s", "--sampa", "--tiqwah2sampa", action="store_true",
                        help="Convert Tiqwah ASCII to SAMPA phonetic ASCII", default=False)
    parser.add_argument('input_file_name',
                        help="file to be processed")
    parser.add_argument('output_file_name',
                        help="result file")
    args = parser.parse_args()
    mode = 'tiqwah'
    if args.unicode:
        mode = 'unicode'
    elif args.sampa:
        mode = 'sampa'
    main(args.input_file_name, args.output_file_name, mode, args.verbose)
