"""Inspect a CSV file before using it in a data analysis or ML project."""

import argparse
import csv
import json
import math
from pathlib import Path


def profile_csv(path: str | Path) -> dict:
    """Summarize columns; reject ambiguous headers and inconsistent row widths.

    Whitespace-only cells count as missing. A column is numeric only when all
    nonmissing cells parse as finite floats. Distinct counts exclude missing cells.
    """
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.reader(stream)
        header = next(reader, None)
        if not header or any(not name.strip() for name in header):
            raise ValueError("CSV must have a nonempty header for every column.")
        header = [name.strip() for name in header]
        if len(set(header)) != len(header):
            raise ValueError("Column names must be unique after trimming whitespace.")
        columns = [{"missing": 0, "values": set(), "numbers": []} for _ in header]
        rows = 0
        for row in reader:
            if not row:  # Ignore completely blank lines, as csv.DictReader does.
                continue
            if len(row) != len(header):
                raise ValueError(
                    f"CSV line {reader.line_num} has {len(row)} cells; "
                    f"expected {len(header)}."
                )
            rows += 1
            for cell, column in zip(row, columns):
                value = cell.strip()
                if not value:
                    column["missing"] += 1
                    continue
                column["values"].add(value)
                try:
                    number = float(value)
                    if math.isfinite(number):
                        column["numbers"].append(number)
                except ValueError:
                    pass
        summary = {}
        for name, column in zip(header, columns):
            count = rows - column["missing"]
            numeric = count > 0 and len(column["numbers"]) == count
            summary[name] = {
                "type": "numeric" if numeric else "text" if count else "empty",
                "missing": column["missing"],
                "nonmissing": count,
                "distinct": len(column["values"]),
            }
            if numeric:
                numbers = column["numbers"]
                summary[name].update(
                    min=min(numbers),
                    max=max(numbers),
                    mean=math.fsum(x / count for x in numbers),
                )
        return {"rows": rows, "columns": summary}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--output", type=Path, help="Optional JSON report path")
    args = parser.parse_args()
    try:
        report = json.dumps(profile_csv(args.csv_file), indent=2, allow_nan=False)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(report + "\n", encoding="utf-8")
        else:
            print(report)
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(2, f"Error: {error}\n")


if __name__ == "__main__":
    main()
