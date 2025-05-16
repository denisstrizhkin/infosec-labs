from typing import Self
import base64
from pathlib import Path

import typer

from lab7.audio_data import AudioData


class BitIterator:
    def __init__(self, audio: AudioData):
        self._audio = audio
        self._channel_i = 0
        self._frame_i = 0

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> int:
        if self._frame_i >= self._audio.nframes:
            raise StopIteration

        sample = self._audio.get_sample(self._frame_i, self._channel_i)
        bit = sample[-1] & 0b00000001

        self._channel_i += 1
        if self._channel_i >= self._audio.nchannels:
            self._channel_i = 0
            self._frame_i += 1

        return bit


class ByteIterator:
    def __init__(self, audio: AudioData):
        self._bit_iter = BitIterator(audio)
        self._bit_i = 0

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> bytes:
        byte = 0
        for i in range(8):
            byte = (byte << 1) | next(self._bit_iter)
        return byte.to_bytes(1)


def decode_audio(audio: AudioData) -> str:
    data = b""
    for byte in ByteIterator(audio):
        if byte == b"\0":
            try:
                return base64.b64decode(data).decode("utf8")
            except Exception as e:
                raise ValueError(
                    f"Encoded data is incorrect or corrupted: {e}"
                )
        data += byte

    raise ValueError("Image does not contain encoded data")


def main(audio_path: Path):
    audio = AudioData.open(audio_path)

    data = decode_audio(audio)
    print(data)


if __name__ == "__main__":
    typer.run(main)
