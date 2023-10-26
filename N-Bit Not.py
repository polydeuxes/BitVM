from circuit import op
from bfcl import circuit, gate, operation

import circuit as circuit_
c = circuit_.circuit()

# Change this to set the bit width
n_bits = 16
g_not = []

inputs = [c.gate(op.id_, is_input=True) for _ in range(n_bits)]

for i in range(n_bits):
    a = inputs[i]

    not_gate = c.gate(op.not_, [a])

    g_not.append(not_gate)

results = [c.gate(op.id_, [g_not[i-1]], is_output=True) for i in range(n_bits)]

#Output in Bristol Fashion
circuit(c).emit().split('\n')
