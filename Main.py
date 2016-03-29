from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from Start import start
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.popup import Popup
from functools import partial


sm = ScreenManager()
finished_screen = Screen(name='Finished')
sm.add_widget(finished_screen)
screen = Screen(name='YieldManagement')
sm.add_widget(screen)




class YieldManagement(App):
    def build(self):
        box_layout = FloatLayout(size=(300, 300), background_color=[0, 100, 100, 1])

        day_spin = Spinner(size_hint=(.3, .1), pos_hint={'x': .15, 'y': .86}, background_color=[0, 1, 100, 1])
        day_spin.text = 'Day of Week'
        day_spin.values = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        spin = Spinner(size_hint=(.3, .1), pos_hint={'x': .50, 'y': .86}, background_color=[0, 1, 100, 1])
        spin.text = 'Choose a Daypart'
        spin.disabled = True

        btn1 = ToggleButton(text='1 Iteration', group='depth', size_hint=(.15, .15), pos_hint={'x': .10, 'y': .65})
        btn2 = ToggleButton(text='100 Iterations', group='depth', state='down', size_hint=(.15, .15),
                            pos_hint={'x': .30, 'y': .65})
        btn3 = ToggleButton(text='500 Iterations', group='depth', size_hint=(.15, .15),
                            pos_hint={'x': .50, 'y': .65})
        btn4 = ToggleButton(text='1000 Iterations', group='depth', size_hint=(.15, .15), pos_hint={'x': .70, 'y': .65})

        depth_label = Label(text='Depth of Search', size_hint=(.2, .2), pos_hint={'x': .39, 'y': .51})

        btn5 = ToggleButton(text='Aggressive', group='unplaced', size_hint=(.15, .15), pos_hint={'x': .20, 'y': .40})
        btn6 = ToggleButton(text='Moderate', group='unplaced', size_hint=(.15, .15), pos_hint={'x': .4, 'y': .40})
        btn7 = ToggleButton(text='Conservative', group='unplaced', state='down', size_hint=(.15, .15),
                            pos_hint={'x': .6, 'y': .40})

        unplaced_label = Label(text='Number of Unplaced Spots', size_hint=(.2, .2), pos_hint={'x': .36, 'y': .26})

        variable_label = Label(text='Variable Commercial Time?', size_hint=(.5, .2), pos_hint={'x': .05, 'y': .2})
        checkbox = CheckBox(size_hint=(.5, .2), pos_hint={'x': .40, 'y': .2})
        checkbox.disabled = True

        btn = Button(text='Calculate', size_hint=(.90, .2), pos_hint={'x': .05, 'y': .05},
                     background_color=[0, 1, 100, 1], disabled=True)

        day_spin.bind(text=partial(self.day_spin_selection, day_spin, spin))
        spin.bind(text=partial(self.spin_selection, spin, checkbox, btn))
        btn.bind(on_press=partial(self.callback, spin, ToggleButton.get_widgets('depth'),
                                  ToggleButton.get_widgets('unplaced'), box_layout, day_spin))
        checkbox.bind(on_press=partial(self.checkbox_pressed, spin, btn))

        box_layout.add_widget(btn1)
        box_layout.add_widget(btn2)
        box_layout.add_widget(btn3)
        box_layout.add_widget(btn4)
        box_layout.add_widget(btn5)
        box_layout.add_widget(btn6)
        box_layout.add_widget(btn7)

        box_layout.add_widget(unplaced_label)
        box_layout.add_widget(variable_label)
        box_layout.add_widget(depth_label)

        box_layout.add_widget(checkbox)
        box_layout.add_widget(day_spin)
        box_layout.add_widget(spin)
        box_layout.add_widget(btn)

        return box_layout

    def callback(self, spin, list_of_depth_buttons, list_of_aggressive_buttons, layout, day_spin, event):
        current = [t for t in list_of_depth_buttons if t.state == 'down'][0]
        if current.text == '1 Iteration':
            depth = 1
        elif current.text == '100 Iterations':
            depth = 100
        elif current.text == '500 Iterations':
            depth = 500
        else:
            depth = 1000
        current = [t for t in list_of_aggressive_buttons if t.state == 'down'][0]
        if current.text == 'Aggressive':
            factor = 0
        elif current.text == 'Moderate':
            factor = 250
        elif current.text == 'Conservative':
            factor = 500
        else:
            pass
        returned_list = start(spin.text, depth, factor)
        print returned_list[0]
        print returned_list[1]
        popup = Popup(title='All Done!',
                      content=Label(
                          text='All finished.  You had ' + str(returned_list[1]) + ' unplaced spots and ' + str(
                              round(returned_list[0], 2)) + ' imps in a file called ' + spin.text + ' ' + day_spin.text,
                          size_hint=(None, None), size=(750, 500), pos_hint={'x': .55, 'y': .05}))
        layout.add_widget(popup)


    def day_spin_selection(self, selection, event, another_event, yet_another):
        event.disabled = False
        if selection.values.index(selection.text) < 5:
            event.values = ['Daytime', 'Early Fringe', 'Prime Access', 'Prime 1', 'Prime 2']
        else:
            event.values = ['Weekend', 'Prime 1', 'Prime 2']

    def spin_selection(self, selection, event, another_event, yet_another, and_another):
        event.disabled = False
        another_event.disabled = False

    def checkbox_pressed(self, selection, event, another_event):
        event.text = "Continue"


class Finished(App):
    def build(self):
        box_layout = FloatLayout(size=(300, 300), background_color=[0, 100, 100, 1])
        trial_button = Button(text='Calculate', size_hint=(.90, .2), pos_hint={'x': .05, 'y': .05},
                              background_color=[0, 1, 100, 1], disabled=True)
        box_layout.add_widget(trial_button)
        finished_screen.add_widget(box_layout)
        return finished_screen


if __name__ == "__main__":
    YieldManagement().run()


