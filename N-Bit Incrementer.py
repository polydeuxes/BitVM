from circuit import op
from bfcl import circuit, gate, operation
from itertools import product #For Evaluation

import circuit as circuit_
c = circuit_.circuit()  

n_bits = 16

def n_bit_incrementer(n_bits):
    c = circuit_.circuit()
    
    # Inputs for the incrementer
    inputs = [c.gate(op.id_, is_input=True) for _ in range(n_bits)]

    g_xor = []
    g_and = []
    
    SET_ZERO = c.gate(op.xor_, [inputs[0], inputs[0]]) # Constant 0
    SET_ONE = c.gate(op.not_, [SET_ZERO])  # Constant 1

    for i in range(n_bits):
        # Adjust the index to access the inputs in descending order
        input_index = n_bits - 1 - i
        
        if i == 0:  # For the least significant bit
            xor_gate = c.gate(op.xor_, [inputs[input_index], SET_ONE])
            and_gate = c.gate(op.and_, [inputs[input_index], SET_ONE])
        else:
            xor_gate = c.gate(op.xor_, [inputs[input_index], g_and[i-1]])
            and_gate = c.gate(op.and_, [inputs[input_index], g_and[i-1]])
        
        g_xor.append(xor_gate)
        g_and.append(and_gate)

    # Outputs, constructed in descending order based on significance
    results = [c.gate(op.id_, [g_xor[n_bits - 1 - i]], is_output=True) for i in range(n_bits)]
    
    return c

## Evaluation

c = n_bit_incrementer(n_bits)

def evaluate_incrementer(circuit, input_bits):
    """
    Evaluate the n-bit incrementer circuit with the given input bits.
    :param circuit: The incrementer circuit.
    :param input_bits: The input bits for the incrementer.
    :return: The incremented output.
    """
    return circuit.evaluate(input_bits)

# Generate the full matrix for n_bits
matrix = list(product(range(2), repeat=n_bits))

for i in matrix:
    print(i, "->", evaluate_incrementer(c, list(i)))

## Bristol Fashion Export

c = n_bit_incrementer(n_bits)
print('\n'.join(circuit(c).emit().split('\n')))
