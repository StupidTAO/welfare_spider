import pymysql
import time

class HtmlOutputer(object):
    def __init__(self):
        self.datas = []  # 列表

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def collect_walfare_data(self, datas):
        if datas is None:
            return
        self.datas = datas

    def output_html(self):
        with open('output.html', 'w', encoding='utf-8') as fout:
            fout.write("<html>")
            fout.write("<head><meta http-equiv=\"content-type\" content=\"text/html;charset=utf-8\"></head>")
            fout.write("<body>")
            fout.write("<table>")

            for data in self.datas:
                fout.write("<tr>")
                fout.write("<td>%s</td>" % data["url"])
                fout.write("<td>%s</td>" % data["title"])
                fout.write("<td>%s</td>" % data["summary"])
                fout.write("</tr>")

            fout.write("</table>")
            fout.write("</body>")
            fout.write("</html>")
    def ouput_walfare_html(self):
        with open('output_walfare.html', 'w', encoding='utf-8') as fout:
            fout.write("<html>")
            fout.write("<head><meta http-equiv=\"content-type\" content=\"text/html;charset=utf-8\"></head>")
            fout.write("<body>")
            fout.write("<table>")

            for data in self.datas:
                print("self.data = ", data)
                fout.write("<tr>")
                fout.write("<td>%s</td>" % data["id"])
                fout.write("<td>%s</td>" % data["title"])
                fout.write("<td>%s</td>" % data["amount"])
                fout.write("<td>%s</td>" % data["donationNameExt"])
                fout.write("<td>%s</td>" % data["tradeType"])
                fout.write("<td>%s</td>" % data["payType"])
                fout.write("<td>%s</td>" % data["payTime"])
                fout.write("<td>%s</td>" % data["createTime"])
                fout.write("</tr>")

            fout.write("</table>")
            fout.write("</body>")
            fout.write("</html>")
    #批量插入数据
    def ouput_walfare_mysql(self):
        # 打开数据库连接
        db = pymysql.connect("127.0.0.1","root","7afZa**t4Xx%$Jy","welfare" )
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        for data in self.datas:
        # SQL 插入语句
            sql = "INSERT INTO donate(item_id, titile, amount,\
                donationNameExt, tradeType, payType, createTime, payTime)\
                VALUES ('%s', '%s', '%f', '%s', '%d', '%d', '%s', '%s')" % \
                (data["id"], data["title"], data["amount"], data["donationNameExt"],
                data["tradeType"], data["payType"], data["createTime"], data["payTime"])
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except:
                # 如果发生错误则回滚
                print("sql db occure error")
                db.rollback()

    def ouput_walfare_one_fundation_mysql(self):
        # 打开数据库连接
        db = pymysql.connect("127.0.0.1","root","123qweasd","welfare" )
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        for data in self.datas:
        # SQL 插入语句
            sql = "INSERT INTO one_fundation(item_id, intention, amount,\
                channel, name, importTime, payTime)\
                VALUES ('%s', '%s', '%f', '%s', '%s', '%s', '%s')" % \
                (data["id"], data["intention"], data["amount"], data["channel"],
                data["name"], self.timestampms_to_str(data["importTime"]), self.timestampms_to_str(data["time"]))
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except:
                # 如果发生错误则回滚
                print("sql db occure error sql is ", sql)
                db.rollback()
    def timestampms_to_str(slef, timeStamp):
        timeStamp = float(int(timeStamp)/1000)
        timeDate = time.localtime(timeStamp)
        timeStr = time.strftime("%Y-%m-%d %H:%M:%S", timeDate)
        return timeStr
