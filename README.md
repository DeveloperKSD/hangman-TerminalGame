# Hangman — Python + Textual

A terminal Hangman game built with **Textual**, a modern Python framework
for building interactive terminal UIs (from the makers of the `rich` library).

## What this helps you learn

- **Reactive state** — `wrong_count`, `guessed`, `game_over`, and `won` are
  declared as `reactive` attributes. Whenever one changes, the relevant
  `watch_*` method fires automatically and updates just the affected part of
  the screen. You never manually say "now redraw the gallows" — you just
  change the value and the UI reacts, the same underlying idea behind
  frameworks like Vue or Svelte, just running in a terminal.
- **CSS in the terminal** — the `CSS` block on the `HangmanApp` class is real
  CSS-like syntax (selectors, `border`, `padding`, `color`, theme variables
  like `$primary`) styling terminal widgets instead of a webpage.
- **Widget composition** — the UI is built by composing `Static` widgets
  inside a `Vertical` container in `compose()`, rather than manually managing
  cursor positions and screen clears.
- **Textual's key/binding system** — letter keys are handled in a generic
  `on_key` handler, while dedicated actions (`restart`, `quit`) are declared
  declaratively in `BINDINGS`. Worth noticing: an earlier draft of this bound
  `q` to quit, which silently broke guessing the letter "q" — a good small
  example of why testing your actual input paths matters, not just eyeballing
  the code.
- **Headless testing** — Textual ships a `run_test()` / `Pilot` API that lets
  you simulate keypresses and assert on app state without a real terminal,
  which is how this game's win/lose logic was actually verified before
  handing it to you.

## Setup

```bash
pip install textual
python hangman.py
```

## How to play

- Type any letter to guess it.
- 6 wrong guesses and the gallows is complete — game over.
- Press `enter` after a round ends to play again with a new word.
- Press `esc` or `ctrl+c` to quit any time.


## Image

<img width="1113" height="779" alt="image" src="https://github.com/user-attachments/assets/5883ba0e-4c9b-4263-bc79-48f57ed0e015" />

