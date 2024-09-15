# Set

Standard set game to one player and run time mode.

Check the instructions and game rules at:
https://en.wikipedia.org/wiki/Set_(card_game)

## Standard mode.

The game will show the user 12 set cards from a mixed deck of 81 cards, and will allow the user to choose which 3 cards is a set.

If the user chose a correct set, the three cards he chose are replaced by the following cards in the deck.

If user select an incorrect set, an error message is 
printed.

If it is not possible to make a set from the opened cards, 
return the cards to the deck, shuffle it and open 12 new cards.

The player wins when no more sets can be made from the 
cards in the deck.


## Run time mode.

There is a time limit of 3 minutes to find as many sets as possible.

shuffles cards and presents them to the user, checks if the answer from the user is correct.

Every time a set is found:

It is added back to the deck, the deck is shuffled and three new cards are revealed,

And adding 5 seconds to the clock.


---

An exercise from Yam Mesica Python course.
