import sqlite3
import os

DATABASE_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "smartdocqa.db"
)


class Database:

    def __init__(self):

        os.makedirs(
            os.path.dirname(DATABASE_PATH),
            exist_ok=True
        )

        self.conn = sqlite3.connect(
            DATABASE_PATH,
            check_same_thread=False
        )

        self.create_tables()

    # =========================
    # CREATE TABLES
    # =========================
    def create_tables(self):

        try:

            cursor = self.conn.cursor()

            cursor.executescript("""

                CREATE TABLE IF NOT EXISTS documents (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    file_name TEXT NOT NULL,

                    file_path TEXT NOT NULL,

                    upload_date TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS queries (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    query TEXT NOT NULL,

                    answer TEXT,

                    created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP
                );

            """)

            self.conn.commit()

        except Exception as e:

            print("Error creating tables:", e)

    # =========================
    # INSERT DOCUMENT
    # =========================
    def insert_document(self, file_name, file_path):

        try:

            cursor = self.conn.cursor()

            cursor.execute(

                """
                INSERT INTO documents
                (file_name, file_path)

                VALUES (?, ?)
                """,

                (file_name, file_path)
            )

            self.conn.commit()

        except Exception as e:

            print("Error inserting document:", e)

    # =========================
    # INSERT QUERY
    # =========================
    def insert_query(self, query, answer):

        try:

            cursor = self.conn.cursor()

            cursor.execute(

                """
                INSERT INTO queries
                (query, answer)

                VALUES (?, ?)
                """,

                (query, answer)
            )

            self.conn.commit()

        except Exception as e:

            print("Error inserting query:", e)

    # =========================
    # GET DOCUMENTS
    # =========================
    def get_documents(self):

        try:

            cursor = self.conn.cursor()

            cursor.execute(

                """
                SELECT
                    id,
                    file_name,
                    file_path,
                    upload_date

                FROM documents

                ORDER BY upload_date DESC
                """
            )

            return cursor.fetchall()

        except Exception as e:

            print("Error fetching documents:", e)

            return []

    # =========================
    # GET QUERIES
    # =========================
    def get_queries(self):

        try:

            cursor = self.conn.cursor()

            cursor.execute(

                """
                SELECT
                    id,
                    query,
                    answer,
                    created_at

                FROM queries

                ORDER BY created_at DESC
                """
            )

            return cursor.fetchall()

        except Exception as e:

            print("Error fetching queries:", e)

            return []

    # =========================
    # DELETE DOCUMENT
    # =========================
    def delete_document(self, doc_id):

        try:

            cursor = self.conn.cursor()

            cursor.execute(

                """
                DELETE FROM documents
                WHERE id = ?
                """,

                (doc_id,)
            )

            self.conn.commit()

        except Exception as e:

            print("Error deleting document:", e)

    # =========================
    # DELETE QUERY
    # =========================
    def delete_query(self, query_id):

        try:

            cursor = self.conn.cursor()

            cursor.execute(

                """
                DELETE FROM queries
                WHERE id = ?
                """,

                (query_id,)
            )

            self.conn.commit()

        except Exception as e:

            print("Error deleting query:", e)


# =========================
# GLOBAL DATABASE INSTANCE
# =========================
db = Database()