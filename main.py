import asyncio
import re
import os
import sys
import random
from telethon import TelegramClient
from telethon.errors import FloodWaitError

# Поддержка .env (опционально)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

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
MESSAGE_DELAY = 0.5  # задержка между сообщениями (сек), 0 = без задержки (риск FloodWait бана)

trolled = False


def clean_text(text: str) -> str:
    """Удаляет @упоминания и лишние пробелы из текста."""
    text = re.sub(r'@\w+\b', '', text)
    return re.sub(r'\s+', ' ', text).strip()


def load_and_process_text(filename: str) -> list[str]:
    """Читает файл, очищает текст и возвращает список слов."""
    if not os.path.exists(filename):
        print(f"Ошибка: Файл {filename} не найден!")
        print("Убедитесь, что файл существует в текущей директории.")
        return []

    try:
        file_size = os.path.getsize(filename)
        if file_size == 0:
            print(f"Ошибка: Файл {filename} пуст (0 байт)!")
            print(f"Пожалуйста, добавьте текст в файл {filename}")
            return []

        with open(filename, 'r', encoding='utf-8') as f:
            raw = f.read()

    except UnicodeDecodeError as e:
        print(f"Ошибка кодировки при чтении файла {filename}: {e}")
        print("Попробуйте сохранить файл в кодировке UTF-8")
        return []
    except OSError as e:
        print(f"Ошибка при чтении файла {filename}: {e}")
        return []

    text = clean_text(raw)
    if not text:
        print(f"Ошибка: Файл {filename} не содержит текста!")
        return []

    words = [w for w in text.split() if w]
    if not words:
        print("Ошибка: Не удалось извлечь слова из файла!")
        return []

    return words


async def spam_messages(client: TelegramClient, chat_entity, words: list[str]):
    if not words:
        print("❌ Нет слов для отправки!")
        return

    CHUNK_SIZE = 5000
    total_words = len(words)
    sent_count = 0

    try:
        for chunk_start in range(0, total_words, CHUNK_SIZE):
            chunk = words[chunk_start:min(chunk_start + CHUNK_SIZE, total_words)]

            for word in chunk:
                try:
                    await client.send_message(chat_entity, word)
                    sent_count += 1
                    if sent_count % 50 == 0:
                        print(f"📨 Отправлено {sent_count}/{total_words} слов...")
                    if MESSAGE_DELAY > 0:
                        await asyncio.sleep(MESSAGE_DELAY)

                except (asyncio.CancelledError, KeyboardInterrupt):
                    raise
                except FloodWaitError as e:
                    print(f"⏳ FloodWait: ожидание {e.seconds} сек...")
                    await asyncio.sleep(e.seconds + 1)
                    try:
                        await client.send_message(chat_entity, word)
                        sent_count += 1
                    except Exception:
                        continue
                except Exception as e:
                    print(f"⚠️ Ошибка отправки слова '{word}': {e}")
                    continue

    except (asyncio.CancelledError, KeyboardInterrupt):
        print(f"\n⚠️ Остановлено. Отправлено {sent_count}/{total_words} слов.")
        raise


async def main():
    global trolled

    print(BANNER)

    words = load_and_process_text(TEXT_FILE)
    if not words:
        print("Не удалось загрузить слова из файла!")
        return

    os.makedirs(SESSION_DIR, exist_ok=True)
    session_file = os.path.join(SESSION_DIR, f"{SESSION_NAME}.session")

    # Читаем из .env или запрашиваем вручную
    api_id_env = os.getenv("API_ID", "").strip()
    api_hash_env = os.getenv("API_HASH", "").strip()

    if api_id_env and api_hash_env:
        try:
            api_id = int(api_id_env)
            api_hash = api_hash_env
        except ValueError:
            print("❌ API_ID в .env должен быть числом!")
            return
    else:
        print("\n" + "=" * 50)
        print("НАСТРОЙКА TELEGRAM API")
        print("=" * 50)
        print("Получите API credentials на https://my.telegram.org")
        print("Или создайте .env файл с API_ID и API_HASH")
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

    client = TelegramClient(session_file, api_id, api_hash)

    try:
        print("\n" + "=" * 50)
        print("ПОДКЛЮЧЕНИЕ К TELEGRAM")
        print("=" * 50)
        await client.start()

        if not await client.is_user_authorized():
            print("\n❌ Не удалось авторизоваться!")
            print("Попробуйте удалить файл сессии из папки session/ и попробовать снова")
            return

        me = await client.get_me()
        username_str = f"@{me.username}" if me.username else "без username"
        print(f"\n✓ Подключен как: {me.first_name} ({username_str})")
        print(f"✓ Сессия сохранена в: {session_file}")

        print("\n" + "=" * 50)
        print("ВВЕДИТЕ ID ЧАТА")
        print("=" * 50)
        print("Введите ID чата (число или @username):")
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
                chat_entity = await client.get_entity(int(chat_input_clean))
            except (ValueError, TypeError):
                chat_entity = await client.get_entity(chat_input_clean)

            chat_name = (
                getattr(chat_entity, 'first_name', None)
                or getattr(chat_entity, 'title', None)
                or getattr(chat_entity, 'username', None)
                or "Неизвестно"
            )
            print(f"✓ Найден чат: {chat_name} (ID: {chat_entity.id})")
            trolled = True

        except Exception as e:
            print(f"❌ Не удалось найти чат '{chat_input}': {e}")
            return

        print(BANNER)
        await spam_messages(client, chat_entity, words)

    except (asyncio.CancelledError, KeyboardInterrupt):
        pass
    except Exception as e:
        print(f"\n❌ Неожиданная ошибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            await client.disconnect()
        except Exception:
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
