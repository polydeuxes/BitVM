from circuit import op
from bfcl import circuit, gate, operation

import circuit as circuit_

n_bits = 8
c = circuit_.circuit()

LT = c.gate(op.id_, is_input=True)
EQ = c.gate(op.id_, is_input=True)
GT = c.gate(op.id_, is_input=True)
Input_X = [c.gate(op.id_, is_input=True) for _ in range(n_bits)]

# Initialize the first two inputs with an OR gate
or_result = c.gate(op.or_, [Input_X[0], Input_X[1]])

# For the subsequent bits, keep OR-ing with the result of the previous OR
for i in range(2, n_bits):
    or_result = c.gate(op.or_, [or_result, Input_X[i]])

# NOT the result of the final OR to get the IsZero output
IsZero = c.gate(op.not_, [or_result])

# For IsNegative:
IsNegative = Input_X[0]  # MSB directly indicates if it's negative

# For IsPositive:
IsPositive = c.gate(op.nor_, [IsZero, IsNegative])

# Connect conditions with their respective outputs
LT_Output = c.gate(op.and_, [LT, IsNegative])
EQ_Output = c.gate(op.and_, [EQ, IsZero])
GR_Output = c.gate(op.and_, [GT, IsPositive])

# Cascade the OR operation for the final output
FinalOutput0 = c.gate(op.or_, [LT_Output, EQ_Output])
FinalOrOutput = c.gate(op.or_, [FinalOutput0, GR_Output])
FinalOutput = c.gate(op.id_, [FinalOrOutput], is_output=True)

#Bristol Fashion output
print("\n".join(circuit(c).emit().split('\n')))

#Evaluation
def evaluate_condition_unit(LT, EQ, GT, X):
    input_values = [LT, EQ, GT] + X
    outputs = c.evaluate(input_values)
    return outputs

# Define the test cases for X based on n_bits
test_cases = [
    [0] * n_bits,                           # X is zero
    [1] + [0] * (n_bits - 1),               # MSB of X is 1
    [0] * (n_bits - 1) + [1]                # LSB of X is 1
]

# Iterate through the test cases
for x_val in test_cases:
    # Test with LT = 1, and EQ and GT = 0
    output = evaluate_condition_unit(1, 0, 0, x_val)
    print(f"LT: 1, EQ: 0, GT: 0, X: {x_val} -> Output: {output[0]}")
    
    # Test with EQ = 1, and LT and GT = 0
    output = evaluate_condition_unit(0, 1, 0, x_val)
    print(f"LT: 0, EQ: 1, GT: 0, X: {x_val} -> Output: {output[0]}")
    
    # Test with GT = 1, and LT and EQ = 0
    output = evaluate_condition_unit(0, 0, 1, x_val)
    print(f"LT: 0, EQ: 0, GT: 1, X: {x_val} -> Output: {output[0]}")
