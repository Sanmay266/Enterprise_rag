from app.storage.sqlite.database import (
    get_connection,
)


class DocumentRepository:

    def __init__(self):

        self.conn = get_connection()

        self.create_table()

        self.create_chunk_table()

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

    def create_chunk_table(self):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER NOT NULL,
                chunk_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                FOREIGN KEY(document_id)
                REFERENCES documents(id)
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

        return cursor.lastrowid

    def add_chunk(
        self,
        document_id: int,
        chunk_id: int,
        content: str,
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT INTO chunks (
                document_id,
                chunk_id,
                content
            )
            VALUES (?, ?, ?)
            """,
            (
                document_id,
                chunk_id,
                content,
            )
        )

        self.conn.commit()

    def get_all_chunks(self):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM chunks
            ORDER BY id
           """
        )
  
        return cursor.fetchall()    

    def get_all_documents(self):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM documents
            ORDER BY id DESC
            """
        )

        return cursor.fetchall()

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

    def get_chunks_by_document(
        self,
        document_id: int,
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM chunks
            WHERE document_id = ?
            ORDER BY chunk_id
            """,
            (document_id,)
        )

        return cursor.fetchall()

    def delete_document(
        self,
        document_id: int,
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            DELETE FROM chunks
            WHERE document_id = ?
            """,
            (document_id,)
        )

        cursor.execute(
            """
            DELETE FROM documents
            WHERE id = ?
            """,
            (document_id,)
        )

        self.conn.commit()