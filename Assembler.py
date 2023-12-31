import time
import re
import os
offset = 0
labels = {}
to_print = []
jumps = []
append_Flag = 0

#----------------------------------------------------------------------------------- Functions

def start():
    print("<<<Hey!>>>") 
    time.sleep(1)
    print("<<<Welcome to Assembler>>>")
    time.sleep(1)
    assemble_from_file()


# ----------------------------------------------------------------------


def convertFunc(number):
    return (binary_to_hex_dict[number[0][0:4]] + binary_to_hex_dict[number[0][4:8]] + " " +
     binary_to_hex_dict[number[0][8:12]] + binary_to_hex_dict[number[0][12:16]])


def convertFunc2(number):
    return (binary_to_hex_dict[number[0][0:4]] +
          binary_to_hex_dict[number[0][4:8]])


def convert16Func2(number):
    return ('66 ' + binary_to_hex_dict[number[0]
          [0:4]] + binary_to_hex_dict[number[0][4:8]])


def convert16Func(number):
    return ('66 ' + binary_to_hex_dict[number[0][0:4]] + binary_to_hex_dict[number[0][4:8]] +
          binary_to_hex_dict[number[0][8:12]] + binary_to_hex_dict[number[0][12:16]])

# ----------------------------------------------------------------------

def assemble(instruction, first_arg, second_arg):
    number = []
    global append_Flag
    if instruction == "JMP":
        to_print.append(" ")
        append_Flag = 1
    elif second_arg is None:
        # Handle cases where second_arg is None
        if first_arg in registers_32bit:
            number.append(instructionOpcode[instruction] + registers_32bit[first_arg])
            return convertFunc2(number)
        elif first_arg in registers_16bit:
            number.append(instructionOpcode[instruction] + registers_16bit[first_arg])
            return convert16Func2(number)
        elif first_arg in registers_8bit:
            number.append(instructionOpcode[instruction] + '00' + '11' + registers_8bit[first_arg])
            return convertFunc(number)
        elif first_arg in registers_32bit_MOD00:
            number.append(instructionOpcode[instruction] + '01' + '00' + registers_32bit_MOD00[first_arg])
            return convertFunc(number)
        elif first_arg in registers_16bit_MOD00:
            number.append(instructionOpcode[instruction] + '01' + '00' + registers_16bit_MOD00[first_arg])
            return convert16Func(number)
        elif first_arg in registers_8bit_MOD00:
            number.append(instructionOpcode[instruction] + '00' + '00' + registers_8bit_MOD00[first_arg])
            return convertFunc(number)
    else :
        if first_arg in registers_32bit and second_arg in registers_32bit:
            number.append(instructionOpcode[instruction]+'01' + '11' +
                        registers_32bit[second_arg]+registers_32bit[first_arg])
            return convertFunc(number)
        elif first_arg in registers_16bit and second_arg in registers_16bit:
            number.append(instructionOpcode[instruction]+'01' + '11' +
                        registers_16bit[second_arg]+registers_16bit[first_arg])
            return convert16Func(number)
        elif first_arg in registers_8bit and second_arg in registers_8bit:
            number.append(instructionOpcode[instruction] + '00' + '11' +
                        registers_8bit[second_arg] + registers_8bit[first_arg])
            return convertFunc(number)
        elif first_arg in registers_32bit_MOD00 and second_arg in registers_32bit:
            number.append(instructionOpcode[instruction] + '01' + '00' +
                        registers_32bit[second_arg] + registers_32bit_MOD00[first_arg])
            return convertFunc(number)
        elif first_arg in registers_32bit_MOD00 and second_arg in registers_16bit:
            number.append(instructionOpcode[instruction] + '01' + '00' +
                        registers_16bit[second_arg] + registers_32bit_MOD00[first_arg])
            return convert16Func(number)
        elif first_arg in registers_32bit_MOD00 and second_arg in registers_8bit:
            number.append(instructionOpcode[instruction] + '00' + '00' +
                        registers_8bit[second_arg] + registers_32bit_MOD00[first_arg])
            return convertFunc(number)
        elif first_arg in registers_32bit and second_arg in registers_32bit_MOD00:
            number.append(instructionOpcode[instruction] + '11' + '00' +
                        registers_32bit[first_arg] + registers_32bit_MOD00[second_arg])
            return convertFunc(number)
        elif first_arg in registers_16bit and second_arg in registers_32bit_MOD00:
            number.append(instructionOpcode[instruction] + '11' + '00' +
                        registers_16bit[first_arg] + registers_32bit_MOD00[second_arg])
            return convert16Func(number)
        elif first_arg in registers_8bit and second_arg in registers_32bit_MOD00:
            number.append(instructionOpcode[instruction] + '10' + '00' +
                        registers_8bit[first_arg] + registers_32bit_MOD00[second_arg])
            return convertFunc(number)
        elif first_arg in registers_32bit:
            number.append(
                instructionOpcode[instruction] + registers_32bit[first_arg])
            return convertFunc2(number)
        elif first_arg in registers_16bit:
            number.append(
                instructionOpcode[instruction] + registers_16bit[first_arg])
            return convert16Func2(number)
        else :
            print("invalid Shit Bruh")

# ----------------------------------------------------------------------


def calculate_16s_complement(negative_number):
    # Step 1: Convert the absolute value to hexadecimal
    hex_representation = hex(abs(negative_number))[2:]

    # Step 2: Calculate the 16's complement
    complement = ''.join([format(15 - int(digit, 16), 'X')
                         for digit in hex_representation])

    # Step 3: Add 1 to the result
    result = format(int(complement, 16) + 1, 'X')

    return result

# ----------------------------------------------------------------------

def assemble_from_file():
    file_path = "InputTest.txt"
    code = ""
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            code = file.read()
    else:
        print("File not found. Please check the file path.")
    #Spliting each line and get the instructions and ...
    lines = code.split('\n')
    global offset
    global append_Flag
    line_number = 0
    for line in lines:
        append_Flag = 0
        if line != '':
            line_number += 1
            
            component = re.split(r'\s|,\s*', line) 
            if ":" in line:
                arg1 = None
                arg2 = None
                Label1 = component[0].split(":")[0]
                labels[Label1] = offset
                to_print.append("0x000000000000000"+ str(offset - increase) + ": "+"NOTHING")

            else:
                instruction = component[0].upper()
                arg1 = component[1]
                if len(component) > 2:
                    arg2 = component[2]
                else: 
                    arg2 = None
                s = assemble(instruction,arg1,arg2)
                if append_Flag == 0 :
                    to_print.append("0x000000000000000" + str(offset) + ": " + s)
                    increase = len(s.replace(" ","")) // 2
                    offset += increase
                else :
                    jumps.append([len(to_print)-1,arg1,offset])
                    offset += 2
                    continue
        else :
            print("The file is Empty BRUHHHH!!")

# ----------------------------------------------------------------------
def jumpings():
    for i in jumps:
        WTF_Jumps(i[0], i[1], i[2])

# ----------------------------------------------------------------------

def WTF_Jumps(index , Label2 , Address ):
    out = ''
    label_address = labels[Label2] 
    Addressing = label_address - (Address + 2)
    if Addressing > 0 :
        out += "EB " + str(Addressing)
        to_print[index] = "0x000000000000000" + str(Address) + ": " + out

    elif Addressing < 0 :
        Siuuuuuu = calculate_16s_complement(Addressing) 
        out += "EB " + str(Siuuuuuu)
        to_print[index] = "0x000000000000000" + str(Address) + ": " + out


# ----------------------------------------------------------------------

def printings():
    for i in to_print:
        print( i ) 

# ----------------------------------------------------------------------------------- Dictionaries 

binary_to_hex_dict = {
    '0000': '0', '0001': '1', '0010': '2', '0011': '3', '0100': '4',
    '0101': '5', '0110': '6', '0111': '7', '1000': '8', '1001': '9',
    '1010': 'A', '1011': 'B', '1100': 'C', '1101': 'D', '1110': 'E', '1111': 'F'
}

registers_32bit = {'eax': "000", 'ebx': "011", 'ecx': '001', 'edx': '010', 'esi': '110', 'edi': '111', 'esp': '100',
                   'ebp': '101'}
registers_16bit = {'ax': "000", 'bx': "011", 'cx': '001', 'dx': '010', 'si': '110', 'di': '111', 'sp': '100',
                   'bp': '101'}
registers_8bit = {'al': '000', 'bl': '011', 'cl': '001', 'dl': '010', 'ah': '100', 'bh': '111', 'ch': '101',
                  'dh': '110'}

registers_8bit_MOD00 = {'[al]': '000', '[bl]': '011', '[cl]': '001', '[dl]': '010', '[ah]': '100', '[bh]': '111',
                        '[ch]': '101', '[dh]': '110'}
registers_16bit_MOD00 = {'[ax]': "000", '[bx]': "011", '[cx]': '001', '[dx]': '010', '[si]': '110', '[di]': '111',
                         '[sp]': '100', '[bp]': '101'}
registers_32bit_MOD00 = {'[eax]': "000", '[ebx]': "011", '[ecx]': '001', '[edx]': '010', '[esi]': '110', '[edi]': '111',
                         '[esp]': '100', '[ebp]': '101'}
instructionOpcode = {
    'ADD': '000000', 'SUB': '001010', 'AND': '001000', 'OR': '000010', 'XOR': '001100', 'PUSH': '01010',
    'POP': '01011', 'INC': '01000', 'DEC': '01001' , 'JMP' : 'EB'
}

# -----------------------------------------------------------------------------------
start()
jumpings()
printings()
