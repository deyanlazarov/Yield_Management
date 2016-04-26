from tkinter import *
from tkinter import ttk
from Demo_List_Names import sum_dict_names
from Preempt_Credit import preempt_credit_names
from Ratings_Import import import_ratings
from Start import start, place_placed_spots, finish
from itertools import repeat
import configparser
import os.path
import pandas as pd
from multiprocessing import Pool
import operator


class DefaultEdit():
    def __init__(self, master, config):
        self.root = master
        self.config = configparser.ConfigParser()
        options = ["Cooking", "DiY", "Food", 'GAC', 'HGTV', 'Travel']
        self.network_variable = StringVar(master)
        self.network = ttk.OptionMenu(master, self.network_variable, config['DEFAULT']['NETWORK'], command=self.update,
                                      *options)
        self.network.config(width=30)
        self.network.place(x=250, y=50)
        Label(master, bg="#D3D3D3", text='Default Potential').place(x=270, y=90)
        Label(master, bg="#D3D3D3", text='Path to Ratings File: ').place(x=150, y=130)
        Label(master, bg="#D3D3D3", text='Path to Spots File: ').place(x=150, y=170)
        self.ratings_var = StringVar(master)
        self.ratings_var.set(config['DEFAULT']['RATINGS_PATH'])
        ratings_label = Label(master, bg="#D3D3D3", textvariable=self.ratings_var)
        ratings_label.place(x=270, y=130)
        self.spots_var = StringVar(master)
        self.spots_var.set(config['DEFAULT']['SPOTS_PATH'])
        spots_label = Label(master, bg="#D3D3D3", textvariable=self.spots_var)
        spots_label.place(x=270, y=170)
        self.current_selection = config['DEFAULT']['NETWORK']

        self.potential = StringVar(master, value=config['DEFAULT']['DEFAULT_POTENTIAL'])
        potential_enter = Entry(master, textvariable=self.potential, width=5)
        potential_enter.place(x=370, y=90)

        self.cancel_button = ttk.Button(master, text="Cancel", command=self.cancel, width=50).place(x=15, y=280)
        self.okay_button = ttk.Button(master, text="Okay", command=self.okay, width=50).place(x=350, y=280)

    def cancel(self):
        for widget in root.winfo_children():
            widget.destroy()
        Ym(self.root)

    def okay(self):
        self.config['DEFAULT'] = {'NETWORK': self.network_variable.get(),
                                  'DEFAULT_POTENTIAL': int(self.potential.get()),
                                  'RATINGS_PATH': self.ratings_var.get(),
                                  'SPOTS_PATH': self.spots_var.get()}
        with open('user.ini', 'w') as configfile:
            self.config.write(configfile)
        for widget in root.winfo_children():
            widget.destroy()
        Ym(self.root)

    def update(self, current):
        self.ratings_var.set(self.ratings_var.get().replace(self.current_selection, current))
        self.spots_var.set(self.spots_var.get().replace(self.current_selection, current))
        self.current_selection = current


class Finished():
    def __init__(self, master, returned_list, daypart):
        self.root = master
        self.root.minsize(width=666, height=320)
        self.root.maxsize(width=666, height=320)
        self.root.wm_title("OptiEdit")
        self.root.config(bg="#D3D3D3")

        self.code_label = Label(master, bg="#D3D3D3", text='You had a imps overage or shortage of ' + str(
            round(returned_list[0], 1)) + ' and ' + str(returned_list[1]) + ' unplaced spots.',
                                font=("Helvetica", 14)).grid(row=1, columnspan=4, pady=(150, 0), padx=(30, 0))
        self.code_label = Label(master, bg="#D3D3D3",
                                text='Your results can be found in a file called ' + daypart +
                                     '.csv which will be found in your Completed folder',
                                font=("Helvetica", 10)).grid(row=2, columnspan=4, pady=(0, 0), padx=(30, 0))


class ChangePotential():
    def __init__(self, master, daypart, aggressive, number_of_trials, potential, ratings_path, spots_path):
        self.daypart = daypart
        self.aggressive = aggressive
        self.number_of_trials = number_of_trials
        self.ratings_path = ratings_path
        self.spots_path = spots_path
        self.root = master
        self.root.minsize(width=666, height=320)
        self.root.maxsize(width=666, height=320)
        self.root.wm_title("OptiEdit")
        self.root.config(bg="#D3D3D3")
        hour_options = Ym.get_hours_from_daypart(daypart)
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
            Label(master, text=hour_options[i]).place(x=x_pos, y=y_pos)
            self.hour_1 = StringVar(master, value=potential)
            hour_enter = Entry(master, textvariable=self.hour_1, width=5)
            hour_enter.place(x=x_pos + 20, y=y_pos)
            self.list_of_boxes[hour_options[i]] = hour_enter
        self.calculate = ttk.Button(master, text="Calculate", command=self.calculate, width=105).place(x=15, y=280)

    def calculate(self):
        for keys in self.list_of_boxes:
            self.list_of_boxes[keys] = int(self.list_of_boxes[keys].get())
        returned_list = start(self.daypart, self.number_of_trials, self.aggressive, self.list_of_boxes,
                              self.ratings_path, self.spots_path, root)
        for widget in root.winfo_children():
            widget.destroy()
        Finished(root, returned_list, self.daypart)


class Ym():
    def __init__(self, master):

        self.config = configparser.ConfigParser()
        if os.path.isfile('user.ini'):
            self.config.read('user.ini')
        else:
            self.config['DEFAULT'] = {'NETWORK': 'Travel',
                                      'DEFAULT_POTENTIAL': 780,
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
        ttk.Radiobutton(master, text="Aggressive", variable=self.aggressive, value=3).grid(row=2, column=0,
                                                                                           columnspan=2,
                                                                                           pady=(35, 0))
        ttk.Radiobutton(master, text="Moderate", variable=self.aggressive, value=2).grid(row=2, column=1,
                                                                                         columnspan=2,
                                                                                         pady=(35, 0))
        ttk.Radiobutton(master, text="Conservative", variable=self.aggressive, value=1).grid(row=2, column=2,
                                                                                             columnspan=2,
                                                                                             pady=(35, 0))
        self.aggressive.set(1)

        self.configure = ttk.Button(master, text="Customize Potential", command=self.configure,
                                    width=48).grid(column=0, columnspan=2, row=3, pady=(40, 0))
        self.calculate = ttk.Button(master, text="Okay", command=self.calculate, width=48).grid(column=2, columnspan=2,
                                                                                                row=3, pady=(40, 0))

        self.progress = ttk.Progressbar(master, orient="horizontal",
                                        length=200, mode="determinate").grid_forget()

    def configure(self):
        for items in root.grid_slaves():
            items.grid_forget()
        ChangePotential(root, self.daypart_variable.get(), self.aggressive.get(), self.v.get(),
                        self.config['DEFAULT']['DEFAULT_POTENTIAL'], self.config['DEFAULT']['RATINGS_PATH'],
                        self.config['DEFAULT']['SPOTS_PATH'])

    def calculate(self):

        frame = import_ratings(self.daypart_variable.get(), self.config['DEFAULT']['RATINGS_PATH'])
        id_list = frame['ID'].tolist()
        spots_lists = [[] for i in repeat(None, len(id_list))]
        for x in range(0, len(id_list)):
            spots_lists[x].append(str(id_list[x]) + ' ')
        spots_frame = preempt_credit_names(self.daypart_variable.get(), self.config['DEFAULT']['SPOTS_PATH'])
        first = spots_frame[' Primary Demo'].unique()
        demo_frame = pd.DataFrame()
        demo_frame['ID'] = frame['ID']
        for demo_cats in first:
            demo_frame[demo_cats] = frame[sum_dict_names[demo_cats]].sum(axis=1) / 30

        demo_list = list(first)

        running_imps = []

        time_dict = dict(zip(self.get_hours_from_daypart(self.daypart_variable.get()),
            repeat(int(self.config['DEFAULT']['DEFAULT_POTENTIAL']))))

        after_placed_imps_shortfall = place_placed_spots(spots_frame, id_list, demo_frame, first, time_dict,
                                                         spots_lists)

        with Pool(4) as p:
            returned = p.starmap(start,
                                 zip(repeat(spots_lists), repeat(time_dict), repeat(id_list), repeat(spots_frame),
                                     repeat(demo_frame), repeat(demo_list), range(self.v.get()),
                                     repeat(after_placed_imps_shortfall), repeat(self.aggressive.get()),
                                     ), chunksize=1)
        d = dict(returned)
        for items in root.grid_slaves():
            items.grid_forget()

        winning = max(d, key=d.get)

        returned = finish(spots_lists, time_dict, id_list, spots_frame, demo_frame, demo_list,
                          winning, after_placed_imps_shortfall, self.aggressive.get(),
                          self.config['DEFAULT']['RATINGS_PATH'], self.daypart_variable.get())

        Finished(root, returned, self.daypart_variable.get())

    @staticmethod
    def get_hours_from_daypart(daypart):
        options = [i for i in range(7, 24)]
        if daypart == "Prime Access":
            hour_options = options[11:13]
        elif daypart == "Weekend":
            hour_options = options[:13]
        elif daypart == "Daytime":
            hour_options = options[2:8]
        elif daypart == "Early Fringe":
            hour_options = options[8:11]
        else:
            hour_options = options[14:]
        return hour_options

    @staticmethod
    def exit_file():
        exit()

    def change_default_ini(self):
        for widget in root.winfo_children():
            widget.destroy()
        DefaultEdit(root, self.config)

    def update_daypart(self, current):
        menu = self.daypart['menu']
        menu.delete(0, 'end')
        self.daypart.config(state=NORMAL)
        if current == 'Saturday' or current == 'Sunday':
            options_day = ['Weekend', 'Prime 1', 'Prime 2']
            for daypart in options_day:
                menu.add_command(label=daypart, command=lambda value=daypart:
                self.daypart_variable.set(value))
        else:
            options_day = ["Daytime", "Early Fringe", "Prime Access", 'Prime 1', 'Prime 2']
            for daypart in options_day:
                menu.add_command(label=daypart, command=lambda value=daypart:
                self.daypart_variable.set(value))


if __name__ == "__main__":
    root = Tk()
    res = Ym(root)
    root.mainloop()