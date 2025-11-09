from database.DB_connect import DBConnect
from model.order import Order
from model.store import Store


class DAO():
    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct s.* 
                from stores s"""

        cursor.execute(query)

        for row in cursor:
            results.append(Store(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(store_name):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct o.*
                from stores s, orders o
                where o.store_id=s.store_id and s.store_name =%s 
                ORDER BY o.order_date"""

        cursor.execute(query, (store_name,))

        for row in cursor:
            results.append(Order(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getNumeroOggetti(id_ordine):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT SUM(quantity) AS totale
            FROM order_items
            WHERE order_id = %s
        """

        cursor.execute(query, (id_ordine,))
        results = cursor.fetchone() #restituisce una sola riga del risultato della query.

        cursor.close()
        conn.close()

        if results["totale"] is None:
            return 0

        return results["totale"]
            #results)[0] #metto questo pk fetchone restituisce una tupla anche quando ho un solo valore, così recuper il valore