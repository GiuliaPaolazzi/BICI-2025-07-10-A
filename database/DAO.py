from database.DB_connect import DBConnect
from model.arco import Arco
from model.category import Category
from model.prodotto import Prodotto


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getAllCategories():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "select * from categories"

        cursor.execute(query)

        for row in cursor:
            results.append(Category(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllProductsConCategoria(categoria):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from products p 
                    where p.category_id = %s"""

        cursor.execute(query,(categoria.category_id,))

        for row in cursor:
            results.append(Prodotto(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(categoria,Data1, Data2, idMapP):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.product_id as id1 ,t2.product_id as id2,t1.n + t2.n as peso
                    from (select p.product_id, COUNT(*) as n
                    from products p , orders o , order_items oi 
                    where p.product_id = oi.product_id and o.order_id =oi.order_id 
                    and o.order_date between %s and %s
                    and p.category_id = %s
                    group by p.product_id) as t1, (select p.product_id, COUNT(*) as n
                    from products p , orders o , order_items oi 
                    where p.product_id = oi.product_id and o.order_id =oi.order_id 
                    and o.order_date between %s and %s
                    and p.category_id = %s
                    group by p.product_id) as t2
                    where t1.product_id <> t2.product_id 
                    and t1.n >= t2.n"""

        cursor.execute(query, (Data1, Data2,categoria.category_id, Data1, Data2,categoria.category_id))

        for row in cursor:
            results.append(Arco(idMapP[row["id1"]],idMapP[row["id2"]],row["peso"]))

        cursor.close()
        conn.close()
        return results
