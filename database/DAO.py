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
    def getArtistsPopolarita(genre):
        conn = DBConnect.get_connection()
        res = []
        cursor = conn.cursor(dictionary=True)
        query= """select ar.ArtistId , ar.Name  , sum(i.Quantity) as popolarita
        from track t , invoiceline i , album a , artist ar, genre g 
        where g.Name  = %s
        and g.GenreId = t.GenreId 
        and t.TrackId = i.TrackId 
        and t.AlbumId = a.AlbumId 
        and ar.ArtistId = a.ArtistId 
        group by ar.ArtistId, ar.Name """
        cursor.execute(query, (genre,))
        for row in cursor:
            res.append(Artist(**row))
        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getConnectedPairs(genre):
        conn = DBConnect.get_connection()
        res = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct art1.ArtistId as idA, art2.ArtistId as idB
        from artist art1
        join album alb1 on art1.ArtistId = alb1.ArtistId
        join track t1 on alb1.AlbumId = t1.AlbumId
        join genre g1 on t1.GenreId = g1.GenreId
        join invoiceline il1 on t1.TrackId = il1.TrackId
        join invoice i1 on il1.InvoiceId = i1.InvoiceId
        
        join invoice i2 on i1.CustomerId = i2.CustomerId
        join invoiceline il2 on i2.InvoiceId = il2.InvoiceId
        join track t2 on il2.TrackId = t2.TrackId
        join genre g2 on t2.GenreId = g2.GenreId
        join album alb2 on t2.AlbumId = alb2.AlbumId
        join artist art2 on alb2.ArtistId = art2.ArtistId
        
        where g1.Name = %s
        and g2.Name = %s
        and art1.ArtistId < art2.ArtistId"""
        cursor.execute(query, (genre,genre))
        for row in cursor:
            res.append((row['idA'], row['idB']))
        cursor.close()
        conn.close()
        return res

