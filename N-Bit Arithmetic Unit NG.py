from circuit import op
from bfcl import circuit, gate, operation

import circuit as circuit_

n_bits = 4

# Initialize the main circuit
c = circuit_.circuit()

# Inputs for operations
Selector_0 = c.gate(op.id_, is_input=True)
Selector_1 = c.gate(op.id_, is_input=True)
Input_X = [c.gate(op.id_, is_input=True) for _ in range(n_bits)]
Input_Y = [c.gate(op.id_, is_input=True) for _ in range(n_bits)]

# Virtual Constants
ZERO = c.gate(op.xor_, [Input_X[-1], Input_X[-1]])
ONE = c.gate(op.not_, [ZERO])

# Virtual Adder
carry_bit = ZERO
VirtualAdder_XOR = []
VirtualAdder_AND = []
VirtualAdder_OR = []

# Following the fixed adder loop order, which starts from LSB.
for i in range(n_bits-1, -1, -1):
    a = Input_X[i]
    b = Input_Y[i]

    # Half Adder Step 1
    sum_temp = c.gate(op.xor_, [a, b])
    carry_temp = c.gate(op.and_, [a, b])

    # Half Adder Step 2
    sum_with_carry_bit = c.gate(op.xor_, [sum_temp, carry_bit])
    carry_from_sum_temp = c.gate(op.and_, [sum_temp, carry_bit])

    # OR gate to get final carry for next iteration
    overall_carry_out = c.gate(op.or_, [carry_temp, carry_from_sum_temp])

    carry_bit = overall_carry_out

    VirtualAdder_XOR.append(sum_with_carry_bit)
    VirtualAdder_OR.append(overall_carry_out)

# Reverse the order for XOR to get MSB to LSB ordering
VirtualAdder_XOR = VirtualAdder_XOR[::-1]

# Virtual Subtractor
borrow_bit = ONE  # Initialize with '1' for the 2's complement operation
VirtualSubtractor_XOR = []
VirtualSubtractor_AND = []
VirtualSubtractor_OR = []

complement_Y = [c.gate(op.not_, [Input_Y[i]]) for i in range(n_bits)]  # 2's complement operation begins with bitwise NOT

for i in range(n_bits-1, -1, -1):
    a = Input_X[i]
    b = complement_Y[i]

    difference_bit = c.gate(op.xor_, [a, b])  # XOR operation generates the difference bit
    borrow_out_from_ab = c.gate(op.and_, [a, b])  # AND operation between a and b determines if a borrow is needed
    borrow_out_from_diff_and_borrow_bit = c.gate(op.and_, [difference_bit, borrow_bit])  # Borrow due to the previous stage and current difference
    difference_with_borrow_bit = c.gate(op.xor_, [difference_bit, borrow_bit])  # Generate the final difference bit considering the borrow
    overall_borrow_out = c.gate(op.or_, [borrow_out_from_ab, borrow_out_from_diff_and_borrow_bit])  # Determine if a borrow is propagated to the next stage
    
    borrow_bit = overall_borrow_out  # The current overall borrow out becomes the borrow for the next iteration

    VirtualSubtractor_XOR.append(difference_with_borrow_bit)
    VirtualSubtractor_OR.append(overall_borrow_out)

VirtualSubtractor_XOR = VirtualSubtractor_XOR[::-1]

# Virtual Incrementer
increment_bit = ONE  # Start with '1' to increment
VirtualIncrementer_XOR = []
VirtualIncrementer_AND = []

for i in range(n_bits-1, -1, -1):
    a = Input_X[i]

    sum_bit = c.gate(op.xor_, [a, increment_bit])  # XOR operation generates the sum bit for incrementing
    carry_out = c.gate(op.and_, [a, increment_bit])  # AND operation determines if a carry is needed to the next bit

    VirtualIncrementer_XOR.append(sum_bit)

    # The current carry out becomes the increment bit for the next iteration
    increment_bit = carry_out

VirtualIncrementer_XOR = VirtualIncrementer_XOR[::-1]
    
# Virtual Decrementer
borrow_bit = ONE  # Start with '1' to decrement
VirtualDecrementer_XOR = []
VirtualDecrementer_AND = []

for i in range(n_bits-1, -1, -1):  # Reversed order
    a = Input_X[i]

    difference_bit = c.gate(op.xor_, [a, borrow_bit])  # XOR operation generates the difference bit for decrementing
    borrow_out = c.gate(op.and_, [c.gate(op.not_, [a]), borrow_bit])  # Generates a borrow if a=0 and borrow_bit=1

    VirtualDecrementer_XOR.append(difference_bit)
    VirtualDecrementer_AND.append(borrow_out)
    
    borrow_bit = borrow_out  # The current borrow out becomes the borrow bit for the next iteration

VirtualDecrementer_XOR = VirtualDecrementer_XOR[::-1]


# Virtual Selector 1 for ADD/SUB
VirtualSelector1_NOT = c.gate(op.not_, [Selector_0])
VirtualSelector1_ADD_Selected = [c.gate(op.and_, [VirtualAdder_XOR[i], VirtualSelector1_NOT]) for i in range(n_bits)]
VirtualSelector1_SUB_Selected = [c.gate(op.and_, [VirtualSubtractor_XOR[i], Selector_0]) for i in range(n_bits)]
VirtualSelector1_Output = [c.gate(op.or_, [VirtualSelector1_ADD_Selected[i], VirtualSelector1_SUB_Selected[i]]) for i in range(n_bits)]

# Virtual Selector 2 for INC/DEC
VirtualSelector2_NOT = c.gate(op.not_, [Selector_0])
VirtualSelector2_INC_Selected = [c.gate(op.and_, [VirtualIncrementer_XOR[i], VirtualSelector2_NOT]) for i in range(n_bits)]
VirtualSelector2_DEC_Selected = [c.gate(op.and_, [VirtualDecrementer_XOR[i], Selector_0]) for i in range(n_bits)]
VirtualSelector2_Output = [c.gate(op.or_, [VirtualSelector2_INC_Selected[i], VirtualSelector2_DEC_Selected[i]]) for i in range(n_bits)]

# Virtual Selector 3 for VirtualSelector1 and VirtualSelector2
VirtualSelector3_NOT = c.gate(op.not_, [Selector_1])
VirtualSelector3_AND = [c.gate(op.and_, [VirtualSelector1_Output[i], VirtualSelector3_NOT]) for i in range(n_bits)]
VirtualSelector3_OR = [c.gate(op.and_, [VirtualSelector2_Output[i], Selector_1]) for i in range(n_bits)]
VirtualSelector3_Output = [c.gate(op.or_, [VirtualSelector3_AND[i], VirtualSelector3_OR[i]]) for i in range(n_bits)]

# Final outputs
Final_Output = [c.gate(op.id_, [VirtualSelector3_Output[i]], is_output=True) for i in range(n_bits)]

#Bristol Fashion
print("\n".join(circuit(c).emit().split('\n')))

#Evaluate
from itertools import product

def evaluate_arithmetic_unit(op0_val, op1_val, X, Y):
    input_values = [op0_val, op1_val] + X + Y
    outputs = c.evaluate(input_values)
    return outputs

# Tester
matrix = list(product(range(2), repeat=n_bits))
operators = list(product(range(2), repeat=2))

for op0, op1 in operators:
    for x_val in matrix:
        for y_val in matrix:
            output = evaluate_arithmetic_unit(op0, op1, list(x_val), list(y_val))
            print(f"op0: {op0}, op1: {op1}, X: {x_val}, Y: {y_val} -> Output: {tuple(output)}")

print("\n".join(circuit(c).emit().split('\n')))
