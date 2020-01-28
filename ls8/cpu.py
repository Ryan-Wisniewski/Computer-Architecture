"""CPU functionality."""

import sys
# print('check here moron', sys.argv)

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 16 #change to 256
        self.reg = [0] * 8
        self.PC = 0
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001
        self.MUL = 0b10100010

    def ram_read(self, mar): #MAR (_Memory Address Register_) *ADDRESS*
        return self.reg[mar]

    def ram_write(self, mar, mdr): #MDR (_Memory Data Register_) *DATA VALUE*
        self.reg[mar] = mdr
        return self.ram[mar]

    def load(self):
        """Load a program into memory."""
        ##put this somewhere
        if len(sys.argv) != 2:
            print("Error")
            sys.exit(1)
        try:
            address = 0
            with open(sys.argv[1]) as f:
                for instruction in f:
                    split_excess = instruction.split('#')
                    split = split_excess[0].strip()
                    if split == '':
                        continue # ignores blank lines
                    self.ram[address] = int(split, 2)
                    address += 1
        except FileNotFoundError:
            print(f"FileNotFound: {sys.argv}")
            sys.exit(2)
            


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')


    def run(self):
        """Run the CPU."""
        is_running = True

        while is_running:
            r = self.ram[self.PC]

            if r == self.HLT:
                print('HALTING PLEASE WAIT...')
                is_running = False
            elif r == self.LDI:
                mar = self.ram[self.PC + 1]
                mdr = self.ram[self.PC + 2]
                # print('hi', mar, mdr)
                self.ram_write(mar, mdr)
                self.PC += 3
            elif r == self.PRN:
                mar = self.ram[self.PC + 1]
                mdr = self.ram_read(mar)
                print(mdr, mar) #prints value at that specific address.
                self.PC += 2
            elif r == self.MUL:
                mar1 = self.ram[self.PC + 1]
                mar2 = self.ram[self.PC + 2]
                # mdr1 = self.ram_read(mar1)
                # mdr2 = self.ram_read(mar2)
                # print(mar1, mdr1, mar2, mdr2)
                self.alu('MUL', mar1, mar2)
                self.PC += 3
            else:
                print(f'Something unknown happened. Stop trying to break me...: {r}, {type(r)}')
                sys.exit(1)
        # print('areee matey', r, self.PC, self.reg, type(r))
