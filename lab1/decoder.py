from collections import defaultdict, Counter
from pathlib import Path
from math import gcd

import typer

RU_LITERALS = [
    "а",
    "б",
    "в",
    "г",
    "д",
    "е",
    "ё",
    "ж",
    "з",
    "и",
    "й",
    "к",
    "л",
    "м",
    "н",
    "о",
    "п",
    "р",
    "с",
    "т",
    "у",
    "ф",
    "х",
    "ц",
    "ч",
    "ш",
    "щ",
    "ъ",
    "ы",
    "ь",
    "э",
    "ю",
    "я",
]
RU_TABLE: dict[str, int] = {c: i for i, c in enumerate(RU_LITERALS)}
RU_SIZE = len(RU_LITERALS)
RU_FREQS: dict[str, float] = {
    "а": 0.0801,
    "б": 0.0159,
    "в": 0.0454,
    "г": 0.0170,
    "д": 0.0298,
    "е": 0.0845,
    "ё": 0.0004,
    "ж": 0.0094,
    "з": 0.0165,
    "и": 0.0735,
    "й": 0.0121,
    "к": 0.0349,
    "л": 0.0440,
    "м": 0.0321,
    "н": 0.0670,
    "о": 0.1097,
    "п": 0.0281,
    "р": 0.0473,
    "с": 0.0547,
    "т": 0.0626,
    "у": 0.0262,
    "ф": 0.0026,
    "х": 0.0097,
    "ц": 0.0048,
    "ч": 0.0144,
    "ш": 0.0073,
    "щ": 0.0036,
    "ъ": 0.0004,
    "ы": 0.0190,
    "ь": 0.0174,
    "э": 0.0032,
    "ю": 0.0064,
    "я": 0.0201,
}


def read_input(input_path: Path) -> str:
    with open(input_path) as f:
        return f.read()


def clean_text(text: str) -> str:
    return "".join(filter(lambda c: c in RU_LITERALS, text.lower()))


def get_key_length(text, min_sequence_length=3) -> int:
    sequences: dict[str, list[int]] = defaultdict(list)
    for i in range(len(text) - min_sequence_length + 1):
        sequence = text[i : i + min_sequence_length]
        sequences[sequence].append(i)
    sequences = {
        sequence: positions
        for sequence, positions in sequences.items()
        if len(positions) > 1
    }

    distances: list[int] = []
    for positions in sequences.values():
        for i in range(1, len(positions)):
            distances.append(positions[i] - positions[i - 1])

    gcd_counts: dict[int] = defaultdict(int)
    for i in range(len(distances)):
        for j in range(i + 1, len(distances)):
            current_gcd = gcd(distances[i], distances[j])
            if current_gcd > 1:
                gcd_counts[current_gcd] += 1

    return max(gcd_counts.items(), key=lambda x: x[1])[0]


def split_into_groups(text: str, key_length: int) -> list[list[str]]:
    groups = [[] for _ in range(key_length)]
    for i, char in enumerate(text):
        groups[i % key_length].append(char)
    return groups


def mse_score(frequences: dict[str, float]) -> float:
    mse = 0.0
    for c in RU_FREQS:
        observed = frequences.get(c, 0)
        expected = RU_FREQS[c]
        mse += (observed - expected) ** 2
    mse /= len(RU_FREQS)
    return mse


def frequency_attack(group: list[list[str]]) -> int:
    best_shift = 0
    best_error = float("inf")
    for shift in range(RU_SIZE):
        decrypted = []
        for c in group:
            decrypted.append(RU_LITERALS[(RU_TABLE[c] - shift) % RU_SIZE])
        counter = Counter(decrypted)
        total = len(decrypted)
        frequences = {c: count / total for c, count in counter.items()}
        error = mse_score(frequences)
        if error < best_error:
            best_error = error
            best_shift = shift
    return best_shift


def find_vigenere_key(text: str, key_length: int) -> str:
    groups = split_into_groups(text, key_length)
    key: list[str] = []
    for group in groups:
        shift = frequency_attack(group)
        key_char = RU_LITERALS[shift]
        key.append(key_char)
    return "".join(key)


def decrypt_vigenere(text: str, key: str) -> str:
    decrypted = []
    key_length = len(key)
    i = 0
    for c in text:
        c_lower = c.lower()
        if c_lower in RU_LITERALS:
            key_char = key[i % key_length]
            shift = RU_TABLE[key_char]
            decrypted_c = RU_LITERALS[(RU_TABLE[c_lower] - shift) % RU_SIZE]
            if c.islower():
                decrypted.append(decrypted_c)
            else:
                decrypted.append(decrypted_c.upper())
            i += 1
        else:
            decrypted.append(c)
    return "".join(decrypted)


def main(input_path: Path):
    text = read_input(input_path)
    print(f"text: {text[:100]} ...")

    cleaned_text = clean_text(text)
    print(f"cleaned text: {cleaned_text[:100]} ...")

    key_length = get_key_length(cleaned_text, 5)
    print(f"key length: {key_length}")

    key = find_vigenere_key(cleaned_text, key_length)
    print(f"key: {key}")

    decrypted_text = decrypt_vigenere(text, key)
    print(f"decrypted text: {decrypted_text[:100]} ...")

    decrypted_path = input_path.with_stem(f"{input_path.stem}_decoded")
    with open(decrypted_path, "w") as f:
        f.write(decrypted_text)


if __name__ == "__main__":
    typer.run(main)
