import tkinter as tk
from tkinter import messagebox


class AutomataSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("DFA / NFA Simulator")
        self.root.geometry("750x600")

        self.states = set()
        self.alphabet = set()
        self.transitions = {}
        self.start_state = ""
        self.final_states = set()

        # ---------- Title ----------
        title = tk.Label(
            root,
            text="DFA / NFA Simulator",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=15)

        # ---------- Automaton Type ----------
        type_frame = tk.Frame(root)
        type_frame.pack(pady=5)

        tk.Label(
            type_frame,
            text="Automaton Type:"
        ).grid(row=0, column=0, padx=5)

        self.automaton_type = tk.StringVar(value="DFA")

        tk.Radiobutton(
            type_frame,
            text="DFA",
            variable=self.automaton_type,
            value="DFA"
        ).grid(row=0, column=1)

        tk.Radiobutton(
            type_frame,
            text="NFA",
            variable=self.automaton_type,
            value="NFA"
        ).grid(row=0, column=2)

        # ---------- States ----------
        tk.Label(
            root,
            text="States (comma separated):"
        ).pack()

        self.states_entry = tk.Entry(root, width=60)
        self.states_entry.pack(pady=5)

        # ---------- Alphabet ----------
        tk.Label(
            root,
            text="Alphabet (comma separated):"
        ).pack()

        self.alphabet_entry = tk.Entry(root, width=60)
        self.alphabet_entry.pack(pady=5)

        # ---------- Start State ----------
        tk.Label(
            root,
            text="Start State:"
        ).pack()

        self.start_entry = tk.Entry(root, width=30)
        self.start_entry.pack(pady=5)

        # ---------- Final States ----------
        tk.Label(
            root,
            text="Final States (comma separated):"
        ).pack()

        self.final_entry = tk.Entry(root, width=60)
        self.final_entry.pack(pady=5)

        # ---------- Transition ----------
        transition_frame = tk.Frame(root)
        transition_frame.pack(pady=10)

        tk.Label(
            transition_frame,
            text="From:",
        ).grid(row=0, column=0)

        self.from_entry = tk.Entry(transition_frame, width=10)
        self.from_entry.grid(row=0, column=1, padx=5)

        tk.Label(
            transition_frame,
            text="Input:",
        ).grid(row=0, column=2)

        self.input_entry = tk.Entry(transition_frame, width=10)
        self.input_entry.grid(row=0, column=3, padx=5)

        tk.Label(
            transition_frame,
            text="To:"
        ).grid(row=0, column=4)

        self.to_entry = tk.Entry(transition_frame, width=10)
        self.to_entry.grid(row=0, column=5, padx=5)

        tk.Button(
            transition_frame,
            text="Add Transition",
            command=self.add_transition
        ).grid(row=0, column=6, padx=10)

        # ---------- Transition List ----------
        self.transition_list = tk.Listbox(root, width=70, height=8)
        self.transition_list.pack(pady=5)

        # ---------- Create Automaton ----------
        tk.Button(
            root,
            text="Create Automaton",
            command=self.create_automaton,
            width=20
        ).pack(pady=8)

        # ---------- Test String ----------
        tk.Label(
            root,
            text="Test String:"
        ).pack()

        self.test_entry = tk.Entry(root, width=40)
        self.test_entry.pack(pady=5)

        tk.Button(
            root,
            text="Check String",
            command=self.check_string,
            width=20
        ).pack(pady=8)

        # ---------- Result ----------
        self.result_label = tk.Label(
            root,
            text="Result will appear here",
            font=("Arial", 14, "bold")
        )
        self.result_label.pack(pady=10)

        # ---------- Path ----------
        self.path_label = tk.Label(
            root,
            text="Transition Path:",
            font=("Arial", 11)
        )
        self.path_label.pack(pady=5)

    # ------------------------------------------------
    # ADD TRANSITION
    # ------------------------------------------------

    def add_transition(self):
        from_state = self.from_entry.get().strip()
        symbol = self.input_entry.get().strip()
        to_state = self.to_entry.get().strip()

        if not from_state or not symbol or not to_state:
            messagebox.showerror(
                "Error",
                "Please enter From, Input and To."
            )
            return

        transition_text = (
            f"{from_state} -- {symbol} --> {to_state}"
        )

        self.transition_list.insert(
            tk.END,
            transition_text
        )

        # Store transition
        key = (from_state, symbol)

        if self.automaton_type.get() == "DFA":
            self.transitions[key] = to_state
        else:
            if key not in self.transitions:
                self.transitions[key] = set()

            self.transitions[key].add(to_state)

        # Clear boxes
        self.from_entry.delete(0, tk.END)
        self.input_entry.delete(0, tk.END)
        self.to_entry.delete(0, tk.END)

    # ------------------------------------------------
    # CREATE AUTOMATON
    # ------------------------------------------------

    def create_automaton(self):
        states_text = self.states_entry.get()
        alphabet_text = self.alphabet_entry.get()
        start_state = self.start_entry.get().strip()
        final_text = self.final_entry.get()

        self.states = {
            state.strip()
            for state in states_text.split(",")
            if state.strip()
        }

        self.alphabet = {
            symbol.strip()
            for symbol in alphabet_text.split(",")
            if symbol.strip()
        }

        self.start_state = start_state

        self.final_states = {
            state.strip()
            for state in final_text.split(",")
            if state.strip()
        }

        if not self.states:
            messagebox.showerror(
                "Error",
                "Please enter states."
            )
            return

        if self.start_state not in self.states:
            messagebox.showerror(
                "Error",
                "Start state must be one of the states."
            )
            return

        if not self.final_states.issubset(self.states):
            messagebox.showerror(
                "Error",
                "Final states must belong to the states."
            )
            return

        messagebox.showinfo(
            "Success",
            "Automaton created successfully!"
        )

    # ------------------------------------------------
    # CHECK STRING
    # ------------------------------------------------

    def check_string(self):
        if not self.start_state:
            messagebox.showerror(
                "Error",
                "First create the automaton."
            )
            return

        test_string = self.test_entry.get().strip()

        if self.automaton_type.get() == "DFA":
            self.check_dfa(test_string)
        else:
            self.check_nfa(test_string)

    # ------------------------------------------------
    # DFA SIMULATION
    # ------------------------------------------------

    def check_dfa(self, string):
        current_state = self.start_state
        path = [current_state]

        for symbol in string:

            key = (current_state, symbol)

            if key not in self.transitions:
                self.result_label.config(
                    text="REJECTED"
                )

                self.path_label.config(
                    text="Transition Path: "
                    + " → ".join(path)
                )

                return

            current_state = self.transitions[key]
            path.append(current_state)

        if current_state in self.final_states:
            self.result_label.config(
                text="ACCEPTED"
            )
        else:
            self.result_label.config(
                text="REJECTED"
            )

        self.path_label.config(
            text="Transition Path: "
            + " → ".join(path)
        )

    # ------------------------------------------------
    # NFA SIMULATION
    # ------------------------------------------------

    def check_nfa(self, string):

        current_states = {self.start_state}

        path = [self.start_state]

        for symbol in string:

            next_states = set()

            for state in current_states:

                key = (state, symbol)

                if key in self.transitions:
                    next_states.update(
                        self.transitions[key]
                    )

            if not next_states:
                self.result_label.config(
                    text="REJECTED"
                )

                self.path_label.config(
                    text="No valid transition found."
                )

                return

            current_states = next_states

            path.append(
                ",".join(current_states)
            )

        accepted = any(
            state in self.final_states
            for state in current_states
        )

        if accepted:
            self.result_label.config(
                text="ACCEPTED"
            )
        else:
            self.result_label.config(
                text="REJECTED"
            )

        self.path_label.config(
            text="Transition Path: "
            + " → ".join(path)
        )


# ------------------------------------------------
# MAIN PROGRAM
# ------------------------------------------------

root = tk.Tk()

app = AutomataSimulator(root)
root.configure(bg="#668C74")

root.mainloop()