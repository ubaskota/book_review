import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL="postgresql://localhost/book_review"
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():
	f = open("books.csv")
	reader = csv.reader(f)
	try:
		for isbn, tit, au, yr in reader:
			print (isbn, tit, au, yr)
			db.execute('INSERT INTO books_des(isbn_num, title, author, publish_year) VALUES(:isbn, :title, :author, :year)',
			{'isbn':isbn, 'title':tit, 'author':au, 'year':yr})
			print("{tit} successfully added")
	except Exception as e:
		print ("THE ERROR IS", e)
	db.commit()

if __name__ == "__main__":
	main()




# def import_to_db(file):
# 	f = open(file)
# 	reader = csv.reader(f)

# 	row_count = sum(1 for row in reader) - 1

# 	i = 0
# 	#print(reader)
# 	for row in reader:

# 	# for isbn, title, author, year in reader:
# 		# print(isbn)
# 	# 	db.execute("INSERT INTO books_des (isbn_num, title, author, publish_year) VALUES(:isbn_num, :title, :author, :publish_year)",\
# 	# 	{'isbn_num': isbn, 'title': title, 'author': author, 'publish_year': year})
# 	# 	i += 1
# 	# db.commit()

# 	if i == row_count:
# 		print("You successfully imported the data to your database.")
# 	else:
# 		print(row_count)
# 		print("Looks like something is wrong!")


# if __name__ == "__main__":
# 	filename = input("Enter the name of the csv file: ")
# 	import_to_db(filename)

# #db.execute("SELECT * FROM books_des")
