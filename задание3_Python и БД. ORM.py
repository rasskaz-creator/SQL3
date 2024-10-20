import json
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker

from задание1_model_orm import create_tables, Publisher, Book, Stock, Shop, Sale

DSN = 'postgresql://postgres:PASSWORD@localhost:5432/orm_db'
engine = sq.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', encoding = 'utf-8') as file:
    data = json.load(file)
    
for item in data:
    if item['model'] == 'publisher':
        name = item['fields'].get('name')
        if name:
            publisher = Publisher(name=name)
            session.add(publisher)
    
    elif item['model'] == 'book':
        title = item['fields'].get('title')
        id_publisher = item['fields'].get('id_publisher')
        
        if title and id_publisher is not None:
            book = Book(title=title, id_publisher=id_publisher)
            session.add(book)
            
    elif item['model'] == 'shop':
        name = item['fields'].get('name')
        
        if name:
            shop = Shop(name=name)
            session.add(shop)
    
    elif item['model'] == 'stock':
        id_shop = item['fields'].get('id_shop')
        id_book = item['fields'].get('id_book')
        count = item['fields'].get('count')
        
        if id_book is not None and id_shop is not None and count is not None:
            stock = Stock(id_book=id_book, id_shop=id_shop, count=count)
            session.add(stock)
            
    elif item['model'] == 'sale':
        price = item['fields'].get('price')
        date_sale = item['fields'].get('date_sale')
        count = item['fields'].get('count')
        id_stock = item['fields'].get('id_stock')
        
        if price is not None and date_sale is not None and count is not None and id_stock is not None:
            sale = Sale(price=price, date_sale=date_sale, count=count, id_stock=id_stock)
            session.add(sale)

try:
    session.commit()   
except Exception as e:
    session.rollback()
    print(f"Error occurred: {e}")
finally:    
    session.close()