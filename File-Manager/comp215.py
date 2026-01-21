#!/usr/bin/env python3

from tkinter import *
from tkinter import filedialog, messagebox, simpledialog
from os.path import *
from os import listdir, mkdir

fileList = None
currentDir = None
textEditor = None
currentFile = None

BG_COLOR = "#2b2b2b"
FG_COLOR = "#ffffff"
ACCENT_COLOR = "#4a9eff"
BUTTON_BG = "#3c3c3c"
BUTTON_FG = "#ffffff"
LISTBOX_BG = "#1e1e1e"
EDITOR_BG = "#1e1e1e"

def chooseDir():
	global currentDir
	global fileList

	directory = filedialog.askdirectory()
	if directory:
		currentDir = directory
		loadDirectory(directory)
		currentDirLabel.config(text=currentDir)

def loadDirectory(directory):
	global fileList

	fileList.delete(0, END)
	files = listdir(directory)
	for file in files:
		if file[0] != '.':
			fileList.insert(END, file)


def	onDoubleClick(event):
	global currentDir
	global currentFile
	global textEditor

	selection = fileList.curselection()
	if not selection:
		return
	item = fileList.get(selection[0])
	fullPath = join(currentDir, item)
	if isdir(fullPath):
		currentDir = fullPath
		loadDirectory(currentDir)
		currentDirLabel.config(text=currentDir)
	else:
		try:
			file = open(fullPath, "r")
			currentFile = fullPath
			content = file.read()
			textEditor.delete(1.0, END)
			textEditor.insert(1.0, content)
			textEditorFrame.pack(side=LEFT, fill=BOTH, expand=True)
			editorButtonsFrame.pack(side=BOTTOM, fill=X, padx=5, pady=5)
			file.close()
		except Exception:
			messagebox.showerror("Error", "Cannot open this file.")

def saveFile():
	global currentFile
	if currentFile:
		try:
			content = textEditor.get(1.0, END)
			with open(currentFile, "w") as file:
				file.write(content)
			messagebox.showinfo("Success", "File saved!")
		except Exception:
			messagebox.showerror("Error", "Cannot save file")

def goBack():
	global currentDir
	if currentDir:
		parentDir = dirname(currentDir)
	if parentDir != currentDir:
		currentDir = parentDir
		loadDirectory(currentDir)
		currentDirLabel.config(text=currentDir)

def closeFile():
	global currentFile
	currentFile = None
	textEditorFrame.pack_forget()
	editorButtonsFrame.pack_forget()
	textEditor.delete(1.0, END)

def	createDir():
	global currentDir

	if not currentDir:
		messagebox.showerror("Error", "Choose a directory first")
		return
	try:
		dirName = simpledialog.askstring("New Folder", "Enter folder name:")
		if dirName:
			mkdir(join(currentDir, dirName))
			loadDirectory(currentDir)
	except Exception:
		messagebox.showerror("Error", "Could not create folder")

def	createFile():
	global currentDir

	if not currentDir:
		messagebox.showerror("Error", "Choose a directory first")
		return
	try:
		fileName = simpledialog.askstring("New File", "Enter file name:")
		fullPath = join(currentDir, fileName)
		with open(fullPath, "w") as f:
			pass
		loadDirectory(currentDir)
	except Exception:
		messagebox.showerror("Error", "Could not create file")

root = Tk()
root.title("File explorer")
root.geometry("1200x700")
root.configure(bg="#2b2b2b") 

topBar = Frame(root, bg=BG_COLOR)
topBar.pack(fill="x", padx=5, pady=5)
middleFrame = Frame(root, bg=BG_COLOR)
middleFrame.pack(fill=BOTH, expand=True, padx=5, pady=5)
textEditorFrame = Frame(middleFrame, bg=BG_COLOR)
editorButtonsFrame = Frame(middleFrame, bg=BG_COLOR)

fileList = Listbox(middleFrame, width=50, height=20, bg=LISTBOX_BG, fg=FG_COLOR)
fileList.bind("<Double-Button-1>", onDoubleClick)

dirButton = Button(root, text="Choose Directory", command=chooseDir, bg=ACCENT_COLOR, fg=BUTTON_FG)

backButton = Button(root, text="← Back", command=goBack, bg=BUTTON_BG, fg=BUTTON_FG)

currentDirLabel = Label(root, text="No directory selected", fg=ACCENT_COLOR, bg=BG_COLOR)

NewDirButton = Button(root, text="📁 New Folder", command=createDir, bg=BUTTON_BG, fg=BUTTON_FG)

NewFile = Button(root, text="📄 New File", command=createFile, bg=BUTTON_BG, fg=BUTTON_FG)

textEditor = Text(textEditorFrame, width=80, height=30, bg=EDITOR_BG, fg=FG_COLOR)
textEditor.pack(fill=BOTH, expand=True)

saveButton = Button(editorButtonsFrame, text="💾 Save", command=saveFile, bg=ACCENT_COLOR, fg=BUTTON_FG)
saveButton.pack(side=LEFT, padx=5)

closeButton = Button(editorButtonsFrame, text="✖ Close", command=closeFile, bg="#ff4444", fg=BUTTON_FG)
closeButton.pack(side=LEFT, padx=5)

backButton.pack(in_=topBar, side=LEFT)
currentDirLabel.pack(in_=topBar, side=LEFT, expand=True, padx=10)
dirButton.pack(in_=topBar, side=RIGHT, padx=5)
NewDirButton.pack(in_=topBar, side=RIGHT, padx=5)
NewFile.pack(in_=topBar, side=RIGHT, padx=5)

fileList.pack(in_=middleFrame, side=LEFT, fill=BOTH, expand=False)

root.mainloop()
