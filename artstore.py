import sqlite3

import os

db = os.path.join('database', 'artstore.db')

class ArtPiece:

    def __init__(self, title, artistID, price, sold=False, id=None):
        self.title = title
        self.artistID = artistID
        self.price = price
        self.sold = sold
        self.id = id

        self.artstore = ArtInventory()

    def save(self):
        if self.id:
            self.artstore._update_artpiece(self)
        else:
            self.artstore._add_artpiece(self)

    def delete(self):
        self.artstore._delete_artpiece(self)

    def __str_(self):
        sold_status = 'has' if self.sold else 'has not'
        return f'ID {self.id}, Title {self.title}, Artist: {self.artistID}. Purchase price is ${self.price} and it {sold_status} been sold.'

    def __repr__(self):
        return f'ID {self.id}, Title {self.title}, Artist: {self.artistID}, Price: ${self.price} Sold: {self.sold}.'
    
    def __eq__(self, other):
        if isinstance(self,other.__class__):
            return self.id == other.id and self.title == other.title and self.artistID == other.artistID and self.price == other.price and self.sold == other.sold 
        return False
    
    def __ne__(self, other):
        if not isinstance(self, other.__class__):
            return True
        return self.id != other.id or self.title != other.title or self.artistID != other.artistID or self.price != other.price or self.sold != other.sold 
    
    def __hash__(self):
        return hash((self.id, self.title, self.artistID, self.price, self.sold))

class Artist:

    def __init__(self, name, email, id=None):
        self.name = name
        self.email = email
        self.id =id


        self.artistlist = ArtistList()

    def save(self):
        if self.id:
            self.artistlist._update_artist(self)
        else:
            self.artistlist._add_artist(self)

    def delete(self):
        self.artistlist._delete_artist(self)

    def __str_(self):
        return f'ID {self.id}, Name: {self.name}, Email: {self.email}'

    def __repr__(self):
        return f'ID {self.id}, Name: {self.name}, Email: {self.email}'
    
    def __eq__(self, other):
        if isinstance(self,other.__class__):
            return self.id == other.id and self.name == other.name and self.email == other.email 
        return False
    
    def __ne__(self, other):
        if not isinstance(self, other.__class__):
            return True
        return self.id != other.id or self.name != other.name or self.email != other.email 
    
    def __hash__(self):
        return hash((self.id, self.name, self.email))

class ArtInventory:

    instance = None

    class __ArtStore:

        def _init__(self):
            create_table_sql = 'CREATE TABLE IF NOT EXISTS inventory (artid INTEGER PRIMARY KEY, title TEXT, price REAL, sold BOOLEAN, FOREIGN KEY(artistid) REFERENCES artistlist(artistid)'

            conn = sqlite3.connect(db)

            with conn:
                conn.execute(create_table_sql)
            
            conn.close()

    def _add_artpiece(self, artpiece):

        insert_sql = 'INSERT INTO inventory(title,price,sold,artistid) VALUES (?,?,?)'

        try:
            with sqlite3.connect(db) as conn:
                res = conn.execute(insert_sql, (artpiece.title, artpiece.price, artpiece.sold, artpiece.artistid))
                new_id = res.lastrowid
                artpiece.id =new_id
        except sqlite3.IntegrityError as e:
            raise StoreError(f'Error - this is already in the database. {artpiece}') from e
        finally:
            conn.close()

    
    
class StoreError(Exception):
    pass


       