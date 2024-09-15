"""Standard set game to one player and run time mode.

The game will show the user 12 set cards from a mixed deck of 81 cards, and will allow the user to choose which 3 cards is a set.
If the user chose a correct set, the three cards he chose are replaced by the following cards in the deck.
If user select an incorrect set, an error message is printed.
If it is not possible to make a set from the opened cards, return the cards to the deck, shuffle it and open 12 new cards.
The player wins when no more sets can be made from the cards in the deck.

Example:
    game = SetGame()
    game.play_game()

Check the instructions and game rules at:
https://en.wikipedia.org/wiki/Set_(card_game)
"""

import datetime
from itertools import combinations
import random
import time

import colorama


class Card:
    """Represents game card.

    Attributes:
        shape (str): The shape of card("◆", "~", "●").
        filling (str): The filling of the shape on the card
        ("Empty", "Striped", "Full").
        color (str): The color of card("Red", "Green", "Purple").
        number (str): The numbers of shapes on the card("1", "2", "3").    
    """

    def __init__(self):
        self.shape = ""
        self.filling = ""
        self.color = ""
        self.number = ""

    def set_card(self, shape, filling, color, number):
        """Set all Attributes of card."""
        self.shape = shape
        self.filling = filling
        self.color = color
        self.number = number

    def __str__(self):
        colors = {
        "Red": colorama.Fore.RED,
        "Green": colorama.Fore.GREEN,
        "Purple": colorama.Fore.MAGENTA,
        }
        return (colors[self.color] + f"{self.shape * int(self.number)} {self.filling}" + colorama.Style.RESET_ALL)


class Deck:
    """Represents deck of cards.

    Attributes:
        cards (list): List of cards in deck.
        Initializes empty, but will later contain 81 and less.
    """
    SHAPES = ("◆", "~", "●")
    FILLING_OF_SHAPES = ("Empty", "Striped", "Full")
    COLOR_OF_SHAPES = ("Red", "Green", "Purple")
    NUMBER_OF_SHAPES = ("1", "2", "3")

    def __init__(self):
        self.cards = []

    def set_deck(self):
        """Creates all the cards in the deck.

        Returns:
            None
        """
        for shape in self.SHAPES:
            for filling in self.FILLING_OF_SHAPES:
                for color in self.COLOR_OF_SHAPES:
                    for number in self.NUMBER_OF_SHAPES:
                        card = Card()
                        card.set_card(shape, filling, color, number)
                        self.cards.append(card)

    def shuffle_deck(self):
        """Randomly shuffle the deck."""
        random.shuffle(self.cards)


class SetGame:
    """The game set.
    Allows to manage a set game with one player who chooses sets, until he wins when there are no more sets left in the cards.

    Attributes:
        deck (Deck): An instance of a class that represents a deck of playing cards, and tools for the deck.
    """
    NUMBER_OF_OPEN_CARDS = 12

    def __init__(self):
        self.deck = Deck()
        self.deck.set_deck()

    def _create_optional_sets(self, cards):
        """Creates all set options in given cards.

        Args:
            cards (list): List of cards.

        Returns:
            set: All set options.
        """
        optional_sets = set(combinations(cards, 3))
        return optional_sets

    def check_if_set(self, given_set):
        """Returns if the selected set is a valid set.

        Args:
            given_set (tuple): Set to check.

        Returns:
            bool: If valid set.
        """
        colors = [card.color for card in given_set]
        fillings = [card.filling for card in given_set]
        numbers = [card.number for card in given_set]
        shapes = [card.shape for card in given_set]
        cards_detail = (colors, fillings, numbers, shapes)
        for detail in cards_detail:
            if len(set(detail)) == 2:
                return False
        return True

    def check_cards(self, cards):
        """Returns if in the given cards, there is a valid set.

        Args:
            cards (list): Cards to check.

        Returns:
            bool: if in the given cards, there is a valid set.
        """
        optional_sets = self._create_optional_sets(cards)
        for optional_set in optional_sets:
            if self.check_if_set(optional_set):
                return True
        return False

    def opening_cards(self, exposed_cards=None):
        """Opens up to 12 set cards(if they have a possible set).

        Args:
            exposed_cards (list, optional): The exposed cards, (at the beginning of the game is empty).

        Returns:
            list: Cards to display to the user.
        """
        if exposed_cards is None:
            exposed_cards = []
        while True:
            while len(self.deck.cards) != 0 and len(exposed_cards) != self.NUMBER_OF_OPEN_CARDS:
                card = self.deck.cards[0]
                self.deck.cards.remove(card)
                exposed_cards.append(card)
            if self.check_cards(exposed_cards):
                return exposed_cards
            self.deck.cards.extend(exposed_cards)
            self.deck.shuffle_deck()

    def print_cards(self, cards):
        """Print cards.

        Args:
            cards (list): The cards to show on the screen.

        Returns:
            None
        """
        table = ""
        for num, card in enumerate(cards, start=1):
            table += f"{num}. {card}\n"
        print(table)

    def remove_set_from_deck(self, open_cards, cards):
        """Removes the selected set from the deck.

        Args:
            open_cards (list): The open cards.
            cards (list): The cards to remove.

        Returns:
            list: The cards that are shown to the player.
        """
        for old_card in cards:
            open_cards.remove(old_card)
        return open_cards

    def returning_set_to_the_deck(self, open_cards, cards):
        """Returning the selected set to the deck.

        Args:
            open_cards (list): The open cards.
            cards (list): The cards to remove.

        Returns:
            list: The cards that are shown to the player.
        """
        for old_card in cards:
            open_cards.remove(old_card)
            self.deck.cards.append(old_card)
        return open_cards

    def check_user_answer(self, open_cards):
        """Receives an answer from the user and checks if it is valid.

        Args:
            open_cards (list): The open cards.

        Returns:
            list: Valid answer from the user.
        """
        check_answer = True
        while check_answer != 3:
            check_answer = 0
            user_answer = input("Enter a set(the number of card separate by a comma): ")
            user_answer = [answer.strip() for answer in user_answer.split(",")]
            for answer in user_answer:
                if len(set(user_answer)) == 3 and answer.isdigit() and int(answer) in range(1, len(open_cards) + 1):
                    check_answer += 1
        return [int(answer) for answer in user_answer]

    def check_if_win(self, open_cards):
        """Checks if the player has won (no more possible sets left).

        Args:
            open_cards (list): The open cards.

        Returns:
            bool: If player won and game is over.
        """
        # When 21 cards remain, there is necessarily a set.
        if len(self.deck.cards) + len(open_cards) <= 21:
            all_cards = self.deck.cards + open_cards
            if not self.check_cards(all_cards):
                print("You win!")
                return True

    def print_scoreboard(self):
        """Print scoreboard"""
        try:
            with open("set_scoreboard.txt", "r") as file:
                file = file.read().split("\n")
                for line in file:
                    line_to_print = ""
                    for word in line.split(", "):
                        line_to_print += f"{word: <13}"
                    print(line_to_print)
        except FileNotFoundError:
            pass

    def save_score(self, score):
        """Save data to scoreboard"""
        with open("set_scoreboard.txt", "a") as file:
            name = input("Enter your name: ")
            date = datetime.datetime.now().strftime("%d.%m.%Y")
            data = f"{name}, {date}, {score}\n"
            file.write(data)

    def run_time_game(self):
        """Play Run time game.
        There is a time limit of 3 minutes to find as many sets as possible.
        shuffles cards and presents them to the user, checks if the answer from the user is correct.
        Every time a set is found:
        It is added back to the deck, the deck is shuffled and three new cards are revealed,
        And adding 5 seconds to the clock.

        Returns:
            bool: If game is over.
        """
        timer = 3 * 60  # 3 minutes in seconds
        start_time = time.time()
        score = 0
        self.deck.shuffle_deck()
        open_cards = self.opening_cards()
        self.print_cards(open_cards)
        while time.time() - start_time < timer:
            user_answer = self.check_user_answer(open_cards)
            user_set_answer = [open_cards[answer - 1] for answer in user_answer]
            if self.check_if_set(user_set_answer):
                print("Nice!")
                timer += 5  # Add seconds to timer
                score += 1
                if time.time() - start_time >= timer:
                    print("Time over")
                    self.save_score(score)
                    return True
                open_cards = self.returning_set_to_the_deck(open_cards, user_set_answer)
                self.deck.shuffle_deck()
                open_cards = self.opening_cards(open_cards)
                self.print_cards(open_cards)
            else:
                print("Oops... that is not a set.")
        print("Time over")
        self.save_score(score)
        return True

    def normal_game(self):
        """Play normal game.
        Shuffles cards and presents them to the user, checks if the answer from the user is correct and if the game is over.

        Returns:
            bool: If game is over.
        """
        self.deck.shuffle_deck()
        open_cards = self.opening_cards()
        self.print_cards(open_cards)
        while True:
            user_answer = self.check_user_answer(open_cards)
            user_set_answer = [open_cards[answer - 1] for answer in user_answer]
            if self.check_if_set(user_set_answer):
                print("Nice!")
                open_cards = self.remove_set_from_deck(open_cards, user_set_answer)
                if self.check_if_win(open_cards):
                    return True
                open_cards = self.opening_cards(open_cards)
                self.print_cards(open_cards)
            else:
                print("Oops... that is not a set.")

    def play_game(self):
        """Game management"""
        game = input("Do you want to play normal game or run time game(n/r)? ")
        if game == "n":
            self.normal_game()
        elif game == "r":
            self.run_time_game()
            scoreboard = input("do you want to print the scoreboard(y/n)? ")
            if scoreboard == "y":
                self.print_scoreboard()
        return None


def main():
    game = SetGame()
    game.play_game()


if __name__ == "__main__":
    main()
