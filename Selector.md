from circuit import op
from bfcl import circuit, gate, operation

#Implementation of the Selector Switch
import circuit as circuit_
c = circuit_.circuit()

g0 = c.gate(circuit_.op.id_, is_input=True)
g1 = c.gate(op.id_, is_input=True)
g2 = c.gate(op.id_, is_input=True)

g3 = c.gate(op.not_, [g0])
g4 = c.gate(op.and_, [g0, g1])
g5 = c.gate(op.and_, [g3, g2])
g6 = c.gate(op.or_, [g4, g5])

g7 = c.gate(op.id_, [g6], is_output=True)

print(c.evaluate([0,0,1]))

inputs = [[0,0,0],
          [0,0,1],
          [0,1,0],
          [0,1,1],
          [1,0,0],
          [1,0,1],
          [1,1,0],
          [1,1,1]]
for i in inputs:
    print(c.evaluate(i))

#Output in Bristol Fashion
circuit(c).emit().split('\n')

## Result
#['5 8',
# '1 3',
# '1 1',
# '1 1 0 3 INV',
# '2 1 0 1 4 AND',
# '2 1 3 2 5 AND',
# '2 1 4 5 6 LOR',
# '1 1 6 7 LID']
