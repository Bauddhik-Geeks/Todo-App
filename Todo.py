from tkinter import *
from tkinter.font import Font
from tkinter import filedialog
import pickle
import sqlite3
import mysql.connector as mysql

root = Tk()
root.title('Nitesh-TODO List!')
root.geometry("500x450")
name = StringVar()

############### Fonts ################

my_font = Font(
    family="PT Sans",
    size=30,
    weight="bold")

################# Frame #################
my_frame = Frame(root)
my_frame.pack(pady=10)


################# List Box #############
my_list = Listbox(my_frame,
           font=my_font,
           width=25,
           height=5,
           bg="SystemButtonFace",
           bd=0,
           fg="#464646",
           highlightthickness=0,
           selectbackground="grey",
           activestyle="none")

my_list.pack(side=LEFT, fill=BOTH)

############### Dummy List ##################

#stuff = ["Do daily Checkin","Do Event checkin","Complete Daily Task","Complete Weekly Task","Take a break"]

############# Add dummmy list to list box ##############
#for item in stuff:
 #   my_list.insert(END, item)
    
################# Ceate Scrollbar ###########################
my_scrollbar= Scrollbar(my_frame)
my_scrollbar.pack(side=RIGHT, fill=BOTH)

#################### Add Scrollbar ######################
my_list.config(yscrollcommand=my_scrollbar.set)
my_scrollbar.config(command=my_list.yview)

################### ADD item entry box#################
my_entry = Entry(root, font=("Helvetica", 24),width=24, textvariable=name)
my_entry.pack(pady=20)

######################## Crete button frame ##########
button_frame=Frame(root)
button_frame.pack(pady=20)


##################### Funnctions ###################
def delete_item():
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    items = my_list.get(ANCHOR)
    query = "DELETE from Items where Todo_list=?"
    cursor.execute(query,(items,))
    my_list.delete(ANCHOR)
    con.commit()
    cursor.close()

def add_item():
    my_list.insert(END, my_entry.get())
    name1 = name.get()
    conn = sqlite3.connect('database.db')
    with conn:
       c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Items(Todo_list TEXT)")   
    c.execute('INSERT INTO Items(Todo_list) VALUES (?)',(name1,)) 
    conn.commit()   
    my_entry.delete(0, END)

 
def cross_off_item():
    # Cross Off Item
    my_list.itemconfig(
        my_list.curselection(),
        fg="#dedede")
    # Get rid of Selection bar
    my_list.selection_clear(0,END)
    
def uncross_item():
    # Cross Off Item
    my_list.itemconfig(
        my_list.curselection(),
        fg="#464646")
    # Get rid of Selection bar
    my_list.selection_clear(0,END)
    
def delete_crossed():
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    items = my_list.get(ANCHOR)
    query = "DELETE from Items where Todo_list=?"
    cursor.execute(query,(items,))
    my_list.delete(ANCHOR)
    con.commit()
    cursor.close()
    count = 0
    while count < my_list.size():
        if my_list.itemcget(count, "fg")=="#dedede":
           my_list.delete(my_list.index(count))
        else:
            count+=1
            
def save_list():
    file = filedialog.asksaveasfile(initialdir="C:\\Users\\Deepu John\\OneDrive\\Deepu 2020\\Projects\\rough",
                                    defaultextension='.txt',
                                    filetypes=[
                                        ("Text file",".txt"),
                                        ("HTML file", ".html"),
                                        ("All files", ".*"),
                                    ])
    if file is None:
        return
    filetext = '\n'.join(my_list.get('0', 'end'))
    file.write(filetext)
    file.close()


def open_list():
    file_name = filedialog.askopenfilename(
           initialdir="C:/gui/data",
            title="Open File",
            filetypes=(("Text Files","*.txt"),
                       ("All Files","*.*"))
    )
    if file_name:
        #DElete current open list
        my_list.delete(0,END)
        
        #Open file name
        input_file=open(file_name, 'rb')
        
        #Load the data from the  file
        stuff = pickle.load(input_file)
        
        #output data to the screen
        for item in stuff:
            my_list.insert(END, item) 
    
    
def delete_list():
    my_list.delete(0,END)

def dark_theme():
    colorbg = 'black'
    colorfg = 'white'
    my_list.config(bg='#152642', fg=colorfg)
    add_button.config(bg=colorbg, fg=colorfg)
    delete_button.config(bg=colorbg, fg=colorfg)
    cross_off_button.config(bg=colorbg, fg=colorfg)
    delete_crossed_button.config(bg=colorbg, fg=colorfg)
    uncross_button.config(bg=colorbg, fg=colorfg)
    my_entry.config(bg='#152642', fg=colorfg)
    dark_mode_button.config(bg=colorbg, fg=colorfg)
    light_mode_button.config(bg=colorbg, fg=colorfg)
    root.config(bg=colorbg)
    button_frame.config(bg=colorbg)

def light_theme():
    colorbg = 'white'
    colorfg = 'black'
    my_list.config(bg=colorbg, fg=colorfg)
    add_button.config(bg=colorbg, fg=colorfg)
    delete_button.config(bg=colorbg, fg=colorfg)
    cross_off_button.config(bg=colorbg, fg=colorfg)
    delete_crossed_button.config(bg=colorbg, fg=colorfg)
    uncross_button.config(bg=colorbg, fg=colorfg)
    my_entry.config(bg=colorbg, fg=colorfg)
    dark_mode_button.config(bg=colorbg, fg=colorfg)
    light_mode_button.config(bg=colorbg, fg=colorfg)
    root.config(bg='#D3D3D3')
    button_frame.config(bg='#D3D3D3')

####################### Create Menu ##############    

my_menu = Menu(root)
root.config(menu=my_menu)

####################### Add items to menu ##########

file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)

############### Add Dorpdowm Items ####################

file_menu.add_command(label="Open List", command=open_list)
file_menu.add_command(label="Clear List", command=delete_list)
file_menu.add_command(label="Save List", command=save_list)

################# Add Buttons ################

delete_button = Button(button_frame, text="Delete Item",command=delete_item)
add_button = Button(button_frame, text="Add Item",command=add_item)
cross_off_button = Button(button_frame, text="Cross Item",command=cross_off_item)
uncross_button = Button(button_frame, text="Uncross Item",command=uncross_item)
delete_crossed_button = Button(button_frame, text="Delete Cross Item",command=delete_crossed)
dark_mode_button = Button(button_frame, text='Night mode', command=dark_theme)
light_mode_button = Button(button_frame, text='Day mode', command=light_theme)

file_menu.add_separator()

delete_button.grid(row=0,column=0)
add_button.grid(row=0,column=1, padx=20)  
cross_off_button.grid(row=0,column=2)  
uncross_button.grid(row=0,column=3, padx=20) 
delete_crossed_button.grid(row=0,column=4)
light_mode_button.grid(row=1,column=2)
dark_mode_button.grid(row=1,column=3) 

root.mainloop()   
