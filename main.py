# import all required library
import customtkinter
import tkinter
from tkinter import messagebox
import json
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

# set the font of the graphs created
sns.set(font_scale=0.3)
# checking if the json file does not exist
# if it doesn't, create an empty file so
if not os.path.exists("users.json"):
    with open('users.json', 'w') as file:
        json.dump({}, file)
# does the same with the csv file
if not os.path.exists('test.csv'):
    pd.DataFrame({'e': [0]}).to_csv('test.csv')


# reads the csv and create a line plot with the csv values
def create_plot():
    df = pd.read_csv('test.csv')
    # label the columns
    df.columns = ['Model', 'Temp']
    f, ax = plt.subplots(figsize=(2, 1.6))
    # plots it
    sns.lineplot(df['Temp'])

    return f


# a class to hold the users data
class User:
    def __init__(self):
        # create an empty user profile when initiatec
        self.loggedin = False
        self.username = ''
        self.password = ''
        self.name = ''
        self.info = {}

    # when this function is called it empties all values
    def reset(self):
        self.loggedin = False
        self.username = None
        self.password = None
        self.name = None
        self.info = None

    def try_login(self, username, password):
        # tries to log in
        try:
            # read the file and saves to a handle
            with open('users.json', 'r') as f:
                users = json.load(f)
            # check if the username is part of the all the users
            if username in users:
                # check if the password is correct
                if password == users[username][0]:
                    print('Logged in')
                    self.loggedin = True
                    self.username = username
                    self.name = users[username][1]
                    self.password = password
                    self.info = users[username][2]

        except Exception as e:
            print(e)

    def delete_user(self):
        # wil delete user
        # get the data from the json
        with open('users.json', 'r') as f:
            users = dict(json.load(f))
        # remove the username with all its information from the json
        users.pop(self.username)
        # update teh new database
        with open('users.json', 'w') as f:
            json.dump(users, f)
        # reset user information as it has been deleted
        self.reset()


class MainPage(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.user = User()
        self.SignInWin = None
        self.signed_in = False
        self.data = []

        # configure window
        self.title("Plaque Pounder")
        self.geometry(f"{1110}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # configure sidebar
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=3, sticky='nsew')
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        # sidebar widgets
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Plaque Pounder",
                                                 font=customtkinter.CTkFont(size=20, weight='bold'))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        # sidebar radio buttons
        self.radio_var = tkinter.IntVar(value=0)
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.sidebar_frame,
                                                           variable=self.radio_var,
                                                           value=0, text='Home',
                                                           command=self.radio_button_event)
        self.radio_button_1.grid(row=1, column=0, pady=20, padx=20, sticky="nw")
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.sidebar_frame,
                                                           variable=self.radio_var,
                                                           value=1, text='Inbox',
                                                           command=self.radio_button_event)
        self.radio_button_2.grid(row=2, column=0, pady=20, padx=20, sticky="nw")
        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.sidebar_frame,
                                                           variable=self.radio_var,
                                                           value=2, text='Analytics',
                                                           command=self.radio_button_event)
        self.radio_button_3.grid(row=3, column=0, pady=20, padx=20, sticky="nw")
        self.radio_button_4 = customtkinter.CTkRadioButton(master=self.sidebar_frame,
                                                           variable=self.radio_var,
                                                           value=3, text='Friends',
                                                           command=self.radio_button_event)
        self.radio_button_4.grid(row=4, column=0, pady=20, padx=20, sticky="nw")
        self.radio_button_5 = customtkinter.CTkRadioButton(master=self.sidebar_frame,
                                                           variable=self.radio_var,
                                                           value=4, text='Settings',
                                                           command=self.radio_button_event)
        self.radio_button_5.grid(row=5, column=0, pady=20, padx=20, sticky='nw')

        # create home frame
        self.dashboard_frame_cover = customtkinter.CTkFrame(self)
        self.dashboard_frame_cover.grid(row=0, column=1, columnspan=3, rowspan=3, sticky='nsew', padx=20, pady=20)
        self.dashboard_frame = customtkinter.CTkScrollableFrame(self.dashboard_frame_cover, height=528, width=858)
        self.dashboard_frame.grid_rowconfigure((1, 2), weight=0)

        self.dashboard_frame.grid(row=0, column=1, columnspan=3, rowspan=3, sticky='nsew')
        # create inbox frame
        self.inbox_frame = customtkinter.CTkFrame(self)
        self.inbox_frame.grid(row=0, column=1, columnspan=3, rowspan=3, sticky='nsew', padx=20, pady=20)
        # create analystics frame
        self.analytics_frame = customtkinter.CTkFrame(self)
        self.analytics_frame.grid(row=0, column=1, columnspan=3, rowspan=3, sticky='nsew', padx=20, pady=20)
        # create friends frame
        self.friends_frame = customtkinter.CTkFrame(self)
        self.friends_frame.grid(row=0, column=1, columnspan=3, rowspan=3, sticky='nsew', padx=20, pady=20)
        # create settings frame
        self.settings_frame = customtkinter.CTkFrame(self)
        self.settings_frame.grid(row=0, column=1, columnspan=3, rowspan=3, sticky='nsew', padx=20, pady=20)

        # Dashboard widgets
        # create alll frames to hold the widgets
        self.top_bar_frame = customtkinter.CTkFrame(self.dashboard_frame, height=20)
        self.top_bar_frame.grid(row=0, column=0, columnspan=5, sticky='nsew')
        self.dash_title_label = customtkinter.CTkLabel(self.top_bar_frame, text=f'Welcome {self.user.username}')
        self.dash_title_label.grid(row=0, column=0, padx=10, pady=10, sticky='nws')

        self.total_brushes_frame = customtkinter.CTkFrame(self.dashboard_frame, width=200, height=110)
        self.total_brushes_frame.grid(row=1, column=0, padx=10, pady=10)
        self.total_uptime_frame = customtkinter.CTkFrame(self.dashboard_frame, width=200, height=110)
        self.total_uptime_frame.grid(row=1, column=1, padx=10, pady=10)
        self.total_teeth_cleaned_frame = customtkinter.CTkFrame(self.dashboard_frame, width=200, height=110)
        self.total_teeth_cleaned_frame.grid(row=1, column=2, padx=10, pady=10)
        self.top_pounders_frame = customtkinter.CTkFrame(self.dashboard_frame, width=200, height=110)
        self.top_pounders_frame.grid(row=1, column=3, padx=10, pady=10)

        # make it that the frame does not change to fit the widgets inside and stay the width and height specified
        self.total_brushes_frame.grid_propagate(False)
        self.total_uptime_frame.grid_propagate(False)
        self.total_teeth_cleaned_frame.grid_propagate(False)
        self.top_pounders_frame.grid_propagate(False)

        self.total_brushes_label = customtkinter.CTkLabel(self.total_brushes_frame,
                                                          text='Total Brushes')
        self.total_brushes_label.grid(row=0, column=0, sticky='nw', pady=(0, 10), padx=10)
        self.total_brushes_data_label = customtkinter.CTkLabel(self.total_brushes_frame, text='0',
                                                               font=customtkinter.CTkFont(size=30, weight='bold'))
        self.total_brushes_data_label.grid(row=1, column=0, sticky='we', pady=20, padx=10)
        self.total_uptime_label = customtkinter.CTkLabel(self.total_uptime_frame,
                                                         text="Total Uptime")
        self.total_uptime_label.grid(row=0, column=0, sticky='nw', pady=(0, 10), padx=10)
        self.total_uptime_data_label = customtkinter.CTkLabel(self.total_uptime_frame, text='0 mins',
                                                              font=customtkinter.CTkFont(size=30, weight='bold'))
        self.total_uptime_data_label.grid(row=1, column=0, sticky='we', pady=20, padx=10)
        self.total_teeth_cleaned_label = customtkinter.CTkLabel(self.total_teeth_cleaned_frame,
                                                                text='Total Teeth Cleaned')
        self.total_teeth_cleaned_label.grid(row=0, column=0, sticky='nw', pady=(0, 10), padx=10)
        self.total_teeth_cleaned_data_label = customtkinter.CTkLabel(self.total_teeth_cleaned_frame, text='0',
                                                                     font=customtkinter.CTkFont(size=30, weight='bold'))
        self.total_teeth_cleaned_data_label.grid(row=1, column=0, sticky='we', pady=20, padx=10)
        self.top_pounders_label = customtkinter.CTkLabel(self.top_pounders_frame,
                                                         text='Top # of pounders')
        self.top_pounders_label.grid(row=0, column=0, sticky='nw', pady=(0, 10), padx=10)
        self.top_pounders_data_label = customtkinter.CTkLabel(self.top_pounders_frame, text='0',
                                                              font=customtkinter.CTkFont(size=30, weight='bold'))
        self.top_pounders_data_label.grid(row=1, column=0, sticky='we', pady=20, padx=10)

        # frames to display graphs
        self.data_graph_frame = customtkinter.CTkFrame(self.dashboard_frame)
        self.data_graph_frame.grid(row=2, column=0, columnspan=2, pady=20, sticky='news')
        self.data_pie_frame = customtkinter.CTkFrame(self.dashboard_frame, width=300, height=300)
        self.data_pie_frame.grid(row=2, column=2, columnspan=2, pady=20, padx=30)

        self.data_pie_frame.grid_propagate(False)
        self.data_graph_label = customtkinter.CTkLabel(self.data_graph_frame, text='Pounding Performance',
                                                       font=customtkinter.CTkFont(size=15, weight='bold'))
        self.data_graph_label.grid(row=0, column=0, sticky='nsw', padx=10)
        self.data_pie_label = customtkinter.CTkLabel(self.data_pie_frame, text='Popular Pounding Pastimes',
                                                     font=customtkinter.CTkFont(size=15, weight='bold'))
        self.data_pie_label.grid(row=0, column=0, sticky='nsw', padx=10)

        # load the csv data and create line graph from that data
        self.fig = create_plot()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.data_graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky='news', padx=30, pady=10, columnspan=3)

        # a scrollable frame to display recent brushes
        self.data_scroll_frame = customtkinter.CTkScrollableFrame(self.dashboard_frame, width=800, height=400)
        self.data_scroll_frame.grid(row=3, column=0, columnspan=5, pady=50, padx=10)

        self.data_title_label = customtkinter.CTkLabel(self.data_scroll_frame, text='Recent Brushes',
                                                       font=customtkinter.CTkFont(size=15, weight='bold'))
        self.data_title_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky='nws')
        # all the headers for the brushes
        self.data_date_title_label = customtkinter.CTkLabel(self.data_scroll_frame, text='Date')
        self.data_date_title_label.grid(row=1, column=0, padx=30, pady=(10, 20))
        self.data_toothbrush_title_label = customtkinter.CTkLabel(self.data_scroll_frame, text='Toothbrush Used')
        self.data_toothbrush_title_label.grid(row=1, column=1, padx=30, pady=(10, 20))
        self.data_teeth_title_label = customtkinter.CTkLabel(self.data_scroll_frame, text='Teeth Cleaned')
        self.data_teeth_title_label.grid(row=1, column=2, padx=30, pady=(10, 20))
        self.data_location_title_label = customtkinter.CTkLabel(self.data_scroll_frame, text='Location')
        self.data_location_title_label.grid(row=1, column=3, padx=30, pady=(10, 20))
        self.data_full2_title_label = customtkinter.CTkLabel(self.data_scroll_frame, text='Full 2 Minutes')
        self.data_full2_title_label.grid(row=1, column=4, padx=30, pady=(10, 20))

        # Inbox widgets
        self.inbox_label = customtkinter.CTkLabel(self.inbox_frame, text='Inbox page')
        self.inbox_label.grid(row=0, column=0, padx=10, pady=10)
        # Analytics widgets
        self.analytics_label = customtkinter.CTkLabel(self.analytics_frame, text='Analytics page')
        self.analytics_label.grid(row=0, column=0, padx=10, pady=10)
        # Friends widgets
        self.friends_label = customtkinter.CTkLabel(self.friends_frame, text='Friends page')
        self.friends_label.grid(row=0, column=0, padx=10, pady=10)
        # Settings widgets
        # change the appearnce of the app
        self.appearance_mode_label = customtkinter.CTkLabel(self.settings_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        # when the combobox value get changed wun the change appearance mode event function
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.settings_frame,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.appearance_mode_optionemenu.set('Dark')
        # change the size of the widgets of the app
        self.scaling_label = customtkinter.CTkLabel(self.settings_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        # if the combobox changes, call the change scaling event function
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.settings_frame,
                                                               values=["80%", "90%", "100%", "110%", "120%", "130%",
                                                                       "140%", "150%", "200%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        self.scaling_optionemenu.set("100%")
        # a logout button that runs the logout function
        self.logout_button = customtkinter.CTkButton(self.settings_frame, command=self.logout, text='Logout')
        self.logout_button.grid(row=9, column=0, padx=20, pady=20, sticky='nsew')
        # a delete user button the runs the delete user funtion when pressed
        self.delete_button = customtkinter.CTkButton(self.settings_frame, command=self.delete_user, text='Delete User')
        self.delete_button.grid(row=10, column=0, padx=30, pady=30, sticky='nsew')

        # making sure the right frame is displayed
        self.radio_button_event()
        # make sure the appearance is the same as the combobox displayed
        self.change_appearance_mode_event(self.appearance_mode_optionemenu.get())
        # make it so the app cant me resized
        self.resizable(False, False)
        # open the sign-in page
        self.open_sign_in()

    def delete_user(self):
        # delete user function
        # sends a conformation box to stop any miss clicks
        choose = messagebox.askyesno('Delete User', "Are you sure to delete user")
        # if yes delete user and open the sign in again
        if choose:
            self.user.delete_user()
            self.open_sign_in()

    def radio_button_event(self):
        # changes the frame displayed
        # first get the value of the radio buttons
        rad_var = self.radio_var.get()
        if rad_var == 0:
            # raise dashboard if 0
            self.dashboard_frame_cover.tkraise()
        elif rad_var == 1:
            self.inbox_frame.tkraise()
        elif rad_var == 2:
            self.analytics_frame.tkraise()
        elif rad_var == 3:
            self.friends_frame.tkraise()
        elif rad_var == 4:
            self.settings_frame.tkraise()
        # depending on  the value each frame gets raised

    def logout(self):
        # logs out the user by first reseting user information and then opening the sign in page
        self.user.reset()
        self.open_sign_in()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        # changes the appearance of the app when called
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        # changes the size of the widgets when called
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def open_sign_in(self):
        # opens the sign in window
        if self.SignInWin is None or not self.SignInWin.winfo_exists():
            self.SignInWin = SignIn(self)  # create window if its None or destroyed
            # "grabs" the window meaning no other window can be interacted with while it is open
            self.SignInWin.grab_set()
            self.SignInWin.focus()  # and focus it when opened
        else:
            self.SignInWin.focus()  # if window exists focus it

    def config_new_user(self):
        # runes when a user signs in
        # will change the values pf the label with relvant data of the user
        # change the name to the user's name
        self.dash_title_label.configure(text=f'Welcome {self.user.name}')

        # load all user data
        with open('users.json', 'r') as f:
            users = dict(json.load(f))
        num_user = 0
        all_users_time = []
        # get all time cleaned by each user
        for key, value in users.items():
            if len(value[2]) > 0:
                num_user += 1
                user_time = 0
                for key2, value2 in value[2].items():
                    user_time += value2['Time Cleaned']
                # adds the final time to a list
                all_users_time.append(user_time)
        # remove all duplicates
        all_users_time = list(set(all_users_time))
        all_users_time.sort(reverse=True)  # sorts the list

        dates = []
        info = []
        total_teeth_cleaned = 0
        total_brushes = 0
        time_brushed = 0.0
        # get all brushes from the user's info
        for key, value in self.user.info.items():
            # seperates the dates and thew info
            dates.append(key)
            info.append(value)
        for i in range(len(dates)):
            # runs through info adding time cleaned amount of brushes and teeth cleaned
            time_brushed += info[i]['Time Cleaned']
            total_brushes += 1
            total_teeth_cleaned += info[i]['Teeth Cleaned']
        # finds the rank of the pounder
        rank = 'NA'
        for i in range(len(all_users_time)):
            if all_users_time[i] == time_brushed:
                rank = i + 1

        # configue the label to display the information
        self.total_uptime_data_label.configure(text=f'{time_brushed} mins')
        self.total_brushes_data_label.configure(text=f'{total_brushes}')
        self.total_teeth_cleaned_data_label.configure(text=f'{total_teeth_cleaned}')
        self.top_pounders_data_label.configure(text=f'#{rank}')

        # deletes all data that is in the recent brushes tab if there is none then nothing happens
        for i in self.data:
            for e in i:
                e.destroy()
        # creates an empty list
        self.data = []
        dates_to_append = 10
        if len(dates) < 10:
            dates_to_append = len(dates)
        for i in range(dates_to_append):
            # add the brushing data to the recent brushes frame
            self.data.append(
                [
                    customtkinter.CTkLabel(self.data_scroll_frame, text=dates[i]),
                    customtkinter.CTkLabel(self.data_scroll_frame, text=info[i]['Toothbrush Used']),
                    customtkinter.CTkLabel(self.data_scroll_frame, text=f"{info[i]['Teeth Cleaned']}"),
                    customtkinter.CTkLabel(self.data_scroll_frame, text=info[i]['Location']),
                    customtkinter.CTkLabel(self.data_scroll_frame, text=f"{info[i]['Full 2 Minutes']}")
                ])
            # place the data
            # 'it' is the column
            it = 0
            for e in self.data[i]:
                e.grid(row=i + 2, column=it, padx=10, pady=10, sticky='news')
                it += 1


# a sign in page
class SignIn(customtkinter.CTkToplevel):
    def __init__(self, win: MainPage):
        super().__init__()
        print('INIT')
        self.app = win
        self.title('Pounder Sign in')
        # create the sign in frame and create new acc frame
        self.signin = customtkinter.CTkFrame(self, width=self.winfo_width(), height=self.winfo_height())
        self.signin.grid(row=0, column=0, sticky="nsew")
        self.create_new_acc = customtkinter.CTkFrame(self, width=self.winfo_width(), height=self.winfo_height())
        self.create_new_acc.grid(row=0, column=0, sticky="nsew")
        self.signin.tkraise()  # the sign in page on top

        # sign in page widgets
        self.label = customtkinter.CTkLabel(self.signin, text="Please Sign in",
                                            font=customtkinter.CTkFont(size=20, weight='bold'))
        self.label.grid(row=0, column=0, padx=20, pady=(20, 0), columnspan=2, sticky='n')

        self.username_entry = customtkinter.CTkEntry(self.signin, placeholder_text="Username")
        self.username_entry.grid(row=1, column=1, padx=20, pady=20, sticky="e")
        self.username_label = customtkinter.CTkLabel(self.signin, text='Username:')
        self.username_label.grid(row=1, column=0, padx=20, pady=20, sticky='w')

        self.password_entry = customtkinter.CTkEntry(self.signin, placeholder_text="Password", show='*')
        self.password_entry.grid(row=2, column=1, padx=20, pady=20, sticky="e")
        self.password_label = customtkinter.CTkLabel(self.signin, text='Password:')
        self.password_label.grid(row=2, column=0, padx=20, pady=20, sticky='w')

        self.submit_button = customtkinter.CTkButton(self.signin, command=self.submit, text="Submit")
        self.submit_button.grid(row=3, column=0, padx=10, pady=10, sticky='sw')
        self.create_new_acc_button = customtkinter.CTkButton(self.signin, command=self.raise_create,
                                                             text="New Account Page", hover_color="green")
        self.create_new_acc_button.grid(row=3, column=1, padx=10, pady=10, sticky='se')

        # create account widgets
        self.create_acc_label = customtkinter.CTkLabel(self.create_new_acc, text="Please Enter Your Details",
                                                       font=customtkinter.CTkFont(size=20, weight='bold'))
        self.create_acc_label.grid(row=0, column=0, padx=20, pady=(20, 0), columnspan=2, sticky='n')

        self.new_username_entry = customtkinter.CTkEntry(self.create_new_acc, placeholder_text="Username")
        self.new_username_entry.grid(row=1, column=1, padx=20, pady=20, sticky="e")
        self.new_name_label = customtkinter.CTkEntry(self.create_new_acc, placeholder_text="Your Name")
        self.new_name_label.grid(row=1, column=0, padx=20, pady=20, sticky='w')

        self.new_password_entry = customtkinter.CTkEntry(self.create_new_acc, placeholder_text="Confirm Password",
                                                         show='*')
        self.new_password_entry.grid(row=2, column=1, padx=20, pady=20, sticky="e")
        self.new_password_entry2 = customtkinter.CTkEntry(self.create_new_acc, placeholder_text="Password", show='*')
        self.new_password_entry2.grid(row=2, column=0, padx=20, pady=20, sticky='w')

        self.submit_user_button = customtkinter.CTkButton(self.create_new_acc, command=self.new_user,
                                                          text="Submit New User")
        self.submit_user_button.grid(row=3, column=0, padx=10, pady=10, sticky='sw')
        self.signin_acc_button = customtkinter.CTkButton(self.create_new_acc, command=self.raise_signin,
                                                         text="Sign In Page")
        self.signin_acc_button.grid(row=3, column=1, padx=10, pady=10, sticky='se')

        # set a protocol when the user closes this window
        self.protocol("WM_DELETE_WINDOW", self.quit_app)
        # make it so the window can't change size
        self.resizable(False, False)

    def new_user(self):
        # validate first
        # get all data
        password1 = f'{self.new_password_entry.get()}'.strip()
        password2 = f'{self.new_password_entry2.get()}'.strip()
        name = f'{self.new_name_label.get()}'.strip().title()
        username = f'{self.new_username_entry.get()}'.strip()
        # ask user if they agree to terms and conditions
        choose = messagebox.askyesno('Disclaimer',
                                     "By creating an account you agree to our terms and conditions\n"
                                     "Do you continue?")
        # if they don't, leave the funtion
        if not choose:
            return

        # make sure all fields are filled out
        if password1 == '' or password2 == '' or username == '' or name == '':
            messagebox.showwarning('Error', "Please make sure that all fields are filled out")
            return
        # make sure the passwords match
        if password1 != password2:
            messagebox.showwarning('Error', "Passwords do not match")
            return
        # check if the username is taken
        with open('users.json', 'r') as f:
            users = json.load(f)
        if username in users:
            messagebox.showwarning('Error', 'Username already taken')
            return
        # if all tests are passed create new account
        users[username] = [password1, name, {}]
        messagebox.showinfo('Success', "New account created")
        # and save it database
        with open('users.json', 'w') as f:
            json.dump(users, f)

    def quit_app(self):
        # destroy the main app when this is closed without logging in
        self.master.destroy()

    def raise_signin(self):
        # raise the sign in page
        self.signin.tkraise()

    def raise_create(self):
        # raise the create new acc page
        self.create_new_acc.tkraise()

    def submit(self):
        # on submit try to sign in
        self.app.user.try_login(self.username_entry.get(), self.password_entry.get())
        if self.app.user.loggedin:
            # if signed in, create a new user
            self.app.config_new_user()
            # and destroy this window
            self.destroy()
        else:
            # if it didn't sign in either password or username in wrong
            messagebox.showwarning("Incorrect Username or Password", "Incorrect username or password")


# if this is the main file
if __name__ == "__main__":
    # create the app
    app = MainPage()
    # and run the main loop of the app
    app.mainloop()
