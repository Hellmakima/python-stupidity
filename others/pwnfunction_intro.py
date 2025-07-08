import os
import time
import random

RED = '\033[1;91m'
CYAN = '\033[1;96m'
RESET = '\033[0m'

name1 = b"Sufiyan"
name2 = b"Attar"
revealed1 = set()
revealed2 = set()

def colorize_ascii(ascii_str, offset, pos, len1, len2):
    out = []
    for i, c in enumerate(ascii_str):
        global_pos = offset + i
        if pos <= global_pos < pos + len1:
            out.append(f"{RED}{c}{RESET}")
        elif pos + 20 <= global_pos < pos + 20 + len2:
            out.append(f"{CYAN}{c}{RESET}")
        else:
            out.append(c)
    return ''.join(out)

def colorize_hex(chunk, offset, pos, len1, len2):
    out = []
    for i, b in enumerate(chunk):
        global_pos = offset + i
        h = f'{b:02X}'
        if pos <= global_pos < pos + len1:
            out.append(f"{RED}{h}{RESET}")
        elif pos + 20 <= global_pos < pos + 20 + len2:
            out.append(f"{CYAN}{h}{RESET}")
        else:
            out.append(h)
    return ' '.join(out)

def hexdump(data, pos, len1, len2, width=16):
    a = ''
    for offset in range(0, len(data), width):
        chunk = data[offset:offset + width]
        hex_str = colorize_hex(chunk, offset, pos, len1, len2)
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        ascii_col = colorize_ascii(ascii_str, offset, pos, len1, len2)
        a += f'{offset:08X}  {hex_str:<{width*3}} {ascii_col}\n'
    print(a[:-1], end='')
def scramble_stateful(original, frame, revealed):
    total = len(original)
    target = min(frame, total)
    # Reveal at most 1 new character every 2-3 frames
    if len(revealed) < target:
        unrevealed = [i for i in range(total) if i not in revealed]
        if unrevealed and random.random() < 0.4:  # 40% chance to reveal one
            revealed.add(random.choice(unrevealed))
    return bytes(
        original[i] if i in revealed else random.randint(33, 126)
        for i in range(total)
    ), revealed

size = 512 + 16*5
pos = size - 252
len1 = len(name1)
len2 = len(name2)
random_data = bytearray(os.urandom(size+40*16))

for i in range(40):
    n1, revealed1 = scramble_stateful(name1, i, revealed1)
    n2, revealed2 = scramble_stateful(name2, i, revealed2)
    data = random_data[i*16:i*16+size]
    data[pos:pos+len1] = n1
    data[pos+20:pos+20+len2] = n2
    hexdump(data, pos, len1, len2)
    time.sleep(0.2)
