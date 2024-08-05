import sqlite3
def sqlite3_run(*sqlite_Query):
    #The function will take multiple queries and output the result in form of list such that output of Query1 lies at index 0 ,Query2 at index 1 and so on.
    output=[]
    try:
        sqliteConnection=sqlite3.connect('asap.db')
        cursor=sqliteConnection.cursor()
        for query in sqlite_Query:
            cursor.execute(query)
            sqliteConnection.commit()
            output.append(cursor.fetchall())
        cursor.close()
        return output
    except sqlite3.Error as error:
        print(error)
        #messagebox.showwarning("Error",error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()
n=10

for i in range(n):
    query=input("Query:")
    print(sqlite3_run(query))
#print(createId())
