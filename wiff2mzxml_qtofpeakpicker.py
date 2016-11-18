__author__ = 'zelezna'

import argparse
import os, fnmatch
import platform
import re
import sys


parser = argparse.ArgumentParser(description='Convertion from wiff to open formats with area peak picking on qtof data')

parser.add_argument('-i', '--input', required=True, type=str, help='Input directory')
parser.add_argument('-o', '--output', required=True, type=str, help='Output directory')

parser.add_argument('-f', '--format', required=False, type=str, default="mzXML")


args = parser.parse_args()

input_files = args.input
output_dir = args.output
output_format = args.format

pattern = "*.wiff$"

path_split = os.path.split(input_files)

if path_split[1] != "":
    pattern = path_split[1]

input_dir = path_split[0]

go_flag = 0
if re.search(r'^[Ww]+in.*?', platform.system()):
    go_flag = 1
    os.system("SET PATH=%PATH%;C:\Program Files\ProteoWizard\ProteoWizard 3.0.10188")

matched_files = fnmatch.filter(os.listdir(input_dir), pattern)

print "Total files to process: {0}".format(len(matched_files))

if not matched_files:
    quit("No files found!")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)



for file in matched_files:

    input_file = os.path.join(input_dir, file)
    file_re = re.compile(r'(.*).wiff$', re.IGNORECASE)
    if file_re.match(file):
        tmp_file = file_re.match(file).group(1)
        output_file = ".".join([tmp_file, output_format])
        output = os.path.join(output_dir, output_file)

        command = ("qtofpeakpicker.exe ",
                  "--resolution=20000 ",
                  "--area=1 ",
                  "--threshold=1 ",
                  "--smoothwidth=1.1 ",
                  "--in {0} ".format(input_file),
                  "--out  {0}".format(output))

        if go_flag == 1:
            os.system(command)
        else:
            print "Do nothing, wrong OS"
            print ' '.join(command)








