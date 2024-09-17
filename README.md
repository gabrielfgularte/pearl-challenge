# Pearl Coding Challenge

> Unfortunately, I wasn't able to get it working as expected. My algorithm keeps swapping two home buyers, and I'm out of ideas at the moment. Since I don't want to keep you waiting any longer for this solution, I'll submit it as is. Please note that one test won't pass (`tests.test_main.TestMainFunctions.test_sample_input_output`) due to the swapping issue. I apologize for that, and I'll continue working on the issue even after submitting the code. Thanks.

## Requirements

- Python >= 3.12
- `virtualenv`
- `pip`

## Setting Up

1. `virtualenv .venv` to create the virtual environment. You can name `.venv` whatever you want.
2. `source /.venv/bin/activate` to activate the virtual environment (or `.\.venv\Scripts\activate` if you're on Windows).
3. `pip install -r reqs.txt` to install project dependencies (most of them are dev libs, such `black` and `isort`).

## Running

`python main.py` to run the application. It will prompt you for an input file. If you don’t have one, simply leave the prompt blank, and it will use the default `input.txt` file located in the project folder. The program will then generate an `output.txt` file containing the result.

## Testing

`python -m unittest` to run tests.
