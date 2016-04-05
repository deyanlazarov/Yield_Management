from tkinter import *
from tkinter import ttk
from Start import start


class finished():
    def __init__(self, master, returned_list):
        self.root = master
        self.root.minsize(width=666, height=320)
        self.root.maxsize(width=666, height=320)
        self.root.wm_title("OptiEdit")
        self.root.config(bg="#D3D3D3")

        self.code_label = Label(master, bg="#D3D3D3", text='You had a imps overage or shortage of ' + str(
            round(returned_list[0], 1)) + ' and ' + str(returned_list[1]) + ' unplaced spots',
                                font=("Helvetica", 16)).grid(row=1, columnspan=4, pady=(150, 0), padx=(10, 0))


class change_potential():
    def __init__(self, master, daypart, aggressive, number_of_trials):
        self.root = master
        self.root.minsize(width=666, height=320)
        self.root.maxsize(width=666, height=320)
        self.root.wm_title("OptiEdit")
        self.root.config(bg="#D3D3D3")

        if daypart == "Prime Access":
            hour_options = ['18', '19']
        elif daypart == "Weekend":
            hour_options = ['7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19']
        elif daypart == "Daytime":
            hour_options = ['9', '10', '11', '12', '13', '14']
        elif daypart == "Early Fringe":
            hour_options = ['15', '16', '17']
        else:
            hour_options = ['21', '22', '23']

        for i in range(0, len(hour_options)):
            if len(hour_options) > 6:
                divisor = len(hour_options)//2
                if i > 5:
                    y_pos = 165
                    x_pos = ((666//(divisor+1))-20) * ((i-6)+1)
                else:
                    y_pos = 115
                    x_pos = ((666//(divisor+1))-20) * (i+1)
            else:
                y_pos = 125
                x_pos = ((666//(len(hour_options)+1))-20) * (i+1)
            Label(master, text=hour_options[i]).place(x=x_pos, y=y_pos)
            self.hour_1 = StringVar(master, value='780')
            self.hour_1_enter = Entry(master, textvariable=self.hour_1, width=5).place(x=x_pos + 20, y=y_pos)
        self.calculate = ttk.Button(master, text="Calculate",  width=105).place(x=15, y=280)


class ym():
    def __init__(self, master):
        def update_daypart(current):
            menu = self.daypart['menu']
            menu.delete(0, 'end')
            self.daypart.config(state=NORMAL)
            if current == 'Saturday' or current == 'Sunday':
                optionsday = ['Weekend', 'Prime 1', 'Prime 2']
                for dayparts in optionsday:
                    menu.add_command(label=dayparts, command=lambda value=dayparts:
                    self.daypart_variable.set(value))
            else:
                optionsday = ["Daytime", "Early Fringe", "Prime Access", 'Prime 1', 'Prime 2']
                for dayparts in optionsday:
                    menu.add_command(label=dayparts, command=lambda value=dayparts:
                    self.daypart_variable.set(value))

        self.root = master
        self.root.minsize(width=666, height=320)
        self.root.maxsize(width=666, height=320)
        self.root.wm_title("OptiEdit")
        self.root.config(bg="#D3D3D3")

        # Add MenuOptions to row 0
        options = ["Monday", "Tuesday", "Wednesday", 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.day_variable = StringVar(master)
        self.date = ttk.OptionMenu(master, self.day_variable, 'Choose Day Of Week', *options, command=update_daypart)
        self.date.config(width=30)
        self.date.grid(row=0, column=0, columnspan=2, pady=40, padx=60)

        # Add MenuOption to row 0, column 1
        self.daypart_variable = StringVar(master)
        self.daypart = ttk.OptionMenu(master, self.daypart_variable, 'Choose Daypart', 'Placeholder')
        self.daypart.config(width=30, state=DISABLED)
        self.daypart.grid(row=0, column=2, columnspan=2, pady=40, padx=70)

        self.v = IntVar()
        ttk.Radiobutton(master, text="1 Iteration", variable=self.v, value=1).grid(row=1, column=0,
                                                                                   pady=(35, 0))
        ttk.Radiobutton(master, text="100 Iterations", variable=self.v, value=100).grid(row=1, column=1,
                                                                                        pady=(35, 0))
        ttk.Radiobutton(master, text="500 Iterations", variable=self.v, value=500).grid(row=1, column=2,
                                                                                        pady=(35, 0))
        ttk.Radiobutton(master, text="1000 Iterations", variable=self.v, value=1000).grid(row=1,
                                                                                          column=3,
                                                                                          pady=(35, 0))
        self.v.set(1000)

        self.aggressive = IntVar()
        ttk.Radiobutton(master, text="Aggressive", variable=self.aggressive, value=0).grid(row=2, column=0,
                                                                                           columnspan=2,
                                                                                           pady=(35, 0))
        ttk.Radiobutton(master, text="Moderate", variable=self.aggressive, value=250).grid(row=2, column=1,
                                                                                           columnspan=2,
                                                                                           pady=(35, 0))
        ttk.Radiobutton(master, text="Conservative", variable=self.aggressive, value=500).grid(row=2, column=2,
                                                                                               columnspan=2,
                                                                                               pady=(35, 0))
        self.aggressive.set(500)

        self.configure = ttk.Button(master, text="Customize Potential", command=self.configure, width=48).grid(column=0,
                                                                                                               columnspan=2,
                                                                                                               row=3,
                                                                                                               pady=(
                                                                                                                   40,
                                                                                                                   0))
        self.calculate = ttk.Button(master, text="Okay", command=self.calculate, width=48).grid(column=2, columnspan=2,
                                                                                                row=3, pady=(40, 0))

        self.progress = ttk.Progressbar(master, orient="horizontal",
                                        length=200, mode="determinate").grid_forget()


    def configure(self):
        for items in root.grid_slaves():
            items.grid_forget()
        change_potential(root, self.daypart_variable.get(), self.aggressive.get(), self.v.get())

    def calculate(self):
        returned_list = start(self.daypart_variable.get(), self.v.get(), self.aggressive.get())
        print(returned_list)
        for items in root.grid_slaves():
            items.grid_forget()
        finished(root, returned_list)


if __name__ == "__main__":
    root = Tk()
    res = ym(root)
    root.mainloop()



