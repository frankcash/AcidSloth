# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "user"
__date__ = "$Sep 26, 2015 7:51:18 AM$"

import gnupg


from Tkinter import Tk, RIGHT, BOTH, RAISED, Text, END, Toplevel, Label, Entry
from ttk import Frame, Button, Style
import os
import gnupg

class SDR(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        self.parent = parent
        self.email = 'arelin@sas.upenn.edu'
        self.initUI()
        
    def initUI(self):
     
        self.parent.title("Send Message")
        self.style = Style()
        self.style.theme_use("default")
        self.e = Text(self)
        self.e.pack(expand = 1, fill= BOTH)
        #frame = Frame(self, relief=RAISED, borderwidth=1)
        #frame.pack(fill=BOTH, expand=1)
        
        self.pack(fill=BOTH, expand=1)
        
        createButton = Button(self, text="New User", command=self.create_key)
        createButton.pack(side=RIGHT, padx=5, pady=5)
        closeButton = Button(self, text="Clear", command=self.clear_text)
        closeButton.pack(side=RIGHT, padx=5, pady=5)
        okButton = Button(self, text="Send", command=self.send_text)
        okButton.pack(side=RIGHT)
        
        
        
    def clear_text(self):
        self.e.delete(1.0, END)

    def send_text(self):
        string_to_encrypt = self.e.get("1.0",END)
        gpg = gnupg.GPG(gnupghome='/home/user/gpghome')
        unencrypted_string = string_to_encrypt
        print string_to_encrypt + "\n"
        encrypted_data = gpg.encrypt(unencrypted_string, self.email)
        encrypted_string = str(encrypted_data)
        print  encrypted_string
       
    def create_key(self):
        top = self.top = Toplevel(self.parent)
        top.wm_title("New User")
        
        Label(top, text="Email").pack()
        

        self.g = Entry(top)

        self.g.pack(padx=5)
        Label(top, text="Password").pack()
        self.e = Entry(top, show="*")
        self.e.pack(padx=5)
        
        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)
        c = Button(top, text="Cancel", command=self.exitC)
        c.pack(pady=5)

    def ok(self):

        gpg = gnupg.GPG(gnupghome='/home/user/gpghome')
        input_data = gpg.gen_key_input(
        name_email=self.e.get(),
        passphrase=self.g.get())
        key = gpg.gen_key(input_data)
        print key

        self.top.destroy()
        
    def exitC(self):
        self.top.destroy()

def main():
  
    root = Tk()
    root.geometry("800x600+300+300")
    app = SDR(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  

