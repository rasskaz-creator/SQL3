import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker

from задание1_model_orm import Publisher, Book, Stock, Shop, Sale

DSN = 'postgresql://postgres:u7f6WRNy.*i+h$p@localhost:5432/orm_db'
engine = sq.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()


def get_shops(session, publisher_input): #Функция принимает обязательный параметр
    query = session.query( #Создаем общее тело запроса на выборку данных и сохраняем в переменную
        Book.title, Shop.name, Sale.price, Sale.date_sale, #Название книги, имя магазина, стоимость продажи и дату продажи
    ).select_from(Shop).join(Stock).join(Book).join(Publisher).join(Sale)
    
    if publisher_input.isdigit(): #Проверяем переданные данные в функцию на то, что строка состоит только из чисел
        query = query.filter(Publisher.id == int(publisher_input)) #Обращаемся к запросу, который составили ранее, и применяем фильтрацию, где айди публициста равно переданным данным в функцию, и сохраняем в переменную
    else:
        query = query.filter(Publisher.name == publisher_input) #Обращаемся к запросу, который составили ранее, и применяем фильтрацию, где имя публициста равно переданным данным в функцию, и сохраняем в переменную
    
    results = query.all()
    
    for title, shop_name, price, date_sale in results: #Проходим в цикле по переменой, в которой сохраняем результат фильтрации, и при каждой итерации получаем кортеж и распаковываем значения в 4 переменные
        print(f"{title: <40} | {shop_name: <10} | {price: <8} | {date_sale.strftime('%d-%m-%Y')}") #Передаем в форматированную строку переменные, которые содержат имя книги, название магазина, стоимость продажи и дату продажи
        


if __name__ == '__main__':
    user_input = input("Enter the publisher name or ID: ") #Просим клиента ввести имя или айди публициста и данные сохраняем в переменную
    get_shops(session, user_input) #Вызываем функцию получения данных из базы, передавая в функцию данные, которые ввел пользователь строкой выше    
    
session.close()