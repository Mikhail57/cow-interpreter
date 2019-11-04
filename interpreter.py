import argparse
import os
from typing import List, Optional


class CowInterpreter:
    available_commands = ["moo", "mOo", "moO", "mOO", "Moo", "MOo", "MoO", "MOO", "OOO", "MMM", "OOM", "oom"]

    def __init__(self) -> None:
        super().__init__()
        self._cells: List[int] = [0 for _ in range(30000)]
        self._commands: List[int] = []
        self._ptr: int = 0
        self._cmd_ptr: int = 0
        self._register: Optional[int] = None

        self._commands_to_functions = {
            0: self._handle_loop_end,
            1: self._move_to_prev_cell,
            2: self._move_to_next_cell,
            3: self._handle_current_as_instruction,
            4: self._print_or_read_char,
            5: self._decriment_current_block,
            6: self._increment_current_block,
            7: self._handle_loop_start,
            8: self._zero_current_cell,
            9: self._copy_or_paste_register,
            10: self._print_int,
            11: self._read_int
        }

    def interpret(self, code: str):
        filtered_cmds = filter(lambda cmd: cmd in self.available_commands, code.split())
        mapped_cmds = map(lambda cmd: self.available_commands.index(cmd), filtered_cmds)
        self._commands = list(mapped_cmds)
        self._ptr = 0

        while self._cmd_ptr < len(self._commands):
            self._handle_command(self._commands[self._cmd_ptr])
            self._cmd_ptr += 1

    def _handle_command(self, current_cmd):
        self._commands_to_functions[current_cmd]()

    def _handle_loop_start(self):
        curr_cell = self._cells[self._ptr]
        if curr_cell == 0:
            le = self._get_loop_end(self._cmd_ptr)
            self._ptr = le

    def _handle_loop_end(self):
        ls = self._get_loop_start(self._cmd_ptr)
        self._ptr = ls - 1

    def _zero_current_cell(self):
        self._cells[self._ptr] = 0

    def _move_to_prev_cell(self):
        self._ptr -= 1

    def _move_to_next_cell(self):
        self._ptr += 1

    def _handle_current_as_instruction(self):
        cell_cmd = self._cells[self._ptr]
        if 0 > cell_cmd >= len(self.available_commands) or cell_cmd == 3:
            raise Exception(f"Invalid command {cell_cmd} when executing mOO command")
        self._handle_command(cell_cmd)

    def _print_or_read_char(self):
        cell = self._cells[self._ptr]
        if cell == 0:
            self._read_char()
        else:
            self._print_char()

    def _decriment_current_block(self):
        self._cells[self._ptr] -= 1

    def _increment_current_block(self):
        self._cells[self._ptr] += 1

    def _copy_or_paste_register(self):
        if self._register is None:
            self._register = self._cells[self._ptr]
        else:
            self._cells[self._ptr] = self._register
            self._register = None

    def _print_int(self):
        print(self._cells[self._ptr], end='')

    def _read_int(self):
        self._cells[self._ptr] = int(input(">>>"))

    def _read_char(self):
        self._cells[self._ptr] = ord(input(">>>")[0])

    def _print_char(self):
        print(chr(self._cells[self._ptr]), end='')

    def _get_loop_end(self, cmd_ptr):
        pass


def main(args: argparse.Namespace):
    filename = args.input

    if not os.path.isfile(filename):
        raise FileNotFoundError(f"File '{filename}' does not exists")

    file = open(filename, "rt")
    if not file.readable():
        raise BlockingIOError("Provided file is not readable")

    lines = '\n'.join(file.readlines())

    interpreter = CowInterpreter()
    interpreter.interpret(lines)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input file to be interpreted")
    args = parser.parse_args()
    main(args)
