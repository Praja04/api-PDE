from lan import Lan
import mysql.connector

def main():
    lan = Lan(1)
    if lan.open("192.168.1.1", 23):
        while True:
            command = input("Please enter the command (Exit with no input): ")
            if command == "":
                break
            if "?" in command:
                msgBuf = lan.SendQueryMsg(command, 1)
                print(msgBuf)
                save_to_database(msgBuf)
            else:
                lan.sendMsg(command)
        lan.close()

def save_to_database(data):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='data_litium',
                                             user='root',
                                             password='')
        cursor = connection.cursor()
        sql_query = """INSERT INTO data_sensor (data) VALUES (%s)"""
        cursor.execute(sql_query, (data,))
        connection.commit()
        print("Data inserted successfully")
    except mysql.connector.Error as error:
        print("Failed to insert data into MySQL table:", error)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

if __name__ == '__main__':
    main()
