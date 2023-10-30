from circuit import op
from bfcl import circuit, gate, operation

import circuit as circuit_

c = circuit_.circuit()

n_bits = 4
inputs = [c.gate(op.id_) for _ in range(2 * n_bits)]

# Creating a zero signal
ZERO = c.gate(op.xor_, [inputs[-1], inputs[-1]])

sums = []  # To hold sum outputs

carry = ZERO
for i in range(n_bits-1, -1, -1):  # Start from LSB, so reverse the loop order
    a = inputs[i]
    b = inputs[i + n_bits]
    
    # Half Adder Step 1
    sum_temp = c.gate(op.xor_, [a, b])
    carry_temp = c.gate(op.and_, [a, b])

    # Half Adder Step 2
    sum_final = c.gate(op.xor_, [sum_temp, carry])
    carry_from_sum_temp = c.gate(op.and_, [sum_temp, carry])

    # OR gate to get final carry for next iteration
    carry = c.gate(op.or_, [carry_temp, carry_from_sum_temp])
    
    sums.append(sum_final)

# The final carry out
carry_out_final = c.gate(op.id_, [carry], is_output=True)

# Making the sum bits outputs in the correct order
sum_outputs = [c.gate(op.id_, [bit], is_output=True) for bit in reversed(sums)]

#Evaluate
def test_circuit(n_bits, c):
    print(f"Testing for {n_bits} bits...\n")
    header_format = f"{'A'.rjust(n_bits)} {'B'.rjust(n_bits)} | {'Result'.rjust(n_bits)} {'Carry Out'}"
    print(header_format)
    print('-' * (len(header_format) + 1))

    for i in range(2**n_bits):
        for j in range(2**n_bits):
            a_str = format(i, f'0{n_bits}b')
            b_str = format(j, f'0{n_bits}b')
            inputs_vals = list(map(int, a_str)) + list(map(int, b_str))
            outputs = c.evaluate(inputs_vals)
            
            # Assuming the first output bit is the carry out
            carry_out = str(outputs[0])
            result = ''.join(map(str, outputs[1:]))
            
            print(f"{a_str} {b_str} | {result} {carry_out}")

test_circuit(n_bits, c)

#Output in Bristol Fashion
circuit(c).emit().split('\n')
