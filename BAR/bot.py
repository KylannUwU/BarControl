import os
import requests
import logging
import asyncio
from twitchio.ext import commands
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Configurar el logging para el bot
logging.basicConfig(level=logging.DEBUG)

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=os.getenv('TWITCH_TOKEN'), prefix='!', initial_channels=['nolleyrcc'])

    async def event_ready(self):
        print(f'Bot conectado a {self.nick}')
        await asyncio.sleep(1)

    async def event_error(self, error):
        print(f"Ocurrió un error: {error}")

    async def is_mod(self, ctx):
        """Verifica si el usuario es moderador."""
        return ctx.author.is_mod

    async def event_message(self, message):
        """Aumenta la barra de progreso en 1 por cada mensaje en el chat."""
        await self.handle_commands(message)

        # Obtener el valor actual de la barra
        current_value_response = requests.get('http://127.0.0.1:5000/get_current_progress')
        if current_value_response.status_code == 200:
            current_value = current_value_response.json()['current_value']
            new_value = current_value + 1  # Aumenta en 1 por cada mensaje
            url = f'http://127.0.0.1:5000/update_progress/{new_value}'
            response = requests.get(url)

            if response.status_code != 200:
                print('Error al actualizar el valor de la barra.')

    async def event_cheer(self, message):
        """Aumenta la barra de progreso en 100 por cada bit donado."""
        bits_donated = message.bits
        if bits_donated:
            print('Bits donados')
            current_value_response = requests.get('http://127.0.0.1:5000/get_current_progress')
            if current_value_response.status_code == 200:
                current_value = current_value_response.json()['current_value']
                new_value = current_value + (bits_donated * 100)  # Añade 100 por cada bit donado
                url = f'http://127.0.0.1:5000/update_progress/{new_value}'
                response = requests.get(url)

                if response.status_code != 200:
                    print('Error al actualizar el valor de la barra.')

    @commands.command()
    async def barset(self, ctx, value: int):
        """Establece el valor de la barra de progreso. Solo para moderadores."""
        if await self.is_mod(ctx):
            url = f'http://127.0.0.1:5000/update_progress/{value}'
            response = requests.get(url)

    @commands.command()
    async def baradd(self, ctx, value: int):
        """Suma un valor al progreso actual. Solo para moderadores."""
        if await self.is_mod(ctx):
            current_value_response = requests.get('http://127.0.0.1:5000/get_current_progress')
            if current_value_response.status_code == 200:
                current_value = current_value_response.json()['current_value']
                new_value = current_value + value
                url = f'http://127.0.0.1:5000/update_progress/{new_value}'
                response = requests.get(url)

    @commands.command()
    async def barsup(self, ctx, value: int):
        """Resta un valor del progreso actual. Solo para moderadores."""
        if await self.is_mod(ctx):
            current_value_response = requests.get('http://127.0.0.1:5000/get_current_progress')
            if current_value_response.status_code == 200:
                current_value = current_value_response.json()['current_value']
                new_value = current_value - value
                url = f'http://127.0.0.1:5000/update_progress/{new_value}'
                response = requests.get(url)

if __name__ == "__main__":
    bot = Bot()
    bot.run()
