import random
from typing import Callable


LOWER_BOUND = 1
UPPER_BOUND = 100
MAX_ATTEMPTS = 7


def play_round(
    secret_number: int,
    input_fn: Callable[[str], str],
    output_fn: Callable[[str], None],
) -> bool:
    attempts = 0

    while attempts < MAX_ATTEMPTS:
        raw_guess = input_fn(f"Your guess ({LOWER_BOUND}-{UPPER_BOUND}): ")
        try:
            guess = int(raw_guess)
        except ValueError:
            output_fn("Please enter a whole number.")
            continue

        if not LOWER_BOUND <= guess <= UPPER_BOUND:
            output_fn(f"Enter a number from {LOWER_BOUND} to {UPPER_BOUND}.")
            continue

        attempts += 1
        if guess == secret_number:
            output_fn(f"Correct! You guessed it in {attempts} attempt(s).")
            return True
        if guess < secret_number:
            output_fn("Too low. Try a higher number.")
        else:
            output_fn("Too high. Try a lower number.")

    output_fn(f"Out of attempts. The number was {secret_number}.")
    return False


def main(
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> None:
    output_fn("I'm thinking of a number from 1 to 100.")

    while True:
        output_fn(f"You have {MAX_ATTEMPTS} valid attempts.")
        secret_number = random.randint(LOWER_BOUND, UPPER_BOUND)
        play_round(secret_number, input_fn, output_fn)

        while True:
            response = input_fn("Play again? (y/n): ").strip().lower()
            if response in ("y", "yes"):
                break
            if response in ("n", "no"):
                output_fn("Thanks for playing!")
                return
            output_fn("Please answer y or n.")


if __name__ == "__main__":
    main()