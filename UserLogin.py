class UserLogin:
    def from_db(self, user_id, db):
        self.__user = db.get_user(user_id)
        return self

    def create(self, user):
        self.__user = user
        # print(self.__user)
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        # print(self.__user['name'])
        # print(self.__user['email'])
        # print(str(self.__user['id']))
        return self.__user['id']
