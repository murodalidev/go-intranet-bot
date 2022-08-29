import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from typing import Union
from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                result = "404"
                if fetch:
                    result = await connection.fetch(command, *args)
                if fetchval:
                    result = await connection.fetchval(command, *args)
                if fetchrow:
                    result = await connection.fetchrow(command, *args)
                if execute:
                    result = await connection.execute(command, *args)
            return result

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, telegram_id, username, first_name, last_name, phone, created_date):
        sql = "INSERT INTO alerts_bot_telegramuser (telegram_id, username, first_name, last_name, phone, created_date) VALUES ($1, $2, $3, $4, $5, $6) returning *"
        return await self.execute(sql, telegram_id, username, first_name, last_name, phone, created_date, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM alerts_bot_telegramuser"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM alerts_bot_telegramuser WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM alerts_bot_telegramuser"
        return await self.execute(sql, fetchval=True)






