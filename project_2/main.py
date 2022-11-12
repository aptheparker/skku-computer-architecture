#!/usr/binary/python3
import sys

filename = sys.argv[1]
N = int(sys.argv[2])
hexa = []
binary = []

counter = 0

#read file
with open(filename, 'rb') as byte_file:

    for i in range(4*N):
      byte = byte_file.read(1) #read 1 byte = 8 bits
      if len(byte) == 0:
        break

      else:
        if len(hex(ord(byte))) == 3: #length
          hexa.append("0x0" + str(hex(ord(byte))[-1]))
        else:
          hexa.append(str(hex(ord(byte))))

      binary.append("0b" + '0' * (10 - len(bin(ord(byte)))) + str(bin(ord(byte))[2:]))
      counter += 1
    
byte_file.close()

if counter < 4*N:
  print('No more instructions')

#sorted lists (hexa and binary)
count = 3 #count
sorted_hexa = []
sorted_binary = []
while (count < len(hexa)):
  sorted_hexa.append(hexa[count])
  sorted_binary.append(binary[count])
  if (count % 4 == 0):
    count += 7
    continue
  count -= 1
  
#inst lists (hexa and bin)
inst_hexa = []
inst_binary = []
for i in range(len(sorted_hexa)):
  if (i % 4 == 0):
    inst_hexa.append(sorted_hexa[i][2:])
    inst_binary.append(sorted_binary[i][2:])
  else:
    inst_hexa[i // 4] += sorted_hexa[i][2:]
    inst_binary[i // 4] += sorted_binary[i][2:]

def unsigned(n):
  return n & 0xffffffff


#define
def register(rs): #register name
  output = 0
  exp = 1
  for i in range(len(rs)):
    output += (int(rs[len(rs) - 1 - i]) * exp)
    exp *= 2
  return output

registers = [] #all registers
for i in range(32):
  registers.append(register('00000'))

def final(x):
  return x % (2**32)

def s2u(x):
  if x >= 0:
    return x
  else:
    return x + 2**32

def dec2hex(input):
  if input < 0:
    input += 2**32
  if len(str(hex(input))) >= 10:
    return str(hex(input % (2**32)))
  else:
    return "0x" + "0" * (10 - len(str(hex(input)))) + str(hex(input))[2:]

def shamt_int_imm(imm):
  output = 0
  exp = 1
  for i in range(len(imm)):
    output += (int(imm[len(imm) - 1 - i]) * exp)
    exp *= 2
  return output

def s_int_imm(imm):
  output = 0
  exp = 1
  if int(imm[0]) == 1:
    output = -(2**(len(imm) - 1))
    for i in range(len(imm) - 1):
      output += (int(imm[len(imm) - 1 - i]) * exp)
      exp *= 2
  else:
    for i in range(len(imm) - 1):
      output += (int(imm[len(imm) - 1 - i]) * exp)
      exp *= 2
  return output

def u_int_imm(imm):
  output = 0
  exp = 2**12
  if int(imm[0]) == 1:
    output = -(2**(len(imm) - 1 + 12))
    for i in range(len(imm) - 1):
      output += (int(imm[len(imm) - 1 - i]) * exp)
      exp *= 2

  else:
    for i in range(len(imm) - 1) :
      output += (int(imm[len(imm) - 1 - i]) * exp)
      exp *= 2
  return output

#types
type_U = ["0110111", "0010111"]
type_I = ["1100111", "0000011", "0010011"]
type_R = ["0110011"]

for i in range(len(inst_hexa)):
  opcode = inst_bin[i][25:32]
  if opcode in U_type:
    imm = inst_bin[i][:20]
    rd = inst_bin[i][20:25]

    if opcode == "0110111":
      #lui
      registers[register(rd)] = final(u_int_imm(imm))

  elif opcode in I_type:
    imm = inst_binary[i][:12]
    rs1 = inst_binary[i][12:17]
    funct3 = inst_binary[i][17:20]
    rd = inst_binary[i][20:25]

    if funct3 == "000":
      #addi
      registers[register(rd)] = final((registers[register(rs1)] + s_int_imm(imm)))

    elif funct3 == "010":
      #slti
      if x[registers(rs1)] >= 2**31:
        temp = registers[register(rs1)] - 2**32
      else:
        temp = registers[register(rs1)]
      if temp < (s_int_imm(imm)):
        x[name_regs(rd)] = 1
      else:
        x[name_regs(rd)] = 0

    elif funct3 == "011":
      #sltui
      if (x[name_regs(rs1)] < (s_int_imm(imm))):
        x[name_regs(rd)] = 1
      else:
        x[name_regs(rd)] = 0

    elif funct3 == "100":
      #xori
      x[name_regs(rd)] = int((s_int_imm(imm)) ^ (x[name_regs(rs1)]))

    elif funct3 == "110":
      #ori
      x[name_regs(rd)] = int((s_int_imm(imm)) | (x[name_regs(rs1)]))

    elif funct3 == "111":
      #andi
      x[name_regs(rd)] = final(int((s_int_imm(imm)) & (x[name_regs(rs1)])))

    elif funct3 == "001":
      shamt = imm[7:]
      if imm[:7] == "0000000":
        #slli
        x[name_regs(rd)] = final(
          int((x[name_regs(rs1)]) << shamt_int_imm(shamt)))

    elif funct3 == "101":
      shamt = imm[7:]
      if imm[:7] == "0000000":
        #srli
        x[name_regs(rd)] = final(
          int((x[name_regs(rs1)]) >> shamt_int_imm(shamt)))

      elif imm[:7] == "0100000":
        #srai
        x[name_regs(rd)] = 0
        if x[name_regs(rs1)] >= 2**31:
          for i in range(shamt_int_imm(shamt)):
            x[name_regs(rd)] += 2**(31 - i)
        x[name_regs(rd)] += int(
          (x[name_regs(rs1)]) >> (shamt_int_imm(shamt)))

  elif opcode in R_type:
    funct7 = inst_bin[i][:7]
    rs2 = inst_bin[i][7:12]
    rs1 = inst_bin[i][12:17]
    funct3 = inst_bin[i][17:20]
    rd = inst_bin[i][20:25]

    if funct7 == "0000000":
      if funct3 == "000":
        #add
        x[name_regs(rd)] = final(x[name_regs(rs1)] + x[name_regs(rs2)])

      elif funct3 == "001":
        #sll
        x[name_regs(rd)] = final(x[name_regs(rs1)] << x[name_regs(rs2)])

      elif funct3 == "010":
        #slt
        if (x[name_regs(rs1)] >= 2**31):
          temp1 = x[name_regs(rs1)] - 2**32
        else:
          temp1 = x[name_regs(rs1)]

        if (x[name_regs(rs2)] >= 2**31):
          temp2 = x[name_regs(rs2)] - 2**32
        else:
          temp2 = x[name_regs(rs2)]

        if (temp1 < temp2):
          x[name_regs(rd)] = 1
        else:
          x[name_regs(rd)] = 0

      elif funct3 == "011":
        #sltu
        if (s2u(x[name_regs(rs1)]) < s2u(x[name_regs(rs2)])):
          x[name_regs(rd)] = 1
        else:
          x[name_regs(rd)] = 0

      elif funct3 == "100":
        #xor
        x[name_regs(rd)] = final((x[name_regs(rs1)]) ^ (x[name_regs(rs2)]))

      elif funct3 == "101":
        #srl
        x[name_regs(rd)] = final((x[name_regs(rs1)]) >> x[name_regs(rs2)])

      elif funct3 == "110":
        #or
        x[name_regs(rd)] = final((x[name_regs(rs1)]) | (x[name_regs(rs2)]))

      elif funct3 == "111":
        #and
        x[name_regs(rd)] = final((x[name_regs(rs1)]) & (x[name_regs(rs2)]))

    elif funct7 == "0100000":
      if funct3 == "000":
        #sub
        x[name_regs(rd)] = final(x[name_regs(rs1)] - x[name_regs(rs2)])

      elif funct3 == "101":
        #sra
        x[name_regs(rd)] = 0
        if (x[name_regs(rs1)] >= 2**31):
          for i in range(x[name_regs(rs2)]):
            x[name_regs(rd)] += 2**(31 - i)
        x[name_regs(rd)] += final((x[name_regs(rs1)]) >> x[name_regs(rs2)])

for i in range(32):
  print(f"x{i}: {dec2hex(registers[i])} ", end='\n')