import mysql.connector
from mysql.connector import pooling
import mysql.connector.cursor
from config import DB_PASSWORD, DB_USER, DB_HOST, DB_NAME, DB_PORT
from classes import User, Transaction, Tax, TaxPayment, Currency, CreditRequest
from datetime import datetime


# ======DB funcs======


def connectToDB() -> bool:
    global pool
    pool = connectionPool()
    if pool is not None:
        return True
    return False


def connectionPool() -> pooling.MySQLConnectionPool | None:
    """Создание пула подключений

    Returns:
        pooling.MySQLConnectionPool | None: возвращает пул подклчений, либо None если возникли ошибки
    """
    db_config = {
        "host": DB_HOST,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "database": DB_NAME,
        "port": DB_PORT,
    }
    try:
        connection_pool = pooling.MySQLConnectionPool(
            pool_name="mypool", pool_size=20, pool_reset_session=True, **db_config
        )
        return connection_pool
    except Exception:
        return None


def getConnection(pool: pooling.MySQLConnectionPool) -> pooling.PooledMySQLConnection:
    return pool.get_connection()


def getCursor(conn: pooling.PooledMySQLConnection) -> mysql.connector.cursor:
    """Возвращает курсор. Курсор буферизирванный, извлекать данные нужно как из генератора/итератора

    Args:
        conn (pooling.PooledMySQLConnection): соединение

    Returns:
        mysql.connector.cursor: курсор
    """
    return conn.cursor(buffered=True)


# ======User funcs======


def getUser(
    id: int | None = None,
    username: str | None = None,
    FIO: str | None = None,
) -> User | None:
    """Возвращает всю информацию о пользователе по id или username или ФИО. ВАЖНО! Использовать только с 1 из критериев отбора.

    Args:
        id (int | None, optional): ID пользователя. Defaults to None.
        username (str | None, optional): имя пользователя. Defaults to None.
        FIO (str | None, optional): ФИО пользователя. Defaults to None.

    Returns:
        User | None: Возвращается найденного пользователя, либо None.
    """
    if [id, username, FIO].count(None) != 2:
        return None
    global pool
    conn = getConnection(pool)
    cursor = getCursor(conn)

    query = """
SELECT * FROM users
WHERE {} = {}
"""
    values = ()
    if id is not None:
        values = ("id", f"{id}")
    elif username is not None:
        values = ("username", f"'{username}'")
    else:
        values = ("FIO", f"'{FIO}'")

    cursor.execute(query.format(*values))
    res = [i for i in cursor]

    cursor.close()
    conn.close()

    if res:
        return User(*res[0])
    else:
        return None


def setUserStats(
    id: int, balance: Currency | None = None, isBanned: bool | None = None
) -> User | None:
    """Обновляет атрибуты пользователя

    Args:
        id (int): id пользователя
        balance (int | None, optional): Новый баланс пользователя. Defaults to None.
        isBanned (bool | None, optional): заблокирован или нет. Defaults to None.

    Returns:
        User | None: возвращает экземпляр пользователя с актуальными полями если удачно, иначе None
    """
    global pool
    conn = getConnection(pool)
    cursor = getCursor(conn)

    cond = ""

    if balance is not None and isBanned is not None:
        cond = f"balance = {balance}, isBanned = {isBanned}"
    elif balance is not None:
        cond = f"balance = {balance}"
    elif isBanned is not None:
        cond = f"isBanned = {isBanned}"

    query = f"""
UPDATE USERS
SET {cond}
WHERE id = {id};
"""
    cursor.execute(query)
    conn.commit()

    query = f"""
SELECT * FROM users
WHERE id = {id};
"""
    cursor.execute(query)

    res = [i for i in cursor]

    cursor.close()
    conn.close()

    if res:
        return User(*res[0])
    else:
        return None


def findUser(pattern: str) -> list[User]:

    def isRu(s: str) -> bool:
        """Определяет русская ли 1 буква в строке по unicode символа"""
        return ord(s[0]) in range(1040, 1104)

    global pool
    conn = getConnection(pool)
    cursor = getCursor(conn)

    if isRu(pattern):
        query = """
SELECT * FROM users
where FIO like %s;
"""
    else:
        query = """
SELECT * FROM users
where username like %s;
"""
    pattern = f"%{pattern}%"
    cursor.execute(query, [pattern])
    res = [User(*i) for i in cursor]

    cursor.close()
    conn.close()

    return res


# ======Credits funcs======


def getCreditRequests() -> list[CreditRequest]:
    global pool
    conn = getConnection(pool)
    cursor = getCursor(conn)

    query = """
SELECT * FROM creditrequest
"""
    cursor.execute(query)

    res = [CreditRequest(*i) for i in cursor]

    cursor.close()
    conn.close()

    return res


def getCreditRequest(id: int) -> CreditRequest | None:
    global pool
    conn = getConnection(pool)
    cursor = getCursor(conn)

    query = """
SELECT * FROM creditrequest
where id = %s
"""
    cursor.execute(query, params=[id])

    res = [i for i in cursor]

    cursor.close()
    conn.close()

    if res:
        return CreditRequest(*res[0])
    else:
        return None


def postCreditRequest(
    userId: int,
    purpose: str,
    sum: Currency,
    status: int,
):
    global pool
    conn = getConnection(pool)
    cursor = getCursor(conn)

    query = """
INSERT INTO creditrequest(userId, purpose, sum, status) 
VALUES (%s, %s, %s, %s); 
"""
    cursor.execute(query, [userId, purpose, sum, status])
    conn.commit()

    query = """
SELECT * FROM creditrequest
WHERE id = %s;
"""
    cursor.execute(query, [cursor.lastrowid])

    res = [i for i in cursor]

    cursor.close()
    conn.close()

    if res:
        return CreditRequest(*res[0])
    else:
        return None


def setCreditRequestStatus(id: int, newStatus: int) -> CreditRequest | None:
    global pool
    conn = getConnection(pool)
    cursor = getCursor(conn)

    query = """
UPDATE creditrequest
SET status = %s
WHERE id = %s;
"""
    cursor.execute(query, [newStatus, id])
    conn.commit()

    query = """
SELECT * FROM creditrequest
WHERE id = %s;
"""
    cursor.execute(query, [id])

    res = [i for i in cursor]

    cursor.close()
    conn.close()

    if res:
        return CreditRequest(*res[0])
    else:
        return None


# ======taxes funcs======


def getTaxes() -> list[Tax]:
    global pool
    conn = getConnection(pool)
    cursor = getCursor(conn)

    query = """
SELECT * FROM taxes
"""
    cursor.execute(query)

    res = [Tax(*i) for i in cursor]

    cursor.close()
    conn.close()

    return res


def newTax(name: str, datetime: datetime, sum: Currency) -> Tax | None:
    global pool
    conn = getConnection(pool)
    cursor = getCursor(conn)

    query = """
INSERT INTO taxes(name, datetime, sum) 
VALUES (%s, %s, %s); 
"""
    cursor.execute(query, [name, datetime, sum])
    conn.commit()

    query = """
SELECT * FROM taxes
WHERE id = %s;
"""
    cursor.execute(query, [cursor.lastrowid])

    res = [i for i in cursor]

    cursor.close()
    conn.close()

    if res:
        return Tax(*res[0])
    else:
        return None


def editTax(
    taxId: int, newName: str = None, newDateTime: datetime = None, newSum: int = None
) -> Tax | None:
    if [newName, newDateTime, newSum].count(None) == 3:
        return None
    global pool
    conn = getConnection(pool)
    cursor = getCursor(conn)

    cond = []
    if newName is not None:
        cond.append(f"name = '{newName}'")
    if newDateTime is not None:
        cond.append(f"datetime = '{newDateTime}'")
    if newSum is not None:
        cond.append(f"sum = {newSum}")

    condStr = ", ".join(cond)
    query = f"""
UPDATE taxes
SET {condStr}
WHERE id = {taxId};
"""
    cursor.execute(query)
    conn.commit()

    query = """
SELECT * FROM taxes
WHERE id = %s;
"""
    cursor.execute(query, [taxId])

    res = [i for i in cursor]

    cursor.close()
    conn.close()

    if res:
        return Tax(*res[0])
    else:
        return None


def newTaxPayment(userId: int, taxId: int) -> TaxPayment | None:
    global pool
    conn = getConnection(pool)
    cursor = getCursor(conn)

    query = """
INSERT INTO taxespayment(userId, taxId) 
VALUES (%s, %s); 
"""
    cursor.execute(query, [userId, taxId])
    conn.commit()

    query = """
SELECT * FROM taxespayment
WHERE id = %s;
"""
    cursor.execute(query, [cursor.lastrowid])

    res = [i for i in cursor]

    cursor.close()
    conn.close()

    if res:
        return TaxPayment(*res[0])
    else:
        return None


def getTax(taxId: int) -> Tax | None:
    global pool
    conn = getConnection(pool)
    cursor = getCursor(conn)

    query = """
SELECT * FROM taxes
WHERE id = %s
"""
    cursor.execute(query, [taxId])

    res = [i for i in cursor]

    cursor.close()
    conn.close()

    if res:
        return Tax(*res[0])
    else:
        return None


def getTaxStats(taxId: int) -> dict:
    """Статистика сбор налога. ВНИМАНИЕ! Если будет передан taxId несуществующего налога, запрос вернёт список всех пользователей.

    Args:
        taxId (int): id налога

    Returns:
        tuple[int, int]: возвращает кортеж где первое число - число участников, оплативших налог, второе - общее число налогоплательщиков
    """

    global pool
    conn = getConnection(pool)
    cursor = getCursor(conn)

    query = """
SELECT 
    COUNT(tp.userId) AS paid_users,
    COUNT(u.id) AS total_users
FROM 
    users AS u
LEFT JOIN 
    (SELECT * FROM taxespayment WHERE taxId = %s) AS tp ON tp.userId = u.id
WHERE 
    u.isOrg = False;
    """
    cursor.execute(query, [taxId])
    res = [i for i in cursor][0]

    cursor.close()
    conn.close()

    return {
        "taxId": taxId,
        "paid": res[0],
        "total": res[1],
    }


def getTaxDefaulters(taxId: int) -> list[User]:
    """Функция возвращает список пользователей (подлежащих оплате налога), которые не оплатили налог taxId.
    ВНИМАНИЕ! Если будет передан taxId несуществующего налога, запрос вернёт список всех пользователей.

    Args:
        taxId (int): id налога

    Returns:
        list[User]: списпок пользователей
    """

    global pool
    conn = getConnection(pool)
    cursor = getCursor(conn)

    query = """
SELECT 
    u.id, u.username, u.FIO, u.balance, u.isBanned, u.isOrg 
FROM 
    users AS u
LEFT JOIN 
    (SELECT * FROM taxespayment WHERE taxId = %s) AS tp ON tp.userId = u.id
WHERE 
    tp.userId is NULL AND u.isOrg = False;
    """

    cursor.execute(query, [taxId])
    res = [User(*i) for i in cursor]

    cursor.close()
    conn.close()

    return res


# ======transactions funcs======

if __name__ == "__main__":
    if not connectToDB():
        raise Exception("Failed connect to DB")

    r = getTaxStats(7)
