import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None


    @classmethod
    def create_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)


    @classmethod   
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
            
        """
        CURSOR.execute(sql)

    def save(self):
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.breed))
        self.id = CURSOR.lastrowid


    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM dogs
        """

        CURSOR.execute(sql)
        rows = CURSOR.fetchall()

        return [cls.new_from_db(row) for row in rows]
    
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM dogs
            WHERE name = ?
            LIMIT 1
        """

        CURSOR.execute(sql,(name,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row) 
        else:
            return None
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM dogs
            WHERE id = ?
            LIMIT 1
        """

        CURSOR.execute(sql,(id,))
        row = CURSOR.fetchone()
        return cls.new_from_db(row) 
    
    @classmethod
    def find_or_create_by(cls, name, breed):
        sql = """
            SELECT * FROM dogs
            WHERE name = ? AND breed = ?

        """
        CURSOR.execute(sql, (name, breed))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return cls.create(name, breed)
        
    def update(self):
        sql = """"
            UPDATE dogs SET name = ?, breed = ? WHERE = id = ?
        """        
        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()