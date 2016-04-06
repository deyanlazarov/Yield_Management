from tkinter import *
from tkinter import ttk
from Start import start
from itertools import repeat
import configparser
import os.path


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
    def __init__(self, master, daypart, aggressive, number_of_trials, potential, ratings_path, spots_path):
        self.daypart = daypart
        self.aggressive = aggressive
        self.number_of_trials = number_of_trials
        self.ratings_path = ratings_path
        self.spots_path - spots_path
        self.root = master
        self.root.minsize(width=666, height=320)
        self.root.maxsize(width=666, height=320)
        self.root.wm_title("OptiEdit")
        self.root.config(bg="#D3D3D3")
        hour_options = ym.get_hours_from_daypart(master, daypart)
        self.list_of_boxes = {}
        for i in range(0, len(hour_options)):
            if len(hour_options) > 6:
                divisor = len(hour_options) // 2
                if i > 5:
                    y_pos = 165
                    x_pos = ((666 // (divisor + 1)) - 20) * ((i - 6) + 1)
                else:
                    y_pos = 115
                    x_pos = ((666 // (divisor + 1)) - 20) * (i + 1)
            else:
                y_pos = 125
                x_pos = ((666 // (len(hour_options) + 1)) - 20) * (i + 1)
            label = Label(master, text=hour_options[i]).place(x=x_pos, y=y_pos)
            self.hour_1 = StringVar(master, value=potential)
            hour_enter = Entry(master, textvariable=self.hour_1, width=5)
            hour_enter.place(x=x_pos + 20, y=y_pos)
            self.list_of_boxes[hour_options[i]] = hour_enter
        self.calculate = ttk.Button(master, text="Calculate", command=self.calculate, width=105).place(x=15, y=280)

    def calculate(self):
        for keys in self.list_of_boxes:
            self.list_of_boxes[keys] = int(self.list_of_boxes[keys].get())
        returned_list = start(self.daypart, self.number_of_trials, self.aggressive, self.list_of_boxes,
                              self.ratings_path, self.spots_path)
        for widget in root.winfo_children():
            widget.destroy()
        finished(root, returned_list)


class ym():
    def __init__(self, master):

        self.config = configparser.ConfigParser()
        if os.path.isfile('user.ini'):
            self.config.read('user.ini')
        else:
            self.config['DEFAULT'] = {'NETWORK': 'Travel',
                                      'DEFAULT_POTENTIAL': 800,
                                      'RATINGS_PATH': r'F:\\Traffic Logs\\Travel\\OptiEdit\\Travel Ratings\\',
                                      'SPOTS_PATH': r'F:\\Traffic Logs\\Travel\\OptiEdit\\Travel Spots\\'}
            with open('user.ini', 'w') as configfile:
                self.config.write(configfile)

        self.root = master
        self.root.minsize(width=666, height=320)
        self.root.maxsize(width=666, height=320)
        self.root.wm_title("OptiEdit")
        self.root.config(bg="#D3D3D3")

        menu = Menu(self.root, tearoff=0)
        self.root.config(menu=menu)

        file = Menu(menu)
        file.add_command(label='Change Default Settings', command=self.change_default_ini)
        file.add_command(label='Exit', command=self.exit_file)
        menu.add_cascade(label='File', menu=file)

        # Add MenuOptions to row 0
        options = ["Monday", "Tuesday", "Wednesday", 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.day_variable = StringVar(master)
        self.date = ttk.OptionMenu(master, self.day_variable, 'Choose Day Of Week', *options,
                                   command=self.update_daypart)
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
        change_potential(root, self.daypart_variable.get(), self.aggressive.get(), self.v.get(),
                         self.config['DEFAULT']['DEFAULT_POTENTIAL'], self.config['DEFAULT']['RATINGS_PATH'],
                         self.config['DEFAULT']['SPOTS_PATH'])

    def calculate(self):
        time_dict = dict(zip(self.get_hours_from_daypart(self.daypart_variable.get()),
            repeat(int(self.config['DEFAULT']['DEFAULT_POTENTIAL']))))
        returned_list = start(self.daypart_variable.get(), self.v.get(), self.aggressive.get(), time_dict,
            self.config['DEFAULT']['RATINGS_PATH'], self.config['DEFAULT']['SPOTS_PATH'])
        for items in root.grid_slaves():
            items.grid_forget()
        finished(root, returned_list)

    def get_hours_from_daypart(self, daypart):
        options = [i for i in range(7, 24)]
        if daypart == "Prime Access":
            hour_options = options[11:13]
        elif daypart == "Weekend":
            hour_options = options[:13]
        elif daypart == "Daytime":
            hour_options = options[2:7]
        elif daypart == "Early Fringe":
            hour_options = options[7:10]
        else:
            hour_options = options[14:]
        return hour_options

    def exit_file(self):
        exit()

    def change_default_ini(self):
        print('here')

    def update_daypart(self, current):
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


if __name__ == "__main__":
    root = Tk()
    res = ym(root)
    root.mainloop()



