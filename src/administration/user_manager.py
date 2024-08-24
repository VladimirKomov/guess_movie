from werkzeug.security import generate_password_hash, check_password_hash

from src.database.database_user_manager import UserDataBaseManager



class UserManager:
    def __init__(self):
        self.user_db_manager = UserDataBaseManager()

    def register(self, nick, email, name, birthdate, password):
        # Registering a new user
        if self.user_db_manager.user_exists(nick, email):
            return False, "User already exists."

        success = self.user_db_manager.register_user(nick, email, name, birthdate, password)
        if success:
            return True, "Registration successful."
        else:
            return False, "Registration failed."

    def authenticate(self, nick_or_email, password):
        # User authorization
        user = self.user_db_manager.authenticate_user(nick_or_email, password)
        if user:
            # Return True and the user object
            return True, user  
        else:
            return False, "Invalid credentials."

    def user_exists(self, nick, email):
        # Verification of the user's existence
        return self.user_db_manager.user_exists(nick, email)
