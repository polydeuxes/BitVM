from circuit import op
from bfcl import circuit, gate, operation

import circuit as circuit_

n_bits = 4  # Replace with the desired number of bits

# Initialize the circuit
c = circuit_.circuit()

# Selector input (S)
selector = c.gate(op.id_, is_input=True)

# Data input (D)
data_inputs = [c.gate(op.id_, is_input=True) for _ in range(n_bits)]

# NOT selector for Bus A
not_selector = c.gate(op.not_, [selector])

# AND gates for Bus A and Bus B
bus_a_gates = [c.gate(op.and_, [data_inputs[i], not_selector]) for i in range(n_bits)]
bus_b_gates = [c.gate(op.and_, [data_inputs[i], selector]) for i in range(n_bits)]

# Identity gates for output (Bus A)
bus_a_outputs = [c.gate(op.id_, [bus_a_gates[i]], is_output=True) for i in range(n_bits)]

# Identity gates for output (Bus B)
bus_b_outputs = [c.gate(op.id_, [bus_b_gates[i]], is_output=True) for i in range(n_bits)]

def evaluate_switch(circuit, n_bits):
    results = []

    for s in [0, 1]:  # Selector input (S)
        for data_value in range(2**n_bits):  # Data input (D)
            s_str = str(s)
            data_str = format(data_value, f'0{n_bits}b')
            inputs_str = s_str + data_str

            inputs_vals = list(map(int, inputs_str))
            outputs = circuit.evaluate(inputs_vals)

            # Split the outputs into Bus A and Bus B parts
            bus_a_outputs = outputs[:n_bits]
            bus_b_outputs = outputs[n_bits:]

            result = f"S: {s}, D: {data_str} => Bus A: {''.join(map(str, bus_a_outputs))}, Bus B: {''.join(map(str, bus_b_outputs))}"
            results.append(result)

    return results

# Usage:
eval_results = evaluate_switch(c, n_bits)
for res in eval_results:
    print(res)

bristol_output = "\n".join(circuit(c).emit().split('\n'))
print(bristol_output)
