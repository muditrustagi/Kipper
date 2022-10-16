# ----------- CORE ----------- #

# Author: Mudit Rustagi
# 06 April 2020
# 15:37


# --Hello_World --
#       If you dont know what this is about, give the README a glance.
#       If you would like to contribute, please do so freely.

from tkinter import filedialog
from tkinter import messagebox
from datetime import datetime
from langdetect import detect
from tkinter import *
import tkinter as tk
from os import walk
import webbrowser
import database
import os
import re


# Alternate the entry state according to button press
def edit():
    global folder
    if(folder["state"]=="normal"):
        folder.config(state='disabled')
    else:
        folder.config(state='normal')
        submit["state"]="normal"

# Reset the entry text
def reset():
    global texti,folder
    texti.set(" ")
    folder.config(state='disabled')
    submit["state"]="disabled"

# Browse ask directory functiality
def browse():
    global texti,filename
    filename = filedialog.askdirectory()
    texti.set(" "+filename)
    submit["state"]="normal"

# Deletes the file
def deleteIt(i):
    global lang
    for i in lang[i]:
        os.remove(i)

# Updates the timer clock every one second
def update_clock():
    global x
    endTime=datetime.now()
    elap=str(endTime-startTime)
    statusbar.config(text="  "+elap[2:-7])
    top.after(1000,update_clock)

# Ask closing confirmation
def on_closing():
    if(messagebox.askquestion (' KIPPER','Are you sure you want to quit?',icon = 'error')=='yes'):
        top.destroy()

# Get the list of files in a folder
def getListOfFiles(dirName):
    listOfFiles=[]
    for extension in database.EXTENSIONS:
        listOfFiles.extend([os.path.join(dirName,file) for file in os.listdir(dirName) if file.endswith('.'+extension)])
    return listOfFiles

# Submit button press functiality
def submit():
    global filename,lang,outcome,texti
    files=[]
    filename=texti.get()
    filename=filename.strip()
    # Get all the list of subdirectory in the folder
    subdirs = [x[0] for x in os.walk(filename)]
    for i in subdirs:
        x=getListOfFiles(i)
        files.extend(x)

    for filepath in files:
        # opening the file
        file = open(filepath, "r",encoding="utf8")
        lines = file.readlines()
        file.close()

        # Generating plain text with no extra characters (digits, etc)
        # Plain text easily detects the language
        # Using Regex expression
        text = ''
        for line in lines:
            if re.search('^[0-9]+$', line) is None and re.search('^[0-9]{2}:[0-9]{2}:[0-9]{2}', line) is None and re.search('^$', line) is None:
                text += ' ' + line.rstrip('\n')
            text = text.lstrip()

        # shrinking the text to 200 characters only
        text=text[max(0,len(text)-200):len(text)]

        # Find the language using detect in langdetect library
        res=detect(text)

        # Append the result values to variables
        try:
            lang[res].append(filepath)
        except:
            lang[res]=[filepath]
        outcome[res]=0
    # Calling a external window
    overlay()

# Hover Animation functions
def on_enter(e):
    e.widget['background'] = '#BCBABB'

def enter(e):
    e.widget['borderwidth']=1

def on_leave(e):
    e.widget['background'] = '#a19d9f'

def leave(e):
    e.widget['borderwidth']=0


# Generating a toplevel window for language selection
def overlay():
    # Generating a toplevel with all the langauges found

    global outcome
    
    # Top level window customization
    window = Toplevel(top)
    window.grab_set()
    window.geometry("380x350+600+300")
    window.iconbitmap(r"logo.ico")
    window.title("  KIPPER  :  Stay Relevant")
    window.resizable(width="false", height="false")

    # Adding Label
    sec = Label(window, text="Select the needed Languages: ")
    sec.place(x=20,y=20)

    # Adding Checkbutton in a 2X1 order using custom ordering
    j=0
    for i,machine in enumerate(outcome):
        outcome[machine] = IntVar()
        l = Checkbutton(window,text=database.LANGUAGES[machine], variable=outcome[machine])
        l.deselect()
        l.place(x=(40 if i%2==0 else 200),y=50+j*30)
        if i%2==1:
            j=j+1

    def delete():
        # Confirmation Box for operation
        if(messagebox.askquestion (' KIPPER','Are you sure you want to proceed?')=='yes'):
            # Kill the toplevel
            window.destroy()
            global outcome
            for i in outcome:
                if not outcome[i].get():
                    deleteIt(i)
        # Operation successful popup
        messagebox.showinfo (' KIPPER','Operation Successful')

    # Adding Save Button
    proceed=Button(window,text="SAVE SELECTED",height=1,width=20, bg='#a19d9f',command=delete)
    proceed.place(x=20,y=280)
    proceed.bind("<Enter>", on_enter)
    proceed.bind("<Leave>", on_leave)

    # Adding status bar     
    white=Frame(window,height=50,width=1000,bg="#fff")
    white.place(x=0,y=329)
    seperator=Frame(window,height=1,width=1000,bg="#ababab")
    seperator.place(x=0,y=328)

    # Adding copyright tag  static
    static= Button(window, bg="#fff",text="%s Mudit Rustagi " % (u"\N{COPYRIGHT SIGN}"), command =website,borderwidth=0,anchor=E)
    static.place(x=281,y=329)
    static.bind("<Enter>", enter)
    static.bind("<Leave>", leave)

    window.mainloop()

# Quick Links Added
def website():
    webbrowser.open_new_tab(database.WEBSITE)

def github():
    webbrowser.open_new_tab(database.GITHUB)

def about():
    webbrowser.open_new_tab(database.ABOUT)

def contribute():
    webbrowser.open_new_tab(database.CONTRIBUTE)

#--Start Main Code:

# filename: browsed file name
filename=""
# lang: computed languages in folder
lang={}
# outcome: langauges selected
outcome={}
# startime recorded for timer
startTime=datetime.now()

#The main window intialization  top
top = Tk()
top.geometry("550x216+600+300")
top.iconbitmap(r"logo.ico")
top.title("  KIPPER  :  Stay Relevant")
top.resizable(width="true", height="true")
top.after(1000,update_clock)
top.protocol("WM_DELETE_WINDOW", on_closing)

#Adding Menu Bar  menubar
menubar = Menu(top, tearoff=True)
menubar.add_command(label=" Website ",command=website)
menubar.add_command(label=" Github ",command=github)
menubar.add_command(label=" Contribute ",command=contribute)
menubar.add_command(label=" About ",command=about)
top.config(menu=menubar)

#Adding Seperator  seperator
seperator=Frame(top,height=1,width=1000,bg="#ababab")
seperator.place(x=0,y=0)

#Adding Browse Button  browse
browse = Button(text="Step 1: BROWSE", width=20,command=browse,bg='#a19d9f')
browse.place(x=20,y=20)
browse.bind("<Enter>", on_enter)
browse.bind("<Leave>", on_leave)

#Adding Entry  folder(variable  text)
texti = StringVar()
folder = Entry(top,width=65,textvariable=texti)
folder.config(state='disabled')
folder.insert(END, '')
folder.place(x=20, y=70)

#Adding Edit Button  editButton
editImage= PhotoImage(file = r"./icons/edit.gif").subsample(7)
editButton = Button(top, image = editImage,command=edit,borderwidth=0)
editButton.place(x=428,y=70)
editButton.bind("<Enter>", enter)
editButton.bind("<Leave>", leave)

#Adding Reset Button  resetButton
resetImage = PhotoImage(file = r"./icons/reset.gif").subsample(2)
resetButton = Button(top, image = resetImage,command=reset,borderwidth=0)
resetButton.place(x=450,y=70)
resetButton.bind("<Enter>", enter)
resetButton.bind("<Leave>", leave)

#Adding Submit Button  submit
submit=Button(top,text="Step 2: SUBMIT",height=1,width=20, bg='#a19d9f',command=submit)
submit.place(x=20,y=115)
submit.bind("<Enter>", on_enter)
submit.bind("<Leave>", on_leave)
submit["state"]="disabled"

#Adding white bar  white
white=Frame(top,height=50,width=1000,bg="#fff")
white.place(x=0,y=175)

#Adding Seperator  seperator
seperator=Frame(top,height=1,width=1000,bg="#ababab")
seperator.place(x=0,y=174)

#Adding timer statusbar
timer = PhotoImage(file = r"./icons/timer.gif").subsample(2,2)
statusbar = Label(top, text="  00:00",bg="#fff", image = timer,compound = LEFT, anchor=W)
statusbar.place(x=5,y=175)

#Adding copyright tag  static
static = Button(top, bg="#fff",text="%s Mudit Rustagi " % (u"\N{COPYRIGHT SIGN}"), command =website,borderwidth=0,anchor=E)
static.place(x=390,y=175)
static.bind("<Enter>", enter)
static.bind("<Leave>", leave)

#--End Main Code--
top.mainloop()
