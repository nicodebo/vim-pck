from enum import Enum
import itertools
import sys
import time
import threading


class Sequence(Enum):
    """Enumeration of spinner sequence

    Ref: https://stackoverflow.com/questions/2685435/cooler-ascii-spinners
    """

    BASIC = ['-', '/', '|', '\\']
    ARROW = ['←', '↖', '↑', '↗', '→', '↘', '↓', '↙']
    VERT_BAR = ['▁', '▃', '▄', '▅', '▆', '▇', '█', '▇', '▆', '▅', '▄', '▃']
    HORIZ_BAR = ['▉', '▊', '▋', '▌', '▍', '▎', '▏', '▎', '▍', '▌', '▋', '▊', '▉']
    SPIN_RECT = ['▖', '▘', '▝', '▗']
    ELAST_BAR = ['▌', '▀', '▐▄']
    TETRIS = ['┤', '┘', '┴', '└', '├', '┌', '┬', '┐']
    TRIANGLE = ['◢', '◣', '◤', '◥']
    SQUARE_QRT = ['◰', '◳', '◲', '◱']
    CIRCLE_QRT = ['◴', '◷', '◶', '◵']
    CIRCLE_HLF = ['◐', '◓', '◑', '◒']
    BALLOON = ['.', 'o', 'O', '@', '*']
    BLINK = ['◡◡', '⊙⊙', '◠◠']
    TURN = ['◜ ', ' ◝', ' ◞', '◟ ']
    LOSANGE = ['◇', '◈', '◆']
    BRAILLE = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']

    def describe(self):
        return self.name, self.value

    @classmethod
    def default_sequence(cls):
        return Sequence.BASIC


class Spinner():
    """A shell spinner
    """

    def __init__(self, busy_message="", interval=0.25, sequence="basic"):
        self.stop_running = threading.Event()
        self.spin_thread = threading.Thread(target=self.init_spin)
        self.interval = interval  # speed rotation
        self.busy_message = busy_message  # spinner text
        self.spinner_cycle = itertools.cycle(self.set_spinner_seq(sequence))
        self.cur_mess_tmp = ""  # store current spinner message

    def set_spinner_seq(self, sequence):
        seq_list = [name for name, members in Sequence.__members__.items()]
        if sequence.upper() in seq_list:
            seq = Sequence[sequence.upper()].value
        else:
            seq = Sequence.default_sequence().value
        return seq

    def start(self):
        self.spin_thread.start()

    def stop(self):
        self.stop_running.set()
        self.spin_thread.join()
        # make sure to clear the line in case printing something shorter
        sys.stdout.write("\033[K")

    def init_spin(self):
        while not self.stop_running.is_set():
            if not self.busy_message:
                self.cur_mess_tmp = next(self.spinner_cycle)
            else:
                self.cur_mess_tmp = "{} {}".format(next(self.spinner_cycle),
                                                   self.busy_message)
            sys.stdout.write(self.cur_mess_tmp)
            sys.stdout.flush()
            time.sleep(self.interval)
            sys.stdout.write('\b' * len(self.cur_mess_tmp))


# Quick exemple usage
if __name__ == "__main__":

    def do_work():
        time.sleep(3)

    messa = 'git clone processing'
    speed = 0.1
    seq = 'LOSANGE'
    spinner1 = Spinner()
    spinner2 = Spinner(messa, speed, seq)
    print('::starting work task 1')
    spinner1.start()

    do_work()

    spinner1.stop()
    print(':: task 1 done')

    print('::starting work task 2')
    spinner2.start()
    do_work()
    spinner2.stop()
    print(':: task 2 done')
    print('all done!')

