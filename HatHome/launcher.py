from tkinter import *

class obj:

    def selection():
        select = l.curselection()


window = Tk()
l = Listbox(window,exportselection=0,height=2)
l.insert(1, "1920x1080")
l.insert(2, "1440x900")

l.pack()

but=Button(window, text="Fermer", command=obj.selection)
but.pack()



window.mainloop()
