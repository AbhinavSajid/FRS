from tkinter import *
import os
import csvio

window = Tk(screenName=None, baseName=None, className='Tk', useTk=True)
window.bind('<Escape>', lambda event: window.destroy())
window.title('FRS')
window.geometry('480x854')
#window.minsize(960, 540)
# window.attributes('-fullscreen', True)

class Gui:
    def __init__(self):
        self.user = ''
        self.status = 'employee'
        self.logo_image = PhotoImage(file='images/logo.png')
        self.attendance_img = PhotoImage(file='images/attendance.png')
        self.logo_image_small = PhotoImage(file='images/logo_small.png')

    def add_text(self, widget, text, color):
        widget.delete("0", "end")
        if color is not False:
            widget.config(fg=color)
        if text is not False:
            widget.insert(0, text)


    def logo_page(self):
        frame = Label(window, bg='light yellow')
        frame.pack(expand=True, fill=BOTH)
        frame.pack_propagate(False)

        self.logo_image_big = PhotoImage(file='images/logo_big.png')
        label = Label(frame, image=self.logo_image_big)
        label.pack(pady=((window.winfo_screenheight()//2) - 354, 0))

        def proceed():
            label.destroy()
            self.departments()
        label.after(3000, proceed)


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
        title_home = Label(self.background, text='Attendance\nTracker',
                           font=('Ariel', 25, 'bold'), bg=bg, fg=fg)
        title_home.grid(row=1, column=1, columnspan=2, sticky='n', padx=(0, 0), pady=(0, 0))

        # add an image
        if os.path.exists("images/attendance.png"):
            attendance_img = Label(self.background, image=self.attendance_img, bd=0)
            attendance_img.grid(row=2, column=1,sticky='n', padx=(0, 0), pady=(0, 0))

        # add a button
        attendance_button = Button(self.background, text='self attendance',
                                   font=('Ariel', 20), bg=bg, command=self.self_attendance)
        attendance_button.grid(row=2, column=1, padx=(0, 0), pady=(60, 0))

        if os.path.exists("images/history.png"):
            self.history_img = PhotoImage(file='images/history.png')
            history_img = Label(self.background, image=self.history_img, bd=0)
            history_img.grid(row=2, column=2,sticky='n', padx=(0, 0), pady=(0, 0))

        history_button = Button(self.background, text='local history', font=('Ariel', 20), bg=bg,
                                command=lambda: self.history(self.user))
        history_button.grid(row=2, column=2, padx=(0, 0), pady=(60, 0))

        col_span = 1
        if os.path.exists("images/leaves.png"):
            self.leaves_img = PhotoImage(file='images/leaves.png')
            leaves_img = Label(self.background, image=self.leaves_img, bd=0)
            leaves_img.grid(row=3, column=1, columnspan=col_span, sticky='n', padx=(0, 0), pady=(0, 0))

        leaves_button = Button(self.background, text='leaves',
                                   font=('Ariel', 20), bg=bg, command=self.leaves)
        leaves_button.grid(row=3, column=1, columnspan=col_span, padx=(0, 0), pady=(60, 0))

        if self.status == 'employer':
            if os.path.exists("images/monitor.png"):
                self.monitor_img = PhotoImage(file='images/monitor.png')
                monitor_img = Label(self.background, image=self.monitor_img, bd=0)
                monitor_img.grid(row=3, column=2, columnspan=1, sticky='n', padx=(0, 0), pady=(0, 0))

                monitor_button = Button(self.background, text='monitor',
                                       font=('Ariel', 20), bg=bg, command=self.monitor)
                monitor_button.grid(row=3, column=2, columnspan=1, padx=(0, 0), pady=(60, 0))
        else:
            if os.path.exists("images/peer.png"):
                self.peer_img = PhotoImage(file='images/peer.png')
                peer_img = Label(self.background, image=self.peer_img, bd=0)
                peer_img.grid(row=3, column=2, columnspan=1, sticky='n', padx=(0, 0), pady=(0, 0))

                peer_button = Button(self.background, text='peer',
                                       font=('Ariel', 20), bg=bg, command=self.peer)
                peer_button.grid(row=3, column=2, columnspan=1, padx=(0, 0), pady=(60, 0))

        if self.user == '':
            log_in_button = Button(self.background, image=self.logo_image_small,
                                   bg=bg, command=self.departments)
        else:
            log_in_button = Button(self.background, text=f"{self.user.capitalize()}",
                                   font=('Ariel', 20), bg=bg, command=self.departments)
        log_in_button.grid(row=1, column=1, sticky='nw', padx=(0, 0), pady=(0, 0))

    def peer(self, text=''):
        for item in self.background.winfo_children():
            item.destroy()
        bg = 'light yellow'

        title_label = Label(self.background, text='Peer Attendance',
                            font=('Ariel', 25, 'bold'), bg=bg)
        title_label.grid(row=1, column=1, columnspan=2, padx=(0, 0), pady=(0, 0))


        back_button = Button(self.background, text='back', font=('Ariel', 20), bg=bg, command=self.home_page)
        back_button.grid(row=4, column=1, sticky='sw', pady=(0, 0))

        reason_label = Label(self.background, text=f"Employee number:", font=('Ariel', 20), bg=bg)
        reason_label.grid(row=2, column=1, columnspan=2, sticky='n', padx=(0, 0), pady=(0, 0))

        entry = Entry(self.background, font=('Ariel', 20), fg='grey')
        entry.grid(row=2, column=1, columnspan=2, sticky='n', padx=(0, 0), pady=(50, 0))
        entry.bind("<FocusIn>", lambda a: self.add_text(entry, ' ', "black"))
        entry.insert(0, ' enter employee id')

        def proceed():
            user = entry.get().strip()
            for row in csvio.get_rows('csv files/users.csv'):
                if row[0] == user:
                    self.self_attendance(user=entry.get().strip())
                    break
            else:
                self.peer('employee not found')


        enter_button = Button(self.background, text='detect face', font=('Ariel', 20), bg=bg, command=proceed)
        enter_button.grid(row=2, column=1, columnspan=2, sticky='n', pady=(100, 0))

        error_label = Label(self.background, text=f"{text}", font=('Ariel', 20), bg=bg, fg='red')
        error_label.grid(row=3, column=1, columnspan=2, sticky='n', padx=(0, 0), pady=(0, 0))

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
                                   font=('Ariel', 30), command=lambda: attendance(user_entry.get().strip()))
        attendance_button.grid(row=2, column=1, sticky='n', padx=(0, 0), pady=(0, 0))

        user_entry = Entry(self.background, font=('Ariel', 30), fg='grey')
        user_entry.grid(row=2, column=2, columnspan=1, sticky='n', padx=(0, 0), pady=(0, 0))
        user_entry.insert(0, ' username')
        user_entry.bind("<FocusIn>", lambda a: self.add_text(user_entry, ' ', "black"))

        def requests(approval='none'):
            rows = []
            for row in csvio.get_rows("csv files/leaves.csv"):
                if row[3] == 'undecided':
                    rows.append(row)
            if len(rows) != 0:
                request_button.config(text=f"by {rows[-1][0]} on {rows[-1][1]}\n{rows[-1][2]}")
                if approval == 'yes':
                    csvio.modify_row('csv files/leaves.csv', rows[-1], [rows[-1][0], rows[-1][1], rows[-1][2], 'yes'])
                    self.monitor()

                elif approval == 'no':
                    csvio.modify_row('csv files/leaves.csv', rows[-1], [rows[-1][0], rows[-1][1], rows[-1][2], 'no'])
                    self.monitor()

        leave_button = Button(self.background, text='leave requests',
                                   font=('Ariel', 30), command=lambda: requests('no'))
        leave_button.grid(row=3, column=1, sticky='n', padx=(0, 0), pady=(0, 0))

        request_button = Button(self.background, text='no pending requests',
                              font=('Ariel', 30), bg=bg, command=lambda: requests('yes'))
        request_button.grid(row=3, column=2, sticky='n',columnspan=2, padx=(0, 0), pady=(0, 0))
        requests()

    def self_attendance(self, text1='select punch time: ', user=None):
        for item in self.background.winfo_children():
            item.destroy()
        self.background.grid_rowconfigure(list(range(1, 5)), weight=1)
        self.background.grid_columnconfigure(list(range(1, 4)), weight=1)
        bg = 'light yellow'
        if user is None:
            user = self.user
        print('user', user)

        logo_img = Label(self.background, image=self.logo_image_small, bd=0, bg=bg)
        logo_img.grid(row=1, column=1, sticky='wn', padx=(0, 0), pady=(0, 0))

        title_label = Label(self.background, text='Take Attendance',
                            font=('Ariel', 20, 'bold'), bg=bg)
        title_label.grid(row=1, column=1, columnspan=3, padx=(0, 0), pady=(0, 0))

        def record(timing):
            text1 = csvio.write_row(user, timing)
            self.self_attendance(text1)

        text_label = Label(self.background, text=f"Date: {csvio.get_date()}", font=('Ariel', 20), bg=bg)
        text_label.grid(row=2, column=1, sticky='nw', columnspan=3, padx=(40, 0), pady=(0, 0))

        if user != '':
            fg = 'black' if text1[0] == 's' else 'dark red'
            self.text_label = Label(self.background, text=text1, font=('Ariel', 20), bg=bg, fg=fg)
            self.text_label.grid(row=2, column=1, sticky='nw', columnspan=3, padx=(40, 0), pady=(180, 0))

            for row in csvio.get_employee_history(user):
                if row[2] == 'in':
                    in_time = row[1]
                    text_label = Label(self.background, text=f"Your punch in time is already recorded as {in_time}",
                                       font=('Ariel', 20), bg=bg)
                    text_label.grid(row=2, column=1, sticky='nw', columnspan=3, padx=(40, 0), pady=(60, 0))
                if row[2] == 'out':
                    out_time = row[1]
                    text_label = Label(self.background, text=f"Your punch out time is already recorded as {out_time}",
                                       font=('Ariel', 20), bg=bg)
                    text_label.grid(row=2, column=1, sticky='nw', columnspan=3, padx=(40, 0), pady=(120, 0))

            in_button = Button(self.background, text='in', font=('Ariel', 25),
                                command=lambda: record('in'))
            in_button.grid(row=3, column=1, padx=(0, 0), pady=(0, 0))

            mid_button = Button(self.background, text='mid', font=('Ariel', 25),
                                command=lambda: record('mid'))
            mid_button.grid(row=3, column=2, padx=(0, 0), pady=(0, 0))

            out_button = Button(self.background, text='out', font=('Ariel', 25),
                                command=lambda: record('out'))
            out_button.grid(row=3, column=3, padx=(0, 0), pady=(0, 0))

        back_button = Button(self.background, text='back', font=('Ariel', 20), bg=bg, command=self.home_page)
        back_button.grid(row=4, column=1, sticky='sw', pady=(0, 0))


    def history(self, user, day=None):
        for item in self.background.winfo_children():
            item.destroy()

        if day is not None:
            if os.path.exists(f"attendance/{day}-09-2024.csv"):
                date = f"{day}-09-2024"
                rows = csvio.get_employee_history(user, file=f"attendance/{day}-09-2024.csv")
            else:
                rows = csvio.get_employee_history(user)
                date = csvio.get_date()
        else:
            rows = csvio.get_employee_history(user)
            date = csvio.get_date()

        row_count = len(rows) + 2
        if len(rows) == 0:
            row_count += 3
        bg = 'light yellow'

        self.background.grid_rowconfigure(1, weight=1)
        self.background.grid_rowconfigure(2, weight=9)
        self.background.grid_rowconfigure(3, weight=1)

        logo_img = Label(self.background, image=self.logo_image_small, bd=0, bg=bg)
        logo_img.grid(row=1, column=1, sticky='wn', padx=(0, 0), pady=(0, 0))

        title_label = Label(self.background, text=f"{user.capitalize()}'s\nAttendance History",
                            font=('Ariel', 15, 'bold'), bg=bg)
        title_label.grid(row=1, column=1, columnspan=2, padx=(0, 0), pady=(0, 0))

        frame = Label(self.background, bg='light blue')
        frame.grid(row=2, column=1, columnspan=2, sticky='nsew', padx=(15, 15), pady=(15, 15))
        frame.grid_rowconfigure(list(range(1, row_count)), weight=1)
        frame.grid_columnconfigure(list(range(1, 4)), weight=1)

        def update(day1):
            if int(day1) < 10:
                day1 = f"0{day1}"
                self.history(user, day1)

        date_frame = Frame(frame, bg='light blue')
        date_frame.grid(row=1, column=1, columnspan=3, sticky='nsew', padx=(0, 0), pady=(0, 0))


        day_label = Label(date_frame, text=f"Date: {date}", font=('Ariel', 20), bg=bg)
        day_label.grid(row=1, column=1, sticky='n', padx=(20, 0), pady=(10, 0))

        day_spinbox = Spinbox(date_frame, from_=1, to=31, font=('Ariel', 25),
                              width=2, wrap=True, command=lambda: update(day_spinbox.get()))
        day_spinbox.grid(row=1, column=2, sticky='ne', padx=(60, 0), pady=(10, 0))
        day_spinbox.delete(0, "end")
        day_spinbox.insert(0, str(date[0: 3]))

        heading_label_1 = Label(frame, text = 'Time', font=('Ariel', 20), bg=bg)
        heading_label_1.grid(row=2, column=1, sticky='n', padx=(0, 0), pady=(0, 0))

        heading_label_2 = Label(frame, text='Details', font=('Ariel', 20), bg=bg)
        heading_label_2.grid(row=2, column=2, sticky='n', padx=(0, 0), pady=(0, 0))

        heading_label_2 = Label(frame, text='Coordinates', font=('Ariel', 20), bg=bg)
        heading_label_2.grid(row=2, column=3, sticky='n', padx=(0, 0), pady=(0, 0))

        if len(rows) == 0:
            text1 = ''
            rows1 = csvio.get_employee_history(user, 'csv files/leaves.csv')
            for row1 in rows1:
                if row1[3] == 'yes':
                    if row1[1] == date:
                        text1 = ' (leave)'
            label = Label(frame, text=f"{user} has no attendance\n on this day{text1}", font=('Ariel', 20), bg=bg)
            label.grid(row=3, column=1, sticky='n',columnspan=3, padx=(0, 0), pady=(60, 0))

        i = 1
        for row in rows:
            col1_label = Label(frame, text = f"{row[1]}", font=('Ariel', 20), bg=bg)
            col1_label.grid(row=3, column=1, sticky='n', padx=(0, 0), pady=(i*60, 0))

            col2_label = Label(frame, text=f"{row[2]}", font=('Ariel', 20), bg=bg)
            col2_label.grid(row=3, column=2, sticky='n', padx=(0, 0), pady=(i * 60, 0))
            i += 1

        back_button = Button(self.background, text='back', font=('Ariel', 20), bg=bg, command=self.home_page)
        back_button.grid(row=3, column=1, sticky='sw', pady=(0, 0))


    def leaves(self, text1=''):
        for item in self.background.winfo_children():
            item.destroy()
        self.background.grid_rowconfigure(list(range(1, 6)), weight=1)
        self.background.grid_columnconfigure(list(range(1, 3)), weight=1)
        bg = 'light yellow'

        logo_img = Label(self.background, image=self.logo_image_small, bd=0, bg=bg)
        logo_img.grid(row=1, column=1, sticky='wn', padx=(0, 0), pady=(0, 0))

        title_label = Label(self.background, text=f"Request Leave",
                            font=('Ariel', 20, 'bold'), bg=bg)
        title_label.grid(row=1, column=1, columnspan=2, padx=(0, 0), pady=(10, 0))

        day_spinbox = Spinbox(self.background, from_=1, to=31, font=('Ariel', 30),
                              width=2, wrap=True)
        day_spinbox.grid(row=2, column=1, sticky='ne', padx=(0, 10), pady=(0, 0))

        label = Label(self.background, text=f"{csvio.get_date()[2:]}", font=('Ariel', 20), bg=bg)
        label.grid(row=2, column=2, sticky='nw', padx=(0, 0), pady=(0, 0))

        reason_label = Label(self.background, text=f"Enter reason:", font=('Ariel', 20), bg=bg)
        reason_label.grid(row=3, column=1,columnspan=2, sticky='n', padx=(0, 0), pady=(0, 0))

        entry = Entry(self.background, font=('Ariel', 20), fg='grey')
        entry.grid(row=3, column=1, columnspan=2, sticky='n', padx=(0, 0), pady=(50, 0))
        entry.bind("<FocusIn>", lambda a: self.add_text(entry, ' ', "black"))
        entry.insert(0, ' provide reason')

        def select(raw_day, reason):
            if reason == '' or reason == ' provide reason':
                self.leaves(f'please provide a reason')
            if int(raw_day) >= 10:
                day = f"{raw_day}"
            else:
                day = f"0{raw_day}"
            rows = csvio.get_employee_history(self.user, "csv files/leaves.csv")
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

        select_button = Button(self.background, text='request', font=('Ariel', 25),
                            command=lambda: select(day_spinbox.get(), entry.get().strip()))
        select_button.grid(row=4, column=1, columnspan=2, sticky = 'n', padx=(0, 0), pady=(0, 0))

        note_label = Label(self.background, text=text1, font=('Ariel', 20), bg=bg)
        note_label.grid(row=5, column=1, columnspan=2, sticky='n', padx=(0, 0), pady=(0, 0))

        allowed = []
        allowed_str = ''
        rows = csvio.get_employee_history(self.user, 'csv files/leaves.csv')
        for row in rows:
            if row[3] == 'yes':
                allowed.append(row[1][:-5])
                if allowed_str == '':
                    allowed_str += row[1][:-5]
                else:
                    allowed_str += f", {row[1][:-5]}"
        if len(allowed) != 0:
            allowed_label = Label(self.background, text=f"Allowed leaves: {allowed_str}", font=('Ariel', 20), bg=bg)
            allowed_label.grid(row=5, column=1, columnspan=2, sticky='n', padx=(0, 0), pady=(0, 0))

        back_button = Button(self.background, text='back', font=('Ariel', 20), bg=bg, command=self.home_page)
        back_button.grid(row=5, column=1, sticky='sw', pady=(0, 0))


    def departments(self):

        bg = 'light yellow'
        fg = 'black'

        self.background = Label(window, bg=bg)
        self.background.pack(fill=BOTH, expand=True)

        '''for item in self.background.winfo_children():
            item.destroy()'''
        self.background.grid_rowconfigure(list(range(1, 8)), weight=1)
        self.background.grid_columnconfigure(list(range(1, 3)), weight=1)

        title_login = Label(self.background, text='Choose department',
                            font=('Ariel', 25, 'bold'), bg=bg, fg=fg)
        title_login.grid(row=1, column=1, columnspan=2, sticky='n', padx=(0, 0), pady=(50, 0))

        back_button = Button(self.background, text='back', font=('Ariel', 20), bg=bg, command=self.home_page)
        back_button.grid(row=7, column=1, sticky='sw', pady=(0, 0))

        if os.path.exists("images/dept1.png"):
            attendance_img = Label(self.background, image=self.attendance_img, bd=0)
            attendance_img.grid(row=2, column=1,sticky='n', padx=(0, 0), pady=(0, 0))

        dept_button = Button(self.background, text='dept1', font=('Ariel', 20), bg=bg,
                             command=lambda: self.login(dept='dept1'))
        dept_button.grid(row=2, column=2, columnspan=1, sticky='n', pady=(0, 0))

        if os.path.exists("images/dept2.png"):
            attendance_img = Label(self.background, image=self.attendance_img, bd=0)
            attendance_img.grid(row=3, column=1,sticky='n', padx=(0, 0), pady=(0, 0))

        dept_button = Button(self.background, text='dept2', font=('Ariel', 20), bg=bg,
                             command= lambda: self.login(dept='dept2'))
        dept_button.grid(row=3, column=2, columnspan=1, sticky='n', pady=(0, 0))

        if os.path.exists("images/dept3.png"):
            attendance_img = Label(self.background, image=self.attendance_img, bd=0)
            attendance_img.grid(row=4, column=1,sticky='n', padx=(0, 0), pady=(0, 0))

        dept_button = Button(self.background, text='dept3', font=('Ariel', 20), bg=bg,
                             command=lambda: self.login(dept='dept3'))
        dept_button.grid(row=4, column=2, columnspan=1, sticky='n', pady=(0, 0))

        if os.path.exists("images/dept4.png"):
            attendance_img = Label(self.background, image=self.attendance_img, bd=0)
            attendance_img.grid(row=5, column=1,sticky='n', padx=(0, 0), pady=(0, 0))

        dept_button = Button(self.background, text='dept4', font=('Ariel', 20), bg=bg,
                             command=lambda: self.login(dept='dept4'))
        dept_button.grid(row=5, column=2, columnspan=1, sticky='n', pady=(0, 0))

        if os.path.exists("images/dept5.png"):
            attendance_img = Label(self.background, image=self.attendance_img, bd=0)
            attendance_img.grid(row=6, column=1,sticky='n', padx=(0, 0), pady=(0, 0))

        dept_button = Button(self.background, text='dept5', font=('Ariel', 20), bg=bg,
                             command=lambda: self.login(dept='dept5'))
        dept_button.grid(row=6, column=2, columnspan=2, sticky='n', pady=(0, 0))

        label = Label(self.background, text="Made by The Algorithm Army",
                            font=('Ariel', 25, 'bold'), bg=bg, fg=fg)
        label.grid(row=7, column=1, columnspan=2, sticky='n', padx=(0, 0), pady=(0, 0))


    def login(self,dept, mode='login', error=''):
        for item in self.background.winfo_children():
            item.destroy()
        self.background.grid_rowconfigure(list(range(1, 6)), weight=1)
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
                            font=('Ariel', 25, 'bold'), bg=bg, fg=fg)
        title_login.grid(row=1, column=1, columnspan=2, sticky='n', padx=(0, 0), pady=(50, 0))

        if os.path.exists("images/{dept}.png"):
            self.dept_img = PhotoImage(file=f"images/{dept}.png")
            dept_img = Label(self.background, image=self.history_img, bd=0)
            dept_img.grid(row=2, column=1, columnspan=2, sticky='n', padx=(0, 0), pady=(0, 0))

        back_button = Button(self.background, text='back', font=('Ariel', 20), bg=bg, command=self.home_page)
        back_button.grid(row=1, column=1, sticky='nw', pady=(0, 0))

        user_label = Label(self.background, text='Username', font=('Ariel', 20), bg=bg)
        user_label.grid(row=3, column=1, sticky='ne', padx=(0, 20), pady=(0, 0))
        self.user_entry = Entry(self.background, font=('Ariel', 20), fg='grey', width=15)
        self.user_entry.grid(row=3, column=2, sticky='nw', padx=(0, 0), pady=(0, 0))
        self.user_entry.bind("<FocusIn>", lambda a: self.add_text(self.user_entry, ' ', "black"))
        self.user_entry.insert(0, ' username')

        pass_label = Label(self.background, text='Password', font=('Ariel', 20), bg=bg)
        pass_label.grid(row=3, column=1, sticky='ne', padx=(0, 20), pady=(80, 0))
        self.pass_entry = Entry(self.background, font=('Ariel', 20), fg='grey', width=15)
        self.pass_entry.grid(row=3, column=2, sticky='nw', padx=(0, 0), pady=(80, 0))
        self.pass_entry.bind("<FocusIn>", lambda a: self.add_text(self.pass_entry, ' ', "black"))
        self.pass_entry.insert(0, ' password')

        self.error_label = Label(self.background, text=error, font=('Ariel', 12), bg=bg, fg='red')
        self.error_label.grid(row=4, column=1, columnspan=2, sticky='n', padx=(0, 0), pady=(0, 0))

        def check_login(user, password):
            out = csvio.valid_user(mode, user, password)
            if out != 'true':
                if out == 'user':
                    self.login(mode, 'Username not found, Sign up?')
                elif out == 'password':
                    self.login(mode, 'Incorrect password')
            else:
                self.user = user.strip().lower()
                print(csvio.get_employee_history(self.user, 'csv files/users.csv'))
                self.status = csvio.get_employee_history(self.user, 'csv files/users.csv')[0][2]
                self.home_page()

        suggest_login = Button(self.background, text=txt, font=('Ariel', 15),
                               bg=bg, relief='flat', command=lambda: self.login(alt_mode), fg='blue')
        suggest_login.grid(row=3, column=1, columnspan=2, pady=(100, 0))

        login_button = Button(self.background, text=text, font=('Ariel', 25), bg='red', fg='white',
                              command=lambda: check_login(self.user_entry.get(), self.pass_entry.get()))
        login_button.grid(row=5, column=1, columnspan=2, pady=(30, 40))

        change_button = Button(self.background, text="change department", font=('Ariel', 15), bg='blue',fg='white',
                              command=lambda: check_login(self.user_entry.get(), self.pass_entry.get()))
        change_button.grid(row=6, column=1, columnspan=2, pady=(30, 40))

mygui = Gui()
mygui.logo_page()
window.mainloop()




