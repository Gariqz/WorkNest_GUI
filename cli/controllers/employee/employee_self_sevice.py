import json
from utils.utils import read_json_db, save_data
from datetime import datetime

# function to format date
def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d %B %Y")
    except ValueError:
        return date_str

# function to format time
def format_time(time_str):
    if not time_str or time_str == "N/A":
        return "N/A"
    try:
        return datetime.strptime(time_str, "%H:%M").strftime("%I:%M %p")
    except ValueError:
        return time_str

# view profile
def view_profile(user):
    print("\n--- 📝 View Profile ---")
    for key, value in user.items():
        print(f"{key.capitalize():<15}: {value}")

# function edit profile
def edit_profile(user):
    print("\n--- ✏️ Edit Profile ---")
    data = read_json_db()
    employees = data.get("employees", [])

    # Cari employee berdasarkan ID user
    employee = next((e for e in employees if e["id"] == user["id"]), None)
    if not employee:
        print(f"⚠️ No employee found with ID: {user['id']}")
        return

    print("\nCurrent Profile Information:")
    for key, value in employee.items():
        print(f"{key.capitalize():<15}: {value}")

    print("\nEnter new values for the fields you want to update. Leave blank to keep the current value.")

    # edit name
    while True:
        new_name = input(f"Name ({employee['name']}): ").strip()
        if not new_name:
            print("⚠️ Name cannot be left blank. Please provide a value.")
            continue
        if not all(part.isalpha() or part.isspace() for part in new_name):
            print("⚠️ Name must contain only alphabets.")
            continue
        employee['name'] = new_name
        break

    # edit NIK
    while True:
        new_nik = input(f"NIK ({employee['nik']}): ").strip()
        if not new_nik:
            print("⚠️ NIK cannot be left blank.")
            continue
        if not new_nik.isdigit():
            print("⚠️ NIK must be an integer.")
            continue
        if not (13 <= len(new_nik) <= 16):
            print("⚠️ NIK must be between 13 and 16 characters long.")
            continue
        employee['nik'] = new_nik
        break

    # edit gender
    while True:
        new_gender = input(f"Gender ({employee['gender']}): ").strip().lower()
        if new_gender not in ['male', 'female']:
            print("⚠️ Gender must be 'Male' or 'Female'.")
            continue
        employee['gender'] = new_gender
        break

    # edit birth place
    while True:
        new_birth_place = input(f"Birth Place ({employee['birth_place']}): ").strip()
        if not new_birth_place:
            print("⚠️ Birth place cannot be left blank.")
            continue
        if not new_birth_place.isalpha():
            print("⚠️ Birth place must contain only alphabets.")
            continue
        employee['birth_place'] = new_birth_place
        break

    # edit birth date
    while True:
        new_birth_date = input(f"Birth Date ({employee['birth_date']}): ").strip()
        if not new_birth_date:
            print("⚠️ Birth date cannot be left blank.")
            continue
        try:
            datetime.strptime(new_birth_date, '%Y-%m-%d')
            employee['birth_date'] = new_birth_date
            break
        except ValueError:
            print("⚠️ Invalid date format. Please use YYYY-MM-DD.")

    # edit phone
    while True:
        new_phone = input(f"Phone ({employee['phone']}): ").strip()
        if new_phone:
            if not new_phone.isdigit() or len(new_phone) < 10:
                print("⚠️ Phone number must contain at least 10 digits and only numbers.")
                continue
            employee['phone'] = new_phone
        else:
            employee['phone'] = None
        break

    # edit religion
    while True:
        new_religion = input(f"Religion ({employee['religion']}): ").strip()
        if new_religion:
            if not new_religion.isalpha():
                print("⚠️ Religion must contain only alphabets.")
                continue
            employee['religion'] = new_religion
        else:
            employee['religion'] = None
        break

    # edit marital status
    while True:
        new_marital_status = input(f"Marital Status ({employee['marital_status']}): ").strip().lower()
        if new_marital_status not in ['single', 'married', 'divorced']:
            print("⚠️ Invalid marital status. Choose from 'Single', 'Married', or 'Divorced'.")
            continue
        employee['marital_status'] = new_marital_status
        break

    # edit address
    while True:
        new_address = input(f"Address ({employee['address']}): ").strip()
        if not new_address:
            print("⚠️ Address cannot be left blank.")
            continue
        if len(new_address) < 11:
            print("⚠️ Address must be at least 11 characters long.")
            continue
        employee['address'] = new_address
        break

    # edit Email
    while True:
        new_email = input(f"Email ({employee['email']}): ").strip()
        if not new_email:
            print("⚠️ Email cannot be left blank.")
            continue
        if "@employee.nest" not in new_email:
            print("⚠️ Email must contain '@employee.nest'.")
            continue
        employee['email'] = new_email
        break

    # edit password
    while True:
        new_password = input(f"Password: ").strip()
        if not new_password:
            print("⚠️ Password cannot be left blank.")
            continue
        if len(new_password) < 8:
            print("⚠️ Password must be at least 8 characters long.")
            continue
        employee['password'] = new_password
        break

    save_data(data)
    print("\n✅ Profile updated successfully!")

# function to view attendance records
def view_attendance(user):
    print("\n--- 📅 View Attendance Records ---")
    data = read_json_db()
    attendances = data['attendances']
    user_attendance = [att for att in attendances if att['employee_id'] == user['id']]

    if user_attendance:
        print("\nAttendance Records:\n")
        print(f"{'Date':<20} {'Check-in':<15} {'Check-out':<15}")
        print("-" * 50)
        for record in user_attendance:
            formatted_date = format_date(record['attendance_date'])
            formatted_check_in = format_time(record['check_in'])
            formatted_check_out = format_time(record.get('check_out', "N/A"))
            print(f"{formatted_date:<20} {formatted_check_in:<15} {formatted_check_out:<15}")
    else:
        print("No attendance records found.")

# function to record attendance
def record_attendance(user):
    print("\n--- 📝 Record Attendance ---")

    # get employee ID from user
    employee_id = user.get("id")
    if not employee_id:
        print("⚠️ Unable to determine the employee ID.")
        return

    while True:
        attendance_date_input = input("Enter Attendance Date (YYYY-MM-DD): ").strip()
        if not attendance_date_input:
            print("⚠️ Attendance date cannot be empty. Please provide a valid date.")
            continue
        try:
            attendance_date = datetime.strptime(attendance_date_input, "%Y-%m-%d").date().isoformat()
            break
        except ValueError:
            print("⚠️ Invalid date format. Please use YYYY-MM-DD.")

    while True:
        check_in_input = input("Enter Check-in Time: ").strip()
        if not check_in_input:
            print("⚠️ Check-in time cannot be empty.")
            continue
        try:
            check_in_time = datetime.strptime(check_in_input, "%H:%M").time()  
            check_in = check_in_time.isoformat()  # Format ISO untuk penyimpanan
            break
        except ValueError:
            print("⚠️ Invalid time format. Please use HH:MM.")

    while True:
        check_out_input = input("Enter Check-out Time (HH:MM): ").strip()
        if not check_out_input:
            print("⚠️ Check-out time cannot be empty.")
            continue
        try:
            check_out_time = datetime.strptime(check_out_input, "%H:%M").time()  
            if check_out_time < check_in_time:
                print("⚠️ Check-out time cannot be earlier than check-in time.")
            else:
                check_out = check_out_time.isoformat()  
                break
        except ValueError:
            print("⚠️ Invalid time format. Please use HH:MM.")


    data = read_json_db()
    employees = data.get("employees", [])
    attendances = data.get("attendances", [])

    employee = next((e for e in employees if e["id"] == employee_id), None)
    if not employee:
        print(f"⚠️ No employee found with ID: {employee_id}")
        return

    # check for duplicate attendance record
    for att in attendances:
        if att["employee_id"] == employee_id and att["attendance_date"] == attendance_date:
            print(f"⚠️ Attendance for {attendance_date} already exists for this employee.")
            return

    attendance_id = len(attendances) + 1
    new_record = {
        "attendance_id": attendance_id,
        "employee_id": employee_id,
        "attendance_date": attendance_date,
        "check_in": check_in,
        "check_out": check_out
    }
    attendances.append(new_record)
    data["attendances"] = attendances

    save_data(data)

    # output
    print(f"\n✅ Attendance recorded successfully for {employee['name']} on {format_date(attendance_date)}!")
    print(f"   Check-in: {format_time(check_in)}")
    if check_out:
        print(f"   Check-out: {format_time(check_out)}")
    else:
        print("   Check-out: Not yet checked out.")


# function to request leave
def request_leave(user):
    print("\n--- 🗒️ Request Leave ---")

    # get employee ID from user
    employee_id = user.get("id")
    if not employee_id:
        print("⚠️ Unable to determine the employee ID.")
        return

    while True:
        leave_type = input("Enter Leave Type (e.g., Sick, Vacation): ").strip()
        if leave_type:
            break
        print("⚠️ Leave Type cannot be empty. Please enter a valid leave type.")

    while True:
        start_date_input = input("Enter Start Date (YYYY-MM-DD): ").strip()
        if not start_date_input:
            print("⚠️ Start Date cannot be empty. Please enter a valid date.")
            continue
        try:
            start_date = datetime.strptime(start_date_input, "%Y-%m-%d").date().isoformat()
            break
        except ValueError:
            print("⚠️ Invalid Start Date format. Please use YYYY-MM-DD.")

    while True:
        end_date_input = input("Enter End Date (YYYY-MM-DD): ").strip()
        if not end_date_input:
            print("⚠️ End Date cannot be empty. Please provide a valid date.")
            continue
        try:
            end_date = datetime.strptime(end_date_input, "%Y-%m-%d").date().isoformat()
            if end_date >= start_date:
                break
            print("⚠️ End Date cannot be earlier than Start Date.")
        except ValueError:
            print("⚠️ Invalid End Date format. Please use YYYY-MM-DD.")


    while True:
        reason = input("Enter Leave Reason: ").strip()
        if reason:
            break
        print("⚠️ Leave Reason cannot be empty. Please enter a valid reason.")

    data = read_json_db()
    employees = data.get("employees", [])
    leave_requests = data.get("leave_requests", [])

    employee = next((e for e in employees if e["id"] == employee_id), None)
    if not employee:
        print(f"⚠️ No employee found with ID: {employee_id}")
        return

    leave_request_id = len(leave_requests) + 1
    new_request = {
        "leave_request_id": leave_request_id,
        "employee_id": employee_id,
        "leave_type": leave_type,
        "start_date": start_date,
        "end_date": end_date,
        "reason": reason,
        "applied_on": datetime.today().isoformat(),
        "status": "Pending"
    }
    leave_requests.append(new_request)
    data["leave_requests"] = leave_requests

    save_data(data)
    print(f"\n✅ Leave request submitted successfully for {employee['name']}!")


# function to view leave requests
def view_leave_status(user):
    print("\n=== 📂 View Leave Status ===")
    data = read_json_db()
    leave_requests = data.get('leave_requests', [])
    user_requests = [req for req in leave_requests if req['employee_id'] == user['id']]

    if user_requests:
        print("\n✨ Your Leave Requests ✨")
        print(f"{'='*50}")
        for idx, req in enumerate(user_requests, start=1):
            formatted_start_date = format_date(req['start_date'])
            formatted_end_date = format_date(req['end_date'])
            print(f"[{idx}]")
            print(f"📝 Type      : {req['leave_type']}")
            print(f"📅 Dates     : {formatted_start_date} ➡ {formatted_end_date}")
            print(f"💬 Reason    : {req['reason']}")
            print(f"📌 Status    : {req['status']}")
            print(f"{'-'*50}")
    else:
        print("\n⚠️ No leave requests found. You have not submitted any leave requests yet!")


