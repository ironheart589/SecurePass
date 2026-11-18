# SecurePass: Password Generator & Strength Checker

**Assignment:** Problem 8 — Password Generator and Strength Checker  
**Course Code:** CS371  
**Academic Year:** 3rd Year, B.Tech  
**Institution:** National Institute of Technology, Meghalaya  

---

### Team Members
| Roll Number | Name |
| :--- | :--- |
| `[Roll No. B24CS018]` | `[ANKITA SINGH]` |
| `[Roll No. B24CS016]` | `[BIBHUTI KUMAR MISHRA]` |
| `[Roll No. B24EC003]` | `[SHIVAM DAS]` |
| `[Roll No. B24EC020]` | `[BOILLA AKSHITH REDDY]` |

---

## Overview
**SecurePass** is an offline desktop security utility built in Python for Problem 8. Designed with a modern dark-themed interface using **Tkinter**, the application combines cryptographically secure random password generation with real-time, regex-driven password strength evaluation—all powered strictly by Python's built-in standard libraries.

---

## Core Features

### 1. Password Generator
* **Custom Length Control:** Supports any length between **4 and 64 characters** with strict numeric input validation.
* **Character Variety Toggles:** Checkboxes to include **Uppercase Letters (`A-Z`)**, **Digits (`0-9`)**, and **Special Characters (`!@#$...`)** alongside mandatory lowercase letters.
* **Guaranteed Diversity:** Ensures every selected character category appears at least once in the generated output before securely shuffling the final string.
* **One-Click Copy:** Copies the generated password directly to the system clipboard with instant confirmation.

### 2. Live Strength Checker
* **Instant Evaluation (`<KeyRelease>`):** Analyzes passwords automatically on every keystroke without requiring a separate submit button.
* **Progressive Disclosure UI:** Keeps metric cards and breakdown panels hidden when the input box is empty, revealing them dynamically once typing begins.
* **Detailed Metrics & Breakdown:** Displays live **Length** and **Character Variety (`X / 4`)** cards, paired with real-time status checks (`✔` / `✘`) for lowercase, uppercase, digits, and symbols.
* **Actionable Feedback:** Classifies passwords into **Weak**, **Medium**, or **Strong** with color-coded indicators and tailored improvement tips.

---

## Quick Start & Execution

### Prerequisites
* **Python 3.8 or newer**
* No external third-party packages (`pip install`) are required. All modules (`tkinter`, `secrets`, `re`, `string`) come pre-installed with Python. *(Note: On some Linux distributions, you may need `sudo apt install python3-tk`.)*

### Running the Application
1. Ensure `password.py` is saved on your local machine.
2. Open your terminal or command prompt in the project directory and run:
   ```bash
   python password.py
   ```
   *(Use `python3 password.py` on macOS/Linux if `python` points to Python 2.)*

---

## Architecture & How It Works

The entire application is structured cleanly into modular functions inside `password.py`:

* **Cryptographic Generation (`generate_password`):**  
  Instead of Python's standard `random` module (which is pseudo-random and predictable), SecurePass uses **`secrets.choice()`** to pick characters securely from `string` constants. After selecting one mandatory character per enabled category and filling the remaining slots, **`secrets.SystemRandom().shuffle()`** randomizes character positions so required characters are never clustered at the start.
* **Clipboard Operations (`copy_password`):**  
  Interfaces directly with the OS clipboard through Tkinter's root window using `root.clipboard_clear()`, `root.clipboard_append()`, and `root.update()` to persist copied strings reliably.
* **Pattern Matching & Scoring (`evaluate_strength`):**  
  Uses Regular Expressions (**`re.search()`**) to scan input against four rules (`[a-z]`, `[A-Z]`, `[0-9]`, and `[^a-zA-Z0-9]`). Passwords are graded using clear thresholds:
  * **Weak:** Length `< 8` OR character variety `<= 2`
  * **Medium:** Length `>= 8` with `3+` character types (or `12+` with `3` types)
  * **Strong:** Length `>= 12` AND all `4` character types present
* **Single-Window Navigation (`show_generator` / `show_checker`):**  
  Uses `pack()` and `pack_forget()` to switch seamlessly between the Generator view and Strength Checker view within a single fixed-size window (`540x650`).

---

## Scope & Limitations
* **Offline Utility:** Runs locally on the host machine; passwords are never stored on disk, logged, or transmitted over a network.
* **Rule-Based Evaluation:** Strength scoring relies on structural complexity (length and character diversity) rather than external leaked-password dictionaries or entropy databases.

---

## Quick Reference Summary
* **Entry Point:** `python password.py`
* **Dependencies:** Built-in Python Standard Library only (`tkinter`, `secrets`, `re`, `string`)
* **Default View:** Opens on the **Generator** tab (`12` characters, all character options enabled)
