# Data Analysis with Python

This Python script performs statistical analysis on a given dataset and generates a frequency distribution table. It calculates various measures such as mean, mode, median, quartiles, deciles, and percentiles. The analysis is based on the input data and user-defined parameters.

## Requirements

- Python 3.6+
- numpy
- pandas
- tabulate

## Usage

1. Prepare your data in a text file named `data.txt`. The data should be integers separated by commas.
2. Run the script with `python main.py`.
3. Follow the prompts to choose the type of rounding and the quartile, decile, and percentile you want to find.

## Install dependencies using:

```bash
pip install numpy pandas tabulate
```

## Functionality

The script calculates the following:

- The number of data points (n)
- The range of the data (r)
- The number of classes (k), which is calculated based on the type of rounding you choose (ceiling or floor)
- The class width (i)
- The frequency distribution table

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
