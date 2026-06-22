import curses
import re
import time
from pathlib import Path

import typer

app = typer.Typer()

TAB_WIDTH = 4
MARGIN = 2
BOX_W = 30
BOX_H = 3
BG_PAIR = 1


def tokenize(text: str) -> list[str]:
    # Words, newlines, and tabs. Space runs are dropped — implicit between words.
    return re.findall(r"\S+|\n|\t", text)


def build_word_indices(tokens: list[str]) -> list[int]:
    return [i for i, t in enumerate(tokens) if t not in ("\n", "\t")]


def layout_tokens(
    tokens: list[str], t_start: int, t_end: int, target_idx: int, width: int
) -> tuple[list[list[tuple[int, str, int]]], int]:
    """
    Layout tokens[t_start:t_end] into wrapped screen lines.
    Each entry: (token_index, display_text, x_pos).
    Also returns the line index of target_idx.
    """
    lines: list[list[tuple[int, str, int]]] = []
    current: list[tuple[int, str, int]] = []
    x = MARGIN
    target_line = 0

    for idx in range(t_start, min(t_end, len(tokens))):
        tok = tokens[idx]

        if tok == "\n":
            lines.append(current)
            current = []
            x = MARGIN
            continue

        if tok == "\t":
            col = x - MARGIN
            advance = TAB_WIDTH - (col % TAB_WIDTH)
            current.append((idx, " " * advance, x))
            x += advance
            continue

        # word: wrap if it won't fit
        if current and x + len(tok) >= width - MARGIN:
            lines.append(current)
            current = []
            x = MARGIN

        if idx == target_idx:
            target_line = len(lines)
        current.append((idx, tok, x))
        x += len(tok) + 1  # +1 for implicit space

    if current:
        lines.append(current)

    return lines, target_line


def draw_paused(stdscr, tokens, word_indices, word_i, width, height):
    token_i = word_indices[word_i]
    radius = 1000
    t_start = max(0, token_i - radius)
    t_end = min(len(tokens), token_i + radius + 1)

    lines, target_line = layout_tokens(tokens, t_start, t_end, token_i, width)
    offset = (height // 2) - target_line

    li_start = max(0, 2 - offset)
    li_end = min(len(lines), height - 1 - offset)

    for li in range(li_start, li_end):
        y = offset + li
        for tidx, text, x in lines[li]:
            if x >= width - MARGIN:
                break
            attr = (curses.A_REVERSE | curses.A_BOLD) if tidx == token_i else curses.A_NORMAL
            try:
                stdscr.addnstr(y, x, text, min(len(text), width - x - 1), attr)
            except curses.error:
                pass


def draw_running(stdscr, tokens, word_indices, word_i, width, height, bg):
    word = tokens[word_indices[word_i]]
    y = height // 2
    x = max(0, (width - len(word)) // 2)

    if bg:
        curses.init_color(curses.COLOR_BLACK, 0, 0, 0) 
        bg_attr = curses.color_pair(BG_PAIR)
        box_x = max(0, (width - BOX_W) // 2)
        box_y = y - BOX_H // 2
        for row in range(BOX_H):
            by = box_y + row
            if 0 <= by < height:
                try:
                    stdscr.addnstr(by, box_x, " " * BOX_W, BOX_W, bg_attr)
                except curses.error:
                    pass
        word_attr = curses.A_BOLD | curses.color_pair(BG_PAIR)
    else:
        word_attr = curses.A_BOLD

    try:
        stdscr.addnstr(y, x, word, width - x - 1, word_attr)
    except curses.error:
        pass


def draw_screen(stdscr, tokens, word_indices, word_i, words_per_second, paused, bg):
    stdscr.erase()
    height, width = stdscr.getmaxyx()

    n = len(word_indices)
    pct = int((word_i + 1) / n * 100)
    status = f"WPS: {words_per_second:.1f} | {word_i + 1}/{n} | {pct}%"
    mode = "PAUSED" if paused else "RUNNING"
    help_line = "Space: pause | ←/→: jump | ↑/↓: speed | q: quit"

    try:
        stdscr.addnstr(0, 0, status, width - 1)
        stdscr.addnstr(1, 0, mode, width - 1)
        stdscr.addnstr(height - 1, 0, help_line, width - 1)
    except curses.error:
        pass

    if paused:
        draw_paused(stdscr, tokens, word_indices, word_i, width, height)
    else:
        draw_running(stdscr, tokens, word_indices, word_i, width, height, bg)

    stdscr.refresh()


def run_reader(stdscr, tokens, word_indices, words_per_second, jump_words, bg):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(BG_PAIR, curses.COLOR_WHITE, curses.COLOR_BLACK)

    n = len(word_indices)
    i = 0
    paused = False
    next_tick = time.monotonic() + (1 / words_per_second)

    draw_screen(stdscr, tokens, word_indices, i, words_per_second, paused, bg)

    while True:
        now = time.monotonic()
        ch = stdscr.getch()
        needs_draw = False

        if ch != -1:
            if ch in (ord("q"), 27):
                return
            elif ch == ord(" "):
                paused = not paused
                next_tick = now + (1 / words_per_second)
                needs_draw = True
            elif ch == curses.KEY_LEFT:
                i = max(0, i - jump_words)
                next_tick = now + (1 / words_per_second)
                needs_draw = True
            elif ch == curses.KEY_RIGHT:
                i = min(n - 1, i + jump_words)
                next_tick = now + (1 / words_per_second)
                needs_draw = True
            elif ch == curses.KEY_UP:
                words_per_second += 0.5
                next_tick = now + (1 / words_per_second)
                needs_draw = True
            elif ch == curses.KEY_DOWN:
                words_per_second = max(0.5, words_per_second - 0.5)
                next_tick = now + (1 / words_per_second)
                needs_draw = True
            elif ch == curses.KEY_RESIZE:
                needs_draw = True

        if not paused and now >= next_tick:
            i += 1
            if i >= n:
                stdscr.erase()
                h, w = stdscr.getmaxyx()
                msg = "THE END"
                try:
                    stdscr.addnstr(
                        h // 2, max(0, (w - len(msg)) // 2), msg, w - 1, curses.A_BOLD
                    )
                except curses.error:
                    pass
                stdscr.refresh()
                time.sleep(1)
                return
            next_tick = now + (1 / words_per_second)
            needs_draw = True

        if needs_draw:
            draw_screen(stdscr, tokens, word_indices, i, words_per_second, paused, bg)
        elif not paused:
            time.sleep(0.005)


@app.command()
def main(
    file: Path = typer.Argument(..., exists=True, dir_okay=False, readable=True),
    words_per_second: float = 6.5,
    jump_words: int = 5,
    bg: bool = typer.Option(False, "--bg", help="Draw a black box behind the current word."),
):
    data = file.read_text(encoding="utf-8", errors="ignore")
    tokens = tokenize(data)
    word_indices = build_word_indices(tokens)

    if not word_indices:
        raise typer.BadParameter("File has no words to display.")

    curses.wrapper(run_reader, tokens, word_indices, words_per_second, jump_words, bg)


if __name__ == "__main__":
    app()
