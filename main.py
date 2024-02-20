import re
from PyPDF2 import PdfReader
from db_connection import *
from models import drop_tables, create_tables, CAN_package, Parameter

drop_tables(engine)
create_tables(engine)

def save_to_database(pattern_list, pattern_number, line):
    if pattern_list == pattern_lists[0]:

        if pattern_number == 1:
            pattern = r'.*\s*Data Length:\s+(.+)'
            str = re.sub(pattern, r'\1', line)
            print(str)

        elif pattern_number == 2:
            pattern = r'.*\s*Parameter Group\s+(.+)\s+\(\s*(.+)\s*\)'
            str = re.sub(pattern, r'\1', line)
            print(str)
            str = re.sub(pattern, r'\2', line)
            print(str)

    else:
        if pattern_number == 0:
            pattern = r'.*\s*-71\s+5\.2\.\S*\s+(.+)'
            str = re.sub(pattern, r'\1', line)
            print(str)

        elif pattern_number == 1:
            pattern = r'.*\s*Slot Length:\s+(.+)'
            str = re.sub(pattern, r'\1', line)
            print(str)

        elif pattern_number == 2:
            pattern = r'.*\s*Slot Scaling:\s+(.+),.+Offset'
            str = re.sub(pattern, r'\1', line)
            print(str)

        elif pattern_number == 3:
            pattern = r'.*\s*Slot Range:\s+(.+)Operational Range:.*'
            str = re.sub(pattern, r'\1', line)
            print(str)

        elif pattern_number == 4:
            pattern = r'.*\s*SPN:\s+(.+)'
            str = re.sub(pattern, r'\1', line)
            print(str)

        elif pattern_number == 5:
            print(str)


if __name__ == '__main__':

    pdf_document = r'C:\Users\green\Desktop\SAE_J1939-71.pdf'
    pdf_content = PdfReader(pdf_document)
    number_pages = len(pdf_content.pages)

    pattern_list_1 = [
        r'-71 5\.3\..+-.+',
        r'Data Length:\s+.+',
        r'Parameter Group\s+.+'
    ]
    pattern_list_2 =[
        r'.*\s*-71\s+5\.2\.\S*\s+.+',
        r'\s*Slot Length:\s+\.+',
        r'Slot Scaling:.+',
        r'Slot Range:.+',
        r'SPN:.+',
        r'\s*PGN Parameter Group Name and Acronym  Doc. and Paragraph.+|\s*Page 8 of 442 J1939 –71 Database Report April 15, 2001.+-71\s+5\.3\.\s*'
    ]

    pattern_lists =[
        pattern_list_1,
        pattern_list_2
    ]
    # list_pages = [5, 6, 7, 8, 120, 121, 122, 338, 339, 340, ]
    # for page_number in list_pages:
    #     page = pdf_content.pages[page_number]
    #     for line in  page.extract_text().split('\n'):
    #         print(line)
    #     print('______________________________________________________________________')


    for pattern_list in pattern_lists:
        pattern_number = 0
        for page_number in range(0, number_pages-1):
        #for page_number in list_pages:
            page = pdf_content.pages[page_number]
            split_page =  page.extract_text().split('\n')
            number_lines = len(split_page)
            line_number = 0
            while line_number < number_lines:
                line = split_page[line_number]
                if re.search(pattern_list[pattern_number], line):
                    save_to_database(pattern_list, pattern_number, line)
                    #print(line)
                    if pattern_list == pattern_lists[0]:
                        if pattern_number == 1:
                            pattern = r'\s*Data Length:\s+(.+)'
                            data_length = re.sub(pattern, r'\1', line)
                        elif pattern_number == 2:
                            pattern = r'\s*Parameter Group\s+(.+)\s+\(\s*(.+)\s*\)'
                            pgn = re.sub(pattern, r'\1', line)
                            id = re.sub(pattern, r'\2', line)
                            can_package = CAN_package(data_length=data_length, PGN=pgn, ID=id)
                            session.add(can_package)
                            session.commit()
                    else:
                        if pattern_number == 0:
                            pattern = r'.*\s*-71\s+5\.2\.\S*\s+(.+)'
                            name = re.sub(pattern, r'\1', line)
                        elif pattern_number == 1:
                            pattern = r'\s*Slot Length:\s+(.+)'
                            length = re.sub(pattern, r'\1', line)
                        elif pattern_number == 2:
                            pattern = r'\s*Slot Scaling:\s+(.+),.*'
                            scaling = re.sub(pattern, r'\1', line)
                        elif pattern_number == 3:
                            pattern = r'\s*Slot Range:\s+(.+)Operational Range:.*'
                            range = re.sub(pattern, r'\1', line)
                        elif pattern_number == 4:
                            pattern = r'\s*SPN:\s+(\d+)'
                            spn = re.sub(pattern, r'\1', line)
                        elif pattern_number == 5:
                            pattern = r'\s*PGN Parameter Group Name and Acronym  Doc. and Paragraph\s+(\d+).*-71\s+5\.3\.\S*\s*'
                            if re.search(pattern, line):
                                id_can = re.sub(pattern, r'\1', line)
                            else:
                                pattern = r'\s*Page 8 of 442 J1939 –71 Database Report April 15, 2001\s+(\d+).*-71\s+5\.3\.\S*\s*'
                                id_can = re.sub(pattern, r'\1', line)
                            parameter = Parameter(name=name, length=length, scaling=scaling, range=range, SPN=spn,
                                                  id_CAN=id_can)
                            session.add(parameter)
                            session.commit()

                    if pattern_number < len(pattern_list)-1:
                        pattern_number += 1
                    else:
                        pattern_number = 0
                        print('____________________________________________________________________')
                line_number += 1

session.close()
