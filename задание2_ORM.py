import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker

from задание1_model_orm import Publisher, Book, Stock, Shop, Sale

DSN = 'postgresql://postgres:PASSWORD@localhost:5432/orm_db'
engine = sq.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

def print_publisher_book_sales(session):
    
    publisher_input = input('Enter publisher name or ID ')
    
    if publisher_input.isdigit():
        publisher_query = session.query(Publisher).filter(Publisher.id == int(publisher_input))
    else:
        publisher_query = session.query(Publisher).filter(Publisher.name == publisher_input)
        
    if not publisher_query:
        print('Publisher is not found')
        return
    
    books = session.query(Book).filter(Book.id_publisher == Publisher.id).all()
    
    for book in books:
        stocks = book.stocks
        for stock in stocks:
            sales_info = stock.sales
            for sale in sales_info:
                shop = stock.shop
                print(f'{book.title} | {shop.name} | {sale.price} | {sale.date_sale}')

print_publisher_book_sales(session)

session.close()

