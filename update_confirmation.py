#!/usr/bin/env python3
"""
Скрипт для обновления кода подтверждения Callback API ВКонтакте
"""
import sys
import requests
import json
import os
from pathlib import Path

def update_confirmation_code(new_code: str, base_url: str = "http://localhost:8000"):
    """Обновляет код подтверждения через API"""
    try:
        url = f"{base_url}/update_confirmation/{new_code}"
        response = requests.get(url)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Код подтверждения успешно обновлён: {result['code']}")
            return True
        else:
            print(f"❌ Ошибка обновления кода: {response.status_code}")
            print(response.text)
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Не удалось подключиться к серверу. Убедитесь, что бот запущен.")
        return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def get_confirmation_status(base_url: str = "http://localhost:8000"):
    """Получает статус кода подтверждения"""
    try:
        url = f"{base_url}/confirmation_status"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            print("📊 Статус кода подтверждения:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return True
        else:
            print(f"❌ Ошибка получения статуса: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Не удалось подключиться к серверу. Убедитесь, что бот запущен.")
        return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def update_env_file(new_code: str):
    """Обновляет код в .env файле"""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ Файл .env не найден!")
        return False
    
    try:
        # Читаем существующий .env
        with open(env_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Ищем и обновляем VK_CONFIRMATION_CODE
        updated = False
        new_lines = []
        
        for line in lines:
            if line.startswith('VK_CONFIRMATION_CODE='):
                new_lines.append(f'VK_CONFIRMATION_CODE={new_code}\n')
                updated = True
                print(f"🔄 Обновлена строка: VK_CONFIRMATION_CODE={new_code}")
            else:
                new_lines.append(line)
        
        # Если строки не было, добавляем её
        if not updated:
            new_lines.append(f'VK_CONFIRMATION_CODE={new_code}\n')
            print(f"➕ Добавлена строка: VK_CONFIRMATION_CODE={new_code}")
        
        # Записываем обратно
        with open(env_file, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        print("✅ Файл .env обновлён")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка обновления .env файла: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Использование:")
        print("  python update_confirmation.py status          # Показать статус")
        print("  python update_confirmation.py код            # Обновить код")
        print("  python update_confirmation.py код --update-env # Обновить код и .env")
        print()
        print("Примеры:")
        print("  python update_confirmation.py 9a624bd2")
        print("  python update_confirmation.py 9a624bd2 --update-env")
        return
    
    command = sys.argv[1]
    
    if command == "status":
        get_confirmation_status()
    elif command.startswith("-"):
        print("❌ Неверная команда. Используйте 'status' или код подтверждения.")
    else:
        new_code = command
        
        print(f"🔄 Обновление кода подтверждения: {new_code}")
        
        # Обновляем через API
        api_success = update_confirmation_code(new_code)
        
        # Обновляем .env если указан флаг
        if "--update-env" in sys.argv:
            env_success = update_env_file(new_code)
            if api_success and env_success:
                print("✅ Код обновлён через API и в .env файле")
            elif api_success:
                print("⚠️ Код обновлён через API, но не удалось обновить .env")
            elif env_success:
                print("⚠️ Код обновлён в .env, но не удалось обновить через API")
        else:
            if api_success:
                print("💡 Совет: используйте флаг --update-env для обновления .env файла")

if __name__ == "__main__":
    main()
