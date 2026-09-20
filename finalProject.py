import tkinter as tk
from tkinter import messagebox


class AutomataSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("DFA / NFA Simulator")
        self.root.geometry("1200x900")
        self.root.minsize(1050, 720)
        self.root.configure(bg="#D8D2C8")

        self.states = set()
        self.alphabet = set()
        self.transitions = {}
        self.start_state = ""
        self.final_states = set()
        self.dead_state = None
        self.epsilon = "ε"

        # ---------- Colors ----------
        content_color = "#A8B8A5"
        frame_color = "#A8B8A5"
        label_color = "#774422"
        entry_bg = "#F8F6F2"
        button_color = "#2F6F7E"
        button_text = "white"
        list_bg = "#D8D2C8"
        border_color = "#6C8B83"
        text_color = "#17343B"

        # ---------- Title ----------
        title = tk.Label(
            root,
            text="DFA / NFA Simulator",
            font=("Arial", 25, "bold"),
            fg="#174A55",
            bg="#D8D2C8"
        )
        title.pack(pady=(10, 8))

        tk.Frame(
            root,
            bg="#F8F6F2",
            height=1
        ).pack(fill="x", padx=22)

        # ============================================================
        # MAIN SCROLLABLE AREA
        # ============================================================
        scroll_container = tk.Frame(root, bg=content_color)
        scroll_container.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=10
        )

        self.canvas = tk.Canvas(
            scroll_container,
            bg=content_color,
            highlightthickness=0
        )

        self.v_scrollbar = tk.Scrollbar(
            scroll_container,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(
            yscrollcommand=self.v_scrollbar.set
        )

        self.v_scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        content_frame = tk.Frame(
            self.canvas,
            bg=content_color
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=content_frame,
            anchor="nw"
        )

        content_frame.bind(
            "<Configure>",
            lambda event: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.bind(
            "<Configure>",
            lambda event: self.canvas.itemconfig(
                self.canvas_window,
                width=max(event.width, 1000)
            )
        )

        self.canvas.bind_all(
            "<MouseWheel>",
            self._on_mousewheel
        )

        # Two-column project layout.
        content_frame.columnconfigure(0, minsize=500)
        content_frame.columnconfigure(1, weight=1)

        # ============================================================
        # LEFT SIDE - INPUT AND SIMULATION CONTROLS
        # ============================================================
        left_panel = tk.Frame(
            content_frame,
            bg=content_color,
            width=500
        )
        left_panel.grid(
            row=0,
            column=0,
            sticky="nw",
            padx=(0, 10)
        )
        left_panel.grid_propagate(False)

        # ---------- Automaton Type ----------
        type_frame = tk.LabelFrame(
            left_panel,
            text="Automaton Type",
            font=("Arial", 12, "bold"),
            bg=frame_color,
            fg=label_color,
            bd=2,
            relief="groove",
            padx=10,
            pady=8
        )
        type_frame.pack(fill="x", pady=(0, 8))

        self.automaton_type = tk.StringVar(value="DFA")

        tk.Radiobutton(
            type_frame,
            text="DFA",
            variable=self.automaton_type,
            value="DFA",
            font=("Arial", 12),
            bg=frame_color,
            fg=label_color,
            activebackground=frame_color,
            activeforeground=label_color,
            selectcolor="#FFFFFF"
        ).grid(row=0, column=0, padx=(5, 20))

        tk.Radiobutton(
            type_frame,
            text="NFA",
            variable=self.automaton_type,
            value="NFA",
            font=("Arial", 12),
            bg=frame_color,
            fg=label_color,
            activebackground=frame_color,
            activeforeground=label_color,
            selectcolor="#FFFFFF"
        ).grid(row=0, column=1, padx=5)

        # ---------- Helper for input fields ----------
        def add_entry(label_text, width=48):
            tk.Label(
                left_panel,
                text=label_text,
                font=("Arial", 11, "bold"),
                bg=content_color,
                fg=label_color,
                anchor="w"
            ).pack(fill="x", pady=(4, 2))

            entry = tk.Entry(
                left_panel,
                width=width,
                font=("Arial", 11),
                bg=entry_bg,
                fg="#222222",
                relief="solid",
                bd=1
            )
            entry.pack(fill="x", ipady=5, pady=(0, 4))
            return entry

        self.states_entry = add_entry(
            "States (comma separated):"
        )

        self.alphabet_entry = add_entry(
            "Alphabet (comma separated):"
        )

        self.start_entry = add_entry(
            "Start State:",
            width=30
        )

        self.final_entry = add_entry(
            "Final States (comma separated):"
        )

        self.regex_entry = add_entry(
            "Regular Expression:"
        )

        tk.Label(
            left_panel,
            text="(e.g. (a|b)*abb)",
            font=("Arial", 9),
            bg=content_color,
            fg=label_color,
            anchor="w"
        ).pack(fill="x", pady=(0, 5))

        tk.Label(
            left_panel,
            text=(
                "Operators: | = OR, + = Positive closure, "
                "* = Kleene closure, ( ) = grouping"
            ),
            font=("Arial", 8),
            bg=content_color,
            fg=label_color,
            anchor="w",
            wraplength=480,
            justify="left"
        ).pack(fill="x", pady=(0, 8))

        # ---------- Main buttons ----------
        button_row = tk.Frame(
            left_panel,
            bg=content_color
        )
        button_row.pack(fill="x", pady=(0, 10))

        tk.Button(
            button_row,
            text="Create Automaton",
            command=self.create_automaton,
            font=("Arial", 11, "bold"),
            bg=button_color,
            fg=button_text,
            activebackground="#245966",
            activeforeground="#FFFFFF",
            relief="raised",
            bd=2,
            padx=10,
            pady=8,
            cursor="hand2"
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 5)
        )

        tk.Button(
            button_row,
            text="Clear",
            command=self.clear_all,
            font=("Arial", 11, "bold"),
            bg="#687878",
            fg="white",
            activebackground="#566565",
            activeforeground="white",
            relief="raised",
            bd=2,
            padx=10,
            pady=8,
            cursor="hand2"
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(5, 0)
        )

        # ---------- Test String ----------
        test_frame = tk.LabelFrame(
            left_panel,
            text="Test String",
            font=("Arial", 12, "bold"),
            bg=frame_color,
            fg=label_color,
            bd=2,
            relief="groove",
            padx=10,
            pady=8
        )
        test_frame.pack(fill="x", pady=(0, 8))

        self.test_entry = tk.Entry(
            test_frame,
            font=("Arial", 11),
            bg=entry_bg,
            fg="#222222",
            relief="solid",
            bd=1
        )
        self.test_entry.pack(fill="x", ipady=5, pady=(2, 7))

        tk.Button(
            test_frame,
            text="Check String",
            command=self.check_string,
            font=("Arial", 11, "bold"),
            bg=button_color,
            fg="white",
            activebackground="#245966",
            activeforeground="white",
            relief="raised",
            bd=2,
            pady=8,
            cursor="hand2"
        ).pack(fill="x")

        # ---------- Result ----------
        result_frame = tk.LabelFrame(
            left_panel,
            text="Result",
            font=("Arial", 12, "bold"),
            bg=frame_color,
            fg=label_color,
            bd=2,
            relief="groove",
            padx=10,
            pady=8
        )
        result_frame.pack(fill="x", pady=(0, 8))

        self.result_label = tk.Label(
            result_frame,
            text="Result will appear here",
            font=("Arial", 14, "bold"),
            bg=entry_bg,
            fg="#174A55",
            relief="solid",
            bd=1,
            anchor="nw",
            justify="left",
            height=3
        )
        self.result_label.pack(fill="x")

        self.path_label = tk.Label(
            result_frame,
            text="Transition Path:",
            font=("Arial", 10),
            bg=frame_color,
            fg=label_color,
            wraplength=450,
            justify="left",
            anchor="w"
        )
        self.path_label.pack(fill="x", pady=(7, 0))

        # Keep the transition Listbox for the existing project logic.
        # It is intentionally hidden because the new GUI uses the tables.
        self.transition_list = tk.Listbox(
            left_panel,
            width=1,
            height=1,
            font=("Consolas", 9),
            bg=list_bg,
            fg=text_color
        )

        # ============================================================
        # RIGHT SIDE - DIAGRAM AND TABLES
        # ============================================================
        right_panel = tk.Frame(
            content_frame,
            bg=content_color,
            width=690
        )
        right_panel.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        # ---------- Automaton Diagram ----------
        diagram_outer = tk.LabelFrame(
            right_panel,
            text="Automaton Diagram",
            font=("Arial", 12, "bold"),
            bg=frame_color,
            fg=label_color,
            bd=2,
            relief="groove",
            padx=8,
            pady=8
        )
        diagram_outer.pack(fill="x", pady=(0, 10))

        self.diagram_frame = tk.Frame(
            diagram_outer,
            bg="#F8F6F2",
            bd=1,
            relief="solid",
            width=660,
            height=315
        )
        self.diagram_frame.pack(
            fill="x",
            expand=False
        )
        self.diagram_frame.pack_propagate(False)

        self.diagram_canvas = tk.Canvas(
            self.diagram_frame,
            width=650,
            height=300,
            bg="#F8F6F2",
            highlightthickness=0
        )

        self.diagram_hbar = tk.Scrollbar(
            self.diagram_frame,
            orient="horizontal",
            command=self.diagram_canvas.xview
        )
        self.diagram_vbar = tk.Scrollbar(
            self.diagram_frame,
            orient="vertical",
            command=self.diagram_canvas.yview
        )

        self.diagram_canvas.configure(
            xscrollcommand=self.diagram_hbar.set,
            yscrollcommand=self.diagram_vbar.set
        )

        self.diagram_vbar.pack(side="right", fill="y")
        self.diagram_hbar.pack(side="bottom", fill="x")
        self.diagram_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        # ---------- Automaton Information ----------
        self.automaton_info = tk.Label(
            right_panel,
            text="Generated automaton will appear below",
            font=("Arial", 9, "bold"),
            bg=content_color,
            fg=label_color,
            wraplength=650,
            justify="center"
        )
        self.automaton_info.pack(fill="x", pady=(0, 7))

        # ---------- Automaton Transition Table ----------
        table_outer = tk.LabelFrame(
            right_panel,
            text="Automaton Transition Table",
            font=("Arial", 12, "bold"),
            bg=frame_color,
            fg=label_color,
            bd=2,
            relief="groove",
            padx=8,
            pady=8
        )
        table_outer.pack(fill="x", pady=(0, 10))

        self.table_frame = tk.Frame(
            table_outer,
            bg="#F8F6F2"
        )
        self.table_frame.pack(fill="x")

        # ---------- NFA Transition Table ----------
        nfa_outer = tk.LabelFrame(
            right_panel,
            text="NFA Transition Table",
            font=("Arial", 12, "bold"),
            bg=frame_color,
            fg=label_color,
            bd=2,
            relief="groove",
            padx=8,
            pady=8
        )
        nfa_outer.pack(fill="x", pady=(0, 10))

        self.nfa_table_frame = tk.Frame(
            nfa_outer,
            bg="#F8F6F2",
            height=105
        )
        self.nfa_table_frame.pack(fill="x")
        self.nfa_table_frame.pack_propagate(False)

        self.nfa_table_message = tk.Label(
            self.nfa_table_frame,
            text="(Not applicable for DFA)",
            font=("Arial", 10),
            bg="#F8F6F2",
            fg="#777777"
        )
        self.nfa_table_message.pack(
            fill="both",
            expand=True
        )

        # ---------- Test String State Transition Table ----------
        test_outer = tk.LabelFrame(
            right_panel,
            text="Test String State Transition Table",
            font=("Arial", 12, "bold"),
            bg=frame_color,
            fg=label_color,
            bd=2,
            relief="groove",
            padx=8,
            pady=8
        )
        test_outer.pack(fill="x")

        self.test_table_frame = tk.Frame(
            test_outer,
            bg="#F8F6F2"
        )
        self.test_table_frame.pack(fill="x")

        self._create_empty_test_table()


    def clear_all(self):
        """Clear GUI fields and generated display data."""
        for entry in (
            self.states_entry,
            self.alphabet_entry,
            self.start_entry,
            self.final_entry,
            self.regex_entry,
            self.test_entry
        ):
            entry.delete(0, tk.END)

        self.states.clear()
        self.alphabet.clear()
        self.transitions.clear()
        self.start_state = ""
        self.final_states.clear()
        self.dead_state = None

        self.transition_list.delete(0, tk.END)

        for widget in self.table_frame.winfo_children():
            widget.destroy()

        for widget in self.nfa_table_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.nfa_table_frame,
            text="(Not applicable for DFA)",
            font=("Arial", 10),
            bg="#F8F6F2",
            fg="#777777"
        ).pack(fill="both", expand=True)

        self.diagram_canvas.delete("all")
        self.diagram_canvas.configure(scrollregion=(0, 0, 650, 300))

        self.diagram_canvas.create_text(
            325,
            150,
            text="Create an automaton to display its diagram.",
            font=("Arial", 11, "italic"),
            fill="#17343B"
        )

        self.automaton_info.config(
            text="Generated automaton will appear below"
        )

        self.result_label.config(
            text="Result will appear here"
        )

        self.path_label.config(
            text="Transition Path:"
        )

        self._create_empty_test_table()

    def update_nfa_section(self):
        """Update the separate NFA panel in the GUI."""
        for widget in self.nfa_table_frame.winfo_children():
            widget.destroy()

        if self.automaton_type.get() == "DFA":
            tk.Label(
                self.nfa_table_frame,
                text="(Not applicable for DFA)",
                font=("Arial", 10),
                bg="#F8F6F2",
                fg="#777777"
            ).pack(fill="both", expand=True)
            return

        symbols = sorted(self.alphabet)
        if self.epsilon not in symbols:
            symbols.append(self.epsilon)

        headers = ["State"] + symbols

        for col, header in enumerate(headers):
            tk.Label(
                self.nfa_table_frame,
                text=header,
                font=("Arial", 9, "bold"),
                bg="#A8B8A5",
                fg="#774422",
                relief="solid",
                bd=1,
                width=14
            ).grid(
                row=0,
                column=col,
                sticky="nsew"
            )

        for row, state in enumerate(sorted(self.states), start=1):
            state_text = (
                ("→ " if state == self.start_state else "")
                + state
                + (" *" if state in self.final_states else "")
            )

            tk.Label(
                self.nfa_table_frame,
                text=state_text,
                font=("Arial", 9, "bold"),
                bg="#F8F6F2",
                fg="#774422",
                relief="solid",
                bd=1,
                width=14
            ).grid(
                row=row,
                column=0,
                sticky="nsew"
            )

            for col, symbol in enumerate(symbols, start=1):
                value = self.transitions.get((state, symbol), set())

                if isinstance(value, set):
                    value = (
                        ",".join(sorted(value))
                        if value else "—"
                    )
                else:
                    value = str(value) if value else "—"

                tk.Label(
                    self.nfa_table_frame,
                    text=value,
                    font=("Consolas", 9),
                    bg="#F8F6F2",
                    fg="#17343B",
                    relief="solid",
                    bd=1,
                    width=14
                ).grid(
                    row=row,
                    column=col,
                    sticky="nsew"
                )

    def _on_mousewheel(self, event):
        """Scroll the main content with the mouse wheel."""
        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    # ================================================================
    # REGULAR EXPRESSION -> AUTOMATON
    # ================================================================

    def normalize_regex(self, regex):
        """
        Converts the user's regular expression into tokens and inserts
        explicit concatenation operators '.' where needed.

        Supported:
            |  alternation / OR
            +  positive closure
            *  Kleene star
            ?  zero or one
            ( ) grouping
            .  explicit concatenation
        """
        regex = regex.replace(" ", "")

        if not regex:
            raise ValueError("Please enter a regular expression.")

        regex = regex.replace("epsilon", self.epsilon)

        tokens = []
        i = 0

        while i < len(regex):
            ch = regex[i]

            if ch == "\\":
                if i + 1 >= len(regex):
                    raise ValueError(
                        "A backslash must be followed by a character."
                    )
                tokens.append(("literal", regex[i + 1]))
                i += 2
                continue

            if ch in "()|*+?.":
                tokens.append(("op", ch))
            elif ch == self.epsilon:
                tokens.append(("epsilon", self.epsilon))
            else:
                tokens.append(("literal", ch))

            i += 1

        result = []

        for token in tokens:
            if result:
                prev = result[-1][1]
                curr = token[1]

                prev_can_end = (
                    result[-1][0] in ("literal", "epsilon")
                    or prev in (")", "*", "+", "?")
                )

                curr_can_start = (
                    token[0] in ("literal", "epsilon")
                    or curr == "("
                )

                if prev_can_end and curr_can_start:
                    result.append(("op", "."))

            result.append(token)

        return result

    def regex_to_postfix(self, regex):
        """
        Convert regex notation to postfix.

        In this simulator:
            | means OR / union
            + means positive closure
            * means Kleene closure
            ? means zero or one
            concatenation is represented internally by '.'
        """
        tokens = self.normalize_regex(regex)

        precedence = {
            "|": 1,
            ".": 2,
            "*": 3,
            "+": 3,
            "?": 3
        }

        output = []
        operators = []

        for token_type, token in tokens:
            if token_type in ("literal", "epsilon"):
                output.append((token_type, token))

            elif token == "(":
                operators.append(token)

            elif token == ")":
                found_open = False

                while operators:
                    top = operators.pop()

                    if top == "(":
                        found_open = True
                        break

                    output.append(("op", top))

                if not found_open:
                    raise ValueError("Mismatched parentheses.")

            elif token in ("*", "+", "?"):
                if not output:
                    raise ValueError(
                        f"Operator '{token}' has no preceding expression."
                    )

                output.append(("op", token))

            elif token in ("|", "."):
                while (
                    operators
                    and operators[-1] != "("
                    and precedence[operators[-1]] >= precedence[token]
                ):
                    output.append(("op", operators.pop()))

                operators.append(token)

        while operators:
            top = operators.pop()

            if top == "(":
                raise ValueError("Mismatched parentheses.")

            output.append(("op", top))

        return output

    def new_state(self):
        index = 0

        while f"q{index}" in self.states:
            index += 1

        state = f"q{index}"
        self.states.add(state)
        return state

    def add_nfa_transition(
        self,
        transitions,
        from_state,
        symbol,
        to_state
    ):
        key = (from_state, symbol)

        if key not in transitions:
            transitions[key] = set()

        transitions[key].add(to_state)

    def build_thompson_nfa(self, postfix):
        """Build an epsilon-NFA using Thompson construction."""
        self.states = set()
        transitions = {}
        stack = []

        def make_fragment(start, end):
            return {"start": start, "end": end}

        for token_type, token in postfix:

            if token_type in ("literal", "epsilon"):
                start = self.new_state()
                end = self.new_state()

                self.add_nfa_transition(
                    transitions,
                    start,
                    token,
                    end
                )

                stack.append(make_fragment(start, end))

            elif token == ".":
                if len(stack) < 2:
                    raise ValueError(
                        "Invalid concatenation in regular expression."
                    )

                right = stack.pop()
                left = stack.pop()

                self.add_nfa_transition(
                    transitions,
                    left["end"],
                    self.epsilon,
                    right["start"]
                )

                stack.append(
                    make_fragment(left["start"], right["end"])
                )

            elif token == "|":
                if len(stack) < 2:
                    raise ValueError(
                        "Invalid OR/union in regular expression."
                    )

                right = stack.pop()
                left = stack.pop()

                start = self.new_state()
                end = self.new_state()

                self.add_nfa_transition(
                    transitions,
                    start,
                    self.epsilon,
                    left["start"]
                )

                self.add_nfa_transition(
                    transitions,
                    start,
                    self.epsilon,
                    right["start"]
                )

                self.add_nfa_transition(
                    transitions,
                    left["end"],
                    self.epsilon,
                    end
                )

                self.add_nfa_transition(
                    transitions,
                    right["end"],
                    self.epsilon,
                    end
                )

                stack.append(make_fragment(start, end))

            elif token == "+":
                if not stack:
                    raise ValueError(
                        "Positive closure has no preceding expression."
                    )

                fragment = stack.pop()

                self.add_nfa_transition(
                    transitions,
                    fragment["end"],
                    self.epsilon,
                    fragment["start"]
                )

                stack.append(make_fragment(fragment["start"], fragment["end"]))

            elif token == "*":
                if not stack:
                    raise ValueError(
                        "Kleene star has no preceding expression."
                    )

                fragment = stack.pop()
                start = self.new_state()
                end = self.new_state()

                self.add_nfa_transition(
                    transitions,
                    start,
                    self.epsilon,
                    fragment["start"]
                )

                self.add_nfa_transition(
                    transitions,
                    start,
                    self.epsilon,
                    end
                )

                self.add_nfa_transition(
                    transitions,
                    fragment["end"],
                    self.epsilon,
                    fragment["start"]
                )

                self.add_nfa_transition(
                    transitions,
                    fragment["end"],
                    self.epsilon,
                    end
                )

                stack.append(make_fragment(start, end))

            elif token == "?":
                if not stack:
                    raise ValueError(
                        "Question mark has no preceding expression."
                    )

                fragment = stack.pop()
                start = self.new_state()
                end = self.new_state()

                self.add_nfa_transition(
                    transitions,
                    start,
                    self.epsilon,
                    fragment["start"]
                )

                self.add_nfa_transition(
                    transitions,
                    start,
                    self.epsilon,
                    end
                )

                self.add_nfa_transition(
                    transitions,
                    fragment["end"],
                    self.epsilon,
                    end
                )

                stack.append(make_fragment(start, end))

        if len(stack) != 1:
            raise ValueError("Invalid regular expression.")

        fragment = stack.pop()

        return (
            transitions,
            fragment["start"],
            fragment["end"]
        )

    def epsilon_closure(self, states, transitions):
        closure = set(states)
        stack = list(states)

        while stack:
            state = stack.pop()
            key = (state, self.epsilon)

            for next_state in transitions.get(key, set()):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)

        return closure

    def nfa_to_dfa(
        self,
        nfa_transitions,
        nfa_start,
        nfa_final
    ):
        """Convert the generated Thompson NFA to a complete DFA."""
        alphabet = set(self.alphabet)

        for (_, symbol), _ in nfa_transitions.items():
            if symbol != self.epsilon:
                alphabet.add(symbol)

        start_subset = frozenset(
            self.epsilon_closure(
                {nfa_start},
                nfa_transitions
            )
        )

        dead_subset = frozenset()

        subset_to_name = {
            start_subset: "D0",
            dead_subset: "DEAD"
        }

        name_to_subset = {
            "D0": start_subset,
            "DEAD": dead_subset
        }

        queue = [start_subset]
        dfa_transitions = {}
        dfa_states = {"D0", "DEAD"}
        dfa_finals = set()

        for symbol in sorted(alphabet):
            dfa_transitions[("DEAD", symbol)] = "DEAD"

        counter = 1

        while queue:
            current_subset = queue.pop(0)
            current_name = subset_to_name[current_subset]

            if nfa_final in current_subset:
                dfa_finals.add(current_name)

            for symbol in sorted(alphabet):
                move = set()

                for nfa_state in current_subset:
                    move.update(
                        nfa_transitions.get(
                            (nfa_state, symbol),
                            set()
                        )
                    )

                next_subset = frozenset(
                    self.epsilon_closure(
                        move,
                        nfa_transitions
                    )
                )

                if next_subset not in subset_to_name:
                    new_name = f"D{counter}"
                    counter += 1

                    subset_to_name[next_subset] = new_name
                    name_to_subset[new_name] = next_subset
                    dfa_states.add(new_name)
                    queue.append(next_subset)

                next_name = subset_to_name[next_subset]

                dfa_transitions[
                    (current_name, symbol)
                ] = next_name

        return (
            dfa_states,
            alphabet,
            dfa_transitions,
            "D0",
            dfa_finals,
            name_to_subset
        )

    def format_transition_list(self):
        self.transition_list.delete(0, tk.END)

        if self.automaton_type.get() == "NFA":
            items = sorted(
                self.transitions.keys(),
                key=lambda item: (item[0], item[1])
            )

            for from_state, symbol in items:
                destinations = sorted(
                    self.transitions[(from_state, symbol)]
                )

                for to_state in destinations:
                    self.transition_list.insert(
                        tk.END,
                        f"{from_state} -- {symbol} --> {to_state}"
                    )

        else:
            items = sorted(
                self.transitions.keys(),
                key=lambda item: (item[0], item[1])
            )

            for from_state, symbol in items:
                to_state = self.transitions[
                    (from_state, symbol)
                ]

                self.transition_list.insert(
                    tk.END,
                    f"{from_state} -- {symbol} --> {to_state}"
                )

    # ================================================================
    # CREATE AUTOMATON
    # ================================================================

    def get_user_states(self):
        states_text = self.states_entry.get().strip()

        return {
            state.strip()
            for state in states_text.split(",")
            if state.strip()
        }

    def remap_generated_automaton(
        self,
        generated_states,
        generated_transitions,
        generated_start,
        generated_finals,
        user_states,
        user_start,
        user_finals
    ):
        """
        Use user's state names while preserving the generated language.
        """
        if len(user_states) < len(generated_states):
            raise ValueError(
                f"At least {len(generated_states)} states are required "
                f"for this regular expression. You entered "
                f"{len(user_states)}."
            )

        if user_start not in user_states:
            raise ValueError(
                "Start state must be one of the entered states."
            )

        if not user_finals.issubset(user_states):
            raise ValueError(
                "All final states must be one of the entered states."
            )

        if len(user_finals) != len(generated_finals):
            raise ValueError(
                f"The regular expression generates "
                f"{len(generated_finals)} final state(s), so enter "
                f"exactly that many final state(s)."
            )

        mapping = {
            generated_start: user_start
        }

        for old, new in zip(
            sorted(generated_finals),
            sorted(user_finals)
        ):
            if old in mapping and mapping[old] != new:
                raise ValueError(
                    "Start state and final state selection conflict."
                )

            mapping[old] = new

        remaining_generated = sorted(
            generated_states - set(mapping)
        )

        remaining_user = sorted(
            user_states - set(mapping.values())
        )

        for old, new in zip(
            remaining_generated,
            remaining_user
        ):
            mapping[old] = new

        if self.automaton_type.get() == "DFA":
            mapped = {
                (mapping[a], symbol): mapping[b]
                for (a, symbol), b
                in generated_transitions.items()
            }

            self.dead_state = mapping.get("DEAD")
        else:
            mapped = {
                (mapping[a], symbol): {
                    mapping[x]
                    for x in destinations
                }
                for (a, symbol), destinations
                in generated_transitions.items()
            }

        return (
            set(user_states),
            mapped,
            user_start,
            {
                mapping[x]
                for x in generated_finals
            }
        )

    def build_transition_table(self):
        """Display the complete automaton transition table."""
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        symbols = sorted(self.alphabet)

        if self.automaton_type.get() == "NFA":
            symbols.append(self.epsilon)

        headers = ["State"] + symbols

        for col, header in enumerate(headers):
            tk.Label(
                self.table_frame,
                text=header,
                font=("Arial", 9, "bold"),
                bg="#A8B8A5",
                fg="#774422",
                relief="solid",
                bd=1,
                width=14
            ).grid(
                row=0,
                column=col,
                sticky="nsew"
            )

        for row, state in enumerate(
            sorted(self.states),
            start=1
        ):
            state_text = (
                "→ " if state == self.start_state else ""
            ) + state

            if state in self.final_states:
                state_text += " *"

            if self.automaton_type.get() == "DFA" and state == self.dead_state:
                state_text += " (DEAD)"

            tk.Label(
                self.table_frame,
                text=state_text,
                font=("Arial", 9, "bold"),
                bg="#F8F6F2",
                fg="#774422",
                relief="solid",
                bd=1,
                width=14
            ).grid(
                row=row,
                column=0,
                sticky="nsew"
            )

            for col, symbol in enumerate(
                symbols,
                start=1
            ):
                value = self.transitions.get(
                    (state, symbol),
                    ""
                )

                if self.automaton_type.get() == "NFA":
                    value = (
                        ",".join(sorted(value))
                        if value
                        else "—"
                    )
                else:
                    if value == self.dead_state:
                        value = "DEAD"
                    else:
                        value = value if value else "—"

                tk.Label(
                    self.table_frame,
                    text=value,
                    font=("Consolas", 9),
                    bg="#F8F6F2",
                    fg="#17343B",
                    relief="solid",
                    bd=1,
                    width=14
                ).grid(
                    row=row,
                    column=col,
                    sticky="nsew"
                )

    def create_automaton(self):
        regex = self.regex_entry.get().strip()
        user_states = self.get_user_states()
        alphabet_text = self.alphabet_entry.get().strip()
        user_start = self.start_entry.get().strip()

        user_finals = {
            x.strip()
            for x in self.final_entry.get().split(",")
            if x.strip()
        }

        if not regex:
            messagebox.showerror(
                "Error",
                "Please enter a regular expression."
            )
            return

        if not user_states:
            messagebox.showerror(
                "Error",
                "Please enter the states."
            )
            return

        if not user_start:
            messagebox.showerror(
                "Error",
                "Please enter the start state."
            )
            return

        if not user_finals:
            messagebox.showerror(
                "Error",
                "Please enter at least one final state."
            )
            return

        self.alphabet = {
            x.strip()
            for x in alphabet_text.split(",")
            if x.strip()
        }

        if not self.alphabet:
            messagebox.showerror(
                "Error",
                "Please enter the alphabet."
            )
            return

        try:
            postfix = self.regex_to_postfix(regex)

            (
                nfa_transitions,
                nfa_start,
                nfa_final
            ) = self.build_thompson_nfa(postfix)

            generated_alphabet = {
                symbol
                for (_, symbol)
                in nfa_transitions
                if symbol != self.epsilon
            }

            missing = generated_alphabet - self.alphabet

            if missing:
                raise ValueError(
                    "The alphabet is missing symbol(s) used by "
                    "the regular expression: "
                    + ", ".join(sorted(missing))
                )

            if self.automaton_type.get() == "NFA":
                self.dead_state = None
                generated_states = set(self.states)

                result = self.remap_generated_automaton(
                    generated_states,
                    nfa_transitions,
                    nfa_start,
                    {nfa_final},
                    user_states,
                    user_start,
                    user_finals
                )

            else:
                (
                    dfa_states,
                    _,
                    dfa_transitions,
                    dfa_start,
                    dfa_finals,
                    _
                ) = self.nfa_to_dfa(
                    nfa_transitions,
                    nfa_start,
                    nfa_final
                )

                result = self.remap_generated_automaton(
                    dfa_states,
                    dfa_transitions,
                    dfa_start,
                    dfa_finals,
                    user_states,
                    user_start,
                    user_finals
                )

            (
                self.states,
                self.transitions,
                self.start_state,
                self.final_states
            ) = result

            self.format_transition_list()
            self.build_transition_table()
            self.update_nfa_section()
            self.draw_automaton_diagram()

            self.automaton_info.config(
                text=(
                    f"{self.automaton_type.get()} generated from regex | "
                    f"States: {len(self.states)} | "
                    f"Alphabet: {{{', '.join(sorted(self.alphabet))}}} | "
                    f"Start: {self.start_state} | "
                    f"Final: "
                    f"{{{', '.join(sorted(self.final_states))}}}"
                )
            )

            self.result_label.config(
                text="Result will appear here"
            )

            self.path_label.config(
                text="Transition Path:"
            )

            self._create_empty_test_table()

            self.canvas.yview_moveto(0)

            messagebox.showinfo(
                "Success",
                f"{self.automaton_type.get()} created successfully "
                f"from the regular expression!"
            )

        except ValueError as error:
            messagebox.showerror(
                "Invalid Input",
                str(error)
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Could not create automaton:\n{error}"
            )

    # ================================================================
    # GUI AUTOMATON DIAGRAM
    # ================================================================

    def draw_automaton_diagram(self):
        """
        Draw a clean DFA/NFA diagram.

        Only the visual layout is changed.
        DFA/NFA generation and simulation logic remain unchanged.
        """

        canvas = self.diagram_canvas
        canvas.delete("all")

        if not self.states:
            canvas.configure(scrollregion=(0, 0, 650, 300))
            canvas.create_text(
                325,
                150,
                text="Create an automaton to display its diagram.",
                font=("Arial", 11, "italic"),
                fill="#17343B"
            )
            return

        # ============================================================
        # STATE ORDER
        # ============================================================

        ordered_states = [self.start_state] + sorted(
            [s for s in self.states if s != self.start_state]
        )

        radius = 30

        left_margin = 75
        state_y = 170
        x_gap = 155

        positions = {
            state: (
                left_margin + i * x_gap,
                state_y
            )
            for i, state in enumerate(ordered_states)
        }

        diagram_width = max(
            700,
            left_margin
            + (len(ordered_states) - 1) * x_gap
            + 100
        )

        diagram_height = 380

        canvas.configure(
            scrollregion=(
                0,
                0,
                diagram_width,
                diagram_height
            )
        )

        # ============================================================
        # GROUP TRANSITIONS
        # ============================================================

        grouped = {}

        for (src, symbol), destinations in self.transitions.items():

            if self.automaton_type.get() == "NFA":
                destinations = set(destinations)
            else:
                destinations = {destinations}

            for dst in destinations:

                key = (src, dst)

                if key not in grouped:
                    grouped[key] = []

                grouped[key].append(str(symbol))

        for key in grouped:
            grouped[key] = sorted(
                list(dict.fromkeys(grouped[key]))
            )

        # ============================================================
        # HELPER FUNCTIONS
        # ============================================================

        def get_border_point(x1, y1, x2, y2):

            dx = x2 - x1
            dy = y2 - y1

            distance = max(
                (dx * dx + dy * dy) ** 0.5,
                1
            )

            return (
                x1 + (dx / distance) * radius,
                y1 + (dy / distance) * radius
            )

        def draw_label(text, x, y):

            text_width = max(
                28,
                len(text) * 5.5 + 14
            )

            canvas.create_rectangle(
                x - text_width / 2,
                y - 11,
                x + text_width / 2,
                y + 11,
                fill="#F8F6F2",
                outline="#D0D0D0",
                width=1
            )

            canvas.create_text(
                x,
                y,
                text=text,
                font=("Arial", 10, "bold"),
                fill="#17343B"
            )

        def draw_straight_arrow(start, end):

            canvas.create_line(
                start[0],
                start[1],
                end[0],
                end[1],
                fill="#2C7180",
                width=2,
                arrow=tk.LAST,
                arrowshape=(10, 12, 5)
            )

        def draw_curve(start, control, end):

            points = []

            for k in range(41):

                t = k / 40.0
                u = 1.0 - t

                x = (
                    u * u * start[0]
                    + 2 * u * t * control[0]
                    + t * t * end[0]
                )

                y = (
                    u * u * start[1]
                    + 2 * u * t * control[1]
                    + t * t * end[1]
                )

                points.extend([x, y])

            canvas.create_line(
                *points,
                fill="#2C7180",
                width=2,
                arrow=tk.LAST,
                arrowshape=(10, 12, 5)
            )

        # ============================================================
        # TRANSITION DRAWING
        # ============================================================

        for (src, dst), symbols in sorted(
            grouped.items(),
            key=lambda item: (
                ordered_states.index(item[0][0]),
                ordered_states.index(item[0][1])
            )
        ):

            if src not in positions or dst not in positions:
                continue

            x1, y1 = positions[src]
            x2, y2 = positions[dst]

            label = ", ".join(symbols)

            # ========================================================
            # SELF LOOP
            # ========================================================

            if src == dst:

                loop_width = 58
                loop_height = 55

                left = x1 - loop_width / 2
                right = x1 + loop_width / 2

                top = y1 - radius - loop_height
                bottom = y1 - radius + 4

                canvas.create_arc(
                    left,
                    top,
                    right,
                    bottom,
                    start=20,
                    extent=320,
                    style=tk.ARC,
                    outline="#2C7180",
                    width=2
                )

                canvas.create_line(
                    x1 + 23,
                    y1 - radius - 12,
                    x1 + 16,
                    y1 - radius - 4,
                    fill="#2C7180",
                    width=2,
                    arrow=tk.LAST,
                    arrowshape=(9, 11, 5)
                )

                draw_label(
                    label,
                    x1,
                    top - 15
                )

                continue

            # ========================================================
            # STATE INDEX
            # ========================================================

            i = ordered_states.index(src)
            j = ordered_states.index(dst)

            distance = abs(j - i)

            start = get_border_point(
                x1,
                y1,
                x2,
                y2
            )

            end = get_border_point(
                x2,
                y2,
                x1,
                y1
            )

            # ========================================================
            # NEIGHBOURING STATES
            # ========================================================

            if distance == 1:

                reverse_exists = (
                    (dst, src) in grouped
                )

                # ----------------------------------------------------
                # ONLY ONE DIRECTION
                # ----------------------------------------------------

                if not reverse_exists:

                    draw_straight_arrow(
                        start,
                        end
                    )

                    label_x = (
                        start[0] + end[0]
                    ) / 2

                    label_y = y1 - 25

                    draw_label(
                        label,
                        label_x,
                        label_y
                    )

                # ----------------------------------------------------
                # BOTH DIRECTIONS
                # ----------------------------------------------------

                else:

                    if i < j:
                        curve_y = y1 - 55
                    else:
                        curve_y = y1 + 55

                    control = (
                        (start[0] + end[0]) / 2,
                        curve_y
                    )

                    draw_curve(
                        start,
                        control,
                        end
                    )

                    label_x = control[0]

                    if curve_y < y1:
                        label_y = curve_y - 15
                    else:
                        label_y = curve_y + 15

                    draw_label(
                        label,
                        label_x,
                        label_y
                    )

                continue

            # ========================================================
            # LONG TRANSITIONS
            # ========================================================

            if i < j:
                direction = -1
            else:
                direction = 1

            lane = (
                75
                + min(distance - 2, 5) * 32
            )

            mid_x = (
                start[0] + end[0]
            ) / 2

            control = (
                mid_x,
                y1 + direction * lane
            )

            draw_curve(
                start,
                control,
                end
            )

            label_x = mid_x

            if direction < 0:
                label_y = control[1] - 15
            else:
                label_y = control[1] + 15

            draw_label(
                label,
                label_x,
                label_y
            )

        # ============================================================
        # START ARROW
        # ============================================================

        sx, sy = positions[self.start_state]

        canvas.create_line(
            sx - 55,
            sy,
            sx - radius,
            sy,
            fill="#774422",
            width=2,
            arrow=tk.LAST,
            arrowshape=(10, 12, 5)
        )

        # ============================================================
        # DRAW STATES LAST
        # ============================================================

        for state in ordered_states:

            x, y = positions[state]

            if (
                self.automaton_type.get() == "DFA"
                and state == self.dead_state
            ):
                fill_color = "#D0D0D4"
            else:
                fill_color = "#A8B8A5"

            canvas.create_oval(
                x - radius,
                y - radius,
                x + radius,
                y + radius,
                fill=fill_color,
                outline="#174A55",
                width=2
            )

            if state in self.final_states:

                canvas.create_oval(
                    x - radius + 6,
                    y - radius + 6,
                    x + radius - 6,
                    y + radius - 6,
                    outline="#174A55",
                    width=2
                )

            canvas.create_text(
                x,
                y,
                text=state,
                font=("Arial", 10, "bold"),
                fill="#17343B"
            )

            if (
                self.automaton_type.get() == "DFA"
                and state == self.dead_state
            ):

                canvas.create_text(
                    x,
                    y + radius + 18,
                    text="DEAD",
                    font=("Arial", 8, "bold"),
                    fill="#774422"
                )

    def check_string(self):
        if not self.start_state:
            messagebox.showerror(
                "Error",
                "First create the automaton."
            )
            return

        test_string = self.test_entry.get().strip()

        self._clear_test_table()

        if self.automaton_type.get() == "DFA":
            self.check_dfa(test_string)
        else:
            self.check_nfa(test_string)

        self.root.after(
            50,
            self._scroll_to_test_result
        )

    def check_dfa(self, string):
        current_state = self.start_state
        path = [current_state]

        rows = [
            (
                0,
                "START",
                "—",
                current_state
            )
        ]

        for step, symbol in enumerate(
            string,
            start=1
        ):
            key = (current_state, symbol)

            if key not in self.transitions:
                rows.append(
                    (
                        step,
                        symbol,
                        current_state,
                        "NO TRANSITION"
                    )
                )

                self.build_test_transition_table(rows)

                self.result_label.config(
                    text="REJECTED"
                )

                self.path_label.config(
                    text="Transition Path: "
                    + " → ".join(path)
                )

                return

            next_state = self.transitions[key]

            rows.append(
                (
                    step,
                    symbol,
                    current_state,
                    next_state
                )
            )

            current_state = next_state
            path.append(current_state)

        self.build_test_transition_table(rows)

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

    def check_nfa(self, string):
        current_states = self.epsilon_closure(
            {self.start_state},
            self.transitions
        )

        path = [
            self.format_state_set(current_states)
        ]

        rows = [
            (
                0,
                "START",
                "—",
                self.format_state_set(
                    current_states
                )
            )
        ]

        for step, symbol in enumerate(
            string,
            start=1
        ):
            next_states = set()

            for state in current_states:
                key = (state, symbol)

                if key in self.transitions:
                    next_states.update(
                        self.transitions[key]
                    )

            if not next_states:
                rows.append(
                    (
                        step,
                        symbol,
                        self.format_state_set(
                            current_states
                        ),
                        "NO TRANSITION"
                    )
                )

                self.build_test_transition_table(rows)

                self.result_label.config(
                    text="REJECTED"
                )

                self.path_label.config(
                    text="Transition Path: "
                    + " → ".join(path)
                )

                return

            previous_states = current_states

            current_states = self.epsilon_closure(
                next_states,
                self.transitions
            )

            current_text = self.format_state_set(
                current_states
            )

            rows.append(
                (
                    step,
                    symbol,
                    self.format_state_set(
                        previous_states
                    ),
                    current_text
                )
            )

            path.append(current_text)

        self.build_test_transition_table(rows)

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

    # ================================================================
    # TEST STRING TRANSITION TABLE
    # ================================================================

    def _clear_test_table(self):
        for widget in self.test_table_frame.winfo_children():
            widget.destroy()

    def _create_empty_test_table(self):
        self._clear_test_table()

        headers = [
            "Step",
            "Input",
            "From State(s)",
            "To State(s)"
        ]

        for col, header in enumerate(headers):
            tk.Label(
                self.test_table_frame,
                text=header,
                font=("Arial", 9, "bold"),
                bg="#A8B8A5",
                fg="#774422",
                relief="solid",
                bd=1,
                width=18
            ).grid(
                row=0,
                column=col,
                sticky="nsew"
            )

        tk.Label(
            self.test_table_frame,
            text="Enter a test string and click Check String.",
            font=("Arial", 9, "italic"),
            bg="#F8F6F2",
            fg="#17343B",
            relief="solid",
            bd=1,
            width=72
        ).grid(
            row=1,
            column=0,
            columnspan=4,
            sticky="nsew"
        )

    def build_test_transition_table(self, rows):
        """
        Display only the transitions actually used while processing
        the user's TEST STRING.
        """
        self._clear_test_table()

        headers = [
            "Step",
            "Input",
            "From State(s)",
            "To State(s)"
        ]

        for col, header in enumerate(headers):
            tk.Label(
                self.test_table_frame,
                text=header,
                font=("Arial", 9, "bold"),
                bg="#A8B8A5",
                fg="#774422",
                relief="solid",
                bd=1,
                width=18
            ).grid(
                row=0,
                column=col,
                sticky="nsew"
            )

        for row_index, data in enumerate(
            rows,
            start=1
        ):
            for col_index, value in enumerate(data):
                tk.Label(
                    self.test_table_frame,
                    text=str(value),
                    font=("Consolas", 9),
                    bg="#F8F6F2",
                    fg="#17343B",
                    relief="solid",
                    bd=1,
                    width=18
                ).grid(
                    row=row_index,
                    column=col_index,
                    sticky="nsew"
                )

        self.test_table_frame.update_idletasks()

    def _scroll_to_test_result(self):
        """Scroll down so the test controls/result remain easy to reach."""
        self.canvas.update_idletasks()

        bbox = self.canvas.bbox("all")

        if not bbox:
            return

        self.canvas.yview_moveto(1.0)

    def format_state_set(self, states):
        return "{" + ",".join(sorted(states)) + "}"


# ------------------------------------------------
# MAIN PROGRAM
# ------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = AutomataSimulator(root)
    root.mainloop()