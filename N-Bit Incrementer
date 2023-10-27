from circuit import op
from bfcl import circuit, gate, operation

import circuit as circuit_
c = circuit_.circuit()  

n_bits = 8

def n_bit_incrementer(n_bits):
    c = circuit_.circuit()
    
    # Create a constant gate with output set to 0
    SET_ZERO = c.gate(op.id_, is_input=False)

    # Inputs for the incrementer
    inputs = [c.gate(op.id_, is_input=True) for _ in range(n_bits)]

    g_xor = []
    g_and = []
    
    SET_ONE = c.gate(op.not_, [SET_ZERO])  # This outputs a constant 1

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

# To get the Bristol Fashion output
c = n_bit_incrementer(n_bits)
print('\n'.join(circuit(c).emit().split('\n')))
