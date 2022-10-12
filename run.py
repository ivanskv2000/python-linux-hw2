import calculator
import argparse

parser = argparse.ArgumentParser(
    description='Simple line-input calculator',
    epilog='''
    Usage is extremely simple. Just input a valid mathematical expression and press Enter. If you want to quit, send 'q'.
    '''
)
args = parser.parse_args()


class bcolors:
    """
    ANSI escape sequences (colorful terminal output)
    """

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'


calc = calculator.Calculator()

print(f"""
{bcolors.HEADER}Welcome to my calculator!{bcolors.ENDC}
Everything is simple: do math, then input 'q' to exit.

Supported operations: '+', '-', '*', '/', '^', '%'.

Docs: https://github.com/ivanskv2000/python-linux-hw2


""")

while True:
    query = input(f"{bcolors.BOLD}Enter math expression:{bcolors.ENDC} ")
    query = query.strip()

    if query == 'q':
        break

    try:
        result = bcolors.OKGREEN + str(calc.calculate(query)) + bcolors.ENDC
    except calculator.CalculatorError as e:
        result = bcolors.FAIL + e.message + bcolors.ENDC
    except ZeroDivisionError:
        result = "Division by zero is not allowed. Sorry!"
        result = bcolors.FAIL + result + bcolors.ENDC
    except BaseException as e:
        result = f"Unexpected error occured. Please check your input. <{e}>"
        result = bcolors.FAIL + result + bcolors.ENDC
    finally:
        print(result)
