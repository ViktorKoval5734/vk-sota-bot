#!/usr/bin/env python3
"""
Тест системы обработки оскорблений бота "Сота Сил"
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from hostile_responses import hostile_response_manager
import time

def test_aggressive_patterns():
    """Тест определения агрессивных сообщений"""
    print("🧪 ТЕСТ: Определение агрессивных сообщений")
    print("=" * 50)
    
    # Тестовые сообщения разной степени агрессивности
    test_messages = [
        # Прямые оскорбления
        ("Заткнись, бот!", True),
        ("Ты дурак!", True),
        ("Иди нахуй!", True),
        ("Ты уёбок!", True),
        
        # Команды молчать
        ("Молчи!", True),
        ("Замолчи, Сота!", True),
        ("Не пиши больше!", True),
        
        # Нейтральные сообщения
        ("Привет, Сота!", False),
        ("Как дела?", False),
        ("Расскажи о Заводном городе", False),
        
        # Сложные оскорбления
        ("Тупой бесполезный бот", True),
        ("Ты ничтожество", True),
        ("Отстой, а не бот", True),
        
        # Эвемеристические оскорбления
        ("Говоришь как аргонианин", True),
        ("Твой уровень знаний хуже каджита", True),
    ]
    
    for message, expected in test_messages:
        is_aggressive = hostile_response_manager.is_aggressive_message(message)
        status = "✅" if is_aggressive == expected else "❌"
        print(f"{status} '{message}' -> {is_aggressive} (ожидалось: {expected})")
    
    print()

def test_cooldown_system():
    """Тест системы кулдауна"""
    print("⏰ ТЕСТ: Система кулдауна")
    print("=" * 50)
    
    # Сбрасываем время последнего ответа
    hostile_response_manager.last_response_time = 0
    hostile_response_manager._save_last_response_time(0)
    
    print(f"Текущий кулдаун: {hostile_response_manager.response_cooldown} секунд")
    
    # Первый ответ должен пройти
    response1 = hostile_response_manager.generate_harsh_response()
    print(f"✅ Первый ответ: {response1[:60]}...")
    
    # Второй ответ должен быть заблокирован (кулдаун)
    response2 = hostile_response_manager.generate_harsh_response()
    if response2 is None:
        print("✅ Второй ответ заблокирован кулдауном")
    else:
        print(f"❌ Второй ответ прошёл: {response2[:60]}...")
    
    # Статистика
    stats = hostile_response_manager.get_stats()
    print(f"📊 Статистика: {stats}")
    print()

def test_harsh_responses():
    """Тест генерации резких ответов"""
    print("💢 ТЕСТ: Генерация резких ответов")
    print("=" * 50)
    
    # Сбрасываем кулдаун
    hostile_response_manager.last_response_time = 0
    hostile_response_manager._save_last_response_time(0)
    
    print("Доступные резкие ответы:")
    for i, response in enumerate(hostile_response_manager.hostile_responses, 1):
        print(f"{i:2d}. {response}")
    
    print(f"\nВсего ответов: {len(hostile_response_manager.hostile_responses)}")
    print()

def test_integration_with_bot():
    """Тест интеграции с ботом"""
    print("🤖 ТЕСТ: Интеграция с ботом")
    print("=" * 50)
    
    # Сбрасываем кулдаун для тестирования
    hostile_response_manager.last_response_time = 0
    hostile_response_manager._save_last_response_time(0)
    
    # Симулируем обработку сообщений ботом
    test_scenarios = [
        {
            "user": "Алексей",
            "message": "Заткнись, тупой бот!",
            "expected": "hostile"
        },
        {
            "user": "Мария", 
            "message": "Привет, Сота! Как дела?",
            "expected": "normal"
        },
        {
            "user": "Иван",
            "message": "Ты бесполезный отстой",
            "expected": "hostile"
        }
    ]
    
    for scenario in test_scenarios:
        message = scenario["message"]
        user = scenario["user"]
        expected = scenario["expected"]
        
        print(f"👤 {user}: '{message}'")
        
        # Проверяем агрессивность
        is_aggressive = hostile_response_manager.is_aggressive_message(message)
        
        if is_aggressive and expected == "hostile":
            harsh_response = hostile_response_manager.generate_harsh_response()
            if harsh_response:
                print(f"💢 Ответ: {harsh_response}")
            else:
                print("⏰ Ответ заблокирован кулдауном")
        elif not is_aggressive and expected == "normal":
            print("✅ Нейтральное сообщение - отправляется в Гигачат")
        else:
            print(f"❌ Неожиданный результат: агрессивность={is_aggressive}, ожидалось={expected}")
        
        print()

if __name__ == "__main__":
    print("🎯 ТЕСТИРОВАНИЕ СИСТЕМЫ ОБРАБОТКИ ОСКОРБЛЕНИЙ")
    print("Бот 'Сота Сил' - VK")
    print("=" * 60)
    print()
    
    try:
        test_aggressive_patterns()
        test_cooldown_system()
        test_harsh_responses()
        test_integration_with_bot()
        
        print("🎉 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        import traceback
        traceback.print_exc()