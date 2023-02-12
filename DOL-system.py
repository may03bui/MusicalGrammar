from mingus.midi import fluidsynth
from mingus.containers import Track


def main():
    melody = "C"
    start, end = 0, 1

    for _ in range(5):
        num_new_notes = 0
        for i in range(start, end):
            if melody[i] == "C":
                melody += "E"
                num_new_notes += 1
            elif melody[i] == "E":
                melody += "CGC"
                num_new_notes += 3

        start = end
        end += num_new_notes
    
    t = Track()
    for note in melody:
        t.add_notes(note)
    fluidsynth.init("FluidR3_GM.sf2")
    fluidsynth.play_Track(t, 1, 140)


if __name__ == "__main__":
    main()
