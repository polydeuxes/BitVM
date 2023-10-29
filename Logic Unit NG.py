from circuit import op
from bfcl import circuit, gate, operation

import circuit as circuit_
from circuit import op

n_bits = 2

# Initialize the circuit
c = circuit_.circuit()

# Inputs for operations
Selector_0 = c.gate(op.id_, is_input=True)  # Selector for VirtualSelector1+2
Selector_1 = c.gate(op.id_, is_input=True)  # Selector for VirtualSelector3

Input_X = [c.gate(op.id_, is_input=True) for _ in range(n_bits)]
Input_Y = [c.gate(op.id_, is_input=True) for _ in range(n_bits)]

# Basic gates operations
AND_Gates = [c.gate(op.and_, [Input_X[i], Input_Y[i]]) for i in range(n_bits)]
OR_Gates = [c.gate(op.or_, [Input_X[i], Input_Y[i]]) for i in range(n_bits)]
XOR_Gates = [c.gate(op.xor_, [Input_X[i], Input_Y[i]]) for i in range(n_bits)]
NOT_Gates = [c.gate(op.not_, [Input_X[i]]) for i in range(n_bits)]

# Virtual Selector 1 for AND/OR
VirtualSelector1_NOT = c.gate(op.not_, [Selector_0])
VirtualSelector1_AND_Selected = [c.gate(op.and_, [AND_Gates[i], VirtualSelector1_NOT]) for i in range(n_bits)]
VirtualSelector1_OR_Selected = [c.gate(op.and_, [OR_Gates[i], Selector_0]) for i in range(n_bits)]
VirtualSelector1_Output = [c.gate(op.or_, [VirtualSelector1_AND_Selected[i], VirtualSelector1_OR_Selected[i]]) for i in range(n_bits)]

# Virtual Selector 2 for XOR/NOT
VirtualSelector2_NOT = c.gate(op.not_, [Selector_0])
VirtualSelector2_XOR_Selected = [c.gate(op.and_, [XOR_Gates[i], VirtualSelector2_NOT]) for i in range(n_bits)]
VirtualSelector2_NOT_Selected = [c.gate(op.and_, [NOT_Gates[i], Selector_0]) for i in range(n_bits)]
VirtualSelector2_Output = [c.gate(op.or_, [VirtualSelector2_XOR_Selected[i], VirtualSelector2_NOT_Selected[i]]) for i in range(n_bits)]

# Virtual Selector 3 for VirtualSelector1 and VirtualSelector2
VirtualSelector3_NOT = c.gate(op.not_, [Selector_1])
VirtualSelector3_AND = [c.gate(op.and_, [VirtualSelector1_Output[i], VirtualSelector3_NOT]) for i in range(n_bits)]
VirtualSelector3_OR = [c.gate(op.and_, [VirtualSelector2_Output[i], Selector_1]) for i in range(n_bits)]
VirtualSelector3_Output = [c.gate(op.or_, [VirtualSelector3_AND[i], VirtualSelector3_OR[i]]) for i in range(n_bits)]

# Final outputs
Final_Output = [c.gate(op.id_, [VirtualSelector3_Output[i]], is_output=True) for i in range(n_bits)]

def eval_circuit(op0_val, op1_val, X, Y):
    input_values = [op0_val, op1_val] + X + Y
    outputs = c.evaluate(input_values)
    return outputs

#Bristol Fashion
bristol_output = "\n".join(circuit(c).emit().split('\n'))
print(bristol_output)

# Evaluation
for op0_val in range(2):
    for op1_val in range(2):
        for i in range(2**n_bits):
            for j in range(2**n_bits):
                x_str = format(i, f'0{n_bits}b')
                y_str = format(j, f'0{n_bits}b')

                output = eval_circuit(op0_val, op1_val, [int(bit) for bit in x_str], [int(bit) for bit in y_str])
                result = ''.join(map(str, output))

                print(f"op0: {op0_val}, op1: {op1_val}, X: {x_str}, Y: {y_str} > Output: {result}")
