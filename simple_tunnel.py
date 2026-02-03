#!/usr/bin/env python3
"""
Простой туннель для создания публичного URL
"""
import asyncio
import aiohttp
import sys
from aiohttp import web
import threading
import time

async def handle_callback(request):
    """Обработка вебхуков от ВКонтакте"""
    print(f"📨 Получен вебхук: {request.method} {request.url}")
    try:
        if request.method == 'POST':
            data = await request.json()
            print(f"📋 Данные вебхука: {data}")
            
            # Возвращаем ответ для подтверждения
            if data.get('type') == 'confirmation':
                return web.Response(text='9abbd7b0')
            
            return web.Response(text='ok')
        else:
            return web.Response(text='VK Bot is running!')
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return web.Response(text='Error', status=500)

async def create_tunnel():
    """Создание простого туннеля"""
    print("🌐 Создание веб-сервера для вебхуков...")
    
    app = web.Application()
    app.router.add_post('/', handle_callback)
    app.router.add_get('/', handle_callback)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, '0.0.0.0', 8000)
    await site.start()
    
    print("✅ Веб-сервер запущен на http://0.0.0.0:8000")
    print("🔗 Для настройки в ВКонтакте используй один из сервисов:")
    print("   - ngrok (если сможешь установить)")
    print("   - localtunnel")
    print("   - cloudflare tunnel")
    print("   - или любой другой HTTPS туннель")
    
    # Ждём вечно
    while True:
        await asyncio.sleep(10)

if __name__ == "__main__":
    print("🚀 Запуск простого туннеля для бота 'Сота Сил'")
    asyncio.run(create_tunnel())