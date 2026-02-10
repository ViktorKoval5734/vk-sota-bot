"""
Клиент для поиска в интернете через Serper API
"""
import aiohttp
import logging
from typing import Dict, List, Optional
from config import SERPER_API_KEY

logger = logging.getLogger(__name__)


class SerperClient:
    """Клиент для работы с Serper Search API"""

    def __init__(self):
        self.api_url = "https://google.serper.dev/search"
        self.api_key = SERPER_API_KEY

    async def search(self, query: str, num_results: int = 1) -> Optional[Dict]:
        """
        Выполнение поиска по запросу

        Args:
            query: Поисковый запрос
            num_results: Количество результатов (по умолчанию 1)

        Returns:
            Словарь с результатами поиска или None при ошибке
        """
        if not self.api_key or self.api_key == "your_serper_api_key":
            logger.error("API ключ Serper не настроен")
            return None

        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }

        payload = {
            'q': query,
            'num': num_results
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"✅ Поиск выполнен: {query}")
                        return data
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ Ошибка Serper API: {response.status}, {error_text}")
                        return None
        except Exception as e:
            logger.error(f"❌ Ошибка при выполнении поиска: {e}")
            return None

    def format_results(self, search_data: Dict) -> str:
        """
        Форматирование результатов поиска в читаемый вид

        Args:
            search_data: Данные от Serper API

        Returns:
            Отформатированный текст с результатами
        """
        if not search_data or "organic" not in search_data:
            return "Магия псиджиков не смогла ничего найти..."

        results = search_data["organic"]
        if not results:
            return "Магия псиджиков не нашла ничего подходящего..."

        # Берём только первый результат (наиболее релевантный)
        result = results[0]
        title = result.get("title", "Без названия")
        snippet = result.get("snippet", "Нет описания")
        link = result.get("link", "")

        formatted = f"{snippet}\n\n🔗 Источник: {link}"

        return formatted


# Глобальный экземпляр клиента
serper_client = SerperClient()
