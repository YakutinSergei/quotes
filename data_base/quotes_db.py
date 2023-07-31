import asyncpg

from environs import Env

env = Env()
env.read_env()


async def db_connect():
    try:
        conn = await asyncpg.connect(user=env('user'),  password=env('password'), database=env('db_name'), host=env('host'))

        await conn.execute('''CREATE TABLE IF NOT EXISTS quotes(id BIGSERIAL NOT NULL PRIMARY KEY,
                                                               quote VARCHAR NOT NULL,
                                                               author VARCHAR NOT NULL);''')

        await conn.execute('''CREATE TABLE IF NOT EXISTS users(id BIGSERIAL NOT NULL PRIMARY KEY,
                                                               user_id BIGSERIAL NOT NULL);''')

    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            print('[INFO] PostgresSQL closed')


async def quotes_add_bd(quote):
    try:
        conn = await asyncpg.connect(user=env('user'),  password=env('password'), database=env('db_name'), host=env('host'))

        for i in range(len(quote)):
            await conn.execute('''INSERT INTO quotes(quote, author) 
                                    VALUES($1, $2)''',
                               quote[i][0], quote[i][1])

    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            print('[INFO] PostgresSQL closed')

#Добавление пользователя в базу данных
async def user_add(user_id):
    try:
        conn = await asyncpg.connect(user=env('user'),  password=env('password'), database=env('db_name'), host=env('host'))

        user = await conn.fetchrow(f'''SELECT * FROM users where user_id ={user_id}''')
        if not user:
            await conn.execute('''INSERT INTO users (user_id)
                                VALUES ($1);''', user_id)

    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            print('[INFO] PostgresSQL closed')