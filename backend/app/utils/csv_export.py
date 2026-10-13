"""CSV export utilities with formula injection protection."""
import csv
import io


def sanitize_for_csv(value):
    """Sanitize a value for CSV export to prevent formula injection.

    CSV formula injection occurs when a cell starts with =, +, -, @,
    which can be interpreted as formulas by spreadsheet applications.

    Args:
        value: The value to sanitize.

    Returns:
        Sanitized string safe for CSV export.
    """
    if value is None:
        return ''

    value = str(value)

    # Prefix with single quote if starts with dangerous characters
    if value and value[0] in ('=', '+', '-', '@', '\t', '\r'):
        value = "'" + value

    return value


def generate_csv_output(headers, rows):
    """Generate CSV output from headers and rows.

    Args:
        headers: List of column headers.
        rows: List of row lists.

    Returns:
        CSV string.
    """
    output = io.StringIO()
    writer = csv.writer(output)

    # Write headers
    writer.writerow(headers)

    # Write data rows with sanitization
    for row in rows:
        sanitized_row = [sanitize_for_csv(cell) for cell in row]
        writer.writerow(sanitized_row)

    output.seek(0)
    return output.getvalue()
