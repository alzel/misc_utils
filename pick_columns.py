import sqlite3
import csv
import os
import sys
import argparse

parser = argparse.ArgumentParser(description='filters specifies columnts from inputfile')
parser.add_argument('-f', '--filter_file', type=str, help='')
parser.add_argument('-i', '--input_file',  required=True, type=str, help='Input directory')
parser.add_argument('-o', '--output_file', required=True, type=str,
                    help='Output filename')

args = parser.parse_args()

input_file = args.input_file
output_file = args.output_file
filter_file = args.filter_file

delimiter = "\t"
select = []
if filter_file:
    select = [line.strip() for line in open(filter_file, 'r')]

if not select:
    select = ("Fragment_Annotation Peak_Area transition_group_id peptide_group_label run_id filename RT id Sequence"
              "FullPeptideName Charge  m/z  Intensity  ProteinName  decoy assay_rt  norm_RT potentialOutlier  sn_ratio"
              "total_xic aggr_Peak_Area  aggr_Fragment_Annotation d_score m_score peak_group_rank")

csvfile = input_file

column_indices = []
rowlen = 0

OUT = open(output_file, 'w')
with open(csvfile, "rb") as f:
    reader = csv.reader(f, delimiter='\t')

    header = True
    for k,row in enumerate(reader):
        if header:
            header = False
            column_indices = [i for i,x in enumerate(row) if x in select]

            if not column_indices:
                print >> sys.stderr, "None of columns were found in the header"
                sys.exit(1)
            rowlen = len(row)

        if len(row) == rowlen:
            content = [row[i] for i in column_indices]
            OUT.write("{0}\n".format(delimiter.join(content)))
        else:
            print >> sys.stderr, "Line {0} has wrong number of columns".format(k + 1)
            sys.exit(1)
OUT.close()