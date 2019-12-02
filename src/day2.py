data = '1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,10,1,19,2,9,19,23,2,13,23,27,1,6,27'\
        ',31,2,6,31,35,2,13,35,39,1,39,10,43,2,43,13,47,1,9,47,51,1,51,13,55,1,'\
        '55,13,59,2,59,13,63,1,63,6,67,2,6,67,71,1,5,71,75,2,6,75,79,1,5,79,83,'\
        '2,83,6,87,1,5,87,91,1,6,91,95,2,95,6,99,1,5,99,103,1,6,103,107,1,107,'\
        '2,111,1,111,5,0,99,2,14,0,0'

base_stream = [int(x) for x in data.split(',')]

def execute_next(stream, position):
  operation = stream[position:position + 4]
  if operation[0] == 1:
    val = stream[operation[1]] + stream[operation[2]]
    stream[operation[3]] = val
  elif operation[0] == 2:
    val = stream[operation[1]] * stream[operation[2]]
    stream[operation[3]] = val
  elif operation[0] == 99:
    return False
  else:
    raise Exception('Invalid operation code {} at position {}'.format(operation[0], position))

  return True



def run_program(stream):
  pointer = 0
  while execute_next(stream, pointer):
    pointer += 4

  print(','.join([str(x) for x in stream]))
  return stream[0]


for noun in range(0, 100):
  for verb in range(0, 100):
    program = base_stream[:]
    program[1] = noun
    program[2] = verb
    result = run_program(program)
    if result == 19690720:
      print('Noun = {}, Verb = {}'.format(noun, verb))
      exit(0)
