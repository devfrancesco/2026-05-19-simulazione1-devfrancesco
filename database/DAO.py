from database.DB_connect import DBConnect
from model.artist import Artist


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllGenre():
        conn = DBConnect.get_connection()
        res = []
        cursor = conn.cursor(dictionary=True)
        query = """select g.Name 
                    from genre g """
        cursor.execute(query)
        for row in cursor:
            res.append(row['Name'])
        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getAllArtists():
        conn = DBConnect.get_connection()
        res = []
        cursor = conn.cursor(dictionary=True)
        query = """select a.ArtistId 
                        from artist a """
        cursor.execute(query)
        for row in cursor:
            res.append(row['ArtistId'])
        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getEdges(genre):
        conn = DBConnect.get_connection()
        res = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct a.ArtistId as idA, a2.ArtistId as idB
                    from invoiceline il1
                    join invoice i on il1.InvoiceId = i.InvoiceId 
                    join track t on t.TrackId = il1.TrackId 
                    join genre g on g.GenreId = t.GenreId 
                    join album a on a.AlbumId = t.AlbumId 
                    join invoiceline il2 on il2.InvoiceId = i.InvoiceId 
                    join track t2 on il2.TrackId = t2.TrackId 
                    join genre g2 on g2.GenreId = t2.GenreId 
                    join album a2 on a2.AlbumId = t2.AlbumId 
                    where g.Name = %s
                    and g2.Name = g.Name
                    and a.ArtistId <> a2.ArtistId"""
        cursor.execute(query, (genre,))
        for row in cursor:
            res.append((row['idA'], row['id2']))
        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getPopolarita(genre):
        conn = DBConnect.get_connection()
        res = []
        cursor = conn.cursor(dictionary=True)
        query= """select a2.ArtistId , a2.Name  , count(*) as popolarita
        from track t , invoiceline i , album a , artist a2, genre g 
        where g.Name  = %s
        and g.GenreId = t.GenreId 
        and t.TrackId = i.TrackId 
        and t.AlbumId = a.AlbumId 
        and a2.ArtistId = a.ArtistId 
        group by a2.Name """
        cursor.execute(query, (genre,))
        for row in cursor:
            res.append(Artist(**row))
        cursor.close()
        conn.close()
        return res


