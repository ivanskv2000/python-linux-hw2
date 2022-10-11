# Python and Linux &mdash; HW-2

<сюда картинку>

## Description
This project is devoted to creating a relatively simple line-input calculator. It works in three steps:
- Tokenize the input: clean out spaces, distinguish operators, operands, parentheses and other characters;
- Convert tokenized input into reverse Polish notation (RPN) using Dijkstra's algorithm;
- Evaluate RPN expression and return the answer.


## Usage
### Step 1. Set Up the Working Environment
To isolate project execution, first create and activate a python virtual environment in the project directory:
``` bash
cd path_to_project/
python -m venv ./venv
source venv/bin/activate 
```

This enables you to install all required packages from `requirements.txt`:
``` bash
pip install -r requirements.txt
```

### Step 2. Run the Calculator
Just run
``` bash
python3 run.py
```
The script does not require any command line arguments. You can ask for a quick overview via `python3 run.py -h`.

### Step 3 [optional]. Test using `pytest`
Automated tests are in the `test_cases.py` file. Of course, all predefined tests are passed successfully by the implementation, but you can add your own tests. To run pytest, do
```bash
pytest
```

## References
- Dijkstra's "shunting yard" algorithm: https://web.archive.org/web/20090605032748/http://montcs.bloomu.edu/~bobmon/Information/RPN/infix2rpn.shtml
- Evaluation of RPN expressions: https://ru.wikipedia.org/wiki/Обратная_польская_запись#Вычисления_на_стеке
- How to distinguish unary minus: http://compiler.su/kak-otlichit-unarnyj-minus-ot-binarnogo.php
