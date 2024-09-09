import csv
import datetime
import geocoder
import os

g = geocoder.ip('me')
location = g.latlng

current_time = datetime.datetime.now()
if current_time.day >= 10:
    day = current_time.day
else:
    day = f"0{current_time.day}"
if current_time.month >= 10:
    month = current_time.month
else:
    month = f"0{current_time.month}"

date = f"{day}-{month}-{current_time.year}"


def valid_user(mode, user, password):
    user = user.strip().lower()
    password = password.strip()
    if mode == 'login':
        with open('users.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if row[0] == user:
                    if row[1] == password:
                        return "true"
                    else:
                        return 'password'
            return 'user'
    else:
        with open('users.csv', 'a+', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if row[0] == user:
                    return "username is already in use"
            csvwriter = csv.writer(csvfile)
            row = [user, password, 'employee']
            csvwriter.writerow(row)


def write_row(name, timing):
    file = f"attendance/{date}.csv"
    with open(file, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        time = f"{current_time.hour}:{current_time.minute}"
        lst = [name, time, timing, location]
        if timing == 'in':
            if len(get_employee_history(name)) == 0:
                csvwriter.writerow(lst)
                return f"{timing} punch added as {time}"
            else:
                return 'You have have already clocked in'
        if timing == 'mid':
            rows = get_employee_history(name)
            if len(rows) != 0:
                for row in rows:
                    if row[2] == 'out':
                        return 'you have already clocked out'
                else:
                    csvwriter.writerow(lst)
                    return f"{timing} punch added as {time}"
        if timing == 'out':
            rows = get_employee_history(name)
            if len(rows) != 0:
                for row in rows:
                    if row[2] == 'out':
                        return 'you have already clocked out'
                else:
                    csvwriter.writerow(lst)
                    return f"{timing} punch added as {time}"


def get_employee_history(name, file=f"attendance/{date}.csv"):
    with open(file, 'r', newline='') as csvfile:
        rows = []
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if len(row) != 0:
                if row[0] == name:
                    rows.append(row)
        return rows


def get_rows(file):
    with open(file, 'r', newline='') as csvfile:
        rows = []
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if len(row) != 0:
                rows.append(row)
        return rows


def get_date():
    return date


def modify_row(file_name, old_value, new_value):
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        rows.remove(old_value)
        rows.append(new_value)

    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)


def write_leave(name, date1, reason):
    with open("leaves.csv", 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        lst = [name, date1, reason, 'undecided']
        csvwriter.writerow(lst)













