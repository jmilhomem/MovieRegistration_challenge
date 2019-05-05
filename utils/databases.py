import sys
import json
import sqlite3
import pandas as pd
import pprint
if __name__ == "__main__":
    import file_operations
    import database_connection
else:
    from utils import file_operations
    from utils.database_connection import DatabaseConnection

# commands to see the "Python interpreter location"
# import pprint
# pprint.pprint(sys.path)


"""
Concerned with storing and retrieving books from a list.
"""


class Movies:
    def __init__(self) -> None:
        # paths where the files live
        self.path_filename = sys.path[0] + "/utils/files/"
        self.path_db = sys.path[0] + "/utils/data.db"

    def add_movie(self, store_type='db') -> bool:
        """
        Function created to add new registers of movies into a json file or into the database
        :param store_type: db (database) or f (file). By default it considers db (database).
        :return: True of False
        """

        self.add_another_movie = "yes"

        while self.add_another_movie == "yes":

            try:
                # request each information of the new movies and store them on variables
                movie_name = input("\nMovie Name: ")
                director_name = input("Director Name: ")
                movie_year = int(input("Year of the production: "))
                name_main_actor_actress = input("Main actor / Actress: ")

                # create a dictionary variable that will be used to store new movies
                new_movie = {
                            "movie_name": movie_name
                            , "director_name": director_name
                            , "movie_year": movie_year
                            , "name_main_actor_actress": name_main_actor_actress
                            , "read": 0
                            }

                if store_type == "f":
                    result_insert_file = self._write_movie_file(new_movie, "a")
                else:
                    result_insert_file = self._add_movie_db(new_movie)

                if result_insert_file:
                    # check if another movie will be inserted by user
                    self.add_another_movie = input("\nDo you want insert other movie (yes/no): ").lower()

                    if self.add_another_movie == "no":
                        return True

            except ValueError as e_value:
                print(f"\nDefinition of an object is not set properly.\nError description: {str(e_value)}")
                return False
            except Exception as e:
                print(f"\nOccurred an error during this process.\nError description: {str(e)}")
                return False

    def delete_movie(self, movie_name, store_type="db") -> bool:
        """
        Function created to delete registers of movies from a json file or from database
        :param movie_name, store_type: movie_name desired to be deleted.
                                       store_type: db (database) or f (file). By default it considers db (database).
        :return: True of False
        """
        if store_type.lower() == "f":
            result_delete_file = self._delete_movie_file(movie_name)
        else:
            result_delete_file = self._delete_movie_db(movie_name)

        return result_delete_file

    def read_movie(self, movie_name, store_type="db") -> bool:
        """
        Function created to read movies from a json file or from database
        :param movie_name, store_type: movie_name desired to be deleted.
                                       store_type: db (database) or f (file). By default it considers db (database).
        :return: True of False
        """
        if store_type.lower() == "f":
            result_read_file = self._apply_read_movie_file(movie_name)
        else:
            result_read_file = self._apply_read_movie_db(movie_name)
        return result_read_file

    def list_movies(self, store_type="f"):
        """
        Function created to delete registers of movies from a json file or from database
        :param store_type: store_type: db (database) or f (file). By default it considers db (database).
        :return: True of False
        """
        if store_type.lower() == "f":
            file = file_operations.read_file("Movie_Registration.json")
            result_list = self._create_dataframe_list(file)

        else:
            with DatabaseConnection(self.path_db) as cursor:

                cursor.execute("select * from tb_movies")
                movies = cursor.fetchall()

                # creates the same structure that the json file has and create the dataframe
                list_movies = []
                for row in movies:
                    row_dict = {}
                    row_dict["movie_name"] = row[0]
                    row_dict["director_name"] = row[1]
                    row_dict["movie_year"] = row[2]
                    row_dict["name_main_actor_actress"] = row[3]
                    row_dict["read"] = row[4]
                    list_movies.append(row_dict)

                result_list = self._create_dataframe_list(list_movies)

        return result_list

    def _write_movie_file(self, content, type_operation, filename="Movie_Registration.json"):
        """
        Private function created to write into a Movie's json file
        :param content, type_operation, filename: Content is a dataset with Movie's data
                                    type_operation is the type of operation: "a" (to add data) or other to overwrite.
                                    filename by default considers "Movie_Registration.json".
        :return: True of False
        """
        file = file_operations.read_file(filename)
        if type_operation.lower() == "a":
            file.append(content)
        else:
            file = content

        if file == []:
            return False
        else:
            check_save_file = file_operations.save_to_file(file, filename, "o")
            return check_save_file

    def _delete_movie_file(self, movie_name, filename="Movie_Registration.json"):
        """
        Private function created to write into a Movie's json file
        :param movie_name, filename: movie_name desired to be deleted.
                                     filename by default considers "Movie_Registration.json".
        :return: True of False
        """
        file = file_operations.read_file(filename)
        movie_found = 0

        for row in file:
            if row["movie_name"].lower() == movie_name.lower():
                file.remove(row)
                movie_found = 1

        if movie_found == 1:
            result = self._write_movie_file(file, "o")
        else:
            result = False
        return result

    def _apply_read_movie_file(self, movie_name, filename="Movie_Registration.json") -> bool:
        """
        Private function created to read from Movie's json file
        :param movie_name, filename: movie_name desired to be deleted.
                                     filename by default considers "Movie_Registration.json".
        :return: True of False
        """
        file = file_operations.read_file(filename)
        row_position = 0
        movie_found = 0
        for row in file:
            if row["movie_name"].lower() == movie_name.lower():
                file[row_position]["read"] = 1
                movie_found = 1
            row_position += 1

        if movie_found == 1:
            result = self._write_movie_file(file, "r")
        else:
            result = False

        return result

    def _create_dataframe_list(self, content):
        """
        Private Function created to create a dataframe using the movies set into a list
        :param filename: filename by default considers "Movie_Registration.json".
        :return: dataset
        """
        if content == []:
            return []
        else:

            # define the lists that will receive the lists of information
            list_movies = []
            list_director = []
            list_year = []
            list_main = []
            list_read_books = []

            try:
                for row in content:
                    list_movies.append(row["movie_name"])
                    list_director.append(row["director_name"])
                    list_year.append(row["movie_year"])
                    list_main.append(row["name_main_actor_actress"])
                    list_read_books.append(row["read"])

                # create the dictionary containing the filter aplied
                dict_movies_filter = {
                    "movie_name": list_movies,
                    "director_name": list_director,
                    "year": list_year,
                    "main_actor": list_main,
                    "read": list_read_books
                }

                # create the dataframe with the dictionary values
                df_movies = pd.DataFrame(dict_movies_filter)

                # return the dataframe with the movies filtered
                return df_movies

            except json.JSONDecodeError as e_json:
                print(f"\nYour settings file(s) contains invalid JSON syntax. {str(e_json)}")
                return []
            except ValueError as e_value:
                print(f"\nDefinition of an object is not set properly. {str(e_value)}")
                return []
            except Exception as e:
                print(f"\nOccurred an error during reading listing operation.\nError description: {str(e)}")
                return []

    def _add_movie_db(self, content) -> bool:
        """
        Private function created to insert new movies into a Movie's table inside a database
        :param content: dictionary with all movies' information.
        :return: True of False
        """
        movie_name = content["movie_name"].upper()
        director_name = content["director_name"].upper()
        year = content["movie_year"]
        main_actor = content["name_main_actor_actress"].upper()
        read = content["read"]

        with DatabaseConnection(self.path_db) as cursor:

            try:
                cursor.execute("Create table if not exists tb_movies("
                               " movie_name varchar(100)"
                               ", director_name varchar(100)"
                               ", year int"
                               ", main_actor varchar(100)"
                               ", read boolean)")
                cursor.execute("insert into tb_movies (movie_name, director_name, year, main_actor, read)"
                               "values (?, ?, ?, ?, ?)",
                               (movie_name, director_name, year, main_actor, read))
                return True

            except ValueError as e_value:
                print(f"\nDefinition of an object is not set properly. {str(e_value)}")
                return False
            except Exception as e:
                print(f"\nOccurred an error during the adding operation. Error description: {str(e)}")
                return False



    def _delete_movie_db(self, movie_name) -> bool:
        """
        Private function created to delete movies into a Movie's table inside a database
        :param content: movie_name.
        :return: True of False
        """
        with DatabaseConnection(self.path_db) as cursor:

            cursor.execute("Create table if not exists tb_movies("
                           " movie_name varchar(100)"
                           ", director_name varchar(100)"
                           ", year int"
                           ", main_actor varchar(100)"
                           ", read boolean)")
            cursor.execute("delete from tb_movies where upper(movie_name) = ?", (movie_name.upper(),))
            return True

    def _apply_read_movie_db(self, movie_name) -> bool:
        """
        Private function created to update the movies to be read into a Movie's table inside a database
        :param content: movie_name.
        :return: True of False
        """
        with DatabaseConnection(self.path_db) as cursor:

            cursor.execute("Create table if not exists tb_movies("
                           " movie_name varchar(100)"
                           ", director_name varchar(100)"
                           ", year int"
                           ", main_actor varchar(100)"
                           ", read boolean)")
            cursor.execute("update tb_movies"
                           "   set read = 1"
                           " where upper(movie_name) = ?", (movie_name.upper(),))

            return True
