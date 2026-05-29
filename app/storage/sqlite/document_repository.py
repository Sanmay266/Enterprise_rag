from app.storage.sqlite.database import (
    get_connection,
)


class DocumentRepository:

    def __init__(self):

        self.conn = get_connection()

        self.create_table()

    def create_table(self):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                chunk_count INTEGER,
                status TEXT
            )
            """
        )

        self.conn.commit()

    def add_document(
        self,
        filename: str,
        chunk_count: int,
        status: str,
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT INTO documents (
                filename,
                chunk_count,
                status
            )
            VALUES (?, ?, ?)
            """,
            (
                filename,
                chunk_count,
                status,
            )
        )

        self.conn.commit()

    def get_all_documents(self):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM documents
            ORDER BY id DESC
            """
        )

        documents = cursor.fetchall()

        return documents

    def get_document_by_id(
        self,
        document_id: int,
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM documents
            WHERE id = ?
            """,
            (document_id,)
        )

        return cursor.fetchone()

    def delete_document(
        self,
        document_id: int,
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            DELETE FROM documents
            WHERE id = ?
            """,
            (document_id,)
        )

        self.conn.commit()