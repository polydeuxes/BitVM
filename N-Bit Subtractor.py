from circuit import op
from bfcl import circuit, gate, operation

import circuit as circuit_

# Initialize the circuit
c = circuit_.circuit()

# Bit width
n_bits = 4

# Inputs
inputs = [c.gate(op.id_, is_input=True) for _ in range(2 * n_bits)]

# Invert b
not_b = [c.gate(op.not_, [inputs[n_bits + i]]) for i in range(n_bits)]

# Adder logic
g_and = []
g_xor = []
g_or = []

# Initial carry-in for subtraction
carry_in = c.gate(op.xor_, [inputs[0], inputs[0]])  # This generates a '0'
carry_in = c.gate(op.not_, [carry_in])  # This generates a '1'

for i in range(n_bits):
    a = inputs[i]
    b = not_b[i]

    xor_gate = c.gate(op.xor_, [a, b])
    and_gate1 = c.gate(op.and_, [a, b])
    and_gate2 = c.gate(op.and_, [xor_gate, carry_in])
    xor_gate2 = c.gate(op.xor_, [xor_gate, carry_in])
    or_gate = c.gate(op.or_, [and_gate1, and_gate2])

    carry_in = or_gate

    g_xor.append(xor_gate2)
    g_and.extend([and_gate1, and_gate2])
    g_or.append(or_gate)

# Output
results = [c.gate(op.id_, [g_xor[i]], is_output=True) for i in range(n_bits)]

#Output in Bristol Fashion
circuit(c).emit().split('\n')

# Evaluate
for i in range(2**n_bits - 1, -1, -1):  # This will loop from 1111 down to 0000 for n_bits=4
    for j in range(2**n_bits):
        a_str = format(i, f'0{n_bits}b')
        b_str = format(j, f'0{n_bits}b')
        inputs_vals = list(map(int, a_str)) + list(map(int, b_str))
        outputs = c.evaluate(inputs_vals)
        result = ''.join(map(str, outputs))
        print(f"{a_str} - {b_str} = {result}")
