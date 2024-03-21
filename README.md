# DateDetective

## Introduction

DateDetective is a Python package that takes a machine learning approach to identifying the format of date strings. This tool is useful for many applications like web scraping where the amount of formats used to represent dates is many and there is no need for 100% accuracy.

## Compatible date formats

DateDetective's model is trained to predict what combination of Python datetime module format codes would make up a given string representation of a date. Currently the model can identify the following format codes:
| Format Code | Description | Examples |
| ----------- | ----------- | -------- |
| %d | Day of the month as zero-padded decimal number | 01, 02, ..., 30, 31 |
| %B | Month as full text name | January, February, March, ..., December |
| %b | Month as abrieviated text name | Jan, Feb, Mar, ..., Dec |
| %m | Month as a zero-padded decimal number | 01, 02, 03, ..., 12 |
| %Y | Year with century as decimal number | 1832, 1996, 2002, 2024 |
| %H | Hours as zero-padded decimal number (24 hour clock) | 00, 01, 02, ..., 22, 23, 24 |
| %I | Hours as zero-padded decimal number (12 hour clock) | 01, 02, 03, ..., 10, 11, 12 |
| %M | Minutes as zero-padded decimal number | 00, 01, 02, ..., 58, 59, 60 |
| %S | Seconds as zero-padded decimal number | 00, 01, 02, ..., 58, 59, 60 |
| %f | Microsecond as decimal number, zero-padded to six digits | 000000, 000001, ..., 999999 |
| %p | AM or PM | AM, PM |
| %Z | Time zone name as text | UTC, GMT, EAT, EDT |
| %z | Time zone as UTC offset decimal number | +0000, -1200, +1000 |

## Installation

Firstly you will need to ensure that the version of PyTorch that is best for you is installed in the Python environment you are using. If possible use CUDA as this should increase date detection speed. Currently PyTorch's website has an install command finder at:
https://pytorch.org/get-started/locally/

After PyTorch is installed you can install DateDetective via Pip.

```
pip install DateDetective
```

## Usage

### Import and Initialise

```python
from datedetective import DateDetective
dd = DateDetective()
```

By default DateDetective will use CUDA cores on your GPU (if available) for some of the calculations. If you do not want to use CUDA then initialise DateFinder like this:

```python
df = DateDetective(useCuda=False)
```

### Generate datetime module format string from date string

```python
>>>dd.get_format("30/12/2023 12:52:23")
'%d/%m/%Y %H:%M:%S'
```

### Create a datetime object string from date string

```python
>>>dd.get_datetime("30/12/2023 12:52:23")
datetime.datetime(2023, 12, 30, 12, 52, 23)
```

> It's important to remember that although DateFinder can be accurate it sometimes gets a date wrong.

### How it was trained

Take a look at my repo that is dedicated to the training of the DateDetective models for more information: [DateDetective Training GitHub Repo](https://github.com/RSalethorn/DateFinder-ModelDevelopment)

# License

Apache License 2.0. See LICENSE file.

# Contact

Rob Salethorn - rob@salethorn.com
Repo link - https://github.com/RSalethorn/DateDetective
