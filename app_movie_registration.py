import sys
from utils import databases


def menu():
    """
    Main function used to call all functionalities for Movie's registers, considering the argument passed by the user
    It is possible to insert new data (a), list all of them (l), read (r) and delete (d).
    """

    user_action = ""
    movie = databases.Movies()
    while user_action.lower() != "q":

        user_action = input(
            "\nEnter the action that you would like to do:"
            "\n Enter 'a' to add a movie "
            "\n Enter 'l' to list movies "
            "\n Enter 'r' to read a movie "
            "\n Enter 'd' to delete a movie "
            "\n Enter 'q' to quit: ").lower()

        if user_action.lower() == 'a':

            check_addition = movie.add_movie()
            if check_addition:
                print("The movie(s) was(were) inserted as expected!")

        elif user_action.lower() == 'l':
            check_list_all = movie.list_movies("db")
            #print(check_list_all)
            if len(check_list_all):
                print("\nAll movies registered: \n", "\n", check_list_all)
            else:
                print("\nNo movies registered yet.")

        elif user_action.lower() == 'r':
            movie_name = input("\nEnter the movie's name: ")
            check_read = movie.read_movie(movie_name, "db")
            if check_read:
                print("Movie found! Have a good reading!")
            else:
                print("Movie not found. Please, check the spelling.")

        elif user_action.lower() == 'd':
            movie_name = input("\nEnter the movie's name: ")
            check_addition = movie.delete_movie(movie_name, "db")
            if check_addition:
                print("The movie was deleted as expected!")
            else:
                print("Movie not found. Please, check the spelling.")

        elif user_action == 'q':
            print("\nGood bye!")
            exit()

        else:
            print("No option selected!")
            pass


# Call the main function
# if the module that is being used to executeis similar, it will return "__main__" and the script will start by
# the main function if it is called by other module, then, the functions will be available
if __name__ == "__main__":
    menu()