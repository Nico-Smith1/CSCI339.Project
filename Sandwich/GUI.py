import tkinter as tk
from tkinter import ttk, messagebox

from Game import grammar, generate_order, count_ingredients
from Main import build_sandwich_tm


class TuringMachineGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Turing Machine Game")
        self.resizable(False, False)
        self.configure(bg="#b60724")

        # State
        self.tm = None
        self.target_sandwich = ""
        self.target_counts = {}
        self.player_sandwich = ""

        # Create two screens
        self.menu_frame = tk.Frame(self, bg="#ffffff", padx=20, pady=20)
        self.game_frame = tk.Frame(self, bg="#ffffff", padx=20, pady=20)

        self._build_menu_screen()
        self._build_game_screen()

        self.show_menu()

    # ----------------- Screen switching -----------------
    def show_menu(self):
        self.game_frame.pack_forget()
        self.menu_frame.pack(padx=40, pady=40)

    def show_game(self):
        self.menu_frame.pack_forget()
        self.game_frame.pack(padx=40, pady=40)

    # ----------------- Menu UI -----------------
    def _build_menu_screen(self):
        title = tk.Label(
            self.menu_frame, text="Turing Machine Game",
            font=("Rockwell", 20, "bold"), bg="#ffffff"
        )
        title.pack(pady=(0, 10))

        authors = tk.Label(
            self.menu_frame, text="Nick & Cameron",
            font=("Rockwell", 12), fg="#555555", bg="#ffffff"
        )
        authors.pack(pady=(0, 20))

        start_button = tk.Button(
            self.menu_frame, text="Start Game",
            font=("Rockwell", 12), bg="#dc0d28", fg="white",
            activebackground="#b60724", relief="flat",
            width=20, command=self.start_game
        )
        start_button.pack()

    # ----------------- Game UI -----------------
    def _build_game_screen(self):
        header = tk.Label(
            self.game_frame, text="Game Page",
            font=("Rockwell", 18, "bold"), bg="#ffffff"
        )
        header.grid(row=0, column=0, columnspan=3, pady=(0, 10))





        self.counts_label = tk.Label(
            self.game_frame, text="Ingredients Requested:\n",
            font=("Rockwell", 10), justify="left",
            bg="#f2f2f2", width=30, height=15,
            relief="groove", anchor="nw", padx=5, pady=5
        )
        self.counts_label.grid(row=2, column=0, columnspan=3, pady=5)

        self.player_label = tk.Label(
            self.game_frame, text="Your sandwich: ",
            font=("Rockwell", 12), bg="#ffffff"
        )
        self.player_label.grid(row=3, column=0, columnspan=3, sticky="w")

        # Ingredient buttons
        letters = ["A","T","C","D","E","F","G","H","I","J"]
        row_start = 4
        for i, letter in enumerate(letters):
            r = row_start + i // 5
            c = i % 5
            tk.Button(
                self.game_frame, text=letter, width=4,
                font=("Rockwell", 12),
                command=lambda ch=letter: self.add_ingredient(ch)
            ).grid(row=r, column=c, padx=2, pady=2)

        # Submit / clear / back
        tk.Button(
            self.game_frame, text="Submit",
            font=("Rockwell", 12), bg="#03681c",
            fg="white", relief="flat", width=15,
            command=self.submit_ingredients
        ).grid(row=row_start + 2, column=0, columnspan=2, pady=10)

        tk.Button(
            self.game_frame, text="Clear",
            font=("Rockwell", 12), width=10,
            command=self.clear_player_sandwich
        ).grid(row=row_start + 2, column=2)

        tk.Button(
            self.game_frame, text="Back to Menu",
            font=("Rockwell", 10),
            command=self.show_menu
        ).grid(row=row_start + 3, column=0, columnspan=3, pady=5)

        self.result_label = tk.Label(
            self.game_frame, text="Result: (not submitted)",
            font=("Rockwell", 12, "bold"), bg="#ffffff"
        )
        self.result_label.grid(row=row_start + 4, column=0, columnspan=3, pady=5)

        # TM transition output
        tm_label = tk.Label(
            self.game_frame, text="Turing Machine Steps:",
            font=("Rockwell", 12, "bold"), bg="#ffffff"
        )
        tm_label.grid(row=row_start + 5, column=0, columnspan=3)

        self.tm_output = tk.Text(
            self.game_frame, width=50, height=12,
            bg="#f2f2f2", font=("Courier", 9),
            relief="groove"
        )
        self.tm_output.grid(row=row_start + 6, column=0, columnspan=3, padx=5, pady=5)

    # ----------------- Game Logic -----------------
    def start_game(self):
        """Called when Start Game pressed."""
        try:
            self.target_sandwich = generate_order(grammar)
            self.target_counts = count_ingredients(self.target_sandwich)
            self.tm = build_sandwich_tm(self.target_counts)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return



        # Format counts
        lines = ["Ingredients Requested:"]
        for k in sorted(self.target_counts.keys()):
            if self.target_counts[k] > 0:
                lines.append(f"  {k}: {self.target_counts[k]}")
        self.counts_label.config(text="\n".join(lines))

        self.player_sandwich = ""
        self.player_label.config(text="Your sandwich: ")
        self.result_label.config(text="Result: (not submitted)")
        self.tm_output.delete("1.0", tk.END)

        self.show_game()

    def add_ingredient(self, ch):
        self.player_sandwich += ch
        self.player_label.config(text=f"Your sandwich: {self.player_sandwich}")

    def clear_player_sandwich(self):
        self.player_sandwich = ""
        self.player_label.config(text="Your sandwich: ")

    def submit_ingredients(self):
        if not self.player_sandwich:
            messagebox.showinfo("Empty", "Choose ingredients first.")
            return

        result = self.tm.run(self.player_sandwich)

        # Show ACCEPT/REJECT
        if result["accepted"]:
            self.result_label.config(text="Result: ACCEPTED ✅", fg="green")
        else:
            self.result_label.config(text="Result: REJECTED ❌", fg="red")

        # Print TM transitions
        self.tm_output.delete("1.0", tk.END)
        for line in result["transitions"]:
            self.tm_output.insert(tk.END, line + "\n")


if __name__ == "__main__":
    app = TuringMachineGame()
    app.mainloop()
