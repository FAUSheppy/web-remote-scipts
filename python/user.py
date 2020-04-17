import flask_login as fl

class UserInDatabase():
    def __init__(self, name, password):
        self.name = name
        self.password = password

class User(fl.UserMixin):

    def __init__(self, name):
        self.id = name
        self.name = "user" + str(id)
        self.password = self.name + "_secret"
        
    def __repr__(self):
        return self.id

def getUserFromDB(userID):
    print(userID)
    return User(userID)

userDB = { "sheppy": UserInDatabase("sheppy", "test") }