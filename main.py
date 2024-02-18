import re
from PyPDF2 import PdfReader


def save_to_database(pattern_list, pattern_number, line):
    if pattern_list == pattern_lists[0]:
        if pattern_number == 0:
            pattern = r'5\.3\.\S*'
            str = re.search(pattern, line)[0]
            print(str)

        elif pattern_number == 1:
            pattern = r'\s*Data Length:\s+(.+)'
            str = re.sub(pattern, r'\1', line)
            print(str)

        elif pattern_number == 2:
            pattern = r'\s*Parameter Group\s+(.+)\s+\(\s*(.+)\s*\)'
            str = re.sub(pattern, r'\1', line)
            print(str)
            str = re.sub(pattern, r'\2', line)
            print(str)

    else:
        if pattern_number == 0:
            pattern = r'\s*-71\s+(5\.2\.\S*)\s+(.+)'
            str = re.sub(pattern, r'\1', line)
            print(str)
            str = re.sub(pattern, r'\2', line)
            print(str)

        elif pattern_number == 1:
            pattern = r'\s*Slot Scaling:\s+(.+),.*'
            str = re.sub(pattern, r'\1', line)
            print(str)

        elif pattern_number == 2:
            pattern = r'\s*Slot Range:\s+(.+)Operational Range:.*'
            str = re.sub(pattern, r'\1', line)
            print(str)

        elif pattern_number == 3:
            pattern = r'\s*SPN:\s+(.+)'
            str = re.sub(pattern, r'\1', line)
            print(str)

        elif pattern_number == 4:
            pattern = r'\s*PGN Parameter Group Name and Acronym  Doc. and Paragraph\s+(\S+).*-71\s+(5\.3\.\S*)'
            str = re.sub(pattern, r'\1', line)
            print(str)
            str = re.sub(pattern, r'\2', line)
            print(str)


pdf_document = r'C:\Users\green\Desktop\SAE_J1939-71.pdf'
pdf_content = PdfReader(pdf_document)
number_pages = len(pdf_content.pages)

pattern_list_1 = [
    r'-71 5\.3\..+-.+',
    r'Data Length:\s+.+',
    r'Parameter Group\s+.+'
]
pattern_list_2 =[
    r'\s*-71\s+(5\.2\.\S*)\s+(.+)',
    r'Slot Scaling:.+',
    r'Slot Range:.+',
    r'SPN:.+',
    r'PGN Parameter Group Name and Acronym  Doc. and Paragraph\s+\S+.+-71 5\.3\.'
]

pattern_lists =[
    pattern_list_1,
    pattern_list_2
]

# list_pages = [120, 121, 122, 338, 339, 340, ]
# for page_number in list_pages:
#     page = pdf_content.pages[page_number]
#     for line in  page.extract_text().split('\n'):
#         print(line)
#     print('______________________________________________________________________')

for pattern_list in pattern_lists:
    pattern_number = 0
    for page_number in range(0, number_pages-1):
        page = pdf_content.pages[page_number]
        split_page =  page.extract_text().split('\n')
        number_lines = len(split_page)
        line_number = 0
        while line_number < number_lines:
            line = split_page[line_number]
            if re.search(pattern_list[pattern_number], line):
                save_to_database(pattern_list, pattern_number, line)
                # print(line)
                if pattern_number < len(pattern_list)-1:
                    pattern_number += 1
                else:
                    pattern_number = 0
                    print('____________________________________________________________________')
            line_number += 1


