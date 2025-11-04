"""
CSV Exporter Module for exporting table data and query results to CSV format.
Handles proper CSV formatting, special characters, and data type conversions.
"""

import csv
import io
import sqlite3
from typing import List, Any, Optional
from datetime import datetime
from .sql_security import validate_identifier, validate_sql_query, SQLSecurityError


def format_csv_filename(base_name: str) -> str:
    """
    Generate a descriptive CSV filename with timestamp.

    Args:
        base_name: Base name for the file (e.g., "users_table" or "query_results")

    Returns:
        Formatted filename with timestamp
    """
    timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    return f"{base_name}_{timestamp}.csv"


def export_table_to_csv(table_name: str) -> tuple[str, str]:
    """
    Export complete table data to CSV format.

    Args:
        table_name: Name of the table to export

    Returns:
        Tuple of (csv_content, filename)

    Raises:
        SQLSecurityError: If table name is invalid
        Exception: For database or export errors
    """
    # Validate table name to prevent SQL injection
    validate_identifier(table_name, "table")

    try:
        # Connect to database
        conn = sqlite3.connect("db/database.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Query all data from the table using safe identifier escaping
        query = f"SELECT * FROM [{table_name}]"
        cursor.execute(query)

        # Fetch all rows
        rows = cursor.fetchall()

        # Get column names
        if rows:
            columns = list(rows[0].keys())
        else:
            # For empty tables, get column info from pragma
            cursor.execute(f"PRAGMA table_info([{table_name}])")
            column_info = cursor.fetchall()
            columns = [col[1] for col in column_info]

        # Create CSV content in memory
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

        # Write headers
        writer.writerow(columns)

        # Write data rows
        for row in rows:
            # Convert Row object to list, handling None values
            row_data = []
            for col in columns:
                value = row[col]
                # Convert None to empty string for CSV
                if value is None:
                    row_data.append('')
                else:
                    row_data.append(str(value))
            writer.writerow(row_data)

        csv_content = output.getvalue()
        output.close()
        conn.close()

        # Generate filename
        filename = format_csv_filename(f"{table_name}_export")

        return csv_content, filename

    except sqlite3.Error as e:
        raise Exception(f"Database error exporting table '{table_name}': {str(e)}")
    except Exception as e:
        raise Exception(f"Error exporting table '{table_name}': {str(e)}")


def export_query_results_to_csv(query: str, params: Optional[List[Any]] = None) -> tuple[str, str]:
    """
    Export query results to CSV format.

    Args:
        query: SQL query to execute
        params: Optional query parameters for safe parameterization

    Returns:
        Tuple of (csv_content, filename)

    Raises:
        SQLSecurityError: If query contains dangerous operations
        Exception: For database or export errors
    """
    # Validate query for dangerous operations
    validate_sql_query(query)

    if params is None:
        params = []

    try:
        # Connect to database
        conn = sqlite3.connect("db/database.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Execute query with parameters if provided
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        # Fetch all results
        rows = cursor.fetchall()

        # Get column names
        if rows:
            columns = list(rows[0].keys())
        else:
            # For empty results, try to get column names from cursor description
            if cursor.description:
                columns = [desc[0] for desc in cursor.description]
            else:
                columns = []

        # Create CSV content in memory
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

        # Write headers if we have columns
        if columns:
            writer.writerow(columns)

        # Write data rows
        for row in rows:
            row_data = []
            for col in columns:
                value = row[col]
                # Convert None to empty string for CSV
                if value is None:
                    row_data.append('')
                else:
                    row_data.append(str(value))
            writer.writerow(row_data)

        csv_content = output.getvalue()
        output.close()
        conn.close()

        # Generate filename
        filename = format_csv_filename("query_results")

        return csv_content, filename

    except SQLSecurityError:
        # Re-raise security errors as-is
        raise
    except sqlite3.Error as e:
        raise Exception(f"Database error executing query: {str(e)}")
    except Exception as e:
        raise Exception(f"Error exporting query results: {str(e)}")


def handle_large_export(cursor: sqlite3.Cursor, columns: List[str], chunk_size: int = 10000) -> str:
    """
    Handle large dataset exports efficiently using chunking.

    Args:
        cursor: Database cursor with executed query
        columns: List of column names
        chunk_size: Number of rows to process at a time

    Returns:
        CSV content as string
    """
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

    # Write headers
    writer.writerow(columns)

    # Process rows in chunks
    while True:
        rows = cursor.fetchmany(chunk_size)
        if not rows:
            break

        for row in rows:
            row_data = []
            for col in columns:
                value = row[col]
                if value is None:
                    row_data.append('')
                else:
                    row_data.append(str(value))
            writer.writerow(row_data)

    csv_content = output.getvalue()
    output.close()
    return csv_content