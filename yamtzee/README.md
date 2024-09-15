# Yamtzee


Welcome to Yamtzee.

The player should use the letter cubes, that they have come out, to create a word in English.
              
A red length cube, gives the player another cube as a gift.

A red letter cube, allows the player to use a letter that appears on the cube several times he wants.

Green cubes, give the player the opportunity to choose whether to re-roll.

Enjoy.


### Details

Each cube has a color, a number of faces, and values that appear on the faces. Rolling a cube randomly selects a value from one of its faces and returns it. On each face of a "numerical die", there is a number between 1 and the number of faces on the die. Each number appears exactly once on the die.

An "unbalanced cube" also has a value called "roll possibility", which specifies the chance of each face being rolled.

In the game , there is a 'large bag' containing many "length dice", and another 'large bag' of unbalanced cube in different colors called "letter dice". 
10% of the dice in each bag are red, 25% are green, and 65% are blue.

A length cube is a numerical cube with 10 faces. If the cube shows 1, it is rolled again until a different number is rolled.

A letter cube is an unbalanced cube with 26 faces, each showing a letter from the English alphabet. The roll possibility for each letter is based on the frequency of that letter in the language [From letter frequency in wikipedia](https://en.wikipedia.org/wiki/Letter_frequency).

Each player, on their turn, rolls the length cube and rolls as many letter dice as the number they get on the length cube. 

For example, if the length cube shows 3, the player rolls 3 letter dice.

The player must use the rolled letter dice to create a valid English word of at least 2 letters. They can rearrange the dice and choose not to use some, but cannot use the same letter cube twice. However, multiple letter dice may show the same letter.

If the player succeeds in forming a word, they score points for each letter used. The score for each letter is 12 divided by the roll possibility of the letter, rounded up, raised to the power of 1.5, then the square root is taken. The result is then rounded down.

For example, for the word "zone", the player scores 17 points according to this calculation:

| Points | Frequency  | Letter |
|--------|------------|--------|
| 12     | 0.077%     | z      |
| 2      | 7.507%     | o      |
| 2      | 6.749%     | n      |
| 1      | 12.702%    | e      |

A red length cube grants the player an extra letter die. 

A red letter cube allows the player to use the letter on the cube as many times as they wish. 

Green dice allow the player to choose whether to reroll them.


Use `words.txt` to verify that the words entered by the player are valid. [word.txt - GitHub](https://raw.githubusercontent.com/dwyl/english-words/master/words.txt)


---

An exercise from Yam Mesica Python course.
