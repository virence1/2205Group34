import pymysql
import sys

db = pymysql.connect(host="localhost", user="dddadmin", password="Securepassword123", database="user_accounts")

cursor = db.cursor()
username = sys.argv[1]
new_vote_status = 1

sql = "UPDATE account SET voteStatus = %s WHERE username = %s"
values = (new_vote_status, username)
cursor.execute(sql, values)

# Commit the changes
db.commit()

# Close the cursor and database connection
cursor.close()
db.close()
