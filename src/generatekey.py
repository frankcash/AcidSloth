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
import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 3000
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

gpg = gnupg.GPG(gnupghome='/home/user/gpghome')

def keyserv_export(key):
        ascii_armored_public_keys = gpg.export_keys(key)
        ascii_armored_private_keys = gpg.export_keys(key, True)
        print ascii_armored_private_keys
        with open('mykeyfile.asc', 'w') as f:
            f.write(ascii_armored_public_keys)
            f.write(ascii_armored_private_keys)
            
            
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
        unencrypted_string = string_to_encrypt
        print string_to_encrypt + "\n"
        encrypted_data = gpg.encrypt(unencrypted_string, "arelin@sas.upenn.edu")
        encrypted_string = str(encrypted_data)
        
        #print "reached"
        print encrypted_string
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))   
        s.send(encrypted_string)
        data = s.recv(BUFFER_SIZE)
        s.close()
        with open('/home/user/NetBeansProjects/decrypt/src/data.txt', 'w') as f:
            f.write(encrypted_string)

       
        decrypted_data = gpg.decrypt(encrypted_string, passphrase='password')
        print("decrypted:" + str(decrypted_data))

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
        name_email="arelin@sas.upenn.edu",
        passphrase="password")
        key = str(gpg.gen_key(input_data))
        keyserv_export(key)
        self.email = "arelin@sas.upenn.edu"
        gpg.send_keys('keyserv.ubuntu.com', key)
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

