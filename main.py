from tkinter import *
import os
import csvio

window = Tk(screenName=None, baseName=None, className='Tk', useTk=True)
window.bind('<Escape>', lambda event: window.destroy())
window.title('FRS')
window.geometry('1280x720')
window.minsize(960, 540)
# window.attributes('-fullscreen', True)

class Gui:
    def __init__(self):
        self.user = 'abhinav'
        self.status = 'employer'

    def add_text(self, widget, text, color):
        widget.delete("0", "end")
        if color is not False:
            widget.config(fg=color)
        if text is not False:
            widget.insert(0, text)


    def home_page(self):
        for item in window.winfo_children():
            item.destroy()
        bg = 'light yellow'
        fg = 'black'

        self.background = Label(window, bg=bg)
        self.background.pack(fill=BOTH, expand=True)
        self.background.grid_columnconfigure(list(range(1, 3)), weight=1)
        self.background.grid_rowconfigure(1, weight=1)
        self.background.grid_rowconfigure(2, weight=5)
        self.background.grid_rowconfigure(3, weight=5)
        # add a label
        title_home = Label(self.background, text='Home',
                           font=('Ariel', 40, 'bold'), bg=bg, fg=fg)
        title_home.grid(row=1, column=1, columnspan=2, sticky='n', padx=(0, 0), pady=(0, 0))

        # add an image
        if os.path.exists("images/attendance.png"):
            self.attendance_img = PhotoImage(file='images/attendance.png')
            attendance_img = Label(self.background, image=self.attendance_img, bd=0)
            attendance_img.grid(row=2, column=1,sticky='n', padx=(0, 0), pady=(0, 0))

        # add a button
        attendance_button = Button(self.background, text='self attendance',
                                   font=('Ariel', 30), bg=bg, command=self.self_attendance)
        attendance_button.grid(row=2, column=1, padx=(0, 0), pady=(60, 0))

        if os.path.exists("images/history.png"):
            self.history_img = PhotoImage(file='images/history.png')
            history_img = Label(self.background, image=self.history_img, bd=0)
            history_img.grid(row=2, column=2,sticky='n', padx=(0, 0), pady=(0, 0))

        history_button = Button(self.background, text='local history', font=('Ariel', 30), bg=bg,
                                command=lambda: self.history(self.user))
        history_button.grid(row=2, column=2, padx=(0, 0), pady=(60, 0))

        col_span = 1 if self.status == 'employer' else 2
        if os.path.exists("images/leaves.png"):
            self.leaves_img = PhotoImage(file='images/leaves.png')
            leaves_img = Label(self.background, image=self.leaves_img, bd=0)
            leaves_img.grid(row=3, column=1, columnspan=col_span, sticky='n', padx=(0, 0), pady=(0, 0))

        leaves_button = Button(self.background, text='leaves',
                                   font=('Ariel', 30), bg=bg, command=self.leaves)
        leaves_button.grid(row=3, column=1, columnspan=col_span, padx=(0, 0), pady=(60, 0))

        if self.status == 'employer':
            if os.path.exists("images/monitor.png"):
                self.monitor_img = PhotoImage(file='images/monitor.png')
                monitor_img = Label(self.background, image=self.monitor_img, bd=0)
                monitor_img.grid(row=3, column=2, columnspan=1, sticky='n', padx=(0, 0), pady=(0, 0))

                monitor_button = Button(self.background, text='monitor',
                                       font=('Ariel', 30), bg=bg, command=self.monitor)
                monitor_button.grid(row=3, column=2, columnspan=1, padx=(0, 0), pady=(60, 0))

        if self.user == '':
            log_in_button = Button(self.background, text='login',
                                       font=('Ariel', 30), bg=bg, command=self.login)
        else:
            log_in_button = Button(self.background, text=f"{self.user.capitalize()}",
                                   font=('Ariel', 30), bg=bg, command=self.login)
            log_in_button.grid(row=1, column=1, sticky='nw', padx=(0, 0), pady=(0, 0))


    def monitor(self):
        for item in self.background.winfo_children():
            item.destroy()
        bg = 'light yellow'

        title_label = Label(self.background, text='Monitor',
                            font=('Ariel', 30, 'bold'), bg=bg)
        title_label.grid(row=1, column=1, columnspan=2, padx=(0, 0), pady=(0, 0))

        back_button = Button(self.background, text='back', font=('Ariel', 30), bg=bg, command=self.home_page)
        back_button.grid(row=1, column=1, sticky='nw', pady=(0, 0))
        
        def attendance(user):
            self.history(user)
        attendance_button = Button(self.background, text='check attendance',
                                   font=('Ariel', 30), bg=bg, command=lambda: attendance(user_entry.get().strip()))
        attendance_button.grid(row=2, column=1, sticky='n', padx=(0, 0), pady=(0, 0))

        user_entry = Entry(self.background, font=('Ariel', 30), fg='grey')
        user_entry.grid(row=2, column=2, columnspan=1, sticky='n', padx=(0, 0), pady=(0, 0))
        user_entry.insert(0, ' username')
        user_entry.bind("<FocusIn>", lambda a: self.add_text(user_entry, ' ', "black"))

        def requests(approval='none'):
            rows = []
            for row in csvio.get_rows("leaves.csv"):
                if row[3] == 'undecided':
                    rows.append(row)
            if len(rows) != 0:
                request_button.config(text=f"by {rows[-1][0]} on {rows[-1][1]}\n{rows[-1][2]}")
                if approval == 'yes':
                    csvio.modify_row('leaves.csv', rows[-1], [rows[-1][0], rows[-1][1], rows[-1][2], 'yes'])
                    self.monitor()

                elif approval == 'no':
                    csvio.modify_row('leaves.csv', rows[-1], [rows[-1][0], rows[-1][1], rows[-1][2], 'no'])
                    self.monitor()

        leave_button = Button(self.background, text='leave requests',
                                   font=('Ariel', 30), bg=bg, command=lambda: requests('no'))
        leave_button.grid(row=3, column=1, sticky='n', padx=(0, 0), pady=(0, 0))

        request_button = Button(self.background, text='no pending requests',
                              font=('Ariel', 30), bg=bg, command=lambda: requests('yes'))
        request_button.grid(row=3, column=2, sticky='n',columnspan=2, padx=(0, 0), pady=(0, 0))
        requests()

    def self_attendance(self, text1='select punch time'):
        for item in self.background.winfo_children():
            item.destroy()
        self.background.grid_rowconfigure(list(range(1, 5)), weight=1)
        self.background.grid_columnconfigure(list(range(1, 4)), weight=1)
        bg = 'light yellow'

        title_label = Label(self.background, text='Take Attendance',
                            font=('Ariel', 30, 'bold'), bg=bg)
        title_label.grid(row=1, column=1, columnspan=3, padx=(0, 0), pady=(0, 0))

        back_button = Button(self.background, text='back', font=('Ariel', 30), bg=bg, command=self.home_page)
        back_button.grid(row=1, column=1, sticky='nw', pady=(0, 0))

        def record(timing):
            text1 = csvio.write_row(self.user, timing)
            self.self_attendance(text1)

        text_label = Label(self.background, text=f"Date: {csvio.get_date()}", font=('Ariel', 30), bg=bg)
        text_label.grid(row=2, column=1, sticky='nw', columnspan=3, padx=(0, 0), pady=(0, 0))

        if self.user != '':
            fg = 'black' if text1[0] == 's' else 'dark red'
            self.text_label = Label(self.background, text=text1, font=('Ariel', 30), bg=bg, fg=fg)
            self.text_label.grid(row=2, column=1, sticky='nw', columnspan=3, padx=(0, 0), pady=(180, 0))

            for row in csvio.get_employee_history(self.user):
                if row[2] == 'in':
                    in_time = row[1]
                    text_label = Label(self.background, text=f"Your punch in time is already recorded as {in_time}",
                                       font=('Ariel', 30), bg=bg)
                    text_label.grid(row=2, column=1, sticky='nw', columnspan=3, padx=(0, 0), pady=(60, 0))
                if row[2] == 'out':
                    out_time = row[1]
                    text_label = Label(self.background, text=f"Your punch out time is already recorded as {out_time}",
                                       font=('Ariel', 30), bg=bg)
                    text_label.grid(row=2, column=1, sticky='nw', columnspan=3, padx=(0, 0), pady=(120, 0))

            in_button = Button(self.background, text='in', font=('Ariel', 30), bg=bg,
                                command=lambda: record('in'))
            in_button.grid(row=3, column=1, padx=(0, 0), pady=(0, 0))

            mid_button = Button(self.background, text='mid', font=('Ariel', 30), bg=bg,
                                command=lambda: record('mid'))
            mid_button.grid(row=3, column=2, padx=(0, 0), pady=(0, 0))

            out_button = Button(self.background, text='out', font=('Ariel', 30), bg=bg,
                                command=lambda: record('out'))
            out_button.grid(row=3, column=3, padx=(0, 0), pady=(0, 0))

    def history(self, user, day=None):
        for item in self.background.winfo_children():
            item.destroy()

        if (day is not None) and (os.path.exists(f"attendance/{day}-09-2024.csv")):
            date = f"{day}-09-2024"
            rows = csvio.get_employee_history(user, file=f"attendance/{day}-09-2024.csv")
        else:
            rows = csvio.get_employee_history(user)
            date = csvio.get_date()

        row_count = len(rows) + 2
        if len(rows) == 0:
            row_count += 3
        bg = 'light yellow'

        self.background.grid_rowconfigure(1, weight=1)
        self.background.grid_rowconfigure(2, weight=9)

        title_label = Label(self.background, text=f"{user.capitalize()}'s Attendance History",
                            font=('Ariel', 30, 'bold'), bg=bg)
        title_label.grid(row=1, column=1, columnspan=2, padx=(0, 0), pady=(0, 0))

        back_button = Button(self.background, text='back', font=('Ariel', 30), bg=bg, command=self.home_page)
        back_button.grid(row=1, column=1, sticky='nw', pady=(0, 0))

        frame = Label(self.background, bg='light blue')
        frame.grid(row=2, column=1, columnspan=2, sticky='nsew', padx=(30, 30), pady=(30, 30))
        frame.grid_rowconfigure(list(range(1, row_count)), weight=1)
        frame.grid_columnconfigure(list(range(1, 4)), weight=1)

        def update(day1):
            if int(day1) < 10:
                day1 = f"0{day1}"
                self.history(self.user, day1)
        day_label = Label(frame, text=f"Date: {date}", font=('Ariel', 25), bg=bg)
        day_label.grid(row=1, column=1, sticky='n', padx=(0, 0), pady=(10, 0))

        day_spinbox = Spinbox(frame, from_=1, to=31, font=('Ariel', 25),
                              width=2, wrap=True, command=lambda: update(day_spinbox.get()))
        day_spinbox.grid(row=1, column=1, sticky='ne', padx=(60, 0), pady=(10, 0))
        day_spinbox.delete(0, "end")
        day_spinbox.insert(0, str(date[0: 3]))

        heading_label_1 = Label(frame, text = 'Time', font=('Ariel', 20), bg=bg)
        heading_label_1.grid(row=2, column=1, sticky='n', padx=(0, 0), pady=(0, 0))

        heading_label_2 = Label(frame, text='Details', font=('Ariel', 20), bg=bg)
        heading_label_2.grid(row=2, column=2, sticky='n', padx=(0, 0), pady=(0, 0))

        heading_label_2 = Label(frame, text='Coordinates', font=('Ariel', 20), bg=bg)
        heading_label_2.grid(row=2, column=3, sticky='n', padx=(0, 0), pady=(0, 0))

        if len(rows) == 0:
            label = Label(frame, text=f"{user} has no attendance on this day", font=('Ariel', 20), bg=bg)
            label.grid(row=3, column=1, sticky='n',columnspan=3, padx=(0, 0), pady=(60, 0))

        i = 1
        for row in rows:
            col1_label = Label(frame, text = f"{row[1]}", font=('Ariel', 20), bg=bg)
            col1_label.grid(row=3, column=1, sticky='n', padx=(0, 0), pady=(i*60, 0))

            col2_label = Label(frame, text=f"{row[2]}", font=('Ariel', 20), bg=bg)
            col2_label.grid(row=3, column=2, sticky='n', padx=(0, 0), pady=(i * 60, 0))
            i += 1

    def leaves(self, text1=''):
        for item in self.background.winfo_children():
            item.destroy()
        self.background.grid_rowconfigure(list(range(1, 6)), weight=1)
        self.background.grid_columnconfigure(list(range(1, 3)), weight=1)
        bg = 'light yellow'

        title_label = Label(self.background, text=f"Request Leave",
                            font=('Ariel', 30, 'bold'), bg=bg)
        title_label.grid(row=1, column=1, columnspan=2, padx=(0, 0), pady=(0, 0))

        back_button = Button(self.background, text='back', font=('Ariel', 30), bg=bg, command=self.home_page)
        back_button.grid(row=1, column=1, sticky='nw', pady=(0, 0))

        day_spinbox = Spinbox(self.background, from_=1, to=31, font=('Ariel', 30),
                              width=2, wrap=True)
        day_spinbox.grid(row=2, column=1, sticky='ne', padx=(0, 10), pady=(0, 0))

        label = Label(self.background, text=f"{csvio.get_date()[2:]}", font=('Ariel', 30), bg=bg)
        label.grid(row=2, column=2, sticky='nw', padx=(0, 0), pady=(0, 0))

        reason_label = Label(self.background, text=f"Enter reason:", font=('Ariel', 30), bg=bg)
        reason_label.grid(row=3, column=1,columnspan=2, sticky='n', padx=(0, 0), pady=(0, 0))

        entry = Entry(self.background, font=('Ariel', 30), bg='light grey')
        entry.grid(row=3, column=1, columnspan=2, sticky='n', padx=(0, 0), pady=(50, 0))

        def select(raw_day, reason):
            if reason == '':
                self.leaves(f'please provide a reason')
            if int(raw_day) >= 10:
                day = f"{raw_day}"
            else:
                day = f"0{raw_day}"
            rows = csvio.get_employee_history(self.user, "leaves.csv")
            post = 'th'
            if day == '01':
                post = 'st'
            elif day == '02':
                post = 'nd'
            elif day == '03':
                post = 'rd'
            brk = False
            if len(rows) != 0:
                for row in rows:
                    if row[1] == f"{day}{csvio.get_date()[2:]}":
                        brk = True
                        self.leaves(f'already requested leave on {raw_day}{post}')
            if not brk:
                csvio.write_leave(self.user, f"{day}{csvio.get_date()[2:]}", reason)
                self.leaves(f'requested leave on {raw_day}{post}')


        select_button = Button(self.background, text='request', font=('Ariel', 30), bg=bg,
                            command=lambda: select(day_spinbox.get(), entry.get().strip()))
        select_button.grid(row=4, column=1, columnspan=2, sticky = 'n', padx=(0, 0), pady=(0, 0))

        note_label = Label(self.background, text=text1, font=('Ariel', 20), bg=bg)
        note_label.grid(row=5, column=1, columnspan=2, sticky='n', padx=(0, 0), pady=(0, 0))

    def login(self, mode='login', error=''):
        for item in self.background.winfo_children():
            item.destroy()
        self.background.grid_rowconfigure(list(range(1, 5)), weight=1)
        bg = 'light yellow'
        fg = 'black'

        if mode == 'login':
            txt = "Don't have an account?  Sign up instead"
            text = 'Login'
            alt_mode = 'signup'
        else:
            txt = 'Already have an account?  Login instead'
            text = 'Sign Up'
            alt_mode = 'login'

        title_login = Label(self.background, text=text,
                            font=('Ariel', 40, 'bold'), bg=bg, fg=fg)
        title_login.grid(row=1, column=1, columnspan=2, sticky='n', padx=(0, 0), pady=(50, 0))

        back_button = Button(self.background, text='back', font=('Ariel', 30), bg=bg, command=self.home_page)
        back_button.grid(row=1, column=1, sticky='nw', pady=(0, 0))

        user_label = Label(self.background, text='Username', font=('Ariel', 30), bg=bg)
        user_label.grid(row=2, column=1, sticky='ne', padx=(0, 20), pady=(0, 0))
        self.user_entry = Entry(self.background, font=('Ariel', 30), fg='grey', width=30)
        self.user_entry.grid(row=2, column=2, sticky='nw', padx=(0, 0), pady=(0, 0))
        self.user_entry.bind("<FocusIn>", lambda a: self.add_text(self.user_entry, ' ', "black"))
        self.user_entry.insert(0, ' username')

        pass_label = Label(self.background, text='Password', font=('Ariel', 30), bg=bg)
        pass_label.grid(row=2, column=1, sticky='ne', padx=(0, 20), pady=(80, 0))
        self.pass_entry = Entry(self.background, font=('Ariel', 30), fg='grey', width=30)
        self.pass_entry.grid(row=2, column=2, sticky='nw', padx=(0, 0), pady=(80, 0))
        self.pass_entry.bind("<FocusIn>", lambda a: self.add_text(self.pass_entry, ' ', "black"))
        self.pass_entry.insert(0, ' password')

        self.error_label = Label(self.background, text=error, font=('Ariel', 12), bg=bg, fg='red')
        self.error_label.grid(row=3, column=1, columnspan=2, sticky='n', padx=(0, 0), pady=(0, 0))

        def check_login(user, password):
            out = csvio.valid_user(mode, user, password)
            if out != 'true':
                if out == 'user':
                    self.login(mode, 'Username not found, Sign up?')
                elif out == 'password':
                    self.login(mode, 'Incorrect password')
            else:
                self.user = user.strip().lower()
                self.home_page()

        suggest_login = Button(self.background, text=txt, font=('Ariel', 15),
                               bg=bg, relief='flat', command=lambda: self.login(alt_mode), fg='blue')
        suggest_login.grid(row=2, column=1, columnspan=2, pady=(100, 0))

        login_button = Button(self.background, text=text, font=('Ariel', 25),
                              command=lambda: check_login(self.user_entry.get(), self.pass_entry.get()))
        login_button.grid(row=4, column=1, columnspan=2, pady=(30, 40))

mygui = Gui()
mygui.home_page()
window.mainloop()




