import json


class IntCalculator:
    # Instructions
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JNZ = 5
    JZ = 6
    LT = 7
    EQ = 8
    END = 99

    # Instruction Details
    INPUT_OFFSET = {ADD: [1, 2], MULTIPLY: [1, 2], INPUT: [], OUTPUT: [1], JNZ: [1, 2], JZ: [1, 2], LT: [1, 2],
                    EQ: [1, 2]}
    OUTPUT_OFFSET = {ADD: 3, MULTIPLY: 3, INPUT: 1, OUTPUT: -1, JNZ: -1, JZ: -1, LT: 3, EQ: 3}
    INSTRUCTION_STEP = {ADD: 4, MULTIPLY: 4, END: 0, INPUT: 2, OUTPUT: 2, JNZ: 3, JZ: 3, LT: 4, EQ: 4}

    # Modes
    IMMEDIATE = 1
    POSITION = 0

    def __init__(self, instructions):
        self.memory = instructions
        self.ip = 0
        self.instruction = self.ADD
        self.register = 0

        self.modes = []
        self.params = []
        self.write_address = 0
        self.output = ""
        self.input = 0
        self.jump_to_register = False

    def execute_program(self, args):
        self.input = args
        while self.memory[self.ip] != self.END:
            self.decode()
            self.load()
            self.exec()
            self.write()
            self.step()
            self.clear()

    #
    # Decode phase
    #
    def decode(self):
        # Read instruction
        instruction = str(self.memory[self.ip])
        self.instruction = int(instruction[-2:])

        # Decode modes
        modes = instruction[:-2]
        for i in range(len(modes) - 1, -1, -1):
            self.modes.append(int(modes[i]))

        # Add unmentioned modes
        len_diff = len(self.INPUT_OFFSET[self.instruction]) - len(self.modes)
        for i in range(0, len_diff):
            self.modes.append(self.POSITION)

        # Read params
        input_offsets = self.INPUT_OFFSET[self.instruction]
        for offset in input_offsets:
            self.params.append(self.memory[self.ip + offset])

        # Read write param
        self.write_address = self.memory[self.ip + self.OUTPUT_OFFSET[self.instruction]]

    #
    # Load phase
    #
    def load(self):
        for i in range(0, len(self.params)):
            if self.modes[i] == self.IMMEDIATE:
                continue
            elif self.modes[i] == self.POSITION:
                self.params[i] = self.memory[self.params[i]]

    #
    # Exec phase
    #
    def exec(self):
        # Probably should've gone with a state pattern
        if self.instruction == self.ADD:
            self.register = self.params[0] + self.params[1]
        elif self.instruction == self.MULTIPLY:
            self.register = self.params[0] * self.params[1]
        elif self.instruction == self.INPUT:
            self.register = self.input
        elif self.instruction == self.OUTPUT:
            pass
        elif self.instruction == self.JNZ:
            if self.params[0] != 0:
                self.jump_to_register = True
                self.register = self.params[1]
        elif self.instruction == self.JZ:
            if self.params[0] == 0:
                self.jump_to_register = True
                self.register = self.params[1]
        elif self.instruction == self.EQ:
            self.register = 1
            if self.params[0] != self.params[1]:
                self.register = 0
        elif self.instruction == self.LT:
            self.register = 1
            if self.params[0] >= self.params[1]:
                self.register = 0
        else:
            raise Exception("Somethings wrong")

    #
    # Write phase
    #
    def write(self):
        if self.instruction in [self.ADD, self.MULTIPLY, self.INPUT, self.EQ, self.LT]:
            self.memory[self.write_address] = self.register
        elif self.instruction == self.OUTPUT:
            self.output = self.output + str(self.params[0])
        elif self.instruction in [self.JNZ, self.JZ]:
            pass
        else:
            raise Exception("Somethings wrong")

    #
    # Perform the step to the next instruction
    #
    def step(self):
        # Check if a custom ip has been set
        if self.jump_to_register:
            self.ip = self.register
            return
        # Otherwise perform default step
        self.ip = self.ip + self.INSTRUCTION_STEP[self.instruction]

    #
    # Clear lists so append doesn't mess up
    #
    def clear(self):
        self.modes = []
        self.params = []
        self.jump_to_register = False


if __name__ == "__main__":
    with open("instructions.json", "r") as instrFp:
        instr = json.load(instrFp)
        calc = IntCalculator(instr)
        calc.execute_program(5)
        print(calc.memory)
        print(calc.output)
