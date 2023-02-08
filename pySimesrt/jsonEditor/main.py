import tkinter as tk
from tkinter import filedialog as fd
import requests
import json
import time

win = tk.Tk()
win.title("translate")
win.geometry("1000x800")

# print(requests.get("http://kappa.cs.petrsu.ru/~dimitrov/info_1/22_23/test.json").text)
def loadJson():
    # print(first_text.get(1.0, "end"))
    data = requests.get(first_text.get(1.0, "end").replace("\n","")).text
    try:
        trans_text.delete('1.0', "end")
    except:
        pass
    trans_text.insert("end",data)

    # print(data)

def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True

def ChekCorrect():
    if validateJSON(trans_text.get(1.0, "end")):
        infoL.config(text="JSON Valid")
    else:
        infoL.config(text="Not valid")

def SaveJson():

    foldername = fd.asksaveasfilename()
    with open(foldername,"w") as f:
        f.write(trans_text.get(1.0, "end"))
    infoL.config(text="Ok save")

textbox = tk.Frame(win)
textbox.pack(side="left", fill="y")

first_text = tk.Text(textbox, width=100, height=2)
first_text.pack()

trans_text = tk.Text(textbox, width=100, height=30)
trans_text.pack()

b = tk.Button(textbox, text="Chek Correct", command=ChekCorrect)
b.pack()
infoL = tk.Label(textbox, text="----")
infoL.pack()
b = tk.Button(textbox, text="Save", command=SaveJson)
b.pack()

transbox = tk.Frame(win)
transbox.pack(side="right", fill="y")

urlb = tk.Button(transbox, text="Load JSON", command=loadJson)
urlb.pack()

win.mainloop()