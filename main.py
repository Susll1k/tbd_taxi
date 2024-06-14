import psycopg2
import time
import random 


class Database_manager:
    def __init__(self, dbname, host, port, user, password):
        self.dbname=dbname
        self.host=host
        self.port=port
        self.user=user
        self.password=password
        self.connection=None
        self.cursor=None

    def connect(self):
        try:
            self.connection=psycopg2.connect(dbname=self.dbname,host= self.host, port=self.port, user=self.user, password=self.password)
            print('Connected successfully')
        except Exception as e:
            print(f'Connection refused: {e}')
        else:
            self.cursor = self.connection.cursor()
    def insert(self, table_name, **kwargs):
        columns=', '.join([column for column in kwargs.get('columns', [])])
        values=', '.join([f"'{column}'" if type(column) == str else f"{column}" for column in kwargs.get('values', [])])

        query =f'''INSERT INTO {table_name}({columns}) values({values})'''
        try:
            self.cursor.execute(query=query)
            self.connection.commit()
        except Exception as error:
            print(f'Error: {error}')
    def select(self, table, **kwargs):
        if kwargs.get('columns', False):
            columns = ', '.join([column for column in kwargs.get('columns', [])])
            query= f'Select {columns} from {table}'
        else:
            query= f'Select * from {table}'
        try:
            self.cursor.execute(query=query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f'Error: {e}')
            
    def delete(self, table, id):
        query= f'delete from {table} where id={id}'
        try:
            self.cursor.execute(query=query)
            self.connection.commit()
        except Exception as e:
            print(f'Error: {e}')
    def update(self, table, column, value, id):
        query= f"update {table} set {column} = '{value}' where id = {id}"
        try:
            self.cursor.execute(query=query)
            self.connection.commit()
        except Exception as e:
            print(f'Error: {e}')
    def call_taxi(self):
        query='Select * from drivers'
        self.cursor.execute(query=query)
        return self.cursor.fetchall()



database=Database_manager('postgres', 'localhost', 5432, 'postgres','admin')
database.connect()
# database.insert('passengers', columns=['name', 'phone_number'], values=['Иван', '+77016532771'])
# database.delete('drivers', 2)
# database.update('drivers', 'class','Komfort',1)

passenger = (database.select('passengers'))[0]

while True:
    print(f'\n\nПривет {passenger[1]}')
    i_task=0
    while True:
        if i_task == 3:
            break
        task = input('Хотите вызвать такси?(y/n): ')
        if task == 'n':
            break
        elif task == 'y':
            break
        else:
            print("Вы ввели что-то не верно")
            i_task+=1
    if i_task == 3:
        print('Было слишком много попыток')
        break
    elif task == 'n':
        break


    destination = input('Место назвачения?: ')
    arrival = input('Место прибытия?: ')
    print('Мы ищем такси поблизости...')
    time.sleep(3)
    driver=random.choice(database.select('drivers'))


    database.insert('orders', columns=['driver_id','passenger_id','destination', 'arrival'], values=[f'{driver[0]}', f'{passenger[0]}', f'{destination}', f'{arrival}'])
    order_id=(database.select('orders')[-1])[0]


    print(f'''\n     К вам едет {driver[1]} ({driver[5]}):
     Машина: {driver[2]} {driver[3]}
     Номер машины: {driver[4]}
     Номер водителя: {driver[6]}\n''')
    

    print(f'Водитель приедет через {random.randint(2,6)} минут')
    time.sleep(4)
    print('Водитель прибыл и ждет вас')
    time.sleep(2)
    print('Поездка началась')
    time.sleep(3)

    while True:
        try:
            rate=float(input('Как вам поездка?(1,10): '))
            break
        except ValueError:
            print('Введите корректные данные')



    database.insert('rates', columns=['order_id', 'rate'], values=[f'{order_id}', f'{rate}'])
    print('Спасибо за оценку')
    break




    


    

