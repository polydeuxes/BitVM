from circuit import op
from bfcl import circuit, gate, operation

import circuit as circuit_
from circuit import op

n_bits = 16

# Initialize the circuit
c = circuit_.circuit()

# Selector input (S)
selector = c.gate(op.id_, is_input=True)

# A and B inputs
a_inputs = [c.gate(op.id_, is_input=True) for _ in range(n_bits)]
b_inputs = [c.gate(op.id_, is_input=True) for _ in range(n_bits)]

# NOT selector for A inputs
not_selector = c.gate(op.not_, [selector])

# AND gates for A and B
a_and_gates = [c.gate(op.and_, [a_inputs[i], not_selector]) for i in range(n_bits)]
b_and_gates = [c.gate(op.and_, [b_inputs[i], selector]) for i in range(n_bits)]

# OR gates to combine the results of A and B
or_gates = [c.gate(op.or_, [a_and_gates[i], b_and_gates[i]]) for i in range(n_bits)]

# Identity gates for output
outputs = [c.gate(op.id_, [or_gates[i]], is_output=True) for i in range(n_bits)]

# Output in Bristol Fashion
bristol_output = "\n".join(circuit(c).emit().split('\n'))
print(bristol_output)
