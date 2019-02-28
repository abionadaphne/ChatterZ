import socket
#from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter import messagebox
#from tkinter import dialogbox
def receive():
   
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg )
        except OSError: 
            break
#def login():


def send(event=None):  
    
    msg = my_msg.get()
    my_msg.set("")  
    if len(msg)>20:
      messagebox.showinfo('Limit Exceeded','Limit Exceeded')

      #client_socket.send(bytes(msg, "utf8"))
      #if msg == "{quit}":
         #client_socket.close()
         #top.quit()
    else:
         client_socket.send(bytes(msg, "utf8"))
         if msg == "{quit}":
          client_socket.close()
          top.quit()
 
         #messagebox.showinfo('Limit Exceeded','Limit Exceeded')



def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()

top = tkinter.Tk()
top.title("ChatterZ")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame) 
msg_list = tkinter.Listbox(messages_frame, height=15, width=50,xscrollcommand=scrollbar.set, yscrollcommand=scrollbar.set,bg="cyan",fg="black",font="italic")
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

HOST = socket.gethostname()
IP = socket.gethostbyname(HOST)
PORT = 9528

BUFSIZ = 1024
ADDR = (IP, PORT)

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect(ADDR)


send_thread = Thread(target=send)
send_thread.start()
recv_thread = Thread(target=receive)          
recv_thread.start()

tkinter.mainloop() 
