from ast import Lambda
from cProfile import label
from concurrent.futures import thread
import socket
from threading import Thread
from tkinter import *

# nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address, port))

print("Connected with the server...")

class GUI:
    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw()

        self.login = Toplevel()
        self.login.title("Login")

        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=300)
        
        self.pls = Label(self.login,
					text = "Please login to continue",
					justify = CENTER,
					font = "Helvetica 14 bold")
        self.pls.place( relheight = 0.15,
                        relx = 0.2,
                        rely = 0.07)

        self.labelName = Label(self.login,
							text = "Name: ",
							font = "Helvetica 12")
        self.labelName.place(   relheight = 0.2,
							    relx = 0.1,
							    rely = 0.2)

        self.entryName = Entry(self.login,
							font = "Helvetica 14")
        self.entryName.place(relwidth = 0.4,
							relheight = 0.12,
							relx = 0.35,
							rely = 0.2)
        self.entryName.focus()

        self.go = Button(self.login,
						text = "CONTINUE",
						font = "Helvetica 14 bold",
						command = lambda: self.goAhead(self.entryName.get()))
        self.go.place(  relx = 0.4,
					    rely = 0.55)
        
        self.Window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        #self.name = name
        self.layout(name)
        rcv = Thread(target=self.receive)
        rcv.start()

    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message == 'NICKNAME':
                    client.send(self.name.encode('utf-8'))
                else:
                    self.show_msg(message)
            except:
                print("An error occured!")
                client.close()
                break

    def layout(self,name):
        self.name = name
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False,height=False)
        self.Window.configure(width=470,height=550,bg="#17202a")
        self.labelhead = Label(self.Window,bg="#FFF001",fg="#000000",text=self.name,font="helvetica 15 bold",pady=5)
        self.labelhead.place(relwidth=1)
        self.line = Label(self.Window,width=450,bg="#abb2b9")
        self.line.place(relwidth=1,rely=0.07,relheight=0.012)
        self.textCons = Text(self.Window,width=20,height=2,bg="#17202a",fg="#eaecee",padx=5,pady=5)
        self.textCons.place(relheight=0.045,relwidth=1,rely=0.08)
        self.labelbottom = Label(self.Window,bg="#2c3e50",height=80)
        self.labelbottom.place(relwidth=1,rely=0.825)
        self.entrymsg = Entry(self.labelbottom,bg="#FFF000",fg="#FF0001",font="Helvetica bold 15")
        self.entrymsg.place(relwidth=0.74,relheight=0.06,rely=0.008,relx=0.001)
        self.entrymsg.focus()
        self.buttonmsg = Button(self.labelbottom,text="Send",font="Helvetica 10 bold",width=20,bg="#abb2b9",command=lambda:self.sendbutton(self.entrymsg.get()))
        self.buttonmsg.place(relx=0.77,rely=0.008,relheight=0.06,relwidth=0.22)
        self.textCons.config(cursor="arrow")
        scrollbar = Scrollbar(self.textCons)
        scrollbar.place(relheight=1,relx=0.974)
        scrollbar.config(command=self.textCons.yview)
        self.cons.config(state=DISABLED)

    def sendbutton(self,msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entrymsg.delete(0,END)
        snd = Thread(target=self.write)
        snd.start()

    def showmsg(self,msg):
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END,msg+"\n\n")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

    def write(self):
        self.textCons.config(state=DISABLED)
        while True:
            msg=(f"{self.name}:{self.msg}")
            client.send(msg.encode('utf-8'))
            self.show_msg(msg)
            break
g = GUI()

# def write():
#     while True:
#         message = '{}: {}'.format(nickname, input(''))
#         client.send(message.encode('utf-8'))

# receive_thread = Thread(target=receive)
# receive_thread.start()
# write_thread = Thread(target=write)
# write_thread.start()
