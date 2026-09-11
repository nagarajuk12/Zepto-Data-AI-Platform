"""
Script to perform database operations on books data set
"""
import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path(__file__).parent / "books.db"
CSV_PATH = Path(__file__).parent / "cleaned_books_dataset.csv"

def create_database(connection):
    """Create the normalized database schema."""
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories(
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT UNIQUE NOT NULL
    )
    """)
    print("categories table has been created")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books(
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        price_gbp REAL,
        price_inr REAL,
        rating INTEGER,
        in_stock INTEGER,
        category_id INTEGER,
        FOREIGN KEY(category_id)
        REFERENCES categories(category_id)
    )
""")
    print("books table has been created successfully")
    connection.commit()

def insert_data(connection, dataframe):
    """Insert cleaned book data (cleaned_books_dataset.csv data) into the tables."""
    cursor = connection.cursor()
    # Insert unique categories first
    categories = dataframe["category"].dropna().unique()
    for category in categories:
        cursor.execute(
            """
            INSERT OR IGNORE INTO categories (category_name)
            VALUES (?)
            """,
            (category,)
        )
    print("Categories data has been inserted successfully")
    # Insert books and connect them to their category
    for _, row in dataframe.iterrows():
        "Fetching category_id by category name"
        cursor.execute(
            """
            SELECT category_id
            FROM categories
            WHERE category_name = ?
            """,
            (row["category"],)
        )
        result = cursor.fetchone()
        if result is None:
            continue
        category_id = result[0]
        cursor.execute(
            """
            INSERT INTO books (
                title,
                price_gbp,
                price_inr,
                rating,
                in_stock,
                category_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                row["title"],
                row["price_gbp"],
                row["price_inr"],
                row["rating"],
                int(row["in_stock"]),
                category_id
            )
        )
    connection.commit()
    print("Books data has been inserted successfully")

def save_query_output(query_name, query, result):
    """Print and save SQL query and its output."""
    output_directory = Path(__file__).parent / "query_outputs"
    output_directory.mkdir(exist_ok=True)
    print(f"\n{'=' * 60}")
    print(query_name)
    print("=" * 60)
    print("SQL:")
    print(query.strip())
    print("\nOutput:")
    print(result.to_string(index=False))
    output_file = output_directory / f"{query_name}.csv"
    result.to_csv(output_file, index=False)
    query_file = output_directory / f"{query_name}.txt"
    query_file.write_text(query.strip(), encoding="utf-8")

def query_select_where(connection):
    """Execute SELECT and WHERE query."""
    query = """
    SELECT title, price_gbp, rating
            FROM books
            WHERE rating >= 1
    """
    result = pd.read_sql_query(query, connection)
    save_query_output("query_1_select_where", query, result)
    return result

def query_order_by(connection):
    """Execute ORDER BY query."""
    query = """
     SELECT title, price_gbp
            FROM books
            ORDER BY price_gbp DESC
    """
    result = pd.read_sql_query(query, connection)
    save_query_output("query_3_limit", query, result)
    return result

def query_limit(connection):
    """Execute LIMIT query."""
    query ="""
            SELECT title, rating
            FROM books
            ORDER BY rating DESC
            LIMIT 10
        """
    result = pd.read_sql_query(query, connection)
    save_query_output("query_3_limit", query, result)
    return result

def query_distinct(connection):
    """Execute DISTINCT query."""
    query = """
    SELECT DISTINCT rating
            FROM books
            ORDER BY rating
    """
    result = pd.read_sql_query(query, connection)
    save_query_output("query_4_distinct", query, result)
    return result

def query_between(connection):
    """Execute BETWEEN query."""
    query = """
     SELECT title, price_gbp
            FROM books
            WHERE price_gbp BETWEEN 10 AND 30
            ORDER BY price_gbp
    """
    result = pd.read_sql_query(query, connection)
    save_query_output("query_5_between", query, result)
    return result

def query_join(connection):
    """Execute JOIN query."""
    query = """
        SELECT
            books.book_id,
            books.title,
            books.price_gbp,
            books.rating,
            books.in_stock,
            categories.category_name
        FROM books
        JOIN categories
            ON books.category_id = categories.category_id
        ORDER BY books.rating DESC
        LIMIT 10
    """
    result = pd.read_sql_query(query, connection)
    save_query_output("query_6_join", query, result)
    return result

def validate_join_with_pandas(connection, sql_result):
    """Compare SQL JOIN result with pandas merge result."""
    books_df = pd.read_sql_query(
        "SELECT * FROM books",
        connection
    )
    categories_df = pd.read_sql_query(
        "SELECT * FROM categories",
        connection
    )
    merged_result = pd.merge(
        books_df,
        categories_df,
        on="category_id",
        how="inner"
    )
    merged_result = merged_result[
        [
            "book_id",
            "title",
            "price_gbp",
            "rating",
            "in_stock",
            "category_name"
        ]
    ]
    merged_result = (
        merged_result
        .sort_values(
            ["rating", "book_id"],
            ascending=[False, True]
        )
        .head(10)
        .reset_index(drop=True)
    )
    sql_result = sql_result.reset_index(drop=True)
    print("\nSQL JOIN - pd.read_sql:")
    print(sql_result.to_string(index=False))
    print("\nPandas JOIN - pd.merge:")
    print(merged_result.to_string(index=False))
    comparison = pd.concat(
        [
            sql_result.add_suffix("_sql"),
            merged_result.add_suffix("_pandas")
        ],
        axis=1
    )
    print("\nSide-by-side comparison:")
    print(comparison.to_string(index=False))
    results_match = sql_result.equals(merged_result)
    print(f"\nResults match: {results_match}")

    if not results_match:
        print("\nSQL dtypes:")
        print(sql_result.dtypes)
        print("\nPandas dtypes:")
        print(merged_result.dtypes)
        raise ValueError(
            "SQL JOIN and pandas merge results do not match."
        )

def run_queries(connection):
    """Execute all required SQL queries."""
    #SQL- Query - 1 : Execute SELECT and WHERE query.
    query_select_where(connection)
    #SQL - Query - 2 : Execute ORDER BY query.
    query_order_by(connection)
    #SQL - Query - 3 : Execute LIMIT query.
    query_limit(connection)
    #SQL - Query - 4 : Execute DISTINCT query.
    query_distinct(connection)
    #SQL - Query - 5 : Execute BETWEEN query.
    query_between(connection)
    #SQL - Query - 6 : Execute JOIN query
    #Save SQL JOIN output and use the result for validation
    join_result = query_join(connection)
    # Compare SQL JOIN with pandas merge
    validate_join_with_pandas(connection, join_result)

def main():
    """Create database, insert data, and execute SQL queries."""
    dataframe = pd.read_csv(CSV_PATH)
    print("books.db has been create successfully")
    connection = sqlite3.connect(DB_PATH)

    try:
        #create_database(connection)
        #insert_data(connection, dataframe)
        run_queries(connection)

    except sqlite3.OperationalError as error:
        print(f"Database operation error: {error}")
    finally:
        connection.close()

if __name__ == "__main__":
    main()
