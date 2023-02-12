from mingus.midi import fluidsynth
from mingus.containers import Track
import numpy as np


def main():
    song = "EDCDEEEDDDEGGEDCDEEEEDDEDC"
    alphabet = ["C", "D", "E", "G"]
    t_probs = {n1: {n2: 0 for n2 in alphabet} for n1 in alphabet}
    t_probs["C"]["E"] = 1    # Wrap the melody back round

    for i in range(len(song)-1):
        row = t_probs[song[i]]
        row[song[i+1]] = row.get(song[i+1]) + 1
    
    for n, row in t_probs.items():
        t_probs[n] = {k: v/sum(row.values()) for k, v in row.items()}

    current_note = np.random.choice(alphabet, p=[song.count(n)/len(song) for n in alphabet])
    melody = current_note
    t = Track()
    t.add_notes(current_note)

    for _ in range(15):
        prev = melody[-1]
        current_note = np.random.choice(alphabet, p=[t_probs[prev][n] for n in alphabet]) 
        melody += current_note
        t.add_notes(current_note)

    print(melody)
    fluidsynth.init("FluidR3_GM.sf2")
    fluidsynth.play_Track(t, 1, 160)

if __name__ == "__main__":
    main()