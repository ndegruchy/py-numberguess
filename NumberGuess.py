#!/usr/bin/env python3

"""
My crappy guessing game

Changelog:
  - Added scores file
  - Command-line arguments
  - Functions

TODO: Create scores file/folder if not found
TODO: Compare scores?
TODO: CSV scores?
"""

import os
import sys
import random
import argparse
from datetime import datetime as date
from pathlib import Path

if "XDG_DATA_HOME" in os.environ:
    scoreboard = Path(os.environ["XDG_DATA_HOME"] + "/guessing-game/scores.txt")
    if not Path(os.environ["XDG_DATA_HOME"] + "guessing-game").exists():
        os.mkdir(os.environ["XDG_DATA_HOME"] + "/guessing-game/")
        Path(scoreboard).touch()
elif "LOCALAPPDATA" in os.environ:
    scoreboard = Path(os.environ["LOCALAPPDATA"] + "\\guessing-game\\scores.txt")
    if not Path(os.environ["LOCALAPPDATA"] + "\\guessing-game\\").exists():
        os.mkdir(os.environ["LOCALAPPDATA"] + "\\guessing-game\\")
        Path(scoreboard).touch()
else:
    scoreboard = Path(os.environ["HOME"] + ".guessing-game-scores")
    if not Path(scoreboard).exists():
        Path(scoreboard).touch()


guesses = []


def collect_guess(guess):
    """Adds a guess to the list of guesses

    Args:
        guess (int): the guess to add to the list
    """
    guesses.append(guess)


def check_guess(number=0, actual=100, attempts=1):
    """Checks the guess against the answer

    Keyword Arguments:
        number {int} -- The guessed number (default: {0})
        actual {int} -- The answer that you're checking against (default: {100})

    Returns:
        Bool -- True if correct, false if not
    """
    if number == actual:
        print("Wow! That was the right answer!")
        print("It took %d guesses to find that answer" % attempts)
        scores.write("%s: User guessed the right number (%d) in %d guesses. Guesed %s\n"\
             % (date.now(), answer, attempts, ', '.join(map(str, guesses))))

        return True

    elif number > actual:
        print("Your answer is too large")
        return False

    elif number < actual:
        print("Your answer is too small")
        return False


# Command-line arguments
parser = argparse.ArgumentParser(description="Play a number guessing game")
parser.add_argument("-g", "--guesses", help="The number of attempts you get", type=int, default=5)
parser.add_argument("-m", "--min", help="Minimum number to pick from", type=int, default=1)
parser.add_argument("-x", "--max", help="Maximum number to pick from", type=int, default=20)

args = parser.parse_args()

# Do some checking for values
if args.min > args.max or args.min == args.max:
    print("The maximum value must be larger than the minimum value.")
    sys.exit(1)

if args.min < 0 or args.max < 0:
    print("Negative numbers aren't supported. Sorry.")
    sys.exit(1)

if args.guesses <= 0:
    print("You cannot have zero or less guesses")
    sys.exit(1)

if args.guesses > 255:
    print("Really?")
    sys.exit(0)

if args.max - args.min >= 100:
    print("Hard mode enabled. Good Luck.")

# Picking a number
answer = random.randint(args.min, args.max)

try:
    if scoreboard.exists:
        with scoreboard.open("a+") as scores:

            print("I'm thinking of a number between %d and %d, can you guess it?"\
                % (args.min, args.max))
            print("I'll give you %d guesses." % args.guesses)

            for attempt in range(1, (args.guesses + 1)):
                guess = int(input("Guess: "))

                print("That was guess #%d" % attempt)

                if check_guess(guess, answer, attempt):
                    # Break out of the loop when we find a correct guess
                    break
                elif attempt == args.guesses:
                    # No more guesses!
                    print("You're out of guesses! The answer was %d." % answer)
                    scores.write("%s: User failed to guess the number (%d) in %d guesses. Guessed: %s\n"\
                         % (date.now(), answer, args.guesses, ', '.join(map(str, guesses))))
                else:
                    # Skip to next guess
                    print("You now have %d guess(es) remaining." % (args.guesses - attempt))

                collect_guess(guess)

except OSError:
    print("Error opening the scores file, does it exist and is it read/writable?")
    print("%s" % scoreboard)
    sys.exit(1)
