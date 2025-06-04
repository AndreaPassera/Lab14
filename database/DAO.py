from database.DB_connect import DBConnect
from model.ordini import Ordini


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getStore():
        cnx=DBConnect.get_connection()
        cursor=cnx.cursor(dictionary=True)
        # store_name, phone, email, street, city, state, zip_code
        query="""select store_id
        from stores s
        """
        cursor.execute(query)

        res=[]

        for row in cursor:
            res.append(row)
        cnx.close()
        cursor.close()
        return res

    @staticmethod
    def getNodes(store):
        cnx=DBConnect.get_connection()
        cursor=cnx.cursor(dictionary=True)

        query="""select *
        from orders o
        where o.store_id=%s
        """
        cursor.execute(query, (store,))

        res=[]

        for row in cursor:
            res.append(Ordini(**row))
        cnx.close()
        cursor.close()
        return res


    @staticmethod
    def getEdges(store, maxG):
        cnx=DBConnect.get_connection()
        cursor=cnx.cursor(dictionary=True)

        query="""select t1.ordine1, t2.ordine2, t1.quantita1 + t2.quantita2 as peso
                    from (select o.order_id ordine1, o.store_id store1, o.order_date data1, sum(oi.quantity) as quantita1
                            from order_items oi, orders o 
                            where o.order_id = oi.order_id 
                            group by o.order_id) t1, 
                            (select o.order_id ordine2, o.store_id store2, o.order_date data2, sum(oi.quantity) as quantita2
                            from order_items oi, orders o 
                            where o.order_id = oi.order_id 
                            group by o.order_id) t2
                    where t1.ordine1 > t2.ordine2 and t1.store1 = t2.store2 and t1.store1= %s and datediff(t1.data1, t2.data2) < %s and datediff(t1.data1, t2.data2) > 0"""
        cursor.execute(query, (store,maxG))

        res=[]

        for row in cursor:
            res.append((row["ordine1"], row["ordine2"], row["peso"]))
        cnx.close()
        cursor.close()
        return res