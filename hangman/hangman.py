# open screen
HANGMAN_ASCII_ART = """Welcome to the game Hangman               
  _    _                                         
 | |  | |                                        
 | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
 |  __  |/ _` | '_ \\ / _` | '_ ` _ \\ / _` | '_ \\ 
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\\__,_|_| |_|\\__, |_| |_| |_|\\__,_|_| |_|
                      __/ |                      
                     |___/\n"""
MAX_TRIES = "You have 6 attempts to guess the word before it hangs"

# all options for hangman
HANGMAN_PHOTOS = {1: '''    x-------x''',
                  2: '''    x-------x
    |
    |
    |
    |
    |''',
                  3: '''    x-------x
    |       |
    |       0
    |
    |
    |''',
                  4: '''    x-------x
    |       |
    |       0
    |       |
    |
    |''',
                  5: '''    x-------x
    |       |
    |       0
    |      /|\\
    |
    |''',
                  6: '''    x-------x
    |       |
    |       0
    |      /|\\
    |      /
    |''',
                  7: '''    x-------x
    |       |
    |       0
    |      /|\\
    |      / \\
    |'''}

# global of tries
num_of_tries = 1


def print_hangman_open_screen():
    """print open screen"""
    print(HANGMAN_ASCII_ART, MAX_TRIES)


def choose_word(file_path, index):
    """
    Gets a file path and index and chooses a word based on it
    :param file_path: path to fill of words
    :param index: num to choose a letter
    :type index: num
    :return: the letter guessed
    :rtype: string
    """
    file_data = open(file_path, "r")
    all_words = file_data.read().split(" ")
    file_data.close()
    return all_words[(index - 1) % len(all_words)]


def print_hangman_photos(num):
    """
    print hangman photos
    :param num: num to key in dict HANGMAN_PHOTOS
    :type num: int
    :return: None
    """
    print(HANGMAN_PHOTOS[num] + "\n")


def show_hidden_word(secret_word, old_letters_guessed):
    """
    Displays guessed letters in the secret word, and '_' for letters that were not guessed yet
    :param: secret_word: the word to be guessed
    :param: old_letters_guessed: the letters that were guessed (user's input)
    :type secret_word: str
    :type old_letters_guessed: list
    :return: the updated string, with all guessed letters
    :rtype: str
    """
    result = ""
    for i in secret_word:
        if i in old_letters_guessed:
            result = result + i + " "
        else:
            result = result + "_ "
    return result[:-1]


def check_valid_input(letter_guessed, old_letters_guessed):
    """
    Checks the validation of user input, if it one English letter, not entered before
    :param letter_guessed: user input
    :param old_letters_guessed: previous inputs
    :type letter_guessed: string
    :type old_letters_guessed: list
    :return: True if input is valid, False if not.
    :rtype: boolean
    """
    return len(letter_guessed) == 1 and letter_guessed.isalpha() and letter_guessed.lower() not in old_letters_guessed


def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """
    Checks validation of user’s input if it one English letter, not entered before.
    if so, adds it to "old_letters_guessed" and returns True. Otherwise returns False.
    :param letter_guessed: user’s input
    :param old_letters_guessed: previous (valid) inputs
    :type letter_guessed: string
    :type old_letters_guessed: list
    :return: True if input is valid, False if not.
    :rtype: boolean
    """
    if check_valid_input(letter_guessed, old_letters_guessed):
        old_letters_guessed.append(letter_guessed.lower())  # adds it to "old_letters_guessed" list
        return True
    else:
        print("X \n" + (" -> ".join(sorted(old_letters_guessed)) + "\ntry again"))  # print "X" and the list
        # sorted and split by " -> "
        return False


def check_letter(letter_guessed, secret_word, old_letters_guessed):
    """
    Checks with the correct guess, and accordingly prints a message or updates a number of attempts
    :param letter_guessed: user’s input
    :param secret_word: the word to be guessed
    :param old_letters_guessed: previous (valid) inputs
    :type letter_guessed: string
    :type secret_word:string
    :type old_letters_guessed: list
    :return: None
    """
    if letter_guessed.lower() in secret_word:
        print("Excellent\n\n" + show_hidden_word(secret_word, old_letters_guessed))
    else:
        global num_of_tries
        num_of_tries += 1  # updates a number of tries
        print(":( \nooppps\n")
        print_hangman_photos(num_of_tries)
        print(show_hidden_word(secret_word, old_letters_guessed))


def check_win(secret_word, old_letters_guessed):
    """
    Checks if the whole secret word was guessed correctly
    :param: secret_word: the word to be guessed
    :param: old_letters_guessed: the letters that were guessed (user's input)
    :type secret_word: str
    :type old_letters_guessed: list
    :return: True if the secret word was guessed, False if not
    :rtype: boolean
    """
    for letter in secret_word:
        if letter not in old_letters_guessed:
            return False
    return True


def main():
    print_hangman_open_screen()
    file_of_words = input("Please enter a path: ")
    index_to_choose = input("Please enter a index: ")
    secret_word = choose_word(file_of_words, int(index_to_choose))
    old_letters_guessed = []  # all letter Already guessed
    print_hangman_photos(1)
    print(show_hidden_word(secret_word, old_letters_guessed))
    while True:
        letter_guessed = input("Please enter a char: ")
        if try_update_letter_guessed(letter_guessed, old_letters_guessed):
            check_letter(letter_guessed, secret_word, old_letters_guessed)
        else:
            continue
        if check_win(secret_word, old_letters_guessed):
            print("WIN \nyou did a good job \nbye")
            break
        elif num_of_tries == 7:  # if max of tries, game over
            print("LOSE \nGo have a coffee and try again")
            break
    exit()


if __name__ == '__main__':
    main()
