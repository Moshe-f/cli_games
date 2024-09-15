import math
import random
import string

import requests


ALL_WORD_PAGE = "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"
ALL_WORD_FILE = r"all_words.txt"


class Dice:
    """A class that represents a cube.
    
    Args:
        color (str): The color of cube(must be a string).
        sides (int): The number of faces of the cube.
        values (list): The values that appear on the sides.

    Attributes:
        _color (str): The color of cube(must be a string).
        _sides (int): The number of faces of the cube.
        _value (str): The current value selected by the roll is initialized as `None`.
        _values (list): The values that appear on the sides.
    """
    def __init__(self, color, sides, values):
        self._color = self._set_color(color)
        if self._check_sides_and_values(sides, values):
            self._sides = sides
            self._value = None
            self._values = values

    def __str__(self):
        return f"{self._value} - {self._color}"

    def _set_color(self, color):
        """Set the color of cube.

        Args:
            color (str): The color of cube.

        Returns:
            None.

        Raises:
            TypeError: If the color not a string.
        """
        if color.isalpha():
            return color
        else:
            raise TypeError("Color must be a string.")

    def _check_sides_and_values(self, sides, values):
        """Return `True` if The number of sides matches the number of values.

        Args:
            sides (int): The number of faces of the cube.
            values (list): The values that appear on the sides.

        Returns:
            bool: True if valid.

        Raises:
            TypeError: If the number of sides does not match the number of values.
        """
        if sides == len(values):
            return True
        else:
            raise TypeError("The number of sides must be a equal to the number of values.")
    
    def roll(self):
        """Rolls the dice and set its value randomly."""
        self._value = random.choices(self._values)[0]
        return self


class UnbalancedDice(Dice):
    """A class that represents a `unbalanced cube`.
    For each value has a different chance of coming out in a roll.
    
    Args:
        color (str): The color of cube(must be a string).
        sides (int): The number of faces of the cube.
        values (list): The values that appear on the sides.
        weights (list): The numbers that represent the rolling possibility for each value of the cube.

    Attributes:
        _color (str): The color of cube(must be a string).
        _sides (int): The number of faces of the cube.
        _value (str): The current value selected by the roll is initialized as `None`.
        _values (list): The values that appear on the sides.
        _weights (list): The numbers that represent the rolling possibility for each value of the cube.
    """
    def __init__(self, color, sides, values, weights):
        super().__init__(color, sides, values)
        self._weights = self._set_weights(weights, sides)

    def _set_weights(self, weights, sides):
        """Return the weights of each side of the cube.

        Args:
            weights (list): The numbers that represent the rolling possibility for each value of the cube.
            sides (int): The number of faces of the cube.

        Returns:
            weights: The numbers that represent the rolling possibility for each value of the cube.

        Raises:
            TypeError: If the weights is not a dict or list and if the number of weights does not match the number of sides.
            ValueError: If weight is not positive.
        """
        if not isinstance(weights, dict) and not isinstance(weights, list):
            raise TypeError("The weights must be a list or dict.")
        if sides != len(weights):
            raise TypeError("The num of sides must be a equal to num of weights.")
        if isinstance(weights, dict):
            weights = [weight for weight in weights.values()]
        for weight in weights:
            if weight <= 0:
                raise ValueError("The weight must be positive.")
        return weights

    def roll(self):
        """Rolls the dice and set its value randomly with a different possibility for each value."""
        self._value = random.choices(self._values, self._weights)[0]
        return self


class NumericalDice(Dice):
    """A class that represents a `numerical cube`.
    The values are numbers between 1 and the number of sides in the cube.
    
    Args:
        color (str): The color of cube(must be a string).
        sides (int): The number of faces of the cube.

    Attributes:
        _color (str): The color of cube(must be a string).
        _sides (int): The number of faces of the cube.
        _value (str): The current value selected by the roll is initialized as `None`.
        _values (list): The values that appear on the sides.
    """
    def __init__(self, color, sides):
        values = list(range(1, sides + 1))
        super().__init__(color, sides, values)


class Yamtzee:
    """The "Yamtzee" game.
    
    Args:
        num_of_player (int): The num of player.
        top_score (int): The top score - whoever reaches the score wins.

    Attributes:
        dice (int): The number of dice for each type of dice.
        COLORS (list): The colors of dice.
        COLORS_WEIGHTS (list): The numbers that represent the rolling possibility for each color.
        LETTERS (list): All ascii letters in the Alphabet.
        LETTERS_WEIGHTS (list): The numbers that represent the rolling possibility for each letter.
                                From: https://en.wikipedia.org/wiki/Letter_frequency.
        _num_of_player (int): The num of player.
        _top_score (int): The top score - whoever reaches the score wins.
        _players_score (dict): The score of each player - dict:(player: score).
        length_dice (list): A lot of cubes -> `Numerical dice`.
        letter_dice (list): A lot of cubes -> `Unbalanced dice`.
        all_words (set): All correct words in English.
    """
    dice = 500
    COLORS = ["Red", "Green", "Blue"]
    COLORS_WEIGHTS = [10, 25, 65]
    LETTERS = list(string.ascii_lowercase)
    LETTERS_WEIGHTS = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 
                       6.094, 6.966, 0.253, 1.772, 4.025, 2.406, 6.749, 
                       7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 
                       0.978, 2.360, 0.250, 1.974, 0.074]

    def __init__(self, num_of_player, top_score):
        self._num_of_player = num_of_player
        self._top_score = top_score
        self._players_score = {str(player): 0 for player in range(1, num_of_player + 1)}
        self.length_dice = self._get_length_dice()
        self.letter_dice = self._get_letter_dice()
        self.all_words = self._get_all_words()

    def _get_color(self):
        """Return random color."""
        return random.choices(self.COLORS, self.COLORS_WEIGHTS)[0]

    def _get_length_dice(self):
        """Returns a list filled with random `NumericalDice` cubes."""
        return [NumericalDice(self._get_color(), 10) for _ in range(self.dice)]

    def _get_letter_dice(self):
        """Returns a list filled with random `UnbalancedDice` cubes."""
        return [UnbalancedDice(self._get_color(), 26, self.LETTERS, self.LETTERS_WEIGHTS) for _ in range(self.dice)]

    def _get_all_words(self):
        """Return all words in english(from github or file)."""
        try:
            r = requests.get(ALL_WORD_PAGE)
        except requests.exceptions.RequestException:
            file = open(ALL_WORD_FILE, "r")
            all_word = file.read()
            file.close()
        else:
            all_word = r.text
        finally:
            all_word = set(all_word.split())
        return all_word

    def _add_score(self, player, word):
        """Adds a score to the player. 
        (according to a certain algorithm according to the frequency of the letter in the English language).
        """
        score = 0
        for letter in word:
            frequency = math.ceil(self.LETTERS_WEIGHTS[self.LETTERS.index(letter)])
            score += math.floor(12 / (math.sqrt(frequency ** 1.5)))
        self._players_score[player] += score
        print(f"{score} points added to player - {player}")

    def _roll_length_dice(self):
        """Return `length dice` instance and rolls the dice, if 1 selected roll again."""
        dice = random.choice(self.length_dice)
        dice.roll()
        while dice._value == 1:
            dice = random.choice(self.length_dice)
            dice.roll()
        return dice

    def _roll_letter_dice(self):
        """Return `letter dice` instance and rolls the dice."""
        dice = random.choice(self.letter_dice)
        dice.roll()
        return dice

    def get_letter_dice(self, current_length_dice):
        """Return number of letter cubes according to the number given in the length cube, if `Red` adds another letter cube."""
        num_of_letter_dice_to_create = current_length_dice._value
        if current_length_dice._color == self.COLORS[0]:
            num_of_letter_dice_to_create += 1
        letter_dice = [self._roll_letter_dice() for _ in range(num_of_letter_dice_to_create)]
        return letter_dice

    def check_input_from_player(self, word, letters):
        letters_values = [letter._value for letter in letters]
        if len(word) < 2:
            return False
        for letter in word.lower():
            if letter not in letters_values:
                return False
            elif letters[letters_values.index(letter)]._color != self.COLORS[0]:
                letters_values.remove(letter)
        if word in self.all_words or word.lower() in self.all_words:
            return True
        else:
            return False

    def print_dice(self, player, current_length_dice, current_letter_dice):
        print(f"\nPlayer: {player}\nPoints: {self._players_score[player]}\n")
        print(f"Number dice: {current_length_dice._value} - {current_length_dice._color}")
        print("Letters:")
        print("\n".join([f"{letter._value} - {letter._color}" for letter in current_letter_dice]))
        print("\n")
        return None

    def roll_again_options(self, player, current_length_dice, current_letter_dice):
        """Roll the dice again if their color is green."""
        roll_again_counter = 0
        dice_to_remove = []
        dice_to_change = []
        if current_length_dice._color == self.COLORS[1]:
            dice_to_change.append(current_length_dice)
        for dice in current_letter_dice:
            if dice._color == self.COLORS[1]:
                dice_to_change.append(dice)
        while len(dice_to_change) > 0:
            print("You can roll again this dice:")
            for num, dice in enumerate(dice_to_change, 1):
                print(f"{num}. {dice._value} - {dice._color}")
            dice_to_roll_again = input("Enter the number of dice you want to roll again, with a comma between them(For example: 1,2,3): ")
            if len(dice_to_roll_again) == 0:
                if roll_again_counter != 0:
                    self.print_dice(player, current_length_dice, current_letter_dice)
                return current_length_dice, current_letter_dice
            for dice in dice_to_roll_again.split(","):
                if dice.strip().isdigit() and int(dice.strip()) <= len(dice_to_change):
                    if dice_to_change[int(dice.strip()) - 1] == current_length_dice:
                        current_length_dice.roll()
                        roll_again_counter += 1
                        current_letter_dice = self.get_letter_dice(current_length_dice)
                        self.print_dice(player, current_length_dice, current_letter_dice)
                        dice_to_change = []
                        dice_to_remove = []
                        for dice in current_letter_dice:
                            if dice._color == self.COLORS[1]:
                                dice_to_change.append(dice)
                        break
                    else:
                        current_letter_dice[current_letter_dice.index(dice_to_change[int(dice.strip()) - 1])].roll()
                        roll_again_counter += 1
                        dice_to_remove.append(current_letter_dice[current_letter_dice.index(dice_to_change[int(dice.strip()) - 1])])
            for dice in dice_to_remove:
                dice_to_change.remove(dice)
        if roll_again_counter != 0:
            self.print_dice(player, current_length_dice, current_letter_dice)
        return current_length_dice, current_letter_dice

    def turn(self, player):
        """Make a turn."""
        current_length_dice = self._roll_length_dice()
        current_letter_dice = self.get_letter_dice(current_length_dice)
        self.print_dice(player, current_length_dice, current_letter_dice)
        
        current_length_dice, current_letter_dice = self.roll_again_options(player, current_length_dice, current_letter_dice)
        
        player_guess = input("Enter word: ")
        if self.check_input_from_player(player_guess, current_letter_dice):
            print(f"Correct answer: {player_guess}")
            self._add_score(player, player_guess)

    def play(self):
        """Play yamtzee."""
        print("""Welcome to Yamtzee.

The player should use the letter cubes, that they have come out, to create a word in English.
              
A red length cube, gives the player another cube as a gift.
A red letter cube, allows the player to use a letter that appears on the cube several times he wants.
Green cubes, give the player the opportunity to choose whether to re-roll.
Enjoy.
              """)
        while True:
            for player in self._players_score:
                self.turn(player)
                if max(self._players_score.values()) >= self._top_score:
                    print(f"\nplayer {player} win!")
                    return True
            

def main():
    yamtzee = Yamtzee(3, 20)
    yamtzee.play()


if __name__ == "__main__":
    main()
