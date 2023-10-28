from circuit import op
from bfcl import circuit, gate, operation

import circuit as circuit_

# Initialize the circuit
c = circuit_.circuit()

# Bit width
n_bits = 16

# Inputs
inputs = [c.gate(op.id_, is_input=True) for _ in range(n_bits)]

# If any of the bits is '1', the ORed result will be '1'.
# We start by ORing the first two bits, then OR that result with the next bit, and so on.
or_result = c.gate(op.or_, [inputs[0], inputs[1]])

for i in range(2, n_bits):
    or_result = c.gate(op.or_, [or_result, inputs[i]])

# If all bits are '0', the negated ORed result will be '1'.
not_gate = c.gate(op.not_, [or_result])

# Making the final gate an output gate with identity operation
output = c.gate(op.id_, [not_gate], is_output=True)

#Output in Bristol Fashion
circuit(c).emit().split('\n')

def is_zero_eval(bin_str):
    """Evaluates if the binary string represents zero."""
    inputs_vals = list(map(int, bin_str))
    outputs = c.evaluate(inputs_vals)
    return outputs[0]  # 1 if equal to zero, 0 otherwise

# Test
for i in range(2**n_bits):
    bin_rep = format(i, f'0{n_bits}b')
    print(f"{bin_rep}: {is_zero_eval(bin_rep)}")
