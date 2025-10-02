import mysql.connector
from colorama import Fore, Style, init
import datetime
from data.person_number_checker import personnummer_checker, gender_checker

init(autoreset=True)

GREEN_HSV = Fore.GREEN
RED_HSV   = Fore.RED


#Work! 10-01
def database_connection():
    db = mysql.connector.connect(
        host="localhost", #127.0.0.1
        port = 3306,
        user="root",
        password="root" #Note on sec pc root on MacBook root12345
    )
    print(f"{GREEN_HSV}Connected to MySQL database{Style.RESET_ALL}")
    return db
#Work! 10-01
def create_database():
    db = database_connection()
    try:
        if db.is_connected():
            cur = db.cursor()
            cur.execute("CREATE DATABASE IF NOT EXISTS Discovers_db DEFAULT CHARACTER SET utf8mb4")
            db.commit()
            print(f"{GREEN_HSV}Database Created Successfully{Style.RESET_ALL}")
            return True
        print(f"{RED_HSV}Database Not Created{Style.RESET_ALL}")
        return False
    finally:
        db.close()
#Work! 10-01
def create_table():
    db = database_connection()
    try:
        if db.is_connected():
            cur = db.cursor()
            cur.execute("USE Discovers_db")
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS customers (
                  id INT AUTO_INCREMENT PRIMARY KEY,
                  person_number VARCHAR(16) NOT NULL UNIQUE,
                  first_name VARCHAR(100) NOT NULL,
                  last_name  VARCHAR(100) NOT NULL,
                  email      VARCHAR(255) NOT NULL,
                  password   VARCHAR(255) NOT NULL,
                  phone      VARCHAR(10),
                  address     VARCHAR(255),
                  permission VARCHAR(5),
                  gender VARCHAR(5),
                  verified   BOOL,
                  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
            db.commit()
            print(f"{GREEN_HSV}Customers Table Created Successfully{Style.RESET_ALL}")
            return True
        print(f"{RED_HSV}Table Not Created{Style.RESET_ALL}")
        return False
    finally:
        db.close()
#Work! 10-01
def insert_customer(person_number, first_name, last_name, email, password, phone, address):
    person_number = str(person_number)
    if person_number[0] == "1" or person_number[0] == "2":
        person_number = person_number[2:]
    current_pno = ""
    for letter in person_number:
        if letter in "-":
            continue
        else:
            current_pno += letter

    db = database_connection()
    try:
        if db.is_connected():
            cur = db.cursor()
            cur.execute("USE Discovers_db")
            cur.execute(
                """
                INSERT INTO customers
                  (person_number, first_name, last_name, email, password, phone, address, permission, verified, gender, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (current_pno, first_name, last_name, email, password, str(phone), address, "user", False, gender_checker(person_number), datetime.datetime.now())
            )
            db.commit()
            print(f"{GREEN_HSV}New customer {first_name} {last_name} has been inserted successfully{Style.RESET_ALL}")
            return True
        print(f"{RED_HSV}customer {first_name} {last_name} not created{Style.RESET_ALL}")
        return False
    finally:
        db.close()
#Work! 10-01
def show_customers():
    db = database_connection()
    try:
        if db.is_connected():
            cur = db.cursor()
            cur.execute("USE Discovers_db")
            cur.execute("SELECT * FROM customers")
            customers = cur.fetchall()
            current_customers = {}
            for customer in customers:
                user_id      = customer[0]
                person_number= customer[1]
                first_name   = customer[2]
                last_name    = customer[3]
                email        = customer[4]
                password     = customer[5]
                phone        = customer[6]
                address      = customer[7]
                permission = customer[8]
                verified = customer[9]
                gender = customer[10]
                created_at = customer[11]
                current_customers.update({user_id : [person_number, first_name, last_name, email, password, phone, address, permission, verified, gender, created_at]})
                #user_lst.append([str(user_id), str(person_number), first_name, last_name, email, password, str(phone) if phone else "", address or "", permission, verified, created_at])
            return current_customers
        print(f"{RED_HSV}No connection{Style.RESET_ALL}")
        return {}
    finally:
        db.close()

#Work! 10-01
def select_customer(person_number):
    person_number = str(person_number)
    current_pno = ""
    if person_number[0] == "1":
        person_number = person_number[2:]
    for letter in person_number:
        if letter in "-":
            continue
        else:
            current_pno += letter
    db = database_connection()
    try:
        if db.is_connected():
            cur = db.cursor()
            cur.execute("USE Discovers_db")
            cur.execute("SELECT * FROM customers WHERE person_number = %s", (current_pno,))
            customers = cur.fetchall()
            found = []
            for customer in customers:
                if customer[1] == current_pno:
                    found = [customer[0], customer[1], customer[2], customer[3], customer[4], customer[5], customer[6], customer[7], customer[8], customer[9], customer[10], customer[11]]
            if found:
                print(f"{GREEN_HSV}Customer {person_number} was found{Style.RESET_ALL}")
                return found
            print(f"{RED_HSV}Customer Not Found{Style.RESET_ALL}")
            return None
        print(f"{RED_HSV}No connection{Style.RESET_ALL}")
        return None
    finally:
        db.close()

#Work! 10-01
def check_customer(email, password):
    db = database_connection()
    try:
        if db.is_connected():
            cur = db.cursor()
            cur.execute("USE Discovers_db")
            cur.execute("SELECT * FROM customers WHERE email = %s AND password = %s", (email, password),)
            customer = cur.fetchall()
            if customer:
                print(f"{GREEN_HSV}Customer {email} was found{Style.RESET_ALL}")
                #print(customer)
                return customer[0]
        print(f"{RED_HSV}No connection{Style.RESET_ALL}")
    except Exception as error:
        print("An error with the connection: ", error)
    finally:
        db.close()

def delete_customer(person_number):
    db = database_connection()
    try:
        if db.is_connected():
            cur = db.cursor()
            cur.execute("USE Discovers_db")
            cur.execute("DELETE FROM customers WHERE person_number = %s", (str(person_number),))
            db.commit()
            if cur.rowcount > 0:
                print(f"{GREEN_HSV}Customer with person_number {person_number} has been deleted successfully{Style.RESET_ALL}")
                return True
            print(f"{RED_HSV}Customer Not Found{Style.RESET_ALL}")
            return False
        print(f"{RED_HSV}No connection!{Style.RESET_ALL}")
        return False
    finally:
        db.close()

# Work! 10-01
def get_information_from_id(user_id):
    db = database_connection()
    try:
        if db.is_connected():
            cur = db.cursor()
            cur.execute("USE Discovers_db")
            qr = "SELECT * FROM customers WHERE id = %s"
            cur.execute(qr, (user_id,))
            customer = list(cur.fetchall()[0])
            if customer:
                print(f"{GREEN_HSV}Customer {id} was found{Style.RESET_ALL}")
                return customer
            print(f"{RED_HSV}No connection{Style.RESET_ALL}")
            return []
        print(f"{RED_HSV}No connection{Style.RESET_ALL}")
    except Exception as error:
        print(f"{RED_HSV}Something went wrong {error} {Style.RESET_ALL}")
    finally:
        db.close()

#############################################################
#                           ADMIN                           #
#############################################################
def create_admins_table():
    db = database_connection()
    try:
        if db.is_connected():
            cur = db.cursor()
            cur.execute("USE Discovers_db")
            cur.execute(
                """CREATE TABLE IF NOT EXISTS admins (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name VARCHAR(100),
                last_name VARCHAR(100),
                email VARCHAR(255),
                password VARCHAR(255),
                phone VARCHAR(255),
                address VARCHAR(255),
                permission VARCHAR(5),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""")
    except Exception as e:
        print(e)
    finally:
        db.close()
        print(f"{RED_HSV}No connection{Style.RESET_ALL}")

def insert_admins(first_name, last_name, email, password, phone, address):
    db = database_connection()
    try:
        if db.is_connected():
            cur = db.cursor()
            cur.execute("USE Discovers_db")
            cur.execute("""
            INSERT INTO admins (first_name, last_name, email, password, phone, address, permission, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (first_name, last_name, email, password, phone, address, "admin", datetime.datetime.now())
                        )
            db.commit()
            print(f"{GREEN_HSV}New Admin {first_name} {last_name} has been inserted successfully{Style.RESET_ALL}")
    except Exception as e:
        print(e)
    finally:
        db.close()


if __name__ == '__main__':
    print("#===================== Welcome to database checker =====================#")
    #create_database()
    #create_table()
    print(get_information_from_id(1))
    #insert_customer(9802141111, "Najem", "Aldeen", "ngmaldin7@gmail.com", "12345", "0737600483", "street")
    #print(select_customer("19980214-1111"))
    print("Users in current DB:")
    for keys, values in show_customers().items():
        print(f"{keys} : {values}")
        print()
