from tkinter import *
from functools import partial
import algoritma as a
baslangic = 0
bitis = 0
def validateLogin(deger1, deger2):
    print("username entered :", deger1.get())
    print("password entered :", deger2.get())
    baslangic = int(deger1.get())
    bitis = int(deger2.get())
    tkWindow.destroy()
    a.main(baslangic,bitis)
    return

#window
tkWindow = Tk()
tkWindow.geometry('280x280')
tkWindow.title('Q LEARNING')

#username label and text entry box
usernameLabel = Label(tkWindow, text="Başlangıç Indexi").grid(row=4, column=0)
username = StringVar()
usernameEntry = Entry(tkWindow, textvariable=username).grid(row=4, column=1)

#password label and password entry box
passwordLabel = Label(tkWindow,text="Bitiş Indexi").grid(row=5, column=0)
password = StringVar()
passwordEntry = Entry(tkWindow, textvariable=password).grid(row=5, column=1)

validateLogin = partial(validateLogin, username, password)

#login button
loginButton = Button(tkWindow, text="Oyna", command=validateLogin).grid(row=7, column=1)


tkWindow.mainloop()