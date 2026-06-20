from database.DB_connect import DBConnect
from model.arco import Arco
from model.employee import Employee


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllCountry():
        conn = DBConnect.get_connection()
        res = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct c.Country 
                    from customer c 
                    order by c.Country asc """
        cursor.execute(query)
        for row in cursor:
            res.append(row['Country'])
        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getAllEmployee(country):
        conn = DBConnect.get_connection()
        res = []
        cursor = conn.cursor(dictionary=True)
        query = """select e.*
                    from employee e , customer c 
                    where e.EmployeeId = c.SupportRepId 
                    and c.Country = %s
                    group by e.EmployeeId """
        cursor.execute(query, (country, ))
        for row in cursor:
            res.append(Employee(**row))
        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getllArchi(country, idMapEmp):
        conn = DBConnect.get_connection()
        res = []
        cursor = conn.cursor(dictionary=True)
        query = """with fattura_media_per_dipendente as (
                select c.SupportRepId, c.Country, AVG(i.Total) as fatturato 
                from invoice i , customer c
                where i.CustomerId = c.CustomerId 
                and c.Country = %s
                group by c.SupportRepId 
                )
                
                select f1.SupportRepID as e1, f2.SupportRepID as e2, f1.fatturato - f2.fatturato as peso
                from fattura_media_per_dipendente f1, fattura_media_per_dipendente f2
                where f1.Country = f2.Country
                and f1.SupportRepID < f2.SupportRepId
                and f1.fatturato> f2.fatturato """
        cursor.execute(query, (country,))
        for row in cursor:
            peso_float = float(row['peso'])
            res.append(Arco(idMapEmp[row['e1']], idMapEmp[row['e2']], peso_float))
        cursor.close()
        conn.close()
        return res

    # UTILE PER LA RICORSIONE
    @staticmethod
    def getClientiPerDipendente(country):
        conn = DBConnect.get_connection()
        res = {}
        cursor = conn.cursor(dictionary=True)
        query = """select c.SupportRepId , count(distinct c.CustomerId ) as num_clienti
                    from customer c
                    where c.Country = %s
                    group by c.SupportRepId """
        cursor.execute(query, (country,))
        for row in cursor:
            res[row['SupportRepId']] = row['num_clienti']
        cursor.close()
        conn.close()
        return res