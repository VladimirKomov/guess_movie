from werkzeug.security import generate_password_hash, check_password_hash

from src.database.database_user_manager import UserDataBaseManager

class User:
    def __init__(self, user_id, nick, name, role_id):
        self.user_id = user_id
        self.nick = nick
        self.name = name
        self.role_id = role_id

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
        user_data = self.user_db_manager.authenticate_user(nick_or_email, password)
        if user_data:
            # Create and return a User object
            user = User(
                user_id=user_data[0],  # Assuming the first field is user_id
                nick=user_data[1],      # Assuming the second field is nick
                name=user_data[3],      # Assuming the fourth field is name
                role_id=user_data[5]    # Assuming the sixth field is role_id
            )
            return True, user
        else:
            return False, "Invalid credentials."

    def user_exists(self, nick, email):
        # Verification of the user's existence
        return self.user_db_manager.user_exists(nick, email)

