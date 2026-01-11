import asyncio
import re
import os
import sys
from telethon import TelegramClient
from telethon.errors import FloodWaitError

if sys.version_info < (3, 7):
    print("Ошибка: Требуется Python 3.7 или новее!")
    print(f"Текущая версия: {sys.version}")
    sys.exit(1)

BANNER = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║              СОЗДАНО @pentawork ДЛЯ ТРОЛЛЕЙ              ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""

TEXT_FILE = "text.txt"
SESSION_DIR = "session"
SESSION_NAME = "telegram_account"
MESSAGE_DELAY = 0

trolled = False

def clean_text(text):
    text = re.sub(r'@\w+\b', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def load_and_process_text(filename):
    try:
        if not os.path.exists(filename):
            print(f"Ошибка: Файл {filename} не найден!")
            print(f"Убедитесь, что файл существует в текущей директории.")
            return []
        
        file_size = os.path.getsize(filename)
        if file_size == 0:
            print(f"Ошибка: Файл {filename} пуст (0 байт)!")
            print(f"Пожалуйста, добавьте текст в файл {filename}")
            return []
        
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        non_empty_lines = [line for line in lines if line.strip()]
        
        if not non_empty_lines:
            print(f"Ошибка: Файл {filename} содержит только пустые строки!")
            return []
        
        text = ' '.join([line.strip() for line in non_empty_lines])
        
        if not text or not text.strip():
            print(f"Ошибка: Файл {filename} содержит только пробелы!")
            return []
        
        text = clean_text(text)
        
        if not text or not text.strip():
            print(f"Ошибка: После обработки текст стал пустым!")
            return []
        
        words = text.split()
        words = [w for w in words if w.strip()]
        
        if not words:
            print(f"Ошибка: Не удалось извлечь слова из файла!")
            return []
        
        return words
    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден!")
        print(f"Убедитесь, что файл существует в текущей директории.")
        return []
    except UnicodeDecodeError as e:
        print(f"Ошибка кодировки при чтении файла {filename}: {e}")
        print(f"Попробуйте сохранить файл в кодировке UTF-8")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла {filename}: {e}")
        import traceback
        traceback.print_exc()
        return []

async def spam_messages(client, chat_entity, words):
    if not words:
        print("❌ Нет слов для отправки!")
        return
    
    CHUNK_SIZE = 5000
    total_words = len(words)
    
    try:
        for chunk_start in range(0, total_words, CHUNK_SIZE):
            chunk_end = min(chunk_start + CHUNK_SIZE, total_words)
            chunk = words[chunk_start:chunk_end]
            
            for word in chunk:
                try:
                    await client.send_message(chat_entity, word)
                except (asyncio.CancelledError, KeyboardInterrupt):
                    raise
                except FloodWaitError as e:
                    await asyncio.sleep(e.seconds)
                    try:
                        await client.send_message(chat_entity, word)
                    except:
                        continue
                except Exception:
                    continue
    except (asyncio.CancelledError, KeyboardInterrupt):
        raise

async def main():
    global trolled
    
    print(BANNER)
    
    words = load_and_process_text(TEXT_FILE)
    if not words:
        print("Не удалось загрузить слова из файла!")
        return
    
    if not os.path.exists(SESSION_DIR):
        os.makedirs(SESSION_DIR)
        print(f"Создана папка {SESSION_DIR}/")
    
    session_file = os.path.join(SESSION_DIR, f"{SESSION_NAME}.session")
    
    print("\n" + "="*50)
    print("НАСТРОЙКА TELEGRAM API")
    print("="*50)
    print("Получите API credentials на https://my.telegram.org")
    print("Войдите с номером телефона -> API development tools")
    print()
    
    try:
        api_id_input = input("Введите API ID: ").strip()
    except KeyboardInterrupt:
        print("\n\nникого не затролили это плохо.... @pentawork недоволен")
        return
    
    if not api_id_input:
        print("❌ API ID обязателен!")
        return
    
    try:
        api_id = int(api_id_input)
    except ValueError:
        print("❌ API ID должен быть числом!")
        return
    
    try:
        api_hash = input("Введите API Hash: ").strip()
    except KeyboardInterrupt:
        print("\n\nникого не затролили это плохо.... @pentawork недоволен")
        return
    
    if not api_hash:
        print("❌ API Hash обязателен!")
        return
    
    client = TelegramClient(
        session_file,
        api_id,
        api_hash
    )
    
    try:
        print("\n" + "="*50)
        print("ПОДКЛЮЧЕНИЕ К TELEGRAM")
        print("="*50)
        print("Следуйте инструкциям в терминале для авторизации...")
        await client.start()
        
        if not await client.is_user_authorized():
            print("\n❌ Не удалось авторизоваться!")
            print("Попробуйте удалить файл сессии из папки session/ и попробовать снова")
            return
        
        me = await client.get_me()
        print(f"\n✓ Подключен как: {me.first_name} (@{me.username})")
        print(f"✓ Сессия сохранена в: {session_file}")
        print(f"✓ При следующем запуске сессия будет использована автоматически")
        print(f"✓ Чтобы сменить аккаунт, удалите файл: {session_file}")
        
        print("\n" + "="*50)
        print("ВВЕДИТЕ ID ЧАТА")
        print("="*50)
        print("Введите ID чата (число или username, например: 7663348900 или @username):")
        try:
            chat_input = input().strip()
        except KeyboardInterrupt:
            print("\n\nникого не затролили это плохо.... @pentawork недоволен")
            return
        
        if not chat_input:
            print("❌ ID чата не указан!")
            return
        
        try:
            chat_input_clean = chat_input.lstrip('@')
            
            try:
                chat_id = int(chat_input_clean)
                chat_entity = await client.get_entity(chat_id)
            except (ValueError, TypeError):
                chat_entity = await client.get_entity(chat_input_clean)
            
            chat_info = await client.get_entity(chat_entity)
            chat_name = getattr(chat_info, 'first_name', None) or getattr(chat_info, 'title', None) or getattr(chat_info, 'username', None) or "Неизвестно"
            chat_id = getattr(chat_info, 'id', 'Unknown')
            print(f"✓ Найден чат: {chat_name} (ID: {chat_id})")
            
            trolled = True
            
        except Exception as e:
            print(f"❌ Не удалось найти чат по ID '{chat_input}': {e}")
            return
        
        print(BANNER)
        
        await spam_messages(client, chat_entity, words)
        
    except (asyncio.CancelledError, KeyboardInterrupt):
        pass
    except Exception as e:
        pass
    finally:
        try:
            await client.disconnect()
        except:
            pass

if __name__ == "__main__":
    original_excepthook = sys.excepthook
    
    def custom_excepthook(exctype, value, traceback):
        if exctype == KeyboardInterrupt:
            if trolled:
                print("\n\nахахах затролякан @pentawork доволен")
            else:
                print("\n\nникого не затролили это плохо.... @pentawork недоволен")
            sys.exit(0)
        else:
            original_excepthook(exctype, value, traceback)
    
    sys.excepthook = custom_excepthook
    
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, asyncio.CancelledError):
        if trolled:
            print("\n\nахахах затролякан @pentawork доволен")
        else:
            print("\n\nникого не затролили это плохо.... @pentawork недоволен")
        sys.exit(0)
    except SystemExit:
        pass
