"""
Hangman — built with Textual (https://textual.textualize.io/)

Run with:
    pip install textual
    python hangman.py
"""

import random

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive
from textual.widgets import Static, Footer, Header

WORDS = [
    "python", "keyboard", "elephant", "mountain", "network",
    "terminal", "function", "variable", "recursion", "reactive",
    "textual", "widget", "asyncio", "interface", "algorithm",
]

MAX_WRONG = 6

STAGES = [
    r"""
  +---+
  |   |
      |
      |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========""",
]


class HangmanApp(App):
    """A terminal Hangman game."""

    CSS = """
    Screen {
        align: center middle;
        background: $surface;
    }

    #board {
        width: 60;
        border: round $primary;
        padding: 1 2;
        background: $panel;
    }

    #gallows {
        color: $warning;
        text-align: center;
        height: 9;
        content-align: center middle;
    }

    #word {
        text-align: center;
        text-style: bold;
        color: $success;
        margin-top: 1;
    }

    #wrong {
        text-align: center;
        color: $error;
        margin-top: 1;
    }

    #message {
        text-align: center;
        text-style: bold;
        margin-top: 1;
        height: 3;
    }

    #help {
        text-align: center;
        color: $text-muted;
        margin-top: 1;
    }
    """

    BINDINGS = [
        ("enter", "restart", "New word"),
        ("escape", "quit", "Quit"),
        ("ctrl+c", "quit", "Quit"),
    ]

    # reactive attributes: whenever these change, watch_* fires
    # and the relevant widget re-renders automatically.
    wrong_count: reactive[int] = reactive(0)
    guessed: reactive[set] = reactive(set)
    game_over: reactive[bool] = reactive(False)
    won: reactive[bool] = reactive(False)

    def __init__(self) -> None:
        super().__init__()
        self.word = random.choice(WORDS)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        with Vertical(id="board"):
            yield Static(STAGES[0], id="gallows")
            yield Static("", id="word")
            yield Static("", id="wrong")
            yield Static("", id="message")
            yield Static("Type a letter to guess. Press esc to quit.", id="help")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Hangman"
        self._refresh_word()
        self._refresh_wrong()

    # ---- reactive watchers: fire automatically on state change ----

    def watch_wrong_count(self, count: int) -> None:
        self.query_one("#gallows", Static).update(STAGES[min(count, MAX_WRONG)])

    def watch_game_over(self, over: bool) -> None:
        message = self.query_one("#message", Static)
        help_text = self.query_one("#help", Static)
        if over:
            if self.won:
                message.update("[bold green]You won! 🎉[/]")
            else:
                message.update(f"[bold red]You lost! The word was: {self.word}[/]")
            help_text.update("Press enter to play again, esc to quit.")
        else:
            message.update("")
            help_text.update("Type a letter to guess. Press esc to quit.")

    # ---- helpers ----

    def _refresh_word(self) -> None:
        display = " ".join(c if c in self.guessed else "_" for c in self.word)
        self.query_one("#word", Static).update(display)

    def _refresh_wrong(self) -> None:
        wrong_letters = sorted(g for g in self.guessed if g not in self.word)
        self.query_one("#wrong", Static).update(
            f"Wrong guesses ({self.wrong_count}/{MAX_WRONG}): {' '.join(wrong_letters)}"
        )

    def _new_game(self) -> None:
        self.word = random.choice(WORDS)
        self.guessed = set()
        self.wrong_count = 0
        self.won = False
        self.game_over = False
        self._refresh_word()
        self._refresh_wrong()

    # ---- input handling ----

    def on_key(self, event) -> None:
        key = event.key

        if self.game_over:
            return  # bindings (enter/q) handle restart/quit

        if len(key) == 1 and key.isalpha():
            letter = key.lower()
            if letter in self.guessed:
                return

            # reassigning triggers reactivity (mutating in place would not)
            self.guessed = self.guessed | {letter}

            if letter not in self.word:
                self.wrong_count += 1

            self._refresh_word()
            self._refresh_wrong()

            if self.wrong_count >= MAX_WRONG:
                self.won = False
                self.game_over = True
            elif all(c in self.guessed for c in self.word):
                self.won = True
                self.game_over = True

    def action_restart(self) -> None:
        if self.game_over:
            self._new_game()


if __name__ == "__main__":
    HangmanApp().run()
