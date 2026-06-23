from database.DB_connect import DBConnect
from model.arco import Arco
from model.track import Track


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllGenre():
        conn = DBConnect.get_connection()
        res = []
        cursor = conn.cursor(dictionary=True)
        query = """select g.Name 
                    from genre g 
                    order by g.Name asc"""
        cursor.execute(query)
        for row in cursor:
            res.append(row['Name'])
        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getAllTracks(genre):
        conn = DBConnect.get_connection()
        res = []
        cursor = conn.cursor(dictionary=True)
        query = """select t.*
                    from track t , genre g 
                    where t.GenreId = g.GenreId 
                    and g.Name = %s """
        cursor.execute(query, (genre,))
        for row in cursor:
            res.append(Track(**row))
        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getAllEdges(genre, idMapT):
        conn = DBConnect.get_connection()
        res = []
        cursor = conn.cursor(dictionary=True)
        query = """with track_playlist as (
                    select t.TrackId as tId, p.PlaylistId as pId
                    from track t , playlisttrack p , genre g 
                    where p.TrackId = t.TrackId 
                    and g.GenreId = t.GenreId 
                    and g.Name = %s
                    )
                    select t.tId as t1, t2.tId as t2, Count(*) as peso
                    from track_playlist t, track_playlist t2
                    where t.tId < t2.tId 
                    and t.pId = t2.pId
                    group by t.tId, t2.tId """
        cursor.execute(query, (genre,))
        for row in cursor:
            res.append(Arco(idMapT[row['t1']], idMapT[row['t2']], int(row['peso'])))
        cursor.close()
        conn.close()
        return res