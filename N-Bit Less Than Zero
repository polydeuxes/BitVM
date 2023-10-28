from circuit import op
from bfcl import circuit, gate, operation

import circuit as circuit_
from circuit import op

# Initialize the circuit
c = circuit_.circuit()

# Bit width
n_bits = 4  # Change this for different bit widths

# Inputs
inputs = [c.gate(op.id_, is_input=True) for _ in range(n_bits)]

# The MSB is the sign bit in two's complement notation
msb = inputs[0]

# If MSB is '1', the number is negative. Thus, directly use MSB as the output.
output = c.gate(op.id_, [msb], is_output=True)

# Output in Bristol Fashion
print('\n'.join(circuit(c).emit().split('\n')))

# Evaluate
# Convert integer to binary string of a given length.
to_bin_str = lambda value, length=n_bits: format(value, f'0{length}b')

for i in range(2**n_bits):
    a_str = to_bin_str(i, n_bits)
    inputs_vals = list(map(int, a_str))
    outputs = c.evaluate(inputs_vals)
    
    result = ''.join(map(str, outputs))
    print(f"{a_str} < 0 = {result}")
