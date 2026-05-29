#!/usr/bin/env python3
"""SAP Interview Prep — Interactive Study Tool for macOS terminal."""

import json
import os
import sys
import time
import textwrap
from pathlib import Path
from typing import Any

# ── Terminal colour helpers (no external deps) ──────────────────────────────

ESC = "\033["
RESET       = f"{ESC}0m"
BOLD        = f"{ESC}1m"
DIM         = f"{ESC}2m"
ITALIC      = f"{ESC}3m"
UNDERLINE   = f"{ESC}4m"

BLACK   = f"{ESC}30m";  BG_BLACK   = f"{ESC}40m"
RED     = f"{ESC}31m";  BG_RED     = f"{ESC}41m"
GREEN   = f"{ESC}32m";  BG_GREEN   = f"{ESC}42m"
YELLOW  = f"{ESC}33m";  BG_YELLOW  = f"{ESC}43m"
BLUE    = f"{ESC}34m";  BG_BLUE    = f"{ESC}44m"
MAGENTA = f"{ESC}35m";  BG_MAGENTA = f"{ESC}45m"
CYAN    = f"{ESC}36m";  BG_CYAN    = f"{ESC}46m"
WHITE   = f"{ESC}37m";  BG_WHITE   = f"{ESC}47m"

B_RED     = f"{ESC}91m"
B_GREEN   = f"{ESC}92m"
B_YELLOW  = f"{ESC}93m"
B_BLUE    = f"{ESC}94m"
B_MAGENTA = f"{ESC}95m"
B_CYAN    = f"{ESC}96m"
B_WHITE   = f"{ESC}97m"

TOPIC_COLORS = {
    "SAP MM":   (BLUE,    BG_BLUE),
    "SAP ECC":  (GREEN,   BG_GREEN),
    "SAP HANA": (MAGENTA, BG_MAGENTA),
}


def clear():
    os.system("clear" if os.name != "nt" else "cls")


def width() -> int:
    try:
        return os.get_terminal_size().columns
    except Exception:
        return 80


def hr(char: str = "─", color: str = DIM) -> None:
    print(f"{color}{char * width()}{RESET}")


def banner(text: str, fg: str = B_WHITE, bg: str = BG_BLUE) -> None:
    w = width()
    pad = (w - len(text) - 4) // 2
    print(f"\n{bg}{fg}{BOLD}{' ' * pad}  {text}  {' ' * pad}{RESET}\n")


def title_box(text: str, color: str = B_CYAN) -> None:
    w = width()
    line = "╔" + "═" * (w - 2) + "╗"
    blank = "║" + " " * (w - 2) + "║"
    pad = (w - 2 - len(text)) // 2
    content = "║" + " " * pad + f"{BOLD}{color}{text}{RESET}" + " " * (w - 2 - pad - len(text)) + "║"
    bottom = "╚" + "═" * (w - 2) + "╝"
    print(f"{color}{line}{RESET}")
    print(f"{color}{blank}{RESET}")
    print(content)
    print(f"{color}{blank}{RESET}")
    print(f"{color}{bottom}{RESET}")


def section_header(text: str, icon: str, color: str) -> None:
    print(f"\n{color}{BOLD}{icon}  {text}{RESET}")
    print(f"{color}{'─' * (len(text) + 5)}{RESET}")


def prompt(text: str, color: str = B_YELLOW) -> str:
    return input(f"{color}{BOLD}{text}{RESET} ").strip()


def pause(msg: str = "Press Enter to continue...") -> None:
    input(f"\n{DIM}{msg}{RESET}")


def slow_print(text: str, delay: float = 0.012, color: str = "") -> None:
    for ch in text:
        sys.stdout.write(f"{color}{ch}{RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    print()


# ── Data loading ────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).parent

STUDY_GUIDES = {
    "SAP MM": BASE_DIR.parent / "study_guides" / "sap_mm_guide.md",
    "SAP ECC": BASE_DIR.parent / "study_guides" / "sap_ecc_guide.md",
    "SAP HANA": BASE_DIR.parent / "study_guides" / "sap_hana_guide.md",
}

QUESTION_FILES = {
    "SAP MM": BASE_DIR / "questions" / "mm_questions.json",
    "SAP ECC": BASE_DIR / "questions" / "ecc_questions.json",
    "SAP HANA": BASE_DIR / "questions" / "hana_questions.json",
}

PROGRESS_FILE = BASE_DIR / ".progress.json"


def load_questions(topic: str) -> list[dict]:
    path = QUESTION_FILES[topic]
    if path.exists():
        return json.loads(path.read_text())
    return []


def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        try:
            return json.loads(PROGRESS_FILE.read_text())
        except Exception:
            pass
    return {"quiz_scores": {}, "study_sections": {}, "total_sessions": 0}


def save_progress(prog: dict) -> None:
    PROGRESS_FILE.write_text(json.dumps(prog, indent=2))


# ── Study Guide Reader ──────────────────────────────────────────────────────

def parse_sections(md_path: Path) -> list[dict]:
    """Split markdown into sections by ## headings."""
    sections: list[dict] = []
    current: dict | None = None
    text = md_path.read_text(encoding="utf-8")
    for line in text.split("\n"):
        if line.startswith("## "):
            if current:
                sections.append(current)
            current = {"title": line[3:].strip(), "lines": []}
        elif current is not None:
            current["lines"].append(line)
    if current:
        sections.append(current)
    return sections


def render_section(section: dict, color: str, topic: str) -> None:
    clear()
    section_header(section["title"], "📖", color)
    print()
    w = width() - 4
    in_code = False
    for line in section["lines"]:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            if in_code:
                print(f"{DIM}{'─' * w}{RESET}")
            else:
                print(f"{DIM}{'─' * w}{RESET}")
            continue
        if in_code:
            print(f"  {CYAN}{line}{RESET}")
            continue
        if stripped.startswith("### "):
            print(f"\n{BOLD}{B_YELLOW}{stripped[4:]}{RESET}")
            print(f"{YELLOW}{'─' * min(len(stripped) - 4, w)}{RESET}")
        elif stripped.startswith("#### "):
            print(f"\n{BOLD}{stripped[5:]}{RESET}")
        elif stripped.startswith("| ") or ("|" in stripped and stripped.startswith("|")):
            cells = [c.strip() for c in stripped.split("|") if c.strip()]
            if cells:
                # Check if separator row
                if all(set(c.replace(":", "").replace("-", "")) == set() or c.replace(":", "").replace("-", "") == "" for c in cells):
                    continue
                row = "  "
                for c in cells:
                    row += f"{c:<22}"
                print(f"{DIM}{row}{RESET}")
        elif stripped.startswith("> **Q:"):
            text = stripped.lstrip("> ").strip().replace("**", "")
            print(f"\n{BG_BLUE}{B_WHITE}{BOLD}  Q: {text[3:]}{RESET}")
        elif stripped.startswith("> **A:") or stripped.startswith("> A:"):
            text = stripped.lstrip("> ").replace("**", "").strip()
            wrapped = textwrap.wrap(text, width=w - 4)
            print(f"{GREEN}{ITALIC}  Answer: {RESET}")
            for wl in wrapped:
                print(f"  {GREEN}{wl}{RESET}")
        elif stripped.startswith("> "):
            text = stripped.lstrip("> ").replace("**Q:", "Q:").replace("**A:", "A:").replace("**", "")
            if text.startswith("Q:"):
                print(f"\n{BG_BLUE}{B_WHITE}{BOLD}  {text}{RESET}")
            elif text.startswith("A:"):
                wrapped = textwrap.wrap(text, width=w - 4)
                for wl in wrapped:
                    print(f"  {GREEN}{wl}{RESET}")
            else:
                wrapped = textwrap.wrap(text, width=w - 4)
                for wl in wrapped:
                    print(f"  {ITALIC}{wl}{RESET}")
        elif stripped.startswith("- ") or stripped.startswith("* "):
            text = stripped[2:].replace("**", "")
            wrapped = textwrap.wrap(text, width=w - 6)
            for i, wl in enumerate(wrapped):
                prefix = "  • " if i == 0 else "    "
                print(f"{color}{prefix}{RESET}{wl}")
        elif stripped.startswith("  - ") or stripped.startswith("  * "):
            text = stripped[4:].replace("**", "")
            print(f"     {DIM}  - {text}{RESET}")
        elif stripped.startswith("---"):
            print(f"\n{DIM}{'─' * w}{RESET}\n")
        elif stripped == "":
            print()
        else:
            text = stripped.replace("**", "").replace("*", "")
            wrapped = textwrap.wrap(text, width=w)
            for wl in wrapped:
                print(wl)


def study_mode(topic: str, prog: dict) -> None:
    color, _ = TOPIC_COLORS[topic]
    md_path = STUDY_GUIDES[topic]
    if not md_path.exists():
        print(f"{RED}Study guide not found: {md_path}{RESET}")
        pause()
        return

    sections = parse_sections(md_path)
    if not sections:
        print(f"{RED}No sections found in guide.{RESET}")
        pause()
        return

    idx = 0
    while True:
        section = sections[idx]
        render_section(section, color, topic)

        total = len(sections)
        print(f"\n{DIM}Section {idx + 1} of {total}  |  {topic}{RESET}")
        hr("─", DIM)
        print(f"  {B_YELLOW}[n]{RESET} Next   {B_YELLOW}[p]{RESET} Previous   "
              f"{B_YELLOW}[g]{RESET} Go to section   {B_YELLOW}[q]{RESET} Back to menu")

        choice = prompt("→").lower()
        if choice in ("n", "") and idx < total - 1:
            idx += 1
        elif choice == "p" and idx > 0:
            idx -= 1
        elif choice == "g":
            print(f"\n{BOLD}Available sections:{RESET}")
            for i, s in enumerate(sections):
                print(f"  {DIM}{i + 1:>2}.{RESET} {s['title']}")
            raw = prompt("Enter section number →")
            try:
                new_idx = int(raw) - 1
                if 0 <= new_idx < total:
                    idx = new_idx
            except ValueError:
                pass
        elif choice == "q":
            break
        else:
            print(f"{DIM}At end of guide.{RESET}") if idx == total - 1 else None
            if idx == total - 1:
                pause("You've reached the end. Press Enter to go back to menu...")
                break


# ── Quiz Mode ───────────────────────────────────────────────────────────────

def run_quiz(topic: str, prog: dict) -> None:
    color, _ = TOPIC_COLORS[topic]
    questions = load_questions(topic)
    if not questions:
        print(f"{RED}No questions found for {topic}.{RESET}")
        pause()
        return

    clear()
    title_box(f"QUIZ MODE — {topic}", color)
    print(f"\n  {DIM}Total questions: {len(questions)}{RESET}")
    print(f"  Choose a mode:")
    print(f"    {B_YELLOW}[1]{RESET} Full Quiz ({len(questions)} questions)")
    print(f"    {B_YELLOW}[2]{RESET} Quick Quiz (10 random questions)")
    print(f"    {B_YELLOW}[3]{RESET} Difficulty filter")
    print(f"    {B_YELLOW}[q]{RESET} Back")

    mode = prompt("→").strip()
    if mode == "q":
        return
    elif mode == "2":
        import random
        quiz_qs = random.sample(questions, min(10, len(questions)))
    elif mode == "3":
        print(f"\n  {B_YELLOW}[1]{RESET} Beginner   {B_YELLOW}[2]{RESET} Intermediate   {B_YELLOW}[3]{RESET} Advanced")
        diff_choice = prompt("→").strip()
        diff_map = {"1": "beginner", "2": "intermediate", "3": "advanced"}
        diff = diff_map.get(diff_choice, "beginner")
        quiz_qs = [q for q in questions if q.get("difficulty") == diff]
        if not quiz_qs:
            print(f"{RED}No questions found for that difficulty.{RESET}")
            pause()
            return
    else:
        quiz_qs = questions

    # Run the quiz
    score = 0
    wrong: list[dict] = []

    for i, q in enumerate(quiz_qs):
        clear()
        section_header(f"Question {i + 1} / {len(quiz_qs)}", "❓", color)
        print(f"  {DIM}Topic: {q.get('topic', '')}  |  Difficulty: {q.get('difficulty', '').upper()}{RESET}\n")

        # Question text
        q_text = textwrap.fill(q["question"], width=width() - 4)
        print(f"  {BOLD}{q_text}{RESET}\n")

        # Options
        for opt in q["options"]:
            print(f"  {color}{opt}{RESET}")

        print()
        user_ans = prompt("Your answer (A/B/C/D) →").upper()
        correct_ans = q["answer"].upper()

        if user_ans == correct_ans:
            score += 1
            print(f"\n  {B_GREEN}{BOLD}✓ CORRECT!{RESET}")
        else:
            wrong.append(q)
            print(f"\n  {B_RED}{BOLD}✗ INCORRECT{RESET}")
            print(f"  {DIM}Correct answer: {correct_ans}{RESET}")

        # Explanation
        print(f"\n  {B_YELLOW}Explanation:{RESET}")
        explanation = textwrap.fill(q.get("explanation", ""), width=width() - 6)
        for line in explanation.split("\n"):
            print(f"    {line}")

        if i < len(quiz_qs) - 1:
            pause("Press Enter for next question...")

    # Results
    clear()
    pct = int(score / len(quiz_qs) * 100)
    title_box("QUIZ RESULTS", color)

    if pct >= 80:
        grade_color = B_GREEN
        grade = "Excellent! Interview-ready on this topic."
        medal = "🏆"
    elif pct >= 60:
        grade_color = B_YELLOW
        grade = "Good. Review the sections you missed."
        medal = "📈"
    else:
        grade_color = B_RED
        grade = "Needs more study. Go back to the study guide."
        medal = "📚"

    print(f"\n  {medal}  Score: {grade_color}{BOLD}{score} / {len(quiz_qs)}  ({pct}%){RESET}\n")
    print(f"  {DIM}{grade}{RESET}\n")

    # Save score
    key = f"{topic}"
    if key not in prog["quiz_scores"]:
        prog["quiz_scores"][key] = []
    prog["quiz_scores"][key].append(pct)
    save_progress(prog)

    if wrong:
        print(f"  {B_RED}{BOLD}Questions to review ({len(wrong)}):{RESET}")
        for wq in wrong:
            print(f"    {DIM}• {wq['question'][:80]}...{RESET}")
            print(f"      Correct: {BOLD}{wq['answer']}{RESET} — {wq.get('explanation', '')[:80]}")
            print()

    pause("Press Enter to continue...")


# ── Progress Dashboard ───────────────────────────────────────────────────────

def show_progress(prog: dict) -> None:
    clear()
    title_box("YOUR PROGRESS DASHBOARD", B_CYAN)
    print()

    for topic, (color, _) in TOPIC_COLORS.items():
        scores = prog["quiz_scores"].get(topic, [])
        if scores:
            avg = sum(scores) / len(scores)
            best = max(scores)
            last = scores[-1]
            bar_fill = int(avg / 100 * 30)
            bar = "█" * bar_fill + "░" * (30 - bar_fill)
            print(f"  {color}{BOLD}{topic}{RESET}")
            print(f"  {color}{bar}{RESET}  {avg:.0f}% avg")
            print(f"  {DIM}Attempts: {len(scores)}  |  Best: {best}%  |  Last: {last}%{RESET}")
        else:
            print(f"  {color}{BOLD}{topic}{RESET}")
            print(f"  {DIM}No quiz attempts yet{RESET}")
        print()

    pause()


# ── Flashcard Mode ──────────────────────────────────────────────────────────

FLASHCARDS: dict[str, list[dict]] = {
    "SAP MM": [
        {"q": "What does GR/IR stand for?", "a": "Goods Receipt / Invoice Receipt — a clearing account that bridges inventory and payables."},
        {"q": "Movement Type for GR against PO?", "a": "101 (standard GR). 102 = Reversal. 103 = GR into Blocked Stock."},
        {"q": "Transaction to view Stock Overview?", "a": "MMBE — shows all stock types across all plants/SLs for a material."},
        {"q": "What is ERS?", "a": "Evaluated Receipt Settlement — auto-creates vendor invoices from GR data. Run via MRRL."},
        {"q": "SPRO path for Account Determination?", "a": "MM > Valuation > Account Determination > Configure Automatic Postings (OBYC)."},
        {"q": "What is a Purchasing Info Record (PIR)?", "a": "Stores price/delivery conditions for a vendor-material combination. Created via ME11."},
        {"q": "Which table stores PO item data?", "a": "EKPO — Purchasing Document Item. EKKO = header, EKBE = history."},
        {"q": "What transaction settles consignment liabilities?", "a": "MRKO — settles all consumed consignment and pipeline quantities with vendors."},
        {"q": "Difference between MAP and Standard Price?", "a": "MAP updates automatically with each GR (V). Standard Price is fixed and differences go to price difference account (S)."},
        {"q": "MRP type for demand-driven planning?", "a": "PD — standard MRP. Creates planned orders or PRs based on requirements from sales orders, production, etc."},
    ],
    "SAP ECC": [
        {"q": "What is the Enqueue work process?", "a": "Manages SAP application-level locks. SM12 shows active locks."},
        {"q": "Transaction for Transport Organizer?", "a": "SE09/SE10 — create and manage transport requests."},
        {"q": "ABAP table for vendor general data?", "a": "LFA1 — General data. LFB1 = Company code data. LFM1 = Purchasing org data."},
        {"q": "How to find user exit for a transaction?", "a": "Transaction SMOD — lists all customer enhancement exits. Use CMOD to create a project."},
        {"q": "What is SU53 used for?", "a": "Shows the last failed authorization check for the current user — includes object name and field values."},
        {"q": "Transaction to schedule background jobs?", "a": "SM36 (schedule). SM37 (monitor). Job classes: A (highest) to C (lowest priority)."},
        {"q": "What is an implicit enhancement?", "a": "Hook at start/end of any ABAP block. Access via SE38 > Enhancement Mode."},
        {"q": "What is ST05?", "a": "SQL Trace / Performance Trace — captures DB queries for performance analysis."},
        {"q": "Transport of Copies vs regular transport?", "a": "Transport of Copies moves objects without marking them as transported — used for hotfixes/testing."},
        {"q": "What does SM13 show?", "a": "Update Work Process records — shows failed updates where the DB write did not complete after a transaction."},
    ],
    "SAP HANA": [
        {"q": "What is the Delta Merge in HANA?", "a": "Merges the row-based delta store (for fast writes) into the column store (for fast reads)."},
        {"q": "What replaces vendor/customer master in S/4HANA?", "a": "Business Partner (BP) — transaction BP. Roles FLVN00/FLVN01 for vendors."},
        {"q": "Is Material Ledger mandatory in S/4HANA?", "a": "Yes — mandatory for all valuation areas in S/4HANA."},
        {"q": "What is MRP Live?", "a": "HANA-native MRP engine. Parallel processing reduces multi-hour runs to minutes."},
        {"q": "What is ACDOCA?", "a": "Universal Journal — single table replacing BKPF+BSEG+COEP+ML tables in S/4HANA."},
        {"q": "What are CDS Views?", "a": "Core Data Services — virtual data models pushing computation to HANA. Used by Fiori analytics."},
        {"q": "Migration approach preserving all ECC history?", "a": "Brownfield (System Conversion) — in-place conversion of ECC to S/4HANA."},
        {"q": "What protocol do Fiori apps use for backend?", "a": "OData (REST-based HTTP protocol). The Fiori frontend calls OData services on the SAP Gateway."},
        {"q": "EWM term equivalent to Transfer Order?", "a": "Warehouse Task (WT). Multiple WTs are grouped into Warehouse Orders (WO)."},
        {"q": "What is the Simplification List?", "a": "SAP's published document of all functional/technical changes from ECC to S/4HANA."},
    ],
}


def flashcard_mode(topic: str) -> None:
    import random
    color, _ = TOPIC_COLORS[topic]
    cards = FLASHCARDS.get(topic, [])
    if not cards:
        print(f"{RED}No flashcards for {topic}.{RESET}")
        pause()
        return

    random.shuffle(cards)
    clear()
    title_box(f"FLASHCARDS — {topic}", color)
    print(f"\n  {DIM}{len(cards)} cards loaded. Press Enter to reveal answer, 'n' for next, 'q' to quit.{RESET}\n")
    pause("Press Enter to start...")

    for i, card in enumerate(cards):
        clear()
        section_header(f"Flashcard {i + 1} / {len(cards)}", "🃏", color)
        print(f"\n  {BOLD}{card['q']}{RESET}\n")
        pause("Press Enter to reveal answer...")

        print(f"\n  {B_GREEN}{BOLD}Answer:{RESET}")
        slow_print(f"  {card['a']}", 0.008, GREEN)
        print()

        nxt = prompt("[n] Next  [q] Quit →").lower()
        if nxt == "q":
            break

    print(f"\n  {B_YELLOW}Flashcard session complete!{RESET}")
    pause()


# ── Topic Menu ───────────────────────────────────────────────────────────────

def topic_menu(topic: str, prog: dict) -> None:
    color, _ = TOPIC_COLORS[topic]
    while True:
        clear()
        title_box(f"SAP INTERVIEW PREP — {topic}", color)
        print()

        # Show last quiz score if available
        scores = prog["quiz_scores"].get(topic, [])
        if scores:
            last = scores[-1]
            score_str = f"Last score: {last}%  |  Sessions: {len(scores)}"
            print(f"  {DIM}{score_str}{RESET}")
        else:
            print(f"  {DIM}No quiz attempts yet for this topic.{RESET}")

        print()
        print(f"  {B_YELLOW}[1]{RESET} {BOLD}Study Guide{RESET}  — Read through all sections interactively")
        print(f"  {B_YELLOW}[2]{RESET} {BOLD}Quiz Mode{RESET}   — Test yourself with MCQ questions")
        print(f"  {B_YELLOW}[3]{RESET} {BOLD}Flashcards{RESET}  — Quick term/concept revision")
        print(f"  {B_YELLOW}[q]{RESET} {BOLD}Back{RESET}        — Return to main menu")
        print()

        choice = prompt("Select →").lower()
        if choice == "1":
            study_mode(topic, prog)
        elif choice == "2":
            run_quiz(topic, prog)
        elif choice == "3":
            flashcard_mode(topic)
        elif choice == "q":
            break


# ── Main Menu ────────────────────────────────────────────────────────────────

WELCOME_ART = r"""
  ███████╗ █████╗ ██████╗     ██████╗ ██████╗ ███████╗██████╗
  ██╔════╝██╔══██╗██╔══██╗    ██╔══██╗██╔══██╗██╔════╝██╔══██╗
  ███████╗███████║██████╔╝    ██████╔╝██████╔╝█████╗  ██████╔╝
  ╚════██║██╔══██║██╔═══╝     ██╔═══╝ ██╔══██╗██╔══╝  ██╔═══╝
  ███████║██║  ██║██║         ██║     ██║  ██║███████╗██║
  ╚══════╝╚═╝  ╚═╝╚═╝         ╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝
"""


def main() -> None:
    prog = load_progress()
    prog["total_sessions"] = prog.get("total_sessions", 0) + 1
    save_progress(prog)

    while True:
        clear()
        print(f"{B_BLUE}{WELCOME_ART}{RESET}")
        print(f"  {BOLD}Interview Preparation Guide{RESET}  |  {DIM}5+ Years Experience Track  |  ECC & S/4HANA{RESET}\n")
        hr("─", DIM)
        print(f"\n  {DIM}Session #{prog['total_sessions']}{RESET}\n")

        print(f"  {BOLD}Choose a topic:{RESET}\n")
        print(f"  {BLUE}{BOLD}[1]{RESET}  SAP MM  — Materials Management")
        print(f"  {GREEN}{BOLD}[2]{RESET}  SAP ECC — Architecture & Configuration")
        print(f"  {MAGENTA}{BOLD}[3]{RESET}  SAP HANA — S/4HANA, Migration & New Features\n")
        print(f"  {B_CYAN}[p]{RESET}  Progress Dashboard")
        print(f"  {DIM}[q]  Quit{RESET}")
        print()

        choice = prompt("Select →").lower()

        if choice == "1":
            topic_menu("SAP MM", prog)
        elif choice == "2":
            topic_menu("SAP ECC", prog)
        elif choice == "3":
            topic_menu("SAP HANA", prog)
        elif choice == "p":
            show_progress(prog)
        elif choice in ("q", "quit", "exit"):
            clear()
            print(f"\n  {B_YELLOW}Good luck with your interviews!{RESET}\n")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {DIM}Interrupted. Goodbye!{RESET}\n")
        sys.exit(0)
