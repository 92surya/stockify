import os
import subprocess

# directory_path = "/home/surya/git/customPrograms/foFiles"
directory_path = "/home/surya/git/customPrograms/eqFiles"
os.chdir(directory_path)

# input_file = "fo12May2021bhav.csv"
# output_file = "fo12May2021bhav_with_comma.csv"
input_file = "cm13Jul2020bhav.csv"
output_file = "cm13Jul2020bhav_with_comma.csv"
with open(input_file) as In, open(output_file, 'w') as Out:
    for line in In:
        Out.write(line.rstrip('\n') + ',\n')

# commands = ["rm fo12May2021bhav.csv",
#             "mv fo12May2021bhav_with_comma.csv fo12May2021bhav.csv"]
commands = ["rm cm13Jul2020bhav.csv",
            "mv cm13Jul2020bhav_with_comma.csv cm13Jul2020bhav.csv"]
for command in commands:
    process = subprocess.Popen(command,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
