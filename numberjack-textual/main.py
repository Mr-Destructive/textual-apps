import random
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Button, Header, Footer, Input, Static


class IndexTray(Static):
    def compose(self) -> ComposeResult:
        indexes = list(range(1, 11))
        index_tray = Container()
        for n in indexes:
            index = Button(f"{n}", classes=f"i{n}", id="index")
            index_tray.mount(index)
        index_tray.id = "index_tray"
        yield index_tray


class NumberTray(Static):
    def compose(self) -> ComposeResult:
        numbers = list(range(1, 11))
        random.shuffle(numbers)
        number_tray = Container()
        for i, n in enumerate(numbers):
            number = Static(f"{n}", name=f"{n}", id="numbers", classes=f"n{i}")
            number_tray.mount(number)
        number_tray.id = "numbers_tray"
        yield number_tray


class NumberJack(App):
    """A Textual app Number Jack game"""

    CSS_PATH = "styles.css"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit_app", "Quit"),
    ]
    number = 0
    number_tray = list(range(1, 11))
    points = 0

    def update_number(self, number) -> int:
        self.number = number
        return self.number

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Called when a button is pressed."""
        button_id = event.button.id
        numbers = [f"n{i}" for i in range(1, 11)]
        number = self.number
        if button_id == "num_choice":
            number = int(self.query_one("#number_inp").value)
            number = self.update_number(number)
            self.number_tray = [int(i.name.strip("n")) for i in self.query("#numbers")]
            self.query_one("#points").update(renderable=str(self.points))

        elif event.button.id == "index":
            button = event.button
            guess_index = int(sorted(list(button.classes))[-1].strip("i")) - 1
            guess_number = str(self.number_tray[guess_index])

            if str(number) == str(guess_number):
                numbers = list(range(1, 11))
                random.shuffle(numbers)
                self.number_tray = numbers
                for i, n in enumerate(numbers):
                    self.query_one(f".n{i}").update(renderable=str(n))
                self.points += 1
                self.query_one("#points").update(renderable=str(self.points))
            else:
                self.query_one("#number_inp").value = ""
                self.query_one("#number_inp").placeholder = f"You Scored {self.points} points!"
                self.points = 0
                self.query_one("#points").update(renderable=str(self.points))

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Input(placeholder="Number", id="number_inp", classes="inp")
        yield Button("Play", id="num_choice", variant="success", classes="inp")
        yield Static("Points", id="points", classes="inp")
        yield Header()
        yield NumberTray("Number Tray", id="number_tray")
        yield IndexTray("Index Tray", id="index_tray")
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_quit_app(self) -> None:
        """An action to quit the app."""
        self.exit()


if __name__ == "__main__":
    app = NumberJack()
    app.run()
