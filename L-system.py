from mingus.midi import fluidsynth
from mingus.containers import Track, Note
import numpy as np


def generate_melody(grammar, iters):
    prodns = grammar["P"]
    prev_melody = grammar["A"]
    pred_list = sorted(list(prodns.keys()), key=lambda x: -len(x))  # Lambda enforces 'longest pred' rule

    for _ in range(iters):
        pos = 0
        melody = ""
        while pos < len(prev_melody):
            for p in pred_list:
                if prev_melody[pos:pos+len(p)] == p:
                    pred = p
                    break
            melody += np.random.choice(**prodns[pred])
            pos += len(pred)
        prev_melody = melody

    return melody


def get_track(melody, scale):
    t = Track()
    crotchet_length = 500
    pitch = 0     # Initialise state
    duration = 1
    octave = 4

    for c in melody:
        match c:
            case "F":
                n = Note(scale[pitch], channel=1, octave=octave)
                n.channel = 1
                t.add_notes(n, crotchet_length * duration)
            case "D":
                duration *= 2
            case "d":
                duration *= .5
            case "+":
                pitch += 1
                if pitch == 7:
                    pitch = 0
                    octave += 1
            case "-":
                pitch -= 1
                if pitch == -1:
                    pitch = 6
                    octave -= 1

    return t


def main():
    # Our grammar
    P = {
        "F": {"a": ["F", "dFFD", "d-F+FD", "d+F-FD"], "p": [0.25, 0.25, 0.25, 0.25]},
        "FF": {"a": ["Fd+F-FD", "Fd-F+FD"], "p": [0.5, 0.5]},
        "F+F": {"a": ["Fd++F-FD", "Fd+++F--FD", "Fd-F++FD", "Fd--F+++FD"], "p": [0.25, 0.25, 0.25, 0.25]},
        "F-F": {"a": ["-Fd++F-FD", "-Fd+++F--FD", "-Fd-F++FD", "-Fd--F+++FD"], "p": [0.25, 0.25, 0.25, 0.25]},
    }

    for symbol in ["+", "-", "D", "d"]:  # Identity productions
        P[symbol] = {"a": [symbol], "p": [1]}

    axiom = input("Axiom: ")
    G = {"P": P, "A": axiom}
    melody = generate_melody(G, 4)
    scale = ["C", "D", "E", "F", "G", "A", "B"]    # Could've picked a different scale!
    t = get_track(melody, scale)

    print("Melody string: ", melody)
    fluidsynth.init("FluidR3_GM.sf2")
    fluidsynth.play_Track(t, 1, 10)


if __name__ == "__main__":
    main()
