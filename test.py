import re
import re,os
from pathlib import Path
import openpyxl
from userfunctions import Extract_Patterns
file = open('J0032069.x', errors='ignore')
p=os.path.abspath(__file__)
path=Path(p).parent
path=str(path)+'\J0032069.x'
# file.close()
pattern1 = r'(?i)\bsysout id\b'
pattern2 = r'(?i)\bgen\b'
pattern3 = r'(?i)return-code'
patterns=[pattern1,pattern2]
Extract_Patterns.extract_info(path,'new.txt',patterns)

with open('new.txt','r') as f:
    data=f.read()
lines = data.strip().split('\n')
filtered_lines = []
seen_ids = set()
x=0
combined_line=[f"{lines[i]} //{lines[i+1]} " for i in range(0, len(lines), 2)]
for i, line in enumerate(combined_line):

    sysout_id = line.split()[2]
    if "SYSOUT ID" in line and x==0:

        # print(sysout_id)

            filtered_lines.append(line)

            # print(line)

    x=1 if x==0 else 0
filtered_output='\n'.join(filtered_lines)
new=filtered_output.split('//')
print(new)
with open('final.txt','w') as file:
    for line in new:
        file.write(line+'\n')
with open('final.txt','r')as file:
    new_lines=file.read()

lines=[n for n in new_lines.split('\n')]



wb = openpyxl.Workbook()
ws = wb.active

# Set the column headers
headers = ["SYSOUT ID", "JOBNAME", "PRINT DATE", "ARCHIVE DATE", "GEN", "JOBID", "PRINT TIME", "ARCHIVE TIME",
           "RETURN-CODE"]
ws.append(headers)

# Process each record
i = 0
j = 1
k=2
while i < len(lines) and j < len(lines):
    sysout_id = re.search(r"SYSOUT ID: (.*?)\s", lines[i]).group(1)

    jobname = re.search(r"JOBNAME: (.*?)\s", lines[i]).group(1)
    print_date = re.search(r"PRINT DATE: (\d{2}/\d{2}/\d{4})\s", lines[i]).group(1)
    archive_date = re.search(r"ARCHIVE DATE: (\d{2}/\d{2}/\d{4})\s", lines[i]).group(1)
    gen = re.search(r"GEN:\s{7}(.*?)\s", lines[j]).group(1)
    jobid = re.search(r"JOBID:\s{3}(.*?)\s", lines[j]).group(1)
    print_time = re.search(r"PRINT TIME: (.*?)\s", lines[j]).group(1)
    archive_time = re.search(r"ARCHIVE TIME: (.*?)\s", lines[j]).group(1)
    # return_code=re.search(r'RETURN-CODE:\s{14}(.*?)\s',lines[k]).group(1)
    i += 2
    j += 2
    k+=2

    # Append data to the Excel sheet
    data = [sysout_id, jobname, print_date.replace('/', '-'), archive_date.replace('/', '-'), gen,
            jobid, print_time,archive_time]
    ws.append(data)

# Save the Excel file
wb.save('output.xlsx')