import json
import os
from datetime import datetime, timedelta
FILE_NAME = "expense_database.json"
transactions = {}
#  Data ko JSON file me SAVE karne wala function 
def save_data():
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(transactions, file, indent=4)
    except Exception as e:
        print(f"❌ Error Saving the data: {e}")

#  Program shuru hote hi data LOAD karne wala function ---
def load_data():
    global transactions
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                data = json.load(file)
                transactions = {int(k): v for k, v in data.items()}
        except Exception as e:
            print(f"❌ Data load karne me error aaya: {e}")
            transactions = {}
    else:
        transactions = {}

# main screen 
def main_screen():
    print("=======================================")
    print("Personal Finance Manager")
    print("=======================================")
    print("")
    print("1. Add Expense\n2. View All Expenses\n3. Delete Expense\n4. Update Expense\n5. Last month summary\n6. Category summary\n7. Total Expense\n8. Highest Expense\n9. Exit ")
    user_choice = check_input("Enter choice", max_val = 9)
    if user_choice == 1:
        return add_expense()
    elif user_choice == 2:
        return all_expenses()
    elif user_choice == 3:
        return delete_expense()
    elif user_choice == 4:
        return update_expense()
    elif user_choice == 5:
        return last_month_expense()
    elif user_choice == 6:
        return category_expense()
    elif user_choice == 7:
        return total_expense()
    elif user_choice == 8:
        return highest_expense()
    else:
        print("thanks visit again")
        return False


#function to add expense
def add_expense():
    expense_id = None
    if not transactions:
        expense_id = 1
    else:
        expense_id = int(list(transactions.keys())[-1])
        expense_id += 1
    amount = check_input("Enter the Amount: ")
    category = category_check()
    if category == "exit":
        return True
    print("Do You want to provide description for the expense\n1. Yes \n2. No")
    description_choice = check_input("Enter choice", max_val = 2, allow_exit = False)
    description = None
    if description_choice == 1:
        description = check_str("Enter Description: ")
    else:
        description = "Not available"
    date = date_input()
    expense_list = {"Amount" : amount, "Category" : category, "Description" : description, "Date" : date}
    transactions[expense_id] = expense_list
    print(f"Succesfully added the above expense with Expense Id : {expense_id} ")


#to get expense date
def date_input():
    while True:
        date = input("Enter date (DD-MM-YYYY): ")
        try:
            date = datetime.strptime(date, "%d-%m-%Y")
            return date.strftime("%d-%m-%Y")
        except ValueError:
            print("Invalid Date! Please enter valid date or in valid format")

#to take category input
def category_check(prompt = "Please select the category in which you want to put this expense: "):
    print(prompt)
    print("1. Food\n2. Transport\n3. Shopping\n4. Bills\n5. Entertainment\n6. Other")
    user_choice = check_input("Enter choice: ", max_val = 6)
    if user_choice == 1:
        return "Food"
    elif user_choice == 2:
        return "Transport"
    elif user_choice == 3:
        return "Shopping"
    elif user_choice == 4:
        return "Bills"
    elif user_choice == 5:
        return "Entertainment"
    elif user_choice == "exit":
        return exit_screen()
    else:
        value = check_str("Please enter the name of the category in which you to put this expense else enter None if you don't want to provide category for it")
        if value == "none":
            return "Other"
        else:
            return value.title()
    

#to check string only input
def check_str(prompt, allow_quit = False):
    while True:
        value = input(prompt)
        try:
            int(value)
            print("Only alphabetical words are allowed")
        except ValueError:
            value = value.strip()
            value = value.lower()
            if value == "exit":
                if allow_exit == True:
                    return "exit"
                else:
                    print("exit not allowed")
            else:
                return value

#to check input
def check_input(prompt, max_val = False, min_val = 1, allow_exit = True):
    while True:
        value = input(prompt)
        try:
            value = int(value)
            if max_val != False:
                if min_val <= value <= max_val:
                    return int(value)
                else:
                    print(f"please enter a valid integer value between {min_val} and {max_val} ")
            else:
                return int(value)
        except ValueError:
            if allow_exit == False:
                print(f"please enter a valid integer value between {min_val} and {max_val} ")
            else:
                value = value.strip()
                value = value.lower()
                if value == "exit":
                    return "exit"
                else:
                    print("Invalid input! Enter a valid value")
            
# to view all expenses
def all_expenses():
    if transactions:
        total_amount = 0
        for id_key, details in transactions.items():
            total_amount += details['Amount']
            print("_____________________________________________")
            print(f"Expense Id    :   {id_key}")
            print(f"Amount         :   ₹{details['Amount']}")
            print(f"Category       :   {details['Category']}")
            print(f"Description   :   {details['Description']}")
            print(f"Date              :   {details['Date']}")
        print("_____________________________________________")
        print(f"Total Expense = ₹{total_amount}")
        print("_____________________________________________")
        print(" ")
        print("Select the appropriate option\n1. Add Another expense\n2. Delete any entry\n3. Update transactions values\n4. Return to previous menu")
        user_next = check_input("Enter_choice: ", max_val = 4, allow_exit = False)
        if user_next == 1:
            add_expense()
        elif user_next == 2:
            delete_expense()
        elif user_next == 3:
            update_expense()
        else:
            return True
    else:
        print("There is no transaction in the database")
    print("_____________________________________________")
    print(" ")
    print("Select the appropriate option\n1. Add expense\n2. Return to previous menu")
    user_next = check_input("Enter_choice: ", max_val = 4, allow_exit = False)
    if user_next == 1:
        add_expense()
    else:
        return True

#get expense for that particular id
def get_expense(prompt):
    while True:
        if not transactions:
            print("No Data found in the Database ")
            return True, None
        expense = check_input(prompt)
        if expense == "exit":
            return exit_screen(), None
        if expense not in transactions:
            print("No transaction found with this Expense ID\n_________________________________\n1. Try again for different ID\n2. No, Return to main menu")
            user_choice = check_input("Enter Choice: ", max_val = 2, allow_exit = False)
            if user_choice == 2:
                return True, None
            print("__________________________________")
        print("______________________________")
        for category, value in transactions[expense].items():
            print(f"{category}: {value}")
        print("______________________________")
        return False, expense

#dalete expense
def delete_expense():
    global transactions
    while True:
        user_choice, expense = get_expense("Enter the expense id of the expense that you want to delete: ")
        if user_choice == True:
            return True
        print("Are you sure, You want to delete above expense\n1. Yes \n2. No")
        choice = check_input("Enter choice: ", max_val = 2, allow_exit = False)
        if choice == 1:
            del transactions[expense]
            updated_expense = {}
            new_id = 1
            for old_id, details in transactions.items():
                updated_expense[new_id] = details
                new_id += 1
            transactions = updated_expense
            print(f"Expense at {expense} Deleted succesfully.\n Note this expense id is now alloted to another expense")
            print("______________________________")
            print("Select the appropriate option for your choice\n1. Delete another expense\n2. View all expense\n3. Return to main menu\n4. Exit")
            user_input = check_input("Enter choice: ", max_val = 4, allow_exit = False)
            if user_input == 2:
                return all_expenses()
            elif user_input == 3:
                return True
            elif user_input == 4:
                    return end_program()
            
#update any expense
def update_expense():
    while True:
        choice, expense_id = get_expense("Enter the expense id of the expense that you want to update")
        if choice == True:
            return True
        while True:
            print("What do you want to update about this expense:\n1. Amount \n2. Category\n3. Description ")
            user_choice = check_input("Enter choice: ", max_val = 3)
            if user_choice == 1:
                new_amount = check_input("Enter the new Amount: ", allow_exit = False)
                transactions[expense_id]["Amount"] = new_amount
            elif user_choice == 2:
                while True:
                    new_category = category_check()
                    if new_category != "exit":
                        transactions[expense_id]["Category"] = new_category
                        break
            elif user_choice == 3:
                new_description = check_str("Enter new description for this expense: ")
            else:
                return True
            print("___________________________________")
            print("Expense information updated succesfully\n1. Update any other information for this expense\n2. Update information of another expense\n3. Return to previous menu\n4. Exit the program")
            next_work = check_input("Enter choice: ", max_val = 4, allow_exit = False)
            print("___________________________________")
            if next_work == 2:
                break
            elif next_work == 3:
                return True
            elif next_work == 4:
                end_program()
            
#category summary 
def category_expense():
    while True:
        category = category_check(prompt = "Select the category for which you want to get summary")
        if category == "exit":
            return exit_screen()
        total_expense = 0
        found = False
        for key, value in transactions.items():
            if category == transactions[key]["Category"]:
                found = True
                total_expense += value['Amount']
                print("_____________________________________________")
                print(f"Expense Id    :   {key}")
                print(f"Amount         :   ₹{value['Amount']}")
                print(f"Category       :   {value['Category']}")
                print(f"Description   :   {value['Description']}")
                print(f"Date              :   {value['Date']}")
        print("_____________________________________________")
        if found == True:
            print(f"Total expense for this category is {total_expense}\n1. Search for another Category summary\n2. Return to main menu\n3. Exit")
            next_choice = check_input("Enter choice: ", max_val = 3, allow_exit = False)
            if next_choice == 2:
                return True
            elif next_choice == 3:
                end_program()
        else:
            print("No expense found for this category \n1. Search for different category\n2. Return to main menu")
            next_choice = check_input("Enter choice: ", max_val = 2, allow_exit = False)
            if next_choice == 2:
                return True
            print("_____________________________________________")

#Total expenditure
def total_expense():
    if not transactions:
        print("_____________________________________________")
        print("No expense found in the database")
        return exit_screen()
    total_amount = 0
    for id_key, details in transactions.items():
        total_amount += details['Amount']
    print(f"Total Expense = ₹{total_amount}")
    print("_____________________________________________")
    return exit_screen()

#highest expenses
def highest_expense():
    if not transactions:
        print("_____________________________________________")
        print("No expense found in the database")
        return exit_screen()
    highest_expense = []
    for id, details in transactions.items():
        highest_expense.append(details["Amount"])
    highest_expense = max(highest_expense)
    print("_____________________________________________")
    print(f"Your highest expense is ₹{highest_expense}. \nAnd expense information are listed below")
    for key, value in transactions.items():
        if highest_expense == transactions[key]["Amount"]:
            print("_____________________________________________")
            print(f"Expense Id    :   {key}")
            print(f"Amount         :   ₹{value['Amount']}")
            print(f"Category       :   {value['Category']}")
            print(f"Description   :   {value['Description']}")
            print(f"Date              :   {value['Date']}")
    print("_____________________________________________")
    return exit_screen()

#track transaction
def track_expenses_between_dates(start_date, end_date):
    found = False
    total_range_expense = 0
    for exp_id, details in transactions.items():
        current_exp_date = datetime.strptime(details["Date"], "%d-%m-%Y")
        if start_date <= current_exp_date <= end_date:
            print(f"Expense ID:   {exp_id}")
            print(f"Amount:   ₹{details['Amount']}")      
            print(f"Category:   {details['Category']}")
            print(f"Description:   {details['Description']}")
            print(f"Date:   {details['Date']}")
            print("——————————————————————————————")
            
            total_range_expense += details["Amount"]
            found = True

    if not found:
        return False, total_range_expense  
    return True, total_range_expense

#monthly summary
def last_month_expense():
    if not transactions:
        print("Database has no transaction details")
        return exit_screen()
    end_date = datetime.today()
    start_date = end_date - timedelta(days = 30)
    next_work, total_expense = track_expenses_between_dates(start_date, end_date)
    if next_work == True:
        print(f"Total expense last month: ₹{total_expense}")
    return exit_screen()

#exit screen
def exit_screen():
    print("Do you want to return to main menu\n1. Yes\n2. Exit")
    user_choice = check_input("Enter_choice: ", max_val = 2, allow_exit = False)
    if user_choice == 1:
        return True
    else:
        end_program()

#force quit the program
def end_program():
    import sys
    print("Thanks for using Personal Expense Manager❤️")
    sys.exit()

#calling main screen
while True:
    if main_screen() == False:
        break
