from circuit import op
from bfcl import circuit, gate, operation

import circuit as circuit_
n_bits = 8

c = circuit_.circuit()

Selector_u = c.gate(op.id_, is_input=True)
Selector_op1 = c.gate(op.id_, is_input=True)
Selector_op0 = c.gate(op.id_, is_input=True)
Selector_zx = c.gate(op.id_, is_input=True)
Selector_sw = c.gate(op.id_, is_input=True)
Input_X = [c.gate(op.id_, is_input=True) for _ in range(n_bits)]
Input_Y = [c.gate(op.id_, is_input=True) for _ in range(n_bits)]

# Virtual Constants
ZERO = c.gate(op.xor_, [Input_X[-1], Input_X[-1]])
ONE = c.gate(op.not_, [ZERO])
ZERO_Input = [ZERO for _ in range(n_bits)]  # Representing 0 for all bits

U_NOT = c.gate(op.not_, [Selector_u])
OP1_NOT = c.gate(op.not_, [Selector_op1])
OP0_NOT = c.gate(op.not_, [Selector_op0])
ZX_NOT = c.gate(op.not_, [Selector_zx])
SW_NOT = c.gate(op.not_, [Selector_sw])

# Lower_Selector1 for when the sw flag is 1, the X and Y inputs are swapped.
ALU_Lower_Selector1_D0 = [c.gate(op.and_, [Input_X[i], SW_NOT]) for i in range(n_bits)]
ALU_Lower_Selector1_D1 = [c.gate(op.and_, [Input_Y[i], Selector_sw]) for i in range(n_bits)]
ALU_Lower_Selector1_Output = [c.gate(op.or_, [ALU_Lower_Selector1_D0[i], ALU_Lower_Selector1_D1[i]]) for i in range(n_bits)]

ALU_Lower_Selector2_D0 = [c.gate(op.and_, [Input_Y[i], SW_NOT]) for i in range(n_bits)]
ALU_Lower_Selector2_D1 = [c.gate(op.and_, [Input_X[i], Selector_sw]) for i in range(n_bits)]
ALU_Lower_Selector2_Output = [c.gate(op.or_, [ALU_Lower_Selector2_D0[i], ALU_Lower_Selector2_D1[i]]) for i in range(n_bits)]

# Lower_Selector3 for when the zx flag is 1, the left operand is replaced with 0. 
ALU_Lower_Selector3_D0 = [c.gate(op.and_, [ALU_Lower_Selector1_Output[i], ZX_NOT]) for i in range(n_bits)]
ALU_Lower_Selector3_D1 = [c.gate(op.and_, [ZERO_Input[i], Selector_zx]) for i in range(n_bits)]
ALU_Lower_Selector3_Output = [c.gate(op.or_, [ALU_Lower_Selector3_D0[i], ALU_Lower_Selector3_D1[i]]) for i in range(n_bits)]

# Basic logic operations using ALU selectors
AND_Gates = [c.gate(op.and_, [ALU_Lower_Selector3_Output[i], ALU_Lower_Selector2_Output[i]]) for i in range(n_bits)]
OR_Gates = [c.gate(op.or_, [ALU_Lower_Selector3_Output[i], ALU_Lower_Selector2_Output[i]]) for i in range(n_bits)]
XOR_Gates = [c.gate(op.xor_, [ALU_Lower_Selector3_Output[i], ALU_Lower_Selector2_Output[i]]) for i in range(n_bits)]
NOT_Gates = [c.gate(op.not_, [ALU_Lower_Selector3_Output[i]]) for i in range(n_bits)]

# Virtual Adder
carry_bit = ZERO
VirtualAdder_XOR = []
VirtualAdder_AND = []
VirtualAdder_OR = []

# Following the fixed adder loop order, which starts from LSB.
for i in range(n_bits-1, -1, -1):
    a = ALU_Lower_Selector3_Output[i]
    b = ALU_Lower_Selector2_Output[i]


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
VirtualAdder_Result = VirtualAdder_XOR[::-1]

# Virtual Subtractor

# Compute the 2's complement of Y before the loop
complement_Y = [c.gate(op.not_, [ALU_Lower_Selector2_Output[i]]) for i in range(n_bits)]
borrow_bit = ONE  # Initialize with '1' for the 2's complement operation
VirtualSubtractor_XOR = []
VirtualSubtractor_OR = []

for i in range(n_bits-1, -1, -1):
    a = ALU_Lower_Selector3_Output[i]
    b = complement_Y[i]

    difference_bit = c.gate(op.xor_, [a, b])  # XOR operation generates the difference bit
    borrow_out_from_ab = c.gate(op.and_, [a, b])  # AND operation between a and b determines if a borrow is needed
    borrow_out_from_diff_and_borrow_bit = c.gate(op.and_, [difference_bit, borrow_bit])  # Borrow due to the previous stage and current difference
    difference_with_borrow_bit = c.gate(op.xor_, [difference_bit, borrow_bit])  # Generate the final difference bit considering the borrow
    overall_borrow_out = c.gate(op.or_, [borrow_out_from_ab, borrow_out_from_diff_and_borrow_bit])  # Determine if a borrow is propagated to the next stage
    
    borrow_bit = overall_borrow_out  # The current overall borrow out becomes the borrow for the next iteration

    VirtualSubtractor_XOR.append(difference_with_borrow_bit)
    VirtualSubtractor_OR.append(overall_borrow_out)

VirtualSubtractor_Result = VirtualSubtractor_XOR[::-1]

# Virtual Incrementer
increment_bit = ONE  # Start with '1' to increment
VirtualIncrementer_XOR = []
VirtualIncrementer_AND = []

for i in range(n_bits-1, -1, -1):
    a = ALU_Lower_Selector3_Output[i]

    sum_bit = c.gate(op.xor_, [a, increment_bit])  # XOR operation generates the sum bit for incrementing
    carry_out = c.gate(op.and_, [a, increment_bit])  # AND operation determines if a carry is needed to the next bit

    VirtualIncrementer_XOR.append(sum_bit)

    # The current carry out becomes the increment bit for the next iteration
    increment_bit = carry_out

VirtualIncrementer_Result = VirtualIncrementer_XOR[::-1]

# Virtual Decrementer
borrow_bit = ONE  # Start with '1' to decrement
VirtualDecrementer_XOR = []
VirtualDecrementer_AND = []

for i in range(n_bits-1, -1, -1):
    a = ALU_Lower_Selector3_Output[i]

    difference_bit = c.gate(op.xor_, [a, borrow_bit])  # XOR operation generates the difference bit for decrementing
    borrow_out = c.gate(op.and_, [c.gate(op.not_, [a]), borrow_bit])  # Generates a borrow if a=0 and borrow_bit=1

    VirtualDecrementer_XOR.append(difference_bit)
    VirtualDecrementer_AND.append(borrow_out)
    
    borrow_bit = borrow_out  # The current borrow out becomes the borrow bit for the next iteration

VirtualDecrementer_Result = VirtualDecrementer_XOR[::-1]

# LU_Selector1 for AND/OR
LU_Selector1_D0 = [c.gate(op.and_, [AND_Gates[i], OP0_NOT]) for i in range(n_bits)]
LU_Selector1_D1 = [c.gate(op.and_, [OR_Gates[i], Selector_op0]) for i in range(n_bits)]
LU_Selector1_Output = [c.gate(op.or_, [LU_Selector1_D0[i], LU_Selector1_D1[i]]) for i in range(n_bits)]

# LU_Selector2 for XOR/NOT
LU_Selector2_D0 = [c.gate(op.and_, [XOR_Gates[i], OP0_NOT]) for i in range(n_bits)]
LU_Selector2_D1 = [c.gate(op.and_, [NOT_Gates[i], Selector_op0]) for i in range(n_bits)]
LU_Selector2_Output = [c.gate(op.or_, [LU_Selector2_D0[i], LU_Selector2_D1[i]]) for i in range(n_bits)]

# LU_Selector3 for LU_Selector1 and LU_Selector2
LU_Selector3_D0 = [c.gate(op.and_, [LU_Selector1_Output[i], OP1_NOT]) for i in range(n_bits)]
LU_Selector3_D1 = [c.gate(op.and_, [LU_Selector2_Output[i], Selector_op1]) for i in range(n_bits)]
LU_Selector3_Output = [c.gate(op.or_, [LU_Selector3_D0[i], LU_Selector3_D1[i]]) for i in range(n_bits)]

# AU_Selector1 for ADD/SUB
AU_Selector1_ADD = [c.gate(op.and_, [VirtualAdder_Result[i], OP0_NOT]) for i in range(n_bits)]
AU_Selector1_INC = [c.gate(op.and_, [VirtualIncrementer_Result[i], Selector_op0]) for i in range(n_bits)]
AU_Selector1_Output = [c.gate(op.or_, [AU_Selector1_ADD[i], AU_Selector1_INC[i]]) for i in range(n_bits)]

# AU_Selector2 for INC/DEC
AU_Selector2_SUB = [c.gate(op.and_, [VirtualSubtractor_Result[i], OP0_NOT]) for i in range(n_bits)]
AU_Selector2_DEC = [c.gate(op.and_, [VirtualDecrementer_Result[i], Selector_op0]) for i in range(n_bits)]
AU_Selector2_Output = [c.gate(op.or_, [AU_Selector2_SUB[i], AU_Selector2_DEC[i]]) for i in range(n_bits)]

# AU_Selector3 for AU_Selector1 or AU_Selector2
AU_Selector3_D0 = [c.gate(op.and_, [AU_Selector1_Output[i], OP1_NOT]) for i in range(n_bits)]
AU_Selector3_D1 = [c.gate(op.and_, [AU_Selector2_Output[i], Selector_op1]) for i in range(n_bits)]
AU_Selector3_Output = [c.gate(op.or_, [AU_Selector3_D0[i], AU_Selector3_D1[i]]) for i in range(n_bits)]

# ALU_Selector for AU or LU
ALU_Upper_Selector_D0 = [c.gate(op.and_, [LU_Selector3_Output[i], U_NOT]) for i in range(n_bits)]
ALU_Upper_Selector_D1 = [c.gate(op.and_, [AU_Selector3_Output[i], Selector_u]) for i in range(n_bits)]
ALU_Upper_Selector_Output = [c.gate(op.or_, [ALU_Upper_Selector_D0[i], ALU_Upper_Selector_D1[i]]) for i in range(n_bits)]

# Marking the final ALU outputs
Final_Output = [c.gate(op.id_, [ALU_Upper_Selector_Output[i]], is_output=True) for i in range(n_bits)]

#Bristol Fashion output
print("\n".join(circuit(c).emit().split('\n')))

#Evaluate
from itertools import product

def evaluate_alu(u_val, op1_val, op0_val, zx_val, sw_val, X, Y):
    input_values = [u_val, op1_val, op0_val, zx_val, sw_val] + X + Y
    outputs = c.evaluate(input_values)
    return outputs

# Tester
matrix = list(product(range(2), repeat=n_bits))
operators = list(product(range(2), repeat=2))

for u_val in range(2):
    for op1, op0 in operators: 
        if u_val == 1:
            for zx_val in range(2):
                for sw_val in range(2):
                    for x_val in matrix:
                        for y_val in matrix:
                            output = evaluate_alu(u_val, op1, op0, zx_val, sw_val, list(x_val), list(y_val))
                            print(f"u: {u_val}, op1: {op1}, op0: {op0}, zx: {zx_val}, sw: {sw_val}, X: {x_val}, Y: {y_val} -> Output: {tuple(output)}")
        else:
            for x_val in matrix:
                for y_val in matrix:
                    output = evaluate_alu(u_val, op1, op0, 0, 0, list(x_val), list(y_val))  # default zx and sw to 0 when u = 0
                    print(f"u: {u_val}, op1: {op1}, op0: {op0}, zx: 0, sw: 0, X: {x_val}, Y: {y_val} -> Output: {tuple(output)}")

