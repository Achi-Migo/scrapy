import pymysql

localhost = "master"
port = 3306
user = "root"
password = "123456"
db = "a91"
charset = "utf8"

ips = []
num = 0


# db = pymysql.connect(host=localhost, port=port, user=user, password=password, db=db, charset=charset);
# db.connect_timeout = 3000
# cursor = db.cursor()
# # zakza.top
# zakza_db = pymysql.connect(host="zakza.top", port=port, user=user, password=password, db=db,
#                            charset=charset);
# zakza_db.connect_timeout = 3000
# zakza_cursor = zakza_db.cursor()
# path = "ip_proxy/socks_proxy.txt"


def init_db():
    global db, cursor
    try:
        db = pymysql.connect(host=localhost, port=port, user=user, password=password, db=db,
                             charset=charset);
        db.connect_timeout = 3000
        cursor = db.cursor()
        # zakza.top
        # zakza_db = pymysql.connect(host="zakza.top", port=port, user=user, password=password, db=db,
        #                            charset=charset);
        # zakza_db.connect_timeout = 3000
        # zakza_cursor = zakza_db.cursor()
        print('init db')
    except Exception as e:
        print(e)


def check_db_connection():
    if not db.open:
        close_db()
        init_db()


def close_db():
    try:
        cursor.close()
        db.close()
        # zakza_cursor.close()
        # zakza_db.close()
        print('db is close')
    except Exception as e:
        print(e)


def insert_item(item, table_name):
    rows_list = []
    v = []
    fields = item.keys()
    for k in fields:
        v.append(item.get(k))
    rows_list.append(v)
    if rows_list.__len__() == 0:
        return 0
    # ---------------------------------插入记录-----------------------------------------
    sql = """
            INSERT INTO `{table_name}` VALUES
            """.format(table_name=table_name)

    field = ""
    for i in range(len(fields)):
        field += ",'{}'"
    aaa = "(null" + field + ")"
    # print(aaa)
    for row in rows_list:
        if len(row) < 2:
            continue
        # value = "(null,'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(*row)
        value = aaa.format(*row)
        sql += (value + ",")
    sql = sql[:-1]
    # ---------------------------------插入记录 结束-----------------------------------------
    try:
        global num
        # 执行sql语句

        check_db_connection()

        print(sql)

        cursor.execute(sql)
        # 提交到数据库执行
        num += 1
        if num % 24 == 0:
            db.commit()
            print("insert finished!")
    except Exception as e:
        # 如果发生错误则回滚
        print("insert" + e)
        db.rollback()


def insert_list(fields, table_name, rows_list):
    # print(rows_list)
    if rows_list.__len__() == 0:
        return 0
    # ---------------------------------------创建表----------------------------------
    # tmp = ""
    # for s in fields:
    #     # `title` varchar(100) DEFAULT NULL,
    #     tmp += ("`{s}` varchar(255) DEFAULT NULL,".format(s=s))
    # creat_table = '''
    #                     Create Table if Not Exists `{table_name}` (
    #                     `id` bigint(255) NOT NULL AUTO_INCREMENT,
    #                     {field}
    #                     PRIMARY KEY (`id`)
    #                     ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    #                 '''.format(table_name=table_name, field=tmp)
    # print(creat_table)
    # ----------------------------------------------------------------------------------

    # ---------------------------------插入记录-----------------------------------------
    sql = """
            INSERT INTO `{table_name}` VALUES
            """.format(table_name=table_name)

    field = ""
    for i in range(len(fields)):
        field += ",'{}'"
    aaa = "(null" + field + ")"
    # print(aaa)
    for row in rows_list:
        if len(row) < 2:
            continue
        # value = "(null,'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(*row)
        value = aaa.format(*row)
        sql += (value + ",")
    sql = sql[:-1]
    # ---------------------------------插入记录 结束-----------------------------------------
    try:
        # 执行sql语句
        # cursor.execute("DROP TABLE IF EXISTS {table_name} ;".format(table_name=table_name))
        check_db_connection()
        # print(creat_table)
        print(sql)
        # cursor.execute(creat_table)
        num = cursor.execute(sql)
        print(num)
        # 提交到数据库执行
        db.commit()
        print("insert finished!")
    except Exception as e:
        # 如果发生错误则回滚
        print(e)
        db.rollback()

    # try:
    # check_db_connection()
    # zakza_cursor.execute(creat_table)
    # num = zakza_cursor.execute(sql)
    # print(num)
    # zakza_db.commit()
    # print("insert to zakza_db finished!")
    # except Exception as e:
    # 如果发生错误则回滚
    # print(e)
    # zakza_db.rollback()


def test_db():
    check_db_connection()
    # print(zakza_cursor.execute("select * from gzf_uer where id=1").__str__())
    close_db()
    return True
