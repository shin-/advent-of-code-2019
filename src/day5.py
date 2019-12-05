data = '''
3,225,1,225,6,6,1100,1,238,225,104,0,2,171,209,224,1001,224,-1040,224,4,224,
102,8,223,223,1001,224,4,224,1,223,224,223,102,65,102,224,101,-3575,224,224,
4,224,102,8,223,223,101,2,224,224,1,223,224,223,1102,9,82,224,1001,224,-738,
224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1101,52,13,224,1001,224,
-65,224,4,224,1002,223,8,223,1001,224,6,224,1,223,224,223,1102,82,55,225,1001,
213,67,224,1001,224,-126,224,4,224,102,8,223,223,1001,224,7,224,1,223,224,223,
1,217,202,224,1001,224,-68,224,4,224,1002,223,8,223,1001,224,1,224,1,224,223,
223,1002,176,17,224,101,-595,224,224,4,224,102,8,223,223,101,2,224,224,1,224,
223,223,1102,20,92,225,1102,80,35,225,101,21,205,224,1001,224,-84,224,4,224,
1002,223,8,223,1001,224,1,224,1,224,223,223,1101,91,45,225,1102,63,5,225,1101,
52,58,225,1102,59,63,225,1101,23,14,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,
0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,
99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,
99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,
1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1008,
677,677,224,1002,223,2,223,1006,224,329,101,1,223,223,1108,226,677,224,1002,
223,2,223,1006,224,344,101,1,223,223,7,677,226,224,102,2,223,223,1006,224,359,
1001,223,1,223,8,677,226,224,102,2,223,223,1005,224,374,1001,223,1,223,1107,677,
226,224,102,2,223,223,1006,224,389,1001,223,1,223,1008,226,226,224,1002,223,
2,223,1005,224,404,1001,223,1,223,7,226,677,224,102,2,223,223,1005,224,419,
1001,223,1,223,1007,677,677,224,102,2,223,223,1006,224,434,1001,223,1,223,107,
226,226,224,1002,223,2,223,1005,224,449,1001,223,1,223,1008,677,226,224,102,2,
223,223,1006,224,464,1001,223,1,223,1007,677,226,224,1002,223,2,223,1005,224,
479,1001,223,1,223,108,677,677,224,1002,223,2,223,1006,224,494,1001,223,1,223,
108,226,226,224,1002,223,2,223,1006,224,509,101,1,223,223,8,226,677,224,102,2,
223,223,1006,224,524,101,1,223,223,107,677,226,224,1002,223,2,223,1005,224,539,
1001,223,1,223,8,226,226,224,102,2,223,223,1005,224,554,101,1,223,223,1108,677,
226,224,102,2,223,223,1006,224,569,101,1,223,223,108,677,226,224,102,2,223,223,
1006,224,584,1001,223,1,223,7,677,677,224,1002,223,2,223,1005,224,599,101,1,
223,223,1007,226,226,224,102,2,223,223,1005,224,614,1001,223,1,223,1107,226,
677,224,102,2,223,223,1006,224,629,101,1,223,223,1107,226,226,224,102,2,223,
223,1005,224,644,1001,223,1,223,1108,677,677,224,1002,223,2,223,1005,224,659,
101,1,223,223,107,677,677,224,1002,223,2,223,1006,224,674,1001,223,1,223,4,223,
99,226
'''

program = [x for x in data.split(',')]

def get_int(stream, pos):
  try:
    return int(stream[pos])
  except IndexError:
    print(pos)
    raise

def get_params(stream, opcode, position, n):
  params = []
  modes = reversed(str(opcode)[:-2])
  for i in range(1, n + 1):
    try:
      mode = next(modes)
      if mode == '1':
        params.append(get_int(stream, position + i))
        continue
    except StopIteration:
      pass
    params.append(get_int(stream, get_int(stream, position + i)))
  return params

def exec_math_op(stream, opcode, optype, position):
  params = get_params(stream, opcode, position, 2)
  if optype == 1:
    val = params[0] + params[1]
  else:
    val = params[0] * params[1]
  stream[int(stream[position + 3])] = val
  return position + 4

def exec_write_op(stream, position, input_val):
  address = int(stream[position + 1])
  stream[address] = input_val
  return position + 2

def exec_read_op(stream, position):
  address = int(stream[position + 1])
  print(f'Opcode 4 output: {stream[address]}')
  return position + 2

def exec_jump(stream, opcode, iftrue, position):
  params = get_params(stream, opcode, position, 2)
  if (params[0] != 0) == iftrue:
    return params[1]
  return position + 3

def exec_comparison(stream, opcode, optype, position):
  params = get_params(stream, opcode, position, 2)
  if (optype == 7):
    val = 1 if params[0] < params[1] else 0
  else:
    val = 1 if params[0] == params[1] else 0
  stream[int(stream[position + 3])] = val
  return position + 4

def execute_next(stream, position, input_val):
  opcode = stream[position]
  optype = int(str(opcode)[-2:])

  new_pos = 0
  if optype == 1 or optype == 2:
    new_pos = exec_math_op(stream, opcode, optype, position)
  elif optype == 3:
    new_pos = exec_write_op(stream, position, input_val)
  elif optype == 4:
    new_pos = exec_read_op(stream, position)
  elif optype == 5 or optype == 6:
    new_pos = exec_jump(stream, opcode, optype == 5, position)
  elif optype in (7, 8):
    new_pos = exec_comparison(stream, opcode, optype, position)
  elif optype == 99:
    return False, 0
  else:
    print(stream)
    raise Exception('Invalid operation code {} at position {}'.format(opcode, position))


  return True, new_pos


def run_program(stream, input_val=0):
  pointer = 0
  while True:
    cont, pointer = execute_next(stream, pointer, input_val)
    if not cont:
      break

  print(stream)
  return stream[0]

run_program(program, 5)
