
import tkinter as tk
from tkinter import messagebox


class AutomataSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("DFA / NFA Simulator")
        self.root.geometry("750x600")
        self.root.configure(bg="#D8D2C8")

        self.states = set()
        self.alphabet = set()
        self.transitions = {}
        self.start_state = ""
        self.final_states = set()

        # ---------- Colors ----------
        #bg_color = "#875F45"
        content_color = "#A8B8A5"
        frame_color = "#A8B8A5"
        label_color = "#774422"
        entry_bg = "#F8F6F2"
        button_color = "#2F6F7E"
        button_text = "white"
        list_bg = "#D8D2C8"

        # ---------- Title ----------
        title = tk.Label(
            root,
            text="DFA / NFA Simulator",
            font=("Arial", 22, "bold"),
          #  bg=bg_color,
            fg="#174A55"
        )
        title.pack(pady=10)

        # ============================================================
        # OUTER CONTENT FRAME
        # ============================================================

        content_frame = tk.Frame(
            root,
            bg=content_color,
            bd=3,
            relief="solid",
            width=850,
            height=800,
        )
        content_frame.pack(
            padx=20,
            pady=5
            
        )
        content_frame.pack_propagate(False)
        # ---------- Automaton Type ----------
        type_frame = tk.Frame(
            content_frame,
            bg=frame_color,
            bd=2,
            relief="groove"
        )
        type_frame.pack(pady=5, padx=20)

        tk.Label(
            type_frame,
            text="Automaton Type:",
            font=("Arial", 11, "bold"),
            bg=frame_color,
            fg=label_color
        ).grid(row=0, column=0, padx=8, pady=8)

        self.automaton_type = tk.StringVar(value="DFA")

        tk.Radiobutton(
            type_frame,
            text="DFA",
            variable=self.automaton_type,
            value="DFA",
            font=("Arial", 10),
            bg=frame_color,
            fg=label_color,
            activebackground=frame_color,
            selectcolor="#FFFFFF"
        ).grid(row=0, column=1, padx=8)

        tk.Radiobutton(
            type_frame,
            text="NFA",
            variable=self.automaton_type,
            value="NFA",
            font=("Arial", 10),
            bg=frame_color,
            fg=label_color,
            activebackground=frame_color,
            selectcolor="#FFFFFF"
        ).grid(row=0, column=2, padx=8)

        # ---------- States ----------
        tk.Label(
            content_frame,
            text="States (comma separated):",
            font=("Arial", 10, "bold"),
            bg=content_color,
            fg=label_color
        ).pack()

        self.states_entry = tk.Entry(
            content_frame,
            width=60,
            font=("Arial", 10),
            bg=entry_bg,
            fg="#222222",
            relief="solid",
            bd=1
        )
        self.states_entry.pack(pady=3, ipady=3)

        # ---------- Alphabet ----------
        tk.Label(
            content_frame,
            text="Alphabet (comma separated):",
            font=("Arial", 10, "bold"),
            bg=content_color,
            fg=label_color
        ).pack()

        self.alphabet_entry = tk.Entry(
            content_frame,
            width=60,
            font=("Arial", 10),
            bg=entry_bg,
            fg="#222222",
            relief="solid",
            bd=1
        )
        self.alphabet_entry.pack(pady=3, ipady=3)

        # ---------- Start State ----------
        tk.Label(
            content_frame,
            text="Start State:",
            font=("Arial", 10, "bold"),
            bg=content_color,
            fg=label_color
        ).pack()

        self.start_entry = tk.Entry(
            content_frame,
            width=30,
            font=("Arial", 10),
            bg=entry_bg,
            fg="#222222",
            relief="solid",
            bd=1
        )
        self.start_entry.pack(pady=3, ipady=3)

        # ---------- Final States ----------
        tk.Label(
            content_frame,
            text="Final States (comma separated):",
            font=("Arial", 10, "bold"),
            bg=content_color,
            fg=label_color
        ).pack()

        self.final_entry = tk.Entry(
            content_frame,
            width=60,
            font=("Arial", 10),
            bg=entry_bg,
            fg="#222222",
            relief="solid",
            bd=1
        )
        self.final_entry.pack(pady=3, ipady=3)

        # ---------- Transition ----------
        transition_frame = tk.Frame(
            content_frame,
            bg=frame_color,
            bd=2,
            relief="groove"
        )
        transition_frame.pack(pady=7, padx=15)

        tk.Label(
            transition_frame,
            text="From:",
            font=("Arial", 10, "bold"),
            bg=frame_color,
            fg=label_color
        ).grid(row=0, column=0, padx=5, pady=7)

        self.from_entry = tk.Entry(
            transition_frame,
            width=10,
            font=("Arial", 10),
            bg=entry_bg,
            relief="solid",
            bd=1
        )
        self.from_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=7,
            ipady=3
        )

        tk.Label(
            transition_frame,
            text="Input:",
            font=("Arial", 10, "bold"),
            bg=frame_color,
            fg=label_color
        ).grid(row=0, column=2, padx=5)

        self.input_entry = tk.Entry(
            transition_frame,
            width=10,
            font=("Arial", 10),
            bg=entry_bg,
            relief="solid",
            bd=1
        )
        self.input_entry.grid(
            row=0,
            column=3,
            padx=5,
            pady=7,
            ipady=3
        )

        tk.Label(
            transition_frame,
            text="To:",
            font=("Arial", 10, "bold"),
            bg=frame_color,
            fg=label_color
        ).grid(row=0, column=4, padx=5)

        self.to_entry = tk.Entry(
            transition_frame,
            width=10,
            font=("Arial", 10),
            bg=entry_bg,
            relief="solid",
            bd=1
        )
        self.to_entry.grid(
            row=0,
            column=5,
            padx=5,
            pady=7,
            ipady=3
        )

        tk.Button(
            transition_frame,
            text="Add Transition",
            command=self.add_transition,
            font=("Arial", 10, "bold"),
            bg=button_color,
            fg=button_text,
            activebackground="#245966",
            activeforeground="#FFFFFF",
            relief="raised",
            bd=2,
            padx=8,
            pady=4,
            cursor="hand2"
        ).grid(
            row=0,
            column=6,
            padx=10
        )

        # ---------- Transition List ----------
        self.transition_list = tk.Listbox(
            content_frame,
            width=70,
            height=5,
            font=("Consolas", 10),
            bg=list_bg,
            fg="#17343B",
            selectbackground="#7FB3BD",
            selectforeground="#FFFFFF",
            relief="solid",
            bd=1
        )
        self.transition_list.pack(pady=3)

        # ---------- Create Automaton ----------
        tk.Button(
            content_frame,
            text="Create Automaton",
            command=self.create_automaton,
            width=20,
            font=("Arial", 10, "bold"),
            bg=button_color,
            fg=button_text,
            activebackground="#245966",
            activeforeground="#FFFFFF",
            relief="raised",
            bd=2,
            padx=8,
            pady=4,
            cursor="hand2"
        ).pack(pady=5)

        # ---------- Test String ----------
        tk.Label(
            content_frame,
            text="Test String:",
            font=("Arial", 10, "bold"),
            bg=content_color,
            fg=label_color
        ).pack()

        self.test_entry = tk.Entry(
            content_frame,
            width=40,
            font=("Arial", 10),
            bg=entry_bg,
            fg="#222222",
            relief="solid",
            bd=1
        )
        self.test_entry.pack(pady=3, ipady=3)

        tk.Button(
            content_frame,
            text="Check String",
            command=self.check_string,
            width=20,
            font=("Arial", 10, "bold"),
            bg=button_color,
            fg=button_text,
            activebackground="#245966",
            activeforeground="#FFFFFF",
            relief="raised",
            bd=2,
            padx=8,
            pady=4,
            cursor="hand2"
        ).pack(pady=5)

        # ---------- Result ----------
        self.result_label = tk.Label(
            content_frame,
            text="Result will appear here",
            font=("Arial", 14, "bold"),
            bg=content_color,
            fg="#174A55"
        )
        self.result_label.pack(pady=5)

        # ---------- Path ----------
        self.path_label = tk.Label(
            content_frame,
            text="Transition Path:",
            font=("Arial", 11),
            bg=content_color,
            fg=label_color
        )
        self.path_label.pack(pady=3)

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

root.mainloop()