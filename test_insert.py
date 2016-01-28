import sqlite3
import csv
import os
import glob
import sys
import warnings


db = sys.argv[1]
  
conn = sqlite3.connect(db)
conn.text_factory = str  # allows utf-8 data to be stored
	 
c = conn.cursor()

numeric_cols = ["Peak_Area", "RT", "Charge", "m_z", "assay_rt", "Intensity", "decoy", "m_score", "d_score",
                "peak_group_rank", "sn_ratio", "total_xic"]


csvfile = os.path.join(sys.argv[2])

# remove the path and extension and use what's left as a table name
tablename = os.path.splitext(os.path.basename(csvfile))[0]
OUT = open(output_file, 'w')

with open(csvfile, "rb") as f:
    reader = csv.reader(f, delimiter='\t')

    header = True
    for row in reader:
        if header:
            # gather column names from the first row of the csv
            header = False

            c.execute('DROP TABLE IF EXISTS {}'.format(tablename))

            row = [column.replace('/', '_') for column in row]
            cols = ", ".join(["%s REAL" % column if column in numeric_cols else "%s TEXT" % column for column in row])

            print cols
            #cols = ", ".join(["%s text" % column for column in row])
            sql = "CREATE TABLE {} ({})".format(tablename, cols)
            c.execute("CREATE TABLE {} ({})".format(tablename, cols))

            for column in row:
                if column in ('Fragment_Annotation', 'transition_group_id', 'FullPeptideName', 'ProteinName', 'filename'):
                    index = "%s__%s" % ( tablename, column)
                    c.execute("CREATE INDEX {} on {} ({})".format(index, tablename, column))

            insertsql = "INSERT INTO %s VALUES (%s)" % (tablename,
                        ", ".join([ "?" for column in row ]))

            rowlen = len(row)
        else:
            # skip lines that don't have the right number of columns
            if len(row) == rowlen:
                c.execute(insertsql, row)

    conn.commit()
 
c.close()
conn.close()
