from pathlib import Path

START = 0x18
RECSIZE = 16

BASE_FILE = "Radioddity_UV-5R EX_20260721-1-factory-baseline.img"
CHANGED_FILE = "01_UV5R_EX_ch1_freq_146125.img"

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
    off = START + (ch - 1) * RECSIZE + pos
    return decode_freq(buf[off:off + 4])

def duplex(rx, tx):
    return "+" if tx > rx else "-" if tx < rx else "simplex"

def duplex(rx, tx):
    return "+" if tx > rx else "-" if tx < rx else "simplex"



base = Path(BASE_FILE).read_bytes()
changed = Path(CHANGED_FILE).read_bytes()

changed_channels = set()

print("Byte differences:")
for i, (a, b) in enumerate(zip(base, changed)):
    if a != b:
        ch, pos = describe_offset(i)
        changed_channels.add(ch)
        print(f"0x{i:04x}: {a:02x} -> {b:02x}   channel {ch}, {field_name(pos)} byte {pos}")

print("\nChannel summary:")
for ch in sorted(changed_channels):
    base_rx = field_freq(base, ch, 0)
    new_rx = field_freq(changed, ch, 0)
    base_tx = field_freq(base, ch, 4)
    new_tx = field_freq(changed, ch, 4)

    print(f"Channel {ch} RX: {base_rx:.3f} -> {new_rx:.3f}")
    print(f"Channel {ch} TX: {base_tx:.3f} -> {new_tx:.3f}")
    print(f"Channel {ch} offset: {base_tx - base_rx:.3f} -> {new_tx - new_rx:.3f}")
    print(f"Channel {ch} duplex: {duplex(base_rx, base_tx)} -> {duplex(new_rx, new_tx)}")
