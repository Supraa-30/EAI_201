import tkinter as tk


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chanakya Navigator")
        self.root.geometry("850x700")

        label = tk.Label(root, text="Welcome to Chanakya Navigator", font=("Arial", 24))
        label.pack(padx=20, pady=20)
        #TO CREATE BUTTONS ETC
        button = tk.Button(root, text="Find", font=("Arial", 12))
        button.pack(padx=20, pady=20)

        buttonframe = tk.Frame(root)
        buttonframe.columnconfigure(0, weight=1)
        buttonframe.columnconfigure(1, weight=1)
        buttonframe.columnconfigure(2, weight=1)

        btn1 =  tk.Button( buttonframe, text="BFS", font=("Arial", 12))
        btn1.grid(row=0, column=0, sticky=tk.W+tk.E)

        btn2 =  tk.Button( buttonframe, text="DFS", font=("Arial", 12))
        btn2.grid(row=0, column=1, sticky=tk.W+tk.E)    

        btn3 =  tk.Button( buttonframe, text="UCS", font=("Arial", 12))
        btn3.grid(row=0, column=2, sticky=tk.W+tk.E)

        btn4 =  tk.Button( buttonframe, text=" A* ", font=("Arial", 12))
        btn4.grid(row=1, column=1, sticky=tk.W+tk.E)

        buttonframe.pack(fill="x" , padx=20, pady=20)

        

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()

