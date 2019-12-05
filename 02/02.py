import json


class IntCalculator:
    instructions = None
    ip = 0
    ADD = 1
    END = 99
    MULTIPLY = 2
    INPUT_OFFSET = [1, 2]
    OUTPUT_OFFSET = 3
    INSTRUCTION_STEP = 4

    def __init__(self, instructions):
        self.instructions = instructions

    def execute(self):
        while self.instructions[self.ip] != self.END:
            # Decode and Load
            instruction = self.instructions[self.ip]
            param1 = self.instructions[self.instructions[self.ip + self.INPUT_OFFSET[0]]]
            param2 = self.instructions[self.instructions[self.ip + self.INPUT_OFFSET[1]]]
            write_address = self.instructions[self.ip + self.OUTPUT_OFFSET]

            # Execute Instruction
            if instruction == self.ADD:
                self.instructions[write_address] = param1 + param2
            elif instruction == self.MULTIPLY:
                self.instructions[write_address] = param1 * param2
            else:
                raise Exception("Somethings wrong")

            # Goto next instruction
            self.ip = self.ip + self.INSTRUCTION_STEP


def part1():
    with open("instructions.json", "r") as instrFp:
        instructions = json.load(instrFp)
    calc = IntCalculator(instructions.copy())
    # Part 1
    calc.instructions[1] = 12
    calc.instructions[2] = 2
    calc.execute()
    print(instructions)


def part2():
    with open("instructions.json", "r") as instrFp:
        instructions = json.load(instrFp)
    verb_pos = 2
    noun_pos = 1
    wanted_result = 19690720

    calc = IntCalculator(instructions.copy())
    noun = -1
    verb = 0
    for verb in range(0, 100):
        for noun in range(0, 100):
            calc = IntCalculator(instructions.copy())
            calc.instructions[verb_pos] = verb
            calc.instructions[noun_pos] = noun
            try:
                calc.execute()
            except Exception:
                pass
            if calc.instructions[0] == wanted_result:
                break
        if calc.instructions[0] == wanted_result:
            break

    print("noun: " + str(noun))
    print("verb: " + str(verb))
    print(calc.instructions)


if __name__ == "__main__":
    part1()
    part2()
