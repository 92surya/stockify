import psycopg2
import os

conn = psycopg2.connect(database="stocks",
                        user='postgres', password='Netradyne123',
                        host='localhost', port='5432'
                        )

cur = conn.cursor()

CWD = os.getcwd()#"/home/surya/git/stockify"

directory_path = CWD + "/foFiles"
os.chdir(directory_path)
print("loading fo data...")
for filename in sorted(os.listdir(directory_path)):
    with open(filename, 'r') as f:
        try:
            cur.execute("INSERT INTO bhavcopy_fo_status VALUES('" +filename + "');")
            # Notice that we don't need the `csv` module.
            next(f)  # Skip the header row.
            cur.copy_from(f, 'bhavcopy_fo', sep=',')
            print("loaded data for", filename, "!")
        except:
            pass
            # print("file already processed!")            
    conn.commit()
    #print("loaded data for", filename, "!")
print("loaded fo data!")


directory_path = CWD + "/eqFiles"
os.chdir(directory_path)
print("loading eq data...")
for filename in sorted(os.listdir(directory_path)):
    with open(filename, 'r') as f:
        try:
            cur.execute("INSERT INTO bhavcopy_eq_status VALUES('" +filename + "');")
            # Notice that we don't need the `csv` module.
            next(f)  # Skip the header row.
            cur.copy_from(f, 'bhavcopy_eq', sep=',')
            print("loaded data for", filename, "!")
        except:
            pass
            # print("file already processed!")            
    conn.commit()
    #print("loaded data for", filename, "!")
print("loaded eq data!")


directory_path = CWD + "/idxFiles"
os.chdir(directory_path)
print("loading idx data...")
for filename in sorted(os.listdir(directory_path)):
    with open(filename, 'r') as f:
        try:
            cur.execute("INSERT INTO bhavcopy_idx_status VALUES('" +filename + "');")
            # Notice that we don't need the `csv` module.
            next(f)  # Skip the header row.
            cur.copy_from(f, 'bhavcopy_idx', sep=',')
            print("loaded data for", filename, "!")
        except:
            pass
            # print("file already processed!")            
    conn.commit()
    #print("loaded data for", filename, "!")
print("loaded idx data!")

print("loading stats data...")
print("this could take a while......")
directory_path = CWD
os.chdir(directory_path)
with open("dataload.sql", 'r') as f:
    cur.execute(f.read())
print("loaded stats data tables!")
conn.commit()

conn.close()
