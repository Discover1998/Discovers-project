from data.checker import read_current_value, write_current_value, month_dict
import hashlib

class Information:
    def __init__(self, first_name, last_name, email, password, year, month, day):
        self._account_id = read_current_value()
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._user_id = first_name[0:2] + last_name[0:3] + str(year)
        self._password = hashlib.sha512(password.encode()).hexdigest()
        self._year = year
        for key, value in month_dict.items():
            if month == key:
                self._month = value
                break
        self._day = day
        write_current_value(self._account_id)

    def __str__(self):
        return ("Account ID: " + str(self._account_id) +
                "\n" + "First name: " + self._first_name +
                "\n" + "Last name: " + self._last_name +
                "\n" + "Email: " + self._email +
                "\n" + "Password: " + self._password +
                "\n" + "Year: " + str(self._year) +
                "\n" + "Month: " + str(self._month) +
                "\n" + "Day: " + str(self._day) + "\n")
        
        
if __name__ == "__main__":
    Test_user = Information("Najem Aldeen", "Abu Hamdah", "ngmaldin7@gmail.com", "test", "1998", "2", "14")
    Test_user2 = Information("Najem Aldeen2", "Abu Hamdah", "ngmaldin7@gmail.com", "test", "1998", "2", "14")
    Test_user3 = Information("Najem Aldeen3", "Abu Hamdah", "ngmaldin7@gmail.com", "test", "1998", "2", "14")

    print(Test_user.__str__())
    print(Test_user2.__str__())
    print(Test_user3.__str__())
