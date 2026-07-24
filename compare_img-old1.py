from pathlib import Path

START = 0x18
RECSIZE = 16

def describe_offset(i):
    rel = i - START
    ch = rel // RECSIZE + 1
    pos = rel % RECSIZE
    return ch, pos

def field_name(pos):
    return "RX frequency" if pos < 4 else "TX frequency" if pos < 8 else "other"

def decode_freq(bs):
    return int(''.join(f'{b:02x}' for b in bs[::-1])) / 100000

def field_freq(buf, ch, pos):
    return decode_freq(buf[START + (ch - 1) * RECSIZE + pos : START + (ch - 1) * RECSIZE + pos + 4])



base = Path("Radioddity_UV-5R EX_20260721-1-factory-baseline.img").read_bytes()
changed = Path("01_UV5R_EX_ch1_freq_146125.img").read_bytes()

changed_channels = set()

for i, (a, b) in enumerate(zip(base, changed)):
    if a != b:
        changed_channels.add(ch)
        ch, pos = describe_offset(i)
        print(f"0x{i:04x}: {a:02x} -> {b:02x}   channel {ch}, {field_name(pos)} byte {pos}")
#print("Channel 1 RX:", decode_freq(base[0x18:0x1c]), "->", decode_freq(changed[0x18:0x1c]))
print(f"Channel 1 RX: {field_freq(base, 1, 0):.3f} -> {field_freq(changed, 1, 0):.3f}")
#print("Channel 1 TX:", decode_freq(base[0x1c:0x20]), "->", decode_freq(changed[0x1c:0x20]))
print(f"Channel 1 TX: {field_freq(base, 1, 4):.3f} -> {field_freq(changed, 1, 4):.3f}")
#print("Channel 1 offset:", decode_freq(base[0x1c:0x20]) - decode_freq(base[0x18:0x1c]), "->", decode_freq(changed[0x1c:0x20]) - decode_freq(changed[0x18:0x1c]))
#print(f"Channel 1 offset: {decode_freq(base[0x1c:0x20]) - decode_freq(base[0x18:0x1c]):.3f} -> {decode_freq(changed[0x1c:0x20]) - decode_freq(changed[0x18:0x1c]):.3f}")
print(f"Channel 1 offset: {field_freq(base, 1, 4) - field_freq(base, 1, 0):.3f} -> {field_freq(changed, 1, 4) - field_freq(changed, 1, 0):.3f}")
