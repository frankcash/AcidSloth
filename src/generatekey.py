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
TCP_PORT = 3009
BUFFER_SIZE = 1024

gpg = gnupg.GPG(gnupghome='~/gpghome')

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
        s.send("It is a melancholy object to those, who walk through this great town, or travel in the country, when they see the streets, the roads and cabbin-doors crowded with beggars of the female sex, followed by three, four, or six children, all in rags, and importuning every passenger for an alms. These mothers instead of being able to work for their honest livelihood, are forced to employ all their time in stroling to beg sustenance for their helpless infants who, as they grow up, either turn thieves for want of work, or leave their dear native country, to fight for the Pretender in Spain, or sell themselves to the Barbadoes.I think it is agreed by all parties, that this prodigious number of children in the arms, or on the backs, or at the heels of their mothers, and frequently of their fathers, is in the present deplorable state of the kingdom, a very great additional grievance; and therefore whoever could find out a fair, cheap and easy method of making these children sound and useful members of the common-wealth, would deserve so well of the publick, as to have his statue set up for a preserver of the nation.But my intention is very far from being confined to provide only for the children of professed beggars: it is of a much greater extent, and shall take in the whole number of infants at a certain age, who are born of parents in effect as little able to support them, as those who demand our charity in the streets.As to my own part, having turned my thoughts for many years, upon this important subject, and maturely weighed the several schemes of our projectors, I have always found them grossly mistaken in their computation. It is true, a child just dropt from its dam, may be supported by her milk, for a solar year, with little other nourishment: at most not above the value of two shillings, which the mother may certainly get, or the value in scraps, by her lawful occupation of begging; and it is exactly at one year old that I propose to provide for them in such a manner, as, instead of being a charge upon their parents, or the parish, or wanting food and raiment for the rest of their lives, they shall, on the contrary, contribute to the feeding, and partly to the cloathing of many thousands.But in order to justify my friend, he confessed, that this expedient was put into his head by the famous Salmanaazor, a native of the island Formosa, who came from thence to London, above twenty years ago, and in conversation told my friend, that in his country, when any young person happened to be put to death, the executioner sold the carcass to persons of quality, as a prime dainty; and that, in his time, the body of a plump girl of fifteen, who was crucified for an attempt to poison the Emperor, was sold to his imperial majesty prime minister of state, and other great mandarins of the court iSome persons of a desponding spirit are in great concern about that vast number of poor people, who are aged, diseased, or maimed; and I have been desired to employ my thoughts what course may be taken, to ease the nation of so grievous an incumbrance. But I am not in the least pain upon that matter, because it is very well known, that they are every day dying, and rotting, by cold and famine, and filth, and vermin, as fast as can be reasonably expected. And as to the young labourers, they are now in almost as hopeful a condition. They cannot get work, and consequently pine away from want of nourishment, to a degree, that if at any time they are accidentally hired to common labour, they have not strength to perform it, and thus the country and themselves are happily delivered from the evils to come.I have too long digressed, and therefore shall return to my subject. I think the advantages by the proposal which I have made are obvious and many, as well as of the highest importance.")
        data = s.recv(BUFFER_SIZE)
        s.close()
        #with open('/home/user/NetBeansProjects/decrypt/src/data.txt', 'w') as f:
        #    f.write(encrypted_string)

       
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

        gpg = gnupg.GPG(gnupghome='~/gpghome')
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

