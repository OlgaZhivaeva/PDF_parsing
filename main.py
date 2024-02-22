import re
from PyPDF2 import PdfReader
from db_connection import *
from models import drop_tables, create_tables, CAN_package, Parameter
from tqdm import tqdm

drop_tables(engine)
create_tables(engine)


if __name__ == '__main__':

    pdf_content = PdfReader(pdf_document)
    number_pages = len(pdf_content.pages)

    pattern_list_1 = [
        r'.*-71\s+5\.3\.\S+\s+(.+)-.+',
        r'.*Data Length:\s+(.+)',
        r'.*Parameter Group\s+(.+)\s+\(\s*(.+)\s*\)'
    ]

    pattern_list_2 =[
        r'.*-71\s+5\.2\.\S*\s+(.+)',
        r'.*Slot Length:\s+(.+)',
        r'.*Slot Scaling:\s+(.+),.+Offset',
        r'.*Slot Range:\s+(.+)Operational Range:.*',
        r'.*SPN:\s+(.+)',
        r'.*PGN Parameter Group Name and Acronym  Doc. and Paragraph\s+(\d+).*-71\s+5\.3\.\S*\s*|/'
        r'\s*Page\s+\d+\s+/of 442 J1939 –71 Database Report April 15, 2001\s*(\d+).*-71\s+5\.3\.\S*\s*'
    ]

    pattern_lists =[
        pattern_list_1,
        pattern_list_2
    ]

    for pattern_list in pattern_lists:
        pattern_number = 0
        for page_number in tqdm(range(0, number_pages)):
            page = pdf_content.pages[page_number]
            split_page =  page.extract_text().split('\n')
            number_lines = len(split_page)
            line_number = 0
            while line_number < number_lines:
                line = split_page[line_number]
                if re.search(pattern_list[pattern_number], line):
                    if pattern_list == pattern_lists[0]:
                        if pattern_number == 1:
                            data_length = re.sub(pattern_list[pattern_number], r'\1', line)
                        elif pattern_number == 2:
                            pgn = re.sub(pattern_list[pattern_number], r'\1', line)
                            id = re.sub(pattern_list[pattern_number], r'\2', line)
                            can_package = CAN_package(data_length=data_length, PGN=pgn, ID=id)
                            session.add(can_package)
                            session.commit()
                    else:
                        if pattern_number == 0:
                            name = re.sub(pattern_list[pattern_number], r'\1', line)
                        elif pattern_number == 1:
                            length = re.sub(pattern_list[pattern_number], r'\1', line)
                        elif pattern_number == 2:
                            scaling = re.sub(pattern_list[pattern_number], r'\1', line)
                        elif pattern_number == 3:
                            range = re.sub(pattern_list[pattern_number], r'\1', line)
                        elif pattern_number == 4:
                            spn = re.sub(pattern_list[pattern_number], r'\1', line)
                        elif pattern_number == 5:
                            pattern = r'.*PGN Parameter Group Name and Acronym  Doc. and Paragraph\s+(\d+).*-71\s+5\.3\.\S*\s*'
                            if re.search(pattern, line):
                                id_can = re.sub(pattern, r'\1', line)
                            else:
                                pattern = r'\s*Page\s+\d+\s+of 442 J1939 –71 Database Report April 15, 2001\s*(\d+).*-71\s+5\.3\.\S*\s*'
                                id_can = re.sub(pattern, r'\1', line)
                            parameter = Parameter(name=name, length=length, scaling=scaling, range=range, SPN=spn,
                                                  id_CAN=id_can)
                            session.add(parameter)
                            session.commit()
                    if pattern_number < len(pattern_list)-1:
                        pattern_number += 1
                    else:
                        pattern_number = 0
                line_number += 1

session.close()
