import customtkinter as ctk
import tkinter  as tk
from PIL import Image as img
import os
from my_fn import * # imported functions from my_fn.py(currently is a copy of kdad.ipynb). needs modifications to work properly here 

class App(ctk.CTk):  
    
    def __init__(self, *args, **kwargs):  
        
        # initialisation of window 
        super().__init__()
        self.geometry("960x540") # size of window Width x Height
        self.minsize(960,540) # also W*H. either of w or h cannot go below it
        self.maxsize(1920,1080) 
        self.title("WIP") 
        container = ctk.CTkFrame(self) # container to hold frames
        container.pack(side="top", fill="both", expand = True) # expand container to cover entire window
        container.grid_rowconfigure(0, weight=1) # setting layout of grids in container
        container.grid_columnconfigure(0, weight=1)  

        self.frames = {}  # dictionary of key=name of frame class, value= frame object of for that name
        for F in (LoginPage, DoWhatPage, SlicerPage, SendPage, ReadPage):  
  
            frame = F(container, self)  
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(LoginPage) # frame shown on startup
  
    def show_frame(self, cont):    
        frame = self.frames[cont]  # frame redraw function
        frame.tkraise()  

class LoginPage(ctk.CTkFrame):  # login page(also the startup page)
  
    def __init__(self, parent, controller):  
        #--------------------------------------------------------------
        # this part is same in all frames

        ctk.CTkFrame.__init__(self,parent)  # initialsation

        # grid setup. creates a 16*9 grid. used to place widgets
        # also makes the grid's cells scale with window size 
        for col in range(16):
            self.columnconfigure(col, weight=1)
        for row in range(9):
            self.rowconfigure(row, weight=1)
    

        # this part is same in all frames 
        #-------------------------------------------------------------- 

        # widgets. order of writing does not matter.
        label = ctk.CTkLabel(self, text="LOG IN",font = ("Gotham Rounded Medium",22))  

        line_img = ctk.CTkImage(light_image=img.open("line.png"),dark_image=img.open("line.png"),size=(60, 2))
        image_label = ctk.CTkLabel(self, image=line_img, text="")
        
        email_entry = ctk.CTkEntry(self, placeholder_text="Email address",font = ("Gotham Rounded Medium",14))
        password_entry = ctk.CTkEntry(self, placeholder_text="Password",font = ("Gotham Rounded Medium",14),show='*')

        log_var = tk.StringVar()
        log_ok = ctk.CTkLabel(self, textvariable=log_var,font = ("Gotham Rounded Medium",14))  

        #controller.show_frame(DoWhatPage) code to go to page

        button = ctk.CTkButton(self, text="LOG IN",command=lambda: [makeglobal(email_entry.get(),password_entry.get()),trylogin(email_entry.get(),password_entry.get(),controller,DoWhatPage,log_var,email_entry,password_entry)],font = ("Gotham Rounded Medium",16),corner_radius=60,fg_color='#187d36',hover_color='#22b14c') 

    
        # widget placement. order of writing does not matter. 
        label.grid(column=6,sticky="sew",row=1,padx=5,columnspan=4) # column and columnspan are finicky. temporary values used currently
        image_label.grid(column=6,sticky="new",row=2,padx=5,columnspan=4) # n-north e-east w-west s-south 
        email_entry.grid(column=6,sticky="ew",row=3,padx=5,columnspan=4,ipadx=5,ipady=5)
        log_ok.grid(column=6,sticky="new",row=5,padx=5,columnspan=4,ipadx=5,ipady=5)
        password_entry.grid(column=6,sticky="new",row=4,padx=5,columnspan=4,ipadx=5,ipady=5)
        button.grid(row=6,column=6,ipadx=5,ipady=5,columnspan=4, sticky="we") # news are used to make the widgets expand in the cell in that direction. 
        def makeglobal(email,password):
            global emailid
            global pass_word
            emailid=email
            pass_word=password
            print(emailid,pass_word)
        
class SlicerPage(ctk.CTkFrame):
  
    def __init__(self, parent, controller):  
        ctk.CTkFrame.__init__(self,parent)  # initialsation
    
        # grid setup. creates a 16*9 grid. used to place widgets
        # also makes the grid's cells scale with window size 
        for col in range(16):
            self.columnconfigure(col, weight=1)
        for row in range(9):
            self.rowconfigure(row, weight=1)

        # widgets
        label = ctk.CTkLabel(self, text="EMAIL SLICING",font = ("Gotham Rounded Medium",22))  
        
        line_img = ctk.CTkImage(light_image=img.open("line.png"),dark_image=img.open("line.png"),size=(130, 2))
        image_label = ctk.CTkLabel(self, image=line_img, text="")
        
        email_entry = ctk.CTkEntry(self, placeholder_text="Email address",font = ("Gotham Rounded Medium",14))
        
        name = ctk.CTkLabel(self, text="name :",font = ("Gotham Rounded Medium",14),anchor="e") 
        dom = ctk.CTkLabel(self, text="domain :",font = ("Gotham Rounded Medium",14),anchor="e") 
        fail = ctk.CTkLabel(self, text="",font = ("Gotham Rounded Medium",14)) 
        
        nameval = ctk.CTkLabel(self, text="",font = ("Gotham Rounded Medium",14),anchor="w") 
        domval = ctk.CTkLabel(self, text="",font = ("Gotham Rounded Medium",14),anchor="w") 
        
        button = ctk.CTkButton(self, text="SLICE",command=lambda: splitandverify(email_entry.get(),nameval,domval,fail),fg_color='#187d36',hover_color='#22b14c',font = ("Gotham Rounded Medium",16),corner_radius=60) # show_frame(arg) arg=which frame to go to

        backbutton = ctk.CTkButton(self,anchor="wn",fg_color="transparent" ,hover=False, text="GO BACK",command=lambda: controller.show_frame(DoWhatPage),font = ("Gotham Rounded Medium",10),corner_radius=60) # show_frame(arg) arg=which frame to go to


        # widget placement 
        label.grid(column=3,sticky="sew",row=0,padx=5,columnspan=6) # column and columnspan are finicky. temporary values used currently
        image_label.grid(column=3,sticky="new",row=1,padx=5,columnspan=6) # n-north e-east w-west s-south 
        
        email_entry.grid(column=3,sticky="ew",row=2,padx=5,columnspan=6,ipadx=5,ipady=5)

        name.grid(column=4,sticky="ne",row=3,padx=5,columnspan=1)
        nameval.grid(column=5,sticky="nw",row=3,padx=5,columnspan=2)

        dom.grid(column=4,sticky="ne",row=4,padx=5,columnspan=1)
        domval.grid(column=5,sticky="nw",row=4,padx=5,columnspan=2)

        fail.grid(column=4,sticky="new",row=5,padx=5,columnspan=4,ipadx=5,ipady=5)
        
        button.grid(row=6,column=4,ipadx=5,ipady=5,columnspan=4, sticky="nwe") 
        backbutton.grid(row=0,column=0,ipadx=5,ipady=5, sticky="w") 

class DoWhatPage(ctk.CTkFrame):
  
    def __init__(self, parent, controller):  
        ctk.CTkFrame.__init__(self,parent)  # initialsation
    
        # grid setup. creates a 16*9 grid. used to place widgets
        # also makes the grid's cells scale with window size 
        for col in range(16):
            self.columnconfigure(col, weight=1)
        for row in range(9):
            self.rowconfigure(row, weight=1)

        # widgets
        label = ctk.CTkLabel(self, text="FUNCTIONS",font = ("Gotham Rounded Medium",22))  
        
        line_img = ctk.CTkImage(light_image=img.open("line.png"),dark_image=img.open("line.png"),size=(90, 2))
        image_label = ctk.CTkLabel(self, image=line_img, text="")
        
        slice_img = ctk.CTkImage(light_image=img.open("slice.png"),dark_image=img.open("slice.png"),size=(175,175))
        go_slice = ctk.CTkButton(self, image=slice_img, text="" ,hover=False,command=lambda: controller.show_frame(SlicerPage),fg_color="transparent") # show_frame(arg) arg=which frame to go to
        
        """read_img = ctk.CTkImage(light_image=img.open("read.png"),dark_image=img.open("read.png"),size=(175,175))
        go_read = ctk.CTkButton(self, image=read_img ,text="",hover=False,command=lambda: controller.show_frame(ReadPage),fg_color="transparent") # show_frame(arg) arg=which frame to go to
        """
        send_img = ctk.CTkImage(light_image=img.open("send.png"),dark_image=img.open("send.png"),size=(175,175))
        go_send = ctk.CTkButton(self, image=send_img ,text="",hover=False,command=lambda: controller.show_frame(SendPage),fg_color="transparent") # show_frame(arg) arg=which frame to go to
        

        backbutton = ctk.CTkButton(self,anchor="wn",fg_color="transparent" ,hover=False, text="LOG OUT",command=lambda: controller.show_frame(LoginPage),font = ("Gotham Rounded Medium",10),corner_radius=60) # show_frame(arg) arg=which frame to go to


        # widget placement 
        backbutton.grid(row=0,column=0,ipadx=5,ipady=5, sticky="w",columnspan=2) 
        label.grid(column=3,sticky="sew",row=0,padx=5,columnspan=5) # column and columnspan are finicky. temporary values used currently
        image_label.grid(column=3,sticky="new",row=1,padx=5,columnspan=5) # n-north e-east w-west s-south 
        go_slice.grid(column=2,row=3,columnspan=3,padx=50,pady=10)
        """go_read.grid(column=4,row=3,columnspan=3,padx=50,pady=10)
        """
        go_send.grid(column=6,row=3,columnspan=3,padx=50,pady=10)
        
class SendPage(ctk.CTkFrame):
  
    def __init__(self, parent, controller):  
        ctk.CTkFrame.__init__(self,parent)  # initialsation

        # grid setup. creates a 16*9 grid. used to place widgets
        # also makes the grid's cells scale with window size 
        for col in range(16):
            self.columnconfigure(col, weight=1)
        for row in range(9):
            self.rowconfigure(row, weight=1)

        label = ctk.CTkLabel(self, text="SEND MAIL",font = ("Gotham Rounded Medium",22))  
        
        line_img = ctk.CTkImage(light_image=img.open("line.png"),dark_image=img.open("line.png"),size=(90, 2))
        image_label = ctk.CTkLabel(self, image=line_img, text="")
        label.grid(column=2,sticky="sew",row=0,padx=5,columnspan=10) # column and columnspan are finicky. temporary values used currently
        image_label.grid(column=2,sticky="new",row=1,padx=5,columnspan=10) # n-north e-east w-west s-south 
        
        
        backbutton = ctk.CTkButton(self,anchor="wn",fg_color="transparent" ,hover=False, text="GO BACK",command=lambda: controller.show_frame(DoWhatPage),font = ("Gotham Rounded Medium",10),corner_radius=60) # show_frame(arg) arg=which frame to go to
        backbutton.grid(row=0,column=0,ipadx=5,ipady=5, sticky="w",columnspan=2) 

        
        self.attach = ctk.CTkButton(self, command=self.attach_click, text="Attachment",fg_color='#187d36',hover_color='#22b14c',font = ("Gotham Rounded Medium",14),corner_radius=60)
        self.attach.grid(row=7,column=10,columnspan=3, padx=5, pady=5,sticky='e')


        self.to = ctk.CTkEntry(self,placeholder_text="To: ",font= ("Gotham Rounded Medium",14))
        self.to.grid(row=1,columnspan=12, column=1, padx=5, pady=5,sticky='sew')
        

        self.sub = ctk.CTkEntry(self, placeholder_text="Subject: ",font= ("Gotham Rounded Medium",14))
        self.sub.grid(row=2,columnspan=12, column=1,padx=5, pady=5,sticky="ew")
        
        self.body = ctk.CTkEntry(self,placeholder_text="Type your message here. Messages can also include html code.",font= ("Gotham Rounded Medium",14))
        self.body.grid(row=3,rowspan=3,columnspan=12, column=1, padx=5, pady=5,sticky='ewns')

        button = ctk.CTkButton(self, command=self.button_click, text="Send Email",fg_color='#187d36',hover_color='#22b14c',font = ("Gotham Rounded Medium",14),corner_radius=60)
        button.grid(row=8,column=10,columnspan=3, padx=5, pady=5,sticky='ne')

    def attach_click(self):
        global filename
        filename= tk.filedialog.askopenfile().name
        self.attach.configure(text=os.path.basename(str(filename)))


    def button_click(self):
        send_email(self.to.get(), self.sub.get(), self.body.get(), 'smtp.gmail.com', 465, emailid, pass_word,filename)
        self.to.configure(text="")
        self.sub.configure(text="")
        self.body.configure(text="")
        
 

class ReadPage(ctk.CTkFrame):
  
    def __init__(self, parent, controller):  
        ctk.CTkFrame.__init__(self,parent)  # initialsation

        # grid setup. creates a 16*9 grid. used to place widgets
        # also makes the grid's cells scale with window size 
        for col in range(16):
            self.columnconfigure(col, weight=1)
        for row in range(9):
            self.rowconfigure(row, weight=1)

        # widgets
        label = ctk.CTkLabel(self, text="Start Page",fg_color="cyan")  
        label2 = ctk.CTkLabel(self, text="???",fg_color="red")  
        button = ctk.CTkButton(self, text="Visit Page 1",command=lambda: controller.show_frame(DoWhatPage)) # show_frame(arg) arg=which frame to go to

        # widget placement 
        label2.grid(column=4,sticky="nsew",row=4)
        label.grid(row=0,column=1,columnspan=14,sticky="nsew")
        button.grid(sticky="wns",row=2,column=2) 

if __name__ == "__main__":
    app = App()  
    app.mainloop()