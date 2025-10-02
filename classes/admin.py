from classes.information import Information

class Admin (Information):
    def __init__(self, first_name, last_name, email, password, year, month, day):
        super().__init__(first_name, last_name, email, password, year, month, day)
        self._permission = "Admin"
        self._verify = False

    def get_permission(self):
        return self._permission

    def get_verify(self):
        return self._verify

    def set_verify(self):
        self._verify = True
        return self._verify
    
    def __str__(self):
        return super().__str__() + "Permission: " + self._permission + "\nVerified: " + str(self.get_verify()) + "\n"
