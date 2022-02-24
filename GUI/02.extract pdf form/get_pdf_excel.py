import pdfplumber
from openpyxl import Workbook

with pdfplumber.open(
        'C:/Users/xh411/Documents/WXWork/1688851257484603/Cache/File/2022-02/12. DESEMBER 2021/12. REKENING KORAN - BNI ESCROW - 01 DES 2021.pdf') as pdf:
    all_table = []
    for page in range(1):
        page01 = pdf.pages[page]
        table = page01.extract_table()
        all_table.append(table)
    workbook = Workbook()
    sheet = workbook.active
    for table in all_table:
        for row in table:
            print(row[-1])
            sheet.append(row)
    workbook.save(
        filename='C:/Users/xh411/Documents/WXWork/1688851257484603/Cache/File/2022-02/12. DESEMBER 2021/12. REKENING KORAN - BNI ESCROW - 01 DES 2021.xlsx')
