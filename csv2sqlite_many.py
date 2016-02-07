import sqlite3
import csv
import os
import sys
import time

start = time.clock()

db = sys.argv[1]

if os.path.exists(db):
    os.remove(db)

conn = sqlite3.connect(db)
conn.text_factory = str  # allows utf-8 data to be stored

c = conn.cursor()

numeric_cols = ["Peak_Area", "RT", "Charge", "m_z", "assay_rt", "Intensity", "decoy", "m_score", "d_score",
                "peak_group_rank", "sn_ratio", "total_xic"]


csvfile = os.path.join(sys.argv[2])

# remove the path and extension and use what's left as a table name
tablename = "my_table"

BUF_SIZE = 100000000

bigfile = open(csvfile,'r')
tmp_lines = bigfile.readlines(BUF_SIZE)

SQL_insert = "INSERT INTO my_table VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
header = True

while tmp_lines:
    data = []
    #print len(tmp_lines)
    if header:
        # gather column names from the first row of the csv
        header = False
        #c.execute("PRAGMA synchronous = OFF")
        #c.execute("PRAGMA temp_store = MEMORY")
        #c.execute("PRAGMA cache_size = 2000")
        #c.execute("PRAGMA page_size=32768")

        c.execute('DROP TABLE IF EXISTS {}'.format(tablename))
        row = tmp_lines[0].strip().split("\t")

        row = [column.replace('/', '_') for column in row]
        cols = ", ".join(["%s REAL" % column if column in numeric_cols else "%s TEXT" % column for column in row])

         #cols = ", ".join(["%s text" % column for column in row])
        sql = "CREATE TABLE {} ({})".format(tablename, cols)
        c.execute(sql)

        data = [tuple(line.rstrip("\n").split("\t")) for line in tmp_lines[1:]]
        c.executemany(SQL_insert, data) # Do the insert test
        conn.commit() ###
    else:
        for line in tmp_lines:
            data.append(tuple(line.rstrip("\n").split("\t")))
        c.executemany(SQL_insert, data) # Do the insert test
        conn.commit() ###
    tmp_lines = bigfile.readlines(BUF_SIZE)

end = time.clock()

c.execute("SELECT COUNT(*) FROM my_table;")
n_rows=c.fetchone()[0]
c.close()
conn.close()

total_time = end - start
print("Imported {} records in {} seconds, on average {} inserts per second\n".format(n_rows, total_time, n_rows/total_time))

