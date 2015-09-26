# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "user"
__date__ = "$Sep 26, 2015 7:51:18 AM$"

import gnupg


from Tkinter import Tk, RIGHT, BOTH, RAISED, Text, END
from ttk import Frame, Button, Style
import os
import gnupg

class SDR(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        self.parent = parent
        
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
        encrypted_data = gpg.encrypt(unencrypted_string, 'arelin@sas.upenn.edu')
        encrypted_string = str(encrypted_data)
        print  encrypted_string
       

def main():
  
    root = Tk()
    root.geometry("800x600+300+300")
    app = SDR(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  
