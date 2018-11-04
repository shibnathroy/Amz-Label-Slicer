from PyPDF2 import PdfFileReader, PdfFileWriter
from copy import copy
from os import path
import os
from glob import glob

import zipfile
zip_ref = zipfile.ZipFile('labels.zip', 'r')
zip_ref.extractall('./original')
zip_ref.close()

def find_ext(dr, ext, ig_case=False):
    if ig_case:
        ext =  "".join(["[{}]".format(
                ch + ch.swapcase()) for ch in ext])
    return glob(path.join(dr, "*." + ext))

pdfs = find_ext("./original/","pdf",True)

for index, single in enumerate(pdfs):
	reader = PdfFileReader(single, 'r')
	reader.getNumPages()

	writer = PdfFileWriter()

	for i in range(reader.getNumPages()):
		base_page = reader.getPage(i)
		page = copy(base_page)
		page1 = copy(base_page)
		page.cropBox.setLowerLeft((15, 420))
		page.cropBox.setUpperRight((228, 800))
		
		page1.cropBox.setLowerLeft((15, 63))
		page1.cropBox.setUpperRight((500, 400))

		writer.addPage(page)
		writer.addPage(page1.rotateCounterClockwise(-90))

	outstream = open('./cropped/' + os.path.basename(single), 'wb')
	writer.write(outstream)
	outstream.close()


