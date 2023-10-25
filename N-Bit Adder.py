from circuit import op
from bfcl import circuit, gate, operation

# Implementation of the Full Adder
import circuit as circuit_
c = circuit_.circuit()

# Change this to set the bit width
n_bits = 16

# Create lists to hold the gates
g_and = []
g_xor = []
g_or = []

inputs = [c.gate(op.id_, is_input=True) for _ in range(2 * n_bits + 1)]

for i in range(n_bits):
    a = inputs[i]
    b = inputs[i + n_bits]
    c_in = inputs[2 * n_bits]

    xor_gate = c.gate(op.xor_, [a, b])
    and_gate1 = c.gate(op.and_, [a, b])
    and_gate2 = c.gate(op.and_, [xor_gate, c_in])
    xor_gate2 = c.gate(op.xor_, [xor_gate, c_in])
    or_gate = c.gate(op.or_, [and_gate1, and_gate2])

    g_xor.append(xor_gate)
    g_and.extend([and_gate1, and_gate2])
    g_xor.append(xor_gate2)
    g_or.append(or_gate)

# The gates lists now hold the gates for the n-bit adder

carry_out = c.gate(op.id_, [g_or[-1]], is_output=True)
results = [c.gate(op.id_, [g_xor[i-1]], is_output=True) for i in range(n_bits)]

# Define the inputs_values with n_bits
input_values = [0] * (2 * n_bits + 1)  # Initialize with zeros
input_values[0] = 1  # Set the carry input (C) to 1 if needed

# Evaluate the adder with the input values
output_values = c.evaluate(input_values)

# Print the output values
print(output_values)

#Output in Bristol Fashion
circuit(c).emit().split('\n')
