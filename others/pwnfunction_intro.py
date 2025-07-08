import os
import time

RED = '\033[1;91m'
CYAN = '\033[1;96m'
RESET = '\033[0m'

name1 = b"Pwn"
name2 = b"Function"

def colorize_ascii(ascii_str, offset, pos):
    result = ""
    name1_pos = pos
    name2_pos = pos + 20
    name1_len = len(name1)
    name2_len = len(name2)

    for i, char in enumerate(ascii_str):
        global_pos = offset + i
        if name1_pos <= global_pos < name1_pos + name1_len:
            result += f"{RED}{char}{RESET}"
        elif name2_pos <= global_pos < name2_pos + name2_len:
            result += f"{CYAN}{char}{RESET}"
        else:
            result += char
    return result

def colorize_hex(chunk, offset, pos):
    result = []
    name1_pos = pos
    name2_pos = pos + 20
    name1_len = len(name1)
    name2_len = len(name2)

    for i, b in enumerate(chunk):
        global_pos = offset + i
        hex_byte = f'{b:02X}'
        if name1_pos <= global_pos < name1_pos + name1_len:
            result.append(f"{RED}{hex_byte}{RESET}")
        elif name2_pos <= global_pos < name2_pos + name2_len:
            result.append(f"{CYAN}{hex_byte}{RESET}")
        else:
            result.append(hex_byte)
    return ' '.join(result)

def hexdump(data, pos, width=16):
    for offset in range(0, len(data), width):
        chunk = data[offset:offset + width]
        hex_bytes = colorize_hex(chunk, offset, pos)
        ascii = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        colored_ascii = colorize_ascii(ascii, offset, pos)
        print(f'{offset:08X}  {hex_bytes:<{width*3}} {colored_ascii}')
import random

def scramble(name, intensity):
    # intensity: 0 = fully scrambled, 20 = fully clear
    name = bytearray(name)
    keep_amt = min(intensity, len(name))
    indices_to_keep = random.sample(range(len(name)), keep_amt)
    for i in range(len(name)):
        if i not in indices_to_keep:
            name[i] = random.randint(33, 126)
    return bytes(name)

size = 512 + 16*5
for i in range(40):
    data = bytearray(os.urandom(size))
    n1 = scramble(name1, i)
    n2 = scramble(name2, i)
    pos = size - 252 #+ i * 16
    data[pos:pos+len(n1)] = n1
    data[pos+20:pos+20+len(n2)] = n2
    hexdump(data, pos)
    print()
    time.sleep(0.2)
