from typing import Self
import sys
import base64
from pathlib import Path

import typer

from lab7.audio_data import AudioData


def get_stdin() -> str:
    return sys.stdin.read()


class BitIterator:
    def __init__(self, data: bytes):
        self._data = data
        self._byte_i = 0
        self._bit_i = 0

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> int:
        if self._byte_i >= len(self._data):
            raise StopIteration

        byte = self._data[self._byte_i]
        bit = (byte >> (7 - self._bit_i)) & 1

        self._bit_i += 1
        if self._bit_i >= 8:
            self._bit_i = 0
            self._byte_i += 1

        return bit


def encode_audio(audio: AudioData, s: str):
    data = base64.b64encode(s.encode("utf8")) + b"\0"
    audio_size = audio.framerate * audio.nframes * audio.nchannels
    if audio_size // 8 < len(data):
        raise ValueError("Not enough bytes to encode all of the data.")

    for i, bit in enumerate(BitIterator(data)):
        fi = i // audio.nchannels
        chi = i % audio.nchannels
        sample = audio.get_sample(fi, chi)
        byte = sample[-1]
        byte = (byte & 0b11111110) | bit
        sample = sample[:-1] + byte.to_bytes(1)
        audio.set_sample(fi, chi, sample)


def main(audio_path: Path):
    audio = AudioData.open(audio_path)

    data = get_stdin()
    encode_audio(audio, data)

    new_stem = audio_path.stem + "_encoded"
    audio.save(audio_path.with_stem(new_stem))


if __name__ == "__main__":
    typer.run(main)
