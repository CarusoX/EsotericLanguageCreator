
print('Please provide a word with 4 or more letters to build your language')

word = input().lower()

if len(word) < 4:
  print('Provide a word with 4 or more characters')
  exit(1)

def generate_language_words(word):
  letters = list(word)
  words = []
  for i in range(12):
    new_word = letters.copy()
    for j in range(4):
      if (1 << j) & i:
        new_word[j] = new_word[j].upper()
    words.append(''.join(new_word))
  return words

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def create_example_program(words):
  hello_world = [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 6, 6, 6, 6, 6, 6, 6, 4, 4, 6, 6, 6, 4, 8, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 5, 5, 5, 5, 5, 5, 5, 5, 4, 6, 6, 6, 4, 5, 5, 5, 5, 5, 5, 4, 5, 5, 5, 5, 5, 5, 5, 5, 4, 8, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4]
  program = chunks([words[x] for x in hello_world], 35)
  return '\n'.join(' '.join(x) for x in program)

lang_words = generate_language_words(word)

with open(f'runner_{word}.py', 'w+') as runner:
  runner.write('import sys\n\n')

  runner.write("command_to_code = {\n")
  runner.write(
      ''.join([f"  '{word}': {i},\n" for i, word in enumerate(lang_words)]))
  runner.write("}\n")

  runner.write("""
def parse_program(program):
  commands = []
  current_command = ''
  for i in range(len(program)):
    if program[i].isspace():
      if current_command != '':
        commands.append(current_command)
        current_command = ''
    else:
      current_command += program[i]

  if current_command != '':
    commands.append(current_command)

  return commands

memory_pos = 0
memory = []
instruction_pos = 0
register = None

def increase_memory():
  while len(memory) <= memory_pos:
    memory.append(0)
    
def read_from_memory():
  increase_memory()
  return memory[memory_pos]

def write_to_memory(what):
  increase_memory()
  memory[memory_pos] = what
  
def mod(x):
  return x % 256

def add(x):
  return x + 1

def sub(x):
  return x - 1

  
code_to_instruction = {}

def instruction_0(commands):
  global memory_pos, memory, instruction_pos, register
  instruction_pos -= 2 # skip previous one
  matched = 0
  while command_to_code[commands[instruction_pos]] != 7 or matched != 0:
    if command_to_code[commands[instruction_pos]] == 0:
      matched += 1
    if command_to_code[commands[instruction_pos]] == 7:
      matched -= 1
    instruction_pos -= 1
  # here we do not skip command 7

def instruction_1(commands):
  global memory_pos, memory, instruction_pos, register
  if memory_pos == 0:
    exit(1)
  memory_pos -= 1
  instruction_pos += 1

def instruction_2(commands):
  global memory_pos, memory, instruction_pos, register
  memory_pos += 1
  instruction_pos += 1

def instruction_3(commands):
  global memory_pos, memory, instruction_pos, register
  code_to_instruction[read_from_memory()]()
  instruction_pos += 1

def instruction_4(commands):
  global memory_pos, memory, instruction_pos, register
  if read_from_memory == 0:
    write_to_memory(ord(sys.stdin.read(1)))
  else:
    print(chr(mod(read_from_memory())), end='')
  instruction_pos += 1

def instruction_5(commands):
  global memory_pos, memory, instruction_pos, register
  write_to_memory(sub(read_from_memory()))
  instruction_pos += 1

def instruction_6(commands):
  global memory_pos, memory, instruction_pos, register
  write_to_memory(add(read_from_memory()))
  instruction_pos += 1

def instruction_7(commands):
  global memory_pos, memory, instruction_pos, register
  if read_from_memory() == 0:
    instruction_pos += 2 # skip next one
    matched = 0
    while command_to_code[commands[instruction_pos]] != 0 or matched != 0:
      if command_to_code[commands[instruction_pos]] == 0:
        matched -= 1
      if command_to_code[commands[instruction_pos]] == 7:
        matched += 1
      instruction_pos += 1
    instruction_pos += 1 # skip the 0 command
  else:
    instruction_pos += 1

def instruction_8(commands):
  global memory_pos, memory, instruction_pos, register
  write_to_memory(0)
  instruction_pos += 1

def instruction_9(commands):
  global memory_pos, memory, instruction_pos, register
  if register is None:
    register = read_from_memory()
  else:
    write_to_memory(register)
    register = None
  instruction_pos += 1

def instruction_10(commands):
  global memory_pos, memory, instruction_pos, register
  print(read_from_memory())
  instruction_pos += 1

def instruction_11(commands):
  global memory_pos, memory, instruction_pos, register
  write_to_memory(int(input()))
  instruction_pos += 1

code_to_instruction[0] = instruction_0
code_to_instruction[1] = instruction_1
code_to_instruction[2] = instruction_2
code_to_instruction[3] = instruction_3
code_to_instruction[4] = instruction_4
code_to_instruction[5] = instruction_5
code_to_instruction[6] = instruction_6
code_to_instruction[7] = instruction_7
code_to_instruction[8] = instruction_8
code_to_instruction[9] = instruction_9
code_to_instruction[10] = instruction_10
code_to_instruction[11] = instruction_11

def run_program(program):
  commands = parse_program(program)
  
  while instruction_pos < len(commands):
    code_to_instruction[command_to_code[commands[instruction_pos]]](commands)


if len(sys.argv) < 2:
  print('Please provide a file...')
  exit(1)
  
program = open(sys.argv[1]).read()
run_program(program)
""")

with open(f'hello_world.{word}', 'w+') as example:
  example.write(create_example_program(lang_words))
