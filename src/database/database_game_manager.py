from database_connection import DatabaseConnection


class InsertGameData():

    # Entering data about the result of the game
    @staticmethod
    def insert_game_result(game, result):
        
        if result == True:
            number_wins = 1
        else:
            number_wins = 0

        with DatabaseConnection() as connection:
            with connection.cursor() as cursor:
                # Checking for an entry in the result table
                cursor.execute('SELECT id FROM result WHERE id_user = %s', (game.user.user_id,))
                existing_record = cursor.fetchone()
                # If the record exists, update it
                if existing_record:
                    cursor.execute('''UPDATE result SET number_games = number_games + 1,
                    number_wins = number_wins + %s WHERE id_user = %s''', (number_wins, game.user.user_id,))
                # If there is no record with the specified user, add a new record
                else:
                    cursor.execute('''INSERT INTO result (id_user, number_games, number_wins) VALUES (%s, 1, %s)''',
                    (game.user.user_id, number_wins))