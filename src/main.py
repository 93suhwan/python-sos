import sys
import mylexer
import myparser
import ply.lex as lex
import ply.yacc as yacc
from semantics import Eval, Step
from memory import Memory
from printer import Printer
import os


def search(dirname):
    filenames = os.listdir(dirname)
    text_list = []

    for filename in filenames:
        full_filename = os.path.join(dirname, filename)
        text = open(full_filename, 'r').read()
        text_list.append(text)

    return filenames, text_list


def input_text():
    text_list = []
    filenames = []
    if len(sys.argv) == 1:
        text_list.append(input("input > "))
    elif len(sys.argv) == 2:
        filenames.append(sys.argv[1])
        text_list.append(open(sys.argv[1], 'r').read())
    elif len(sys.argv) == 3:
        if sys.argv[1] == '-d':
            filenames, text_list = search(sys.argv[2])

    if text_list == []:
        print("    1. python3 main.py \n" + \
              "    2. python3 main.py file_name \n" + \
              "    3. python3 main.py -d dir_name")
        sys.exit(1)

    return filenames, text_list


if __name__ == '__main__':
    filenames, text_list = input_text()
    lex.lex(module=mylexer)
    parser = yacc.yacc(module=myparser)

    count = 0
    for text in text_list:
        ast = parser.parse(text)

        print("filename : ", filenames[count], "\n")
        printer = Printer()
        printer.write(ast)
        print()
    
        memory1 = Memory()
        evaluator = Eval(ast, memory1)
        evaluator.eval()
        print('1. Big-step evaluation semantics:')
        print(memory1)

        memory2 = Memory()
        reducer = Step(ast, memory2)
        reducer.eval()
        print('2. Small-step evaluation semantics:')
        print(memory2)
        print()
        count += 1
