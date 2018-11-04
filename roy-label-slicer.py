from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from glob import glob
from PyPDF2 import PdfFileReader, PdfFileWriter
from copy import copy
from os import path
from os.path import splitext
import os
import shutil
import datetime
import time

# if document exists set destinatioin to document or else set it to current
#https://yagisanatode.com/2018/03/10/how-to-check-a-users-home-directory-for-a-folder-python-3/
home = os.path.expanduser('~')
location = os.path.join(home, 'Documents')
folder_check = os.path.isdir(location)
if(folder_check):
	destination = location
else:
	destination = "."

root = Tk()

root.geometry("400x350")
root.resizable(width=False, height=False)
root.grid_columnconfigure(0, weight=1)
root.title('Amz Label Slicer')
root.iconbitmap("assets/images/icon.ico")
root.configure(background='#30353B')
folder_path = StringVar()

#Browse File
def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
	button2.config(bg="#e0e0e0",state=DISABLED)
	global folder_path
	filename = filedialog.askopenfilename(filetypes=[('Label Zip', '*.zip'), ('Label PDF', '*.pdf')])
	folder_path.set(filename)
	if filename:
		button2.config(state=NORMAL, bg="#ff7530")

def find_ext(dr, ext, ig_case=False):
    if ig_case:
        ext =  "".join(["[{}]".format(
                ch + ch.swapcase()) for ch in ext])
    return glob(path.join(dr, "*." + ext))

#Start Conversion
def slice_pdf():
	start = time.time()
	timeStamp = datetime.datetime.now()
	original_path = "./original-" + str(timeStamp.strftime("%Y-%m-%d_%H-%M-%S")) + "/"
	cropped_path = destination + "/sliced-labels-"+ str(timeStamp.strftime("%Y-%m-%d")) +"/"
	global folder_path

	# Clear old folders
	if not os.path.exists(cropped_path) and not os.path.isdir(cropped_path):
		os.makedirs(cropped_path)
	os.makedirs(original_path)


	# Find the file type
	file_name, extension = splitext(folder_path.get())

	if extension == ".zip":
		import zipfile
		zip_ref = zipfile.ZipFile(folder_path.get(), 'r')
		zip_ref.extractall(original_path)
		zip_ref.close()
	else:
		shutil.copy(folder_path.get(), original_path + os.path.basename(folder_path.get()))

	pdfs = find_ext(original_path,"pdf",True)

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
		filename_w_ext = os.path.basename(single)
		file_name, extension = splitext(filename_w_ext)
		currentDT = datetime.datetime.now()
		outstream = open(cropped_path + file_name + "-" + str(currentDT.strftime("%Y-%m-%d_%H-%M-%S")) + extension, 'wb')
		writer.write(outstream)
		outstream.close()
	button2.config(state=DISABLED,  bg="#e0e0e0")
	folder_path.set('')
	if os.path.exists(original_path) and os.path.isdir(original_path):
		shutil.rmtree(original_path)
	end = time.time()
	messagebox.showinfo("Successful", str(len(pdfs)) + " PDFs Sliced in " + str(round((end - start), 2)) + " secs")

title = Label(root, pady=10, text="AMZ LABEL SLICER", bg="#1B1E22", fg="#FFFFFF", font=("Impact", 24))
title.grid(columnspan=2, sticky=W+E, pady=(0, 10))
browseButtonImage = PhotoImage(file='./assets/images/button.png')
button1 = Button(root,  fg="#ffffff", image=browseButtonImage, bg="#30353B", cursor="hand2", borderwidth=0, activebackground="#30353B", compound=CENTER,  command=browse_button)
button2 = Button(root, borderwidth=0, height=3, width=20, font=('Arial', 12), state=DISABLED, text="Slice Labels", bg="#e0e0e0", cursor="hand2", fg="#ffffff",command=slice_pdf)
button2 = Button(root, borderwidth=0, height=3, width=20, font=('Arial', 12), state=DISABLED, text="Slice Labels", bg="#e0e0e0", cursor="hand2", fg="#ffffff",command=slice_pdf)


button1.grid(row=1,column=0, sticky=E+W, padx=(10, 10), pady=(0, 20))
button2.grid(row=2,column=0, padx=(10, 10))

lbl1 = Label(master=root,textvariable=folder_path, bg="#30353B", fg="#fff")
lbl1.grid(columnspan=2, padx=(20, 20), pady=(20, 20))

ll = Label(root, text='Author: Shibnath Roy', bg="#1f4560", fg="#ffffff")
ll.place(relx=0.0, rely=1.0, anchor='sw')

root.mainloop()