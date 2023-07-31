import asyncpg
from create_bot import bot

from environs import Env

env = Env()
env.read_env()

async def start_quote():
    try:
        conn = await asyncpg.connect(user=env('user'), password=env('password'), database=env('db_name'),
                                     host=env('host'))

        quote = await conn.fetchrow('''SELECT * FROM quotes 
                                WHERE id >= (SELECT (max(id) - min(id)) * RANDOM() + min(id) FROM quotes) 
                                ORDER BY id LIMIT 1;''')

        users = await conn.fetch('''SELECT * FROM users''')
        for user in users:
            text = f'{quote["quote"]}\n\n' \
                   f'<b><i>{quote["author"]}</i></b>'
            await bot.send_message(chat_id=user['user_id'], text=text)

        await conn.execute(f"DELETE FROM quotes WHERE id = '{quote['id']}'")

    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            print('[INFO] PostgresSQL closed')