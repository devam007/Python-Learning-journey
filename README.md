# Python Learning Journey

I am Devam Shah, learning Python, C++ DSA, and classical machine learning.
This repository records small projects and experiments as I develop those skills.

## Project 1: CSV Data Profiler

A standard-library command-line tool for inspecting a dataset before analysis.
It reports row counts, missing cells, distinct nonmissing values, and numeric
minimum, maximum, and mean. It rejects duplicate/blank headers and ragged rows.

```bash
python csv_profiler.py examples/study_sessions.csv
python csv_profiler.py examples/study_sessions.csv --output report.json
python -m unittest discover -s tests -v
```

Requires Python 3.12; no third-party dependencies. See the synthetic
[sample data](examples/study_sessions.csv) and its
[generated report](examples/study_sessions_report.json).

### Data rules and limitations

- Leading/trailing whitespace is trimmed; blank cells are missing.
- A numeric column must have only finite numeric nonmissing cells. Mixed text,
  NaN, and infinity cause the column to be treated as text.
- Distinct counts use trimmed text, so `1` and `1.0` are distinct cell strings.
- Empty files, duplicate headers, and inconsistent row widths give clear errors.
- Numeric cells and distinct values are retained in memory. This is a tool for
  small datasets, not streaming analysis of files larger than available RAM.
- Missingness does not automatically justify dropping rows or imputing values;
  those decisions depend on the dataset and analysis goal.

## What to learn from this project

1. Trace how `csv.reader` handles quoted commas and blank lines.
2. Explain the difference between missing, empty, and nonfinite numeric values.
3. Run the tests, deliberately introduce a bug, and explain which test detects it.
4. Add a feature yourself, such as a configurable missing-value marker, with tests.

## Related learning projects

- [ML Fundamentals with NumPy](https://github.com/devam007/ml-fundamentals-numpy)
- [Handwritten Digits Benchmark](https://github.com/devam007/digits-ml-benchmark)

## Learning goals

- Improve Python programming and data handling.
- Practise Git branches, commits, pull requests, and code review.
- Understand classical ML algorithms and evaluate them correctly.
- Make useful, tested open-source contributions.

Future entries will record experiments, results, and explanations as I learn.

