#!/usr/bin/env python3
import os
import random
import sys
import time

try:
    import tkinter as tk
    from tkinter import font, simpledialog
except ImportError:
    tk = None

class Tamagotchi:
    def __init__(self, name: str):
        self.name = name
        self.age = 0
        self.hunger = 50
        self.happiness = 50
        self.energy = 50
        self.health = 100
        self.alive = True
        self.last_action = None

    def status(self) -> str:
        bars = lambda value: "[" + "#" * (value // 10) + " " * (10 - value // 10) + "]"
        return (
            f"Name: {self.name}\n"
            f"Age: {self.age} cycles\n"
            f"Health: {self.health:3d} {bars(self.health)}\n"
            f"Hunger: {self.hunger:3d} {bars(self.hunger)}\n"
            f"Happiness: {self.happiness:3d} {bars(self.happiness)}\n"
            f"Energy: {self.energy:3d} {bars(self.energy)}\n"
            f"Last action: {self.last_action or 'None'}\n"
        )

    def _clamp_stats(self) -> None:
        self.hunger = max(0, min(100, self.hunger))
        self.happiness = max(0, min(100, self.happiness))
        self.energy = max(0, min(100, self.energy))
        self.health = max(0, min(100, self.health))

    def _check_alive(self) -> None:
        if self.health <= 0 or self.hunger >= 100 or self.energy <= 0:
            self.alive = False

    def tick(self) -> None:
        self.age += 1
        self.hunger += random.randint(5, 12)
        self.energy -= random.randint(5, 9)
        self.happiness -= random.randint(2, 7)
        if self.hunger > 80:
            self.health -= random.randint(5, 10)
        if self.energy < 20:
            self.health -= random.randint(2, 6)
        if self.happiness < 20:
            self.health -= random.randint(1, 5)
        self._clamp_stats()
        self._check_alive()

    def feed(self) -> str:
        self.hunger -= random.randint(15, 30)
        self.energy += random.randint(3, 8)
        self.happiness += random.randint(1, 4)
        self.last_action = "Fed"
        self._clamp_stats()
        self.tick()
        return "You fed your Tamagotchi. Yum!"

    def play(self) -> str:
        self.happiness += random.randint(15, 25)
        self.energy -= random.randint(10, 18)
        self.hunger += random.randint(5, 12)
        self.last_action = "Played"
        self._clamp_stats()
        self.tick()
        return "You played together. Fun!"

    def sleep(self) -> str:
        self.energy += random.randint(20, 35)
        self.hunger += random.randint(5, 10)
        self.happiness += random.randint(2, 5)
        self.last_action = "Slept"
        self._clamp_stats()
        self.tick()
        return "Your Tamagotchi rested and feels refreshed."

    def medicine(self) -> str:
        self.health += random.randint(15, 25)
        self.energy -= random.randint(5, 10)
        self.happiness -= random.randint(2, 6)
        self.last_action = "Took medicine"
        self._clamp_stats()
        self.tick()
        return "You gave medicine. Healing begins."

    def special(self) -> str:
        event = random.choice(["bubble", "song", "treat"])
        if event == "bubble":
            self.happiness += 20
            self.energy -= 8
            effect = "Your Tamagotchi blew bubbles and smiled."
        elif event == "song":
            self.happiness += 15
            self.energy -= 5
            self.hunger += 5
            effect = "You sang a silly song together."
        else:
            self.hunger -= 20
            self.happiness += 10
            effect = "You shared a surprise treat."
        self.last_action = "Special"
        self._clamp_stats()
        self.tick()
        return effect

    def action(self, choice: str) -> str:
        actions = {
            "1": self.feed,
            "2": self.play,
            "3": self.sleep,
            "4": self.medicine,
            "5": self.special,
        }
        if choice not in actions:
            return "That isn't a valid action. Try again."
        return actions[choice]()

    def is_happy(self) -> bool:
        return self.happiness >= 70 and self.health >= 70

    def is_needy(self) -> bool:
        return self.hunger >= 70 or self.energy <= 30 or self.happiness <= 30


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def get_character() -> str:
    return (
        "  (o.o)\n"
        "  /| |\\\n"
        "   | |\n"
        "  /   \\\n"
        " (     )\n"
        "  \\___/"
    )


def terminal_main() -> None:
    clear_screen()
    print("Welcome to the Terminal Tamagotchi Simulator!")
    name = input("Name your Tamagotchi: ").strip() or "Tama"
    pet = Tamagotchi(name)

    while pet.alive:
        clear_screen()
        print(get_character())
        print()
        print(pet.status())
        if pet.is_happy():
            print("Your Tamagotchi is happy and healthy. Keep up the good care!\n")
        elif pet.is_needy():
            print("Your Tamagotchi needs attention soon. Choose an action carefully.\n")
        else:
            print("Quiet moment. Choose something fun to do.\n")

        print("Actions:")
        print("  1) Feed")
        print("  2) Play")
        print("  3) Sleep")
        print("  4) Medicine")
        print("  5) Surprise")
        print("  q) Quit")
        choice = input("Choose an action: ").strip().lower()

        if choice == "q":
            print("Goodbye! Your Tamagotchi will miss you.")
            break

        message = pet.action(choice)
        print(f"\n{message}")
        if not pet.alive:
            print("\nOh no! Your Tamagotchi didn't make it this time.")
            break

        time.sleep(1.2)

    if pet.alive:
        print("Thanks for playing! Come back any time.")
    else:
        print("Game over. You can restart to try again.")


class TamagotchiGUI:
    def __init__(self):
        if tk is None:
            raise RuntimeError("Tkinter is not available. Please use --cli to run in terminal mode.")

        self.root = tk.Tk()
        self.root.title("Terminal Tamagotchi")
        self.root.configure(bg="#B24670")
        self.root.geometry("600x550")
        self.root.resizable(False, False)

        self.mono = font.Font(family="Courier", size=11)
        self.header_font = font.Font(family="Courier", size=14, weight="bold")

        self.root.withdraw()
        name = simpledialog.askstring("Tamagotchi Name", "Name your Tamagotchi:", parent=self.root)
        self.root.deiconify()

        if name is None:
            name = "Tama"
            
        self.pet = Tamagotchi(name.strip() or "Tama")

        self.main_frame = tk.Frame(self.root, bg="#FAF6F6", padx=12, pady=12)
        self.main_frame.pack(fill="both", expand=True)

        self.title_label = tk.Label(
            self.main_frame,
            text="TERMINAL TAMAGOTCHI",
            bg="#111111",
            fg="#70ff70",
            font=self.header_font,
        )
        self.title_label.pack(pady=(0, 10))

        # Status frame with character and stats
        self.status_frame = tk.Frame(self.main_frame, bg="#050505", bd=2, relief="sunken")
        self.status_frame.pack(fill="x", pady=(0, 8))

        # Character display
        self.char_label = tk.Label(
            self.status_frame,
            text=self.get_character(),
            bg="#050505",
            fg="#80ff80",
            font=font.Font(family="Courier", size=12),
            justify="center",
        )
        self.char_label.pack(side="left", padx=10, pady=10)

        # Stats frame
        self.stats_frame = tk.Frame(self.status_frame, bg="#050505")
        self.stats_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.name_label = tk.Label(
            self.stats_frame,
            text=f"Name: {self.pet.name}",
            bg="#050505",
            fg="#80ff80",
            font=self.mono,
            anchor="w",
        )
        self.name_label.pack(fill="x")

        self.age_label = tk.Label(
            self.stats_frame,
            text=f"Age: {self.pet.age} cycles",
            bg="#050505",
            fg="#80ff80",
            font=self.mono,
            anchor="w",
        )
        self.age_label.pack(fill="x")

        # Progress bars for stats
        self.health_bar = self.create_progress_bar("Health", "#ff7070")
        self.hunger_bar = self.create_progress_bar("Hunger", "#ffff70")
        self.happiness_bar = self.create_progress_bar("Happiness", "#70ff70")
        self.energy_bar = self.create_progress_bar("Energy", "#7070ff")

        self.last_action_label = tk.Label(
            self.stats_frame,
            text=f"Last action: {self.pet.last_action or 'None'}",
            bg="#050505",
            fg="#80ff80",
            font=self.mono,
            anchor="w",
        )
        self.last_action_label.pack(fill="x", pady=(5, 0))

        self.message_label = tk.Label(
            self.main_frame,
            text="Welcome! Choose an action below.",
            anchor="w",
            justify="left",
            bg="#050505",
            fg="#a6f7a6",
            font=self.mono,
            bd=2,
            relief="sunken",
            padx=10,
            pady=8,
            width=60,
            height=3,
        )
        self.message_label.pack(fill="x", pady=(8, 8))

        buttons_frame = tk.Frame(self.main_frame, bg="#111111")
        buttons_frame.pack(fill="x")

        self.buttons = []
        actions = [
            ("Feed", "1"),
            ("Play", "2"),
            ("Sleep", "3"),
            ("Medicine", "4"),
            ("Surprise", "5"),
        ]

        for text, code in actions:
            button = tk.Button(
                buttons_frame,
                text=text,
                command=lambda choice=code: self.perform_action(choice),
                bg="#000000",
                fg="#70ff70",
                activebackground="#022002",
                activeforeground="#c8ffc8",
                font=self.mono,
                bd=2,
                relief="raised",
                padx=10,
                pady=6,
            )
            button.pack(side="left", expand=True, fill="x", padx=4, pady=2)
            self.buttons.append(button)

        self.quit_button = tk.Button(
            self.main_frame,
            text="Quit",
            command=self.root.destroy,
            bg="#000000",
            fg="#ff7070",
            activebackground="#330000",
            activeforeground="#ff9c9c",
            font=self.mono,
            bd=2,
            relief="raised",
            padx=10,
            pady=8,
            width=12,
        )
        self.quit_button.pack(pady=(10, 0))

        self.update_display()

    def get_character(self) -> str:
        # Cute ASCII art character
        return (
            "  (o.o)\n"
            "  /| |\\\n"
            "   | |\n"
            "  /   \\\n"
            " (     )\n"
            "  \\___/"
        )

    def create_progress_bar(self, label_text: str, color: str):
        frame = tk.Frame(self.stats_frame, bg="#050505")
        frame.pack(fill="x", pady=2)

        label = tk.Label(
            frame,
            text=f"{label_text}:",
            bg="#050505",
            fg="#80ff80",
            font=self.mono,
            width=10,
            anchor="w",
        )
        label.pack(side="left")

        try:
            import tkinter.ttk as ttk
            bar = ttk.Progressbar(
                frame,
                orient="horizontal",
                length=200,
                mode="determinate",
                maximum=100,
            )
            bar.pack(side="right", padx=(5, 0))
            bar.config(style=f"{color}.Horizontal.TProgressbar")
            # Custom style for color
            style = ttk.Style()
            style.configure(f"{color}.Horizontal.TProgressbar", background=color, troughcolor="#333333")
        except ImportError:
            # Fallback to text bar if ttk not available
            bar = tk.Label(
                frame,
                text="[          ]",
                bg="#050505",
                fg=color,
                font=self.mono,
                anchor="w",
            )
            bar.pack(side="right", padx=(5, 0))

        return bar

    def update_display(self) -> None:
        self.name_label.config(text=f"Name: {self.pet.name}")
        self.age_label.config(text=f"Age: {self.pet.age} cycles")
        self.last_action_label.config(text=f"Last action: {self.pet.last_action or 'None'}")

        # Update progress bars
        self.update_bar(self.health_bar, self.pet.health, "#ff7070")
        self.update_bar(self.hunger_bar, self.pet.hunger, "#ffff70")
        self.update_bar(self.happiness_bar, self.pet.happiness, "#70ff70")
        self.update_bar(self.energy_bar, self.pet.energy, "#7070ff")

        # Update character based on mood
        self.char_label.config(text=self.get_character())

        # Update message
        if self.pet.is_happy():
            self.message_label.config(text="Your Tamagotchi is happy and healthy. Keep up the good care!")
        elif self.pet.is_needy():
            self.message_label.config(text="Your Tamagotchi needs attention soon. Choose an action carefully.")
        else:
            self.message_label.config(text="Quiet moment. Choose something fun to do.")

        if not self.pet.alive:
            self.message_label.config(text="Oh no! Your Tamagotchi didn't make it this time. Game over.")
            self.disable_buttons()

    def update_bar(self, bar, value: int, color: str) -> None:
        if hasattr(bar, 'config'):  # ttk Progressbar
            bar['value'] = value
        else:  # Fallback text bar
            filled = value // 10
            bar.config(text=f"[{'#' * filled}{' ' * (10 - filled)}]", fg=color)

    def perform_action(self, choice: str) -> None:
        if not self.pet.alive:
            return

        message = self.pet.action(choice)
        self.message_label.config(text=message)
        self.update_display()

    def disable_buttons(self) -> None:
        for button in self.buttons:
            button.config(state="disabled")

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    if "--cli" in sys.argv or tk is None:
        terminal_main()
    else:
        TamagotchiGUI().run()
