import unittest
from unittest.mock import patch

import main as game


class PlayRoundTests(unittest.TestCase):
    def test_correct_guess_wins(self):
        responses = iter(["42"])
        messages = []

        won = game.play_round(42, lambda prompt: next(responses), messages.append)

        self.assertTrue(won)
        self.assertIn("Correct!", messages[-1])

    def test_higher_and_lower_hints(self):
        responses = iter(["25", "75", "50"])
        messages = []

        game.play_round(50, lambda prompt: next(responses), messages.append)

        self.assertIn("Too low", messages[0])
        self.assertIn("Too high", messages[1])

    def test_invalid_guesses_do_not_consume_attempts(self):
        responses = iter(["hello", "0", "101", "42"])
        messages = []

        won = game.play_round(42, lambda prompt: next(responses), messages.append)

        self.assertTrue(won)
        self.assertEqual(sum("Please enter a whole number." in message for message in messages), 1)
        self.assertEqual(sum("Enter a number from 1 to 100." in message for message in messages), 2)
        self.assertIn("in 1 attempt(s)", messages[-1])

    def test_seven_valid_guesses_end_the_round(self):
        responses = iter(["1"] * game.MAX_ATTEMPTS)
        messages = []

        won = game.play_round(100, lambda prompt: next(responses), messages.append)

        self.assertFalse(won)
        self.assertIn("Out of attempts", messages[-1])
        self.assertEqual(sum("Too low" in message for message in messages), game.MAX_ATTEMPTS)


class MainTests(unittest.TestCase):
    @patch("main.random.randint", side_effect=[10, 20])
    def test_replay_and_exit(self, randint):
        responses = iter(["10", "maybe", "yes", "20", "no"])
        messages = []

        game.main(lambda prompt: next(responses), messages.append)

        self.assertEqual(randint.call_count, 2)
        self.assertTrue(any("Please answer y or n." in message for message in messages))
        self.assertTrue(any("Thanks for playing!" in message for message in messages))


if __name__ == "__main__":
    unittest.main()