from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

DATABASE = "stargaze_schema"


class Publication:

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.event_date = data["event_date"]
        self.location = data["location"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.author_first_name = data.get("author_first_name")
        self.author_last_name = data.get("author_last_name")
        self.likes_count = data.get("likes_count", 0)
        self.user_liked = data.get("user_liked", 0)

    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO publications
            (name, description, event_date, location, user_id)
            VALUES
            (%(name)s, %(description)s, %(event_date)s, %(location)s, %(user_id)s);
        """

        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all(cls, data):
        query = """
            SELECT
                publications.*,
                users.first_name AS author_first_name,
                users.last_name AS author_last_name,
                COUNT(likes.id) AS likes_count,
                COUNT(
                    CASE
                        WHEN likes.user_id = %(user_id)s THEN 1
                    END
                ) AS user_liked
            FROM publications
            JOIN users
                ON users.id = publications.user_id
            LEFT JOIN likes
                ON likes.publication_id = publications.id
            GROUP BY publications.id
            ORDER BY publications.event_date ASC;
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        publications = []

        for row in results:
            publications.append(cls(row))

        return publications

    @classmethod
    def get_by_id(cls, data):
        query = """
            SELECT *
            FROM publications
            WHERE id = %(id)s;
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        if not results:
            return None

        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = """
            UPDATE publications
            SET
                name = %(name)s,
                description = %(description)s,
                event_date = %(event_date)s,
                location = %(location)s
            WHERE id = %(id)s;
        """

        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = """
            DELETE FROM publications
            WHERE id = %(id)s;
        """

        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_by_name(cls, data):
        query = """
            SELECT *
            FROM publications
            WHERE name = %(name)s;
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        if not results:
            return None

        return cls(results[0])

    @classmethod
    def add_like(cls, data):
        query = """
            INSERT IGNORE INTO likes
            (user_id, publication_id)
            VALUES
            (%(user_id)s, %(publication_id)s);
        """

        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate_publication(data, publication_id=None):

        is_valid = True

        if len(data["name"].strip()) < 1:
            flash(
                "El nombre de la publicación es obligatorio.",
                "publication"
            )
            is_valid = False

        if len(data["description"].strip()) < 1:
            flash(
                "La descripción es obligatoria.",
                "publication"
            )
            is_valid = False

        if not data["event_date"]:
            flash(
                "La fecha es obligatoria.",
                "publication"
            )
            is_valid = False

        if len(data["location"].strip()) < 1:
            flash(
                "La ubicación es obligatoria.",
                "publication"
            )
            is_valid = False

        existing = Publication.get_by_name({
            "name": data["name"]
        })

        if existing:

            if publication_id is None:
                flash(
                    "Ya existe una publicación con ese nombre.",
                    "publication"
                )
                is_valid = False

            elif existing.id != publication_id:
                flash(
                    "Ya existe una publicación con ese nombre.",
                    "publication"
                )
                is_valid = False

        return is_valid