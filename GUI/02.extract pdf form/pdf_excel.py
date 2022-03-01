from PyPDF2 import PdfFileReader, PdfFileWriter
import get_file_name

file_write = PdfFileWriter()
filename = get_file_name.get_file_nema()

for page in filename:
    file_reader = PdfFileReader(
        "C:/Users/xh411/Documents/WXWork/1688851257484603/Cache/File/2022-02/12. DESEMBER 2021/{}".format(page))
    for pages in range(file_reader.getNumPages()):
        file_write.addPage(file_reader.getPage(pages))

with open("C:/Users/xh411/Documents/WXWork/1688851257484603/Cache/File/2022-02/12. DESEMBER 2021/合并.pdf", 'wb') as out:
    file_write.write(out)
