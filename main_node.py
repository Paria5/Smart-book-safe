import tkinter as tk
import json
import threading
import socket
import time
import bluetooth
from tkinter import filedialog

def load_users():
    try:
        with open('users.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)

def register(username,password):
    users = load_users()

    if username in users:
        print("User ID already exists.")
        return 1
    users[username] = {'password': password}
    save_users(users)
    print("Registration successful.")
    return 0

def login(username,password):
    users = load_users()

    if username not in users or users[username]['password'] != password:
        print("Password Incorrect")
        return "Failure"
    else:
         print("Login successful.")
         return "Success"

def run_code(listbox):
    i=0
    while i<5:
        try:    
            server_address = ('192.168.246.15', 800)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(server_address)
            i=6
        except ValueError:
            i=i+1
        
    rawtext="abctestxyz"
    s.sendall(rawtext.encode())
    #rawtext="abctestxyz"
    #s.sendall(rawtext.encode())
    #time.sleep(2)
    #rawtext="test"
    #s.sendall(rawtext.encode())
    #time.sleep(3)
    #rawtext="test"
    #s.sendall(rawtext.encode())
    time.sleep(5)
    while True:
        #Choosing Data
        CommandRequest = s.recv(1024)
        listbox.insert(tk.END, "command:"+CommandRequest.decode())
        UserName_Data = s.recv(1024)
        listbox.insert(tk.END, "UserName:"+UserName_Data.decode())
        Password_Data = s.recv(1024)
        listbox.insert(tk.END, "Password:"+Password_Data.decode())
        if CommandRequest.decode()=='1':
            Status=register(UserName_Data.decode(),Password_Data.decode())
            if Status==1:
                rawtext="0000abcExistsxyz0000"
            else:
                rawtext="0000abcCreatexyz0000"
            s.sendall(rawtext.encode())
            time.sleep(2)
            #s.sendall(rawtext.encode())
            #time.sleep(2)
            #s.sendall(rawtext.encode())
            #time.sleep(2)
            s.sendall(rawtext.encode())
            time.sleep(2)
        elif CommandRequest.decode()=='2':
            Status=login(UserName_Data.decode(),Password_Data.decode())
            if Status=="Failure":
                rawtext="0000abcIncorrectxyz0000"
            else:
                rawtext="0000abcSuccessxyz0000"
            #rawtext=login(UserName_Data.decode(),Password_Data.decode())
            s.sendall(rawtext.encode())
            time.sleep(2)
            #rawtext=login(UserName_Data.decode(),Password_Data.decode())
            #s.sendall(rawtext.encode())
            #time.sleep(2)#s.close()
            s.sendall(rawtext.encode())
            time.sleep(2)
            #rawtext=login(UserName_Data.decode(),Password_Data.decode())
            s.sendall(rawtext.encode())
            time.sleep(2)#s.close()

def start_thread_run_code(listbox):
    t = threading.Thread(target=run_code, args=(listbox,))
    t.start()

def connect_to_hc06(listbox):
    #HC06_MAC_ADDRESS = '00:22:10:01:16:49'
    HC06_MAC_ADDRESS = '00:22:10:01:16:49'
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((HC06_MAC_ADDRESS, 1))
    listbox.insert(tk.END, "Connected to HC-06 module")
    data = "1"
    encoded_data = data.encode('utf-8')
    sock.send(encoded_data)
    response = sock.recv(1024).decode()
    listbox.insert(tk.END, "Received:", response)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")    
    # write_response_to_file(response, timestamp) # If you have a function to write the response to a file
    listbox.insert(tk.END, f"Received response '{response}' at {timestamp}")

def display_usernames():
    usernames = []
    try:
        with open('users.json', 'r') as file:
            data = json.load(file)
            for key in data:
                usernames.append(key)
    except FileNotFoundError:
        print("Error: JSON file not found.")
    
    # Clear existing listbox content
    display_listbox.delete(0, tk.END)
    
    # Display usernames in listbox
    for username in usernames:
        display_listbox.insert(tk.END, username)

def delete_user():
    selected_index = display_listbox.curselection()
    if selected_index:
        selected_item = display_listbox.get(selected_index[0])
        display_listbox.delete(selected_index[0])
        try:
            with open('users.json', 'r') as file:
                data = json.load(file)
                if selected_item in data:
                    del data[selected_item]
            with open('users.json', 'w') as file:
                json.dump(data, file, indent=4)
        except FileNotFoundError:
            print("Error: JSON file not found.")

def load_file():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filename:
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                load_listbox.insert(tk.END, line.strip())

def setup_ui(root):
    root.title("Usernames Viewer and HC-06 Connection")

    # Create a label for the display listbox
    display_label = tk.Label(root, text="Usernames", bg="blue", fg="white")
    display_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # Create a label for the load listbox
    load_label = tk.Label(root, text="Loaded File", bg="blue", fg="white")
    load_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    # Create a label for the run code listbox
    run_code_label = tk.Label(root, text="Run Code", bg="blue", fg="white")
    run_code_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    # Create a label for the HC-06 connection listbox
    hc06_label = tk.Label(root, text="HC-06 Connection", bg="blue", fg="white")
    hc06_label.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    # Create a frame for the display listbox and scrollbar
    display_frame = tk.Frame(root)
    display_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    # Create a frame for the load listbox and scrollbar
    load_frame = tk.Frame(root)
    load_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    # Create a frame for the run code listbox and scrollbar
    run_code_frame = tk.Frame(root)
    run_code_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

    # Create a frame for the HC-06 connection listbox and scrollbar
    hc06_frame = tk.Frame(root)
    hc06_frame.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

    # Create a listbox to display usernames
    global display_listbox
    display_listbox = tk.Listbox(display_frame, width=30, height=20)
    display_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a listbox to load file
    global load_listbox
    load_listbox = tk.Listbox(load_frame, width=30, height=20)
    load_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a listbox to display run code results
    global run_code_listbox
    run_code_listbox = tk.Listbox(run_code_frame, width=30, height=10)
    run_code_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a listbox to display HC-06 connection results
    global hc06_listbox
    hc06_listbox = tk.Listbox(hc06_frame, width=30, height=10)
    hc06_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a scrollbar for the display listbox
    display_scrollbar = tk.Scrollbar(display_frame, orient=tk.VERTICAL, command=display_listbox.yview)
    display_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    display_listbox.config(yscrollcommand=display_scrollbar.set)

    # Create a scrollbar for the load listbox
    load_scrollbar = tk.Scrollbar(load_frame, orient=tk.VERTICAL, command=load_listbox.yview)
    load_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    load_listbox.config(yscrollcommand=load_scrollbar.set)

    # Create a scrollbar for the run code listbox
    run_code_scrollbar = tk.Scrollbar(run_code_frame, orient=tk.VERTICAL, command=run_code_listbox.yview)
    run_code_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    run_code_listbox.config(yscrollcommand=run_code_scrollbar.set)

    # Create a scrollbar for the HC-06 connection listbox
    hc06_scrollbar = tk.Scrollbar(hc06_frame, orient=tk.VERTICAL, command=hc06_listbox.yview)
    hc06_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    hc06_listbox.config(yscrollcommand=hc06_scrollbar.set)

    # Create a button to trigger displaying usernames
    display_button = tk.Button(root, text="Display Usernames", command=display_usernames)
    display_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

    # Create a button to delete selected username
    delete_button = tk.Button(root, text="Delete Selected", command=delete_user)
    delete_button.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

    # Create a button to load a file
    load_button = tk.Button(root, text="Load File", command=load_file)
    load_button.grid(row=4, column=2, padx=10, pady=10, sticky="ew")

    # Create a button to start the run code thread
    run_code_button = tk.Button(root, text="Start Run Code", command=lambda: start_thread_run_code(run_code_listbox))
    run_code_button.grid(row=4, column=3, padx=10, pady=10, sticky="ew")

    # Create a button to connect to HC-06
    hc06_button = tk.Button(root, text="Connect to HC-06", command=lambda: connect_to_hc06(hc06_listbox))
    hc06_button.grid(row=4, column=4, padx=10, pady=10, sticky="ew")



def create_gui():
    root = tk.Tk()
    setup_ui(root)
    root.mainloop()

if __name__ == "__main__":
    create_gui()