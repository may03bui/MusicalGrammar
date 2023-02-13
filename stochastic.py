from mingus.midi import fluidsynth
from mingus.containers import Track
import numpy as np


def get_transition_probs(string, alphabet):
    t_probs = {n1: {n2: 0 for n2 in alphabet} for n1 in alphabet}

    for i in range(len(string) - 1):
        row = t_probs[string[i]]
        row[string[i + 1]] = row.get(string[i + 1]) + 1

    for n, row in t_probs.items():
        print(row.items())
        t_probs[n] = {k: v / sum(row.values()) for k, v in row.items()}

    return t_probs


def generate_melody(starting_note, t_probs, alphabet, iters):
    melody = starting_note
    t = Track()
    t.add_notes(melody)

    for _ in range(iters):
        prev = melody[-1]
        print(t_probs)
        current_note = np.random.choice(alphabet, p=[t_probs[prev][n] for n in alphabet])
        melody += current_note
        t.add_notes(current_note)

    return t, melody


def main():
    alphabet = ["C", "D", "E", "G"]
    song = "EDCDEEEDDDEGGEDCDEEEEDDEDCC"  # Added C to wrap the melody back around
    t_probs = get_transition_probs(song, alphabet)
    track, melody = generate_melody("C", t_probs, alphabet, 15)

    fluidsynth.init("FluidR3_GM.sf2")
    fluidsynth.play_Track(track, 1, 160)


if __name__ == "__main__":
    main()
