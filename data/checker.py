directory = "C:/Users/ngmal/Desktop/Self_Company-main/current_value.txt"

month_dict = {"1": "january", 
              "2": "february", 
              "3": "march", 
              "4": "april", 
              "5": "may", 
              "6": "jun", 
              "7": "july", 
              "8": "august", 
              "9": "september", 
              "10": "october", 
              "11": "november", 
              "12": "december"}

def read_current_value():
    try:
        f = open(directory, "r")
        current_counter = f.read()
        f.close()
        return int(current_counter)
    except FileNotFoundError as e:
        print(e)

def write_current_value(current_value):
    try:
        f = open(directory, "w")
        new_value = int(current_value) + 1
        f.write(str(new_value))
        f.close()
        return
    except FileNotFoundError as e:
        print(e)

def check_if_admin(customer):
    try:
        if customer[8] == "admin":
            return True
        return False
    except Exception as e:
        print(e)
    finally:
        print(f"the current customer is: {customer[8]}.")
