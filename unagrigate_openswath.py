
import warnings
import argparse
import glob
import time

start_time = time.time()

parser = argparse.ArgumentParser(description='unagrigates openswath results')
parser.add_argument('-i', '--input', required=True, type=str, help='Input directory')
parser.add_argument('-o', '--output', required=True, type=str,
                    help='Output filename')
args = parser.parse_args()

input_files = args.input
output_file = args.output

myfiles = glob.glob(input_files)

columns = ["aggr_Peak_Area", "aggr_Fragment_Annotation"]
delimiter = "\t"
column_indices = []


OUT = open(output_file, 'w')
header_printed = False
for file in myfiles:
    with open(file) as f:
        for i, line in enumerate(f):
            global_list = line.strip().split(delimiter)
            tmp_list = global_list[:]
            if i == 0:
                #first finds at the header the requested columns
                column_indices = [i for i, x in enumerate(tmp_list) if any(thing in x for thing in columns)]
                if column_indices:
                    if not header_printed:
                        tmp_list.insert(0, "Peak_Area")
                        tmp_list.insert(0, "Fragment_Annotation")
                        OUT.write("{0}\n".format(delimiter.join(tmp_list)))
                        header_printed = True
                else:
                    warnings.warn("Warning: file {0} didn't have header, skipping".format(file))
                    break
                continue
            if column_indices:
                area = tmp_list[column_indices[0]].split(";")
                annotation = tmp_list[column_indices[1]].split(";")
                #print area
                #print annotation
                for a, n in zip(area, annotation):
                    #print a,n
                    tmp_list = global_list[:]
                    tmp_list.insert(0, a)
                    tmp_list.insert(0, n)
                    #tmp_list.append("\n")
                    #OUT.write(delimiter.join(tmp_list))
                    #print "{0}\n".format(delimiter.join(tmp_list))
                    OUT.write("{0}\n".format(delimiter.join(tmp_list)))
            else:
                warnings.warn("Warning: file {0} didn't have header, skipping".format(file))
                break
    column_indices = []

OUT.close()














