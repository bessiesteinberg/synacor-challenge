from central_processing_unit import CentralProcessingUnit, ProgramTerminated, NoCommandError
import pytest
from random import randint


def test_halt():
    """ test the halt opcode """
    program = [0]
    cpu = CentralProcessingUnit()

    with pytest.raises(ProgramTerminated):
        cpu.run_program(program)


def test_out():
    """ test the out (print to terminal) opcode """
    cpu = CentralProcessingUnit(capture_terminal_log=True)

    # Write ascii value of 'a' to the 2nd register
    # and value of 'b' to memory address 9
    cpu.registers.write_to(2, 97)

    # This program says print out the value in the 2nd register
    # then print out the value of 98 as an ascii character
    program = [19, 32770, 19, 98]

    cpu.run_program(program)
    assert 'ab' == cpu.terminal_log


def test_noop():
    """ test the out (print to terminal) opcode """
    cpu = CentralProcessingUnit(capture_terminal_log=True)

    # Write ascii value of 'a' to the 2nd register
    cpu.registers.write_to(2, 97)

    # This program says print out the value in the 2nd register
    # then noop
    # then print out the value of 98 as an ascii character
    program = [19, 32770, 21, 19, 98]

    cpu.run_program(program)
    assert 'ab' == cpu.terminal_log


def test_invalid_opcodes():
    """ Assert that invalid opcodes raise NoCommandError """
    cpu = CentralProcessingUnit()

    program = [22]
    with pytest.raises(NoCommandError):
        cpu.run_program(program)


def test_load_program_into_memory():
    """ Assert that program is loaded into memory properly """
    cpu = CentralProcessingUnit()
    program = [randint(0, 65535) in range(5)]
    cpu.memory.load_program(program)

    for memory_pointer in range(len(program)):
        assert program[memory_pointer] == cpu.memory.read_from(memory_pointer).value


# TODO: write better tests for add
# TODO: get the tests to pass
# TODO: i think registers should be holding 15 bit values - maybe worry abotu that when you get to bitwise operators

def test_given_example():
    """ Test the example given in the arch-spec """
    cpu = CentralProcessingUnit(capture_terminal_log=True)
    program = [9, 32768, 32769, 4, 19, 32768]

    # initialize register 1 to 65
    cpu.registers.write_to(1, 65)

    cpu.run_program(program)
    # This program should ...
    # Store into register 0 the sum of 4 and the value contained in register 1.
    assert 69 == cpu.registers.read_from(0).value

    # Output to the terminal the character with the ascii code contained in register 0.
    assert 'E' == cpu.terminal_log
