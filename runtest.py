
from app.util.sample_state import SampleState

if __name__ == "__main__":
    s = SampleState()

    print("STARTING")

    while s.state != "END":
        c = input("> ")
        s.next(c)