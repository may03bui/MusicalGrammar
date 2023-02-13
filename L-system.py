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
        print("RESTART")
        while pos < len(prev_melody):
            print(pos)
            for p in pred_list:
                if prev_melody[pos:pos+len(p)] == p:
                    pred = p
                    break

            melody += np.random.choice(prodns[pred][0], p=prodns[pred][1])  # KeyError if the input is bad
            pos += len(pred)

        prev_melody = melody

    return melody



def main():
    # Our grammar
    P = {
        "F": (["F", "dFFD", "d-F+FD", "d+F-FD"], [0.25, 0.25, 0.25, 0.25]),
        "FF": (["Fd+F-FD", "Fd-F+FD"], [0.5, 0.5]),
        "F+F": (["Fd++F-FD", "Fd+++F--FD", "Fd-F++FD", "Fd--F+++FD"], [0.25, 0.25, 0.25, 0.25]),
        "F-F": (["-Fd++F-FD", "-Fd+++F--FD", "-Fd-F++FD", "-Fd--F+++FD"], [0.25, 0.25, 0.25, 0.25]),
        "+": (["+"], [1]),
        "-": (["+"], [1]),
        "D": (["+"], [1]),
        "d": (["+"], [1])
    }

    for symbol in ["+", "-", "D", "d"]:  # Identity productions
        P[symbol] = ([symbol], [1])

    axiom = input("Enter an axiom. (X to stop.) ")
    G = {"P": P, "A": axiom}

    melody = generate_melody(G, 4)

    # Parsing string...
    scale = ["C", "D", "E", "F", "G", "A", "B"]    # Could've picked a different scale!
    crotchet_length = 600
    # get_track()
    t = Track()

    pitch = 0     # Current state
    duration = 1
    octave = 4
    print(melody)

    for c in melody:
        match c:
            case "F":
                n = Note(scale[pitch], channel=1, octave=octave)
                print(n)
                n.channel = 1
                print(t.add_notes(n, crotchet_length * duration))
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

    print(t)
    fluidsynth.init("FluidR3_GM.sf2")
    fluidsynth.play_Track(t, 1, 10)


if __name__ == "__main__":
    main()