# DFA / NFA Simulator

A Python-based desktop application for generating, visualizing, and testing **Deterministic Finite Automata (DFA)** and **Non-Deterministic Finite Automata (NFA)** from regular expressions.

This project is developed as an educational tool for students studying **Theory of Computation, Formal Languages, Regular Expressions, DFA, and NFA**.

---

## 📌 Project Overview

Understanding the relationship between Regular Expressions, NFA, and DFA can be difficult when working only with theoretical representations.

The **DFA / NFA Simulator** provides an interactive graphical interface where users can:

- Enter a regular expression
- Define the alphabet
- Define states
- Select DFA or NFA
- Specify the start state
- Specify final states
- Generate the automaton
- View the automaton transitions
- View the complete transition table
- Enter a test string
- Check whether the string is accepted or rejected
- View the transition path followed by the test string
- View a separate test-string state transition table

The application is designed to make finite automata concepts easier to understand through practical experimentation.

---

## 🎯 Objectives

The main objectives of this project are:

1. To develop an interactive simulator for DFA and NFA.
2. To provide a graphical interface for entering automaton information.
3. To generate automata from regular expressions.
4. To display the generated automaton's transition table.
5. To test user-provided strings against the generated automaton.
6. To display the step-by-step transition path of the tested string.
7. To provide an educational platform for understanding finite automata.

---

## ✨ Features

### Regular Expression Processing

The application accepts regular expressions containing supported operators such as:

- `+` → OR / Union
- `*` → Kleene Closure
- `?` → Optional
- `()` → Grouping
- Concatenation is implicit

Example:

```text
ab*
