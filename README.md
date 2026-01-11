# Telegram Spam Script

Скрипт для автоматической отправки сообщений в Telegram чат.

**Создано @pentawork для троллей**

## Требования

- Python 3.7 или новее
- pip (менеджер пакетов Python)

## Поддерживаемые платформы

- ✅ Windows (7/8/10/11)
- ✅ Linux (Ubuntu, Debian, Fedora, и др.)
- ✅ Debian 12
- ✅ macOS (10.9+)
- ✅ Android (через Termux)

## Установка

### Windows

1. Скачайте и установите Python с [python.org](https://www.python.org/downloads/)
   - При установке отметьте "Add Python to PATH"

2. Скачайте репозиторий:
```cmd
git clone https://github.com/Kidpun/trolokid.git
cd trolokid
```

3. Установите зависимости:
```cmd
pip install -r requirements.txt
```

4. Запустите скрипт:
```cmd
python main.py
```

### Linux (Ubuntu/Debian)

1. Установите Python и pip:
```bash
sudo apt update
sudo apt install python3 python3-pip git
```

2. Клонируйте репозиторий:
```bash
git clone https://github.com/Kidpun/trolokid.git
cd trolokid
```

3. Установите зависимости:
```bash
pip3 install -r requirements.txt
```

4. Запустите скрипт:
```bash
python3 main.py
```

### Debian 12

1. Установите Python и pip:
```bash
sudo apt update
sudo apt install python3 python3-pip git
```

2. Клонируйте репозиторий:
```bash
git clone https://github.com/Kidpun/trolokid.git
cd trolokid
```

3. Установите зависимости:
```bash
pip3 install -r requirements.txt
```

4. Запустите скрипт:
```bash
python3 main.py
```

### macOS

1. Установите Python (если не установлен):
```bash
brew install python3
```
Или скачайте с [python.org](https://www.python.org/downloads/)

2. Клонируйте репозиторий:
```bash
git clone https://github.com/Kidpun/trolokid.git
cd trolokid
```

3. Установите зависимости:
```bash
pip3 install -r requirements.txt
```

4. Запустите скрипт:
```bash
python3 main.py
```

### Termux (Android)

1. Установите Termux с [F-Droid](https://f-droid.org/packages/com.termux/) или [Google Play](https://play.google.com/store/apps/details?id=com.termux)

2. Откройте Termux и обновите пакеты:
```bash
pkg update && pkg upgrade
```

3. Установите Python и git:
```bash
pkg install python git
```

4. Клонируйте репозиторий:
```bash
git clone https://github.com/Kidpun/trolokid.git
cd trolokid
```

5. Установите зависимости:
```bash
pip install -r requirements.txt
```

6. Запустите скрипт:
```bash
python main.py
```

## Настройка

1. Получите API credentials на [https://my.telegram.org](https://my.telegram.org):
   - Войдите с номером телефона
   - Перейдите в "API development tools"
   - Создайте приложение и получите `api_id` и `api_hash`

2. Подготовьте файл `text.txt`:
   - Поместите текст для отправки в файл `text.txt` в корне проекта
   - Скрипт автоматически удалит все упоминания, начинающиеся с `@` (например, `@username`)
   - Пустые строки также будут автоматически отфильтрованы

## Использование

1. Запустите скрипт:
   - **Windows:** `python main.py`
   - **Linux/macOS:** `python3 main.py`
   - **Termux:** `python main.py`

2. Введите данные при запросе:
   - **API ID** - ваш API ID с https://my.telegram.org
   - **API Hash** - ваш API Hash
   - **Номер телефона** - ваш номер в формате +79991234567
   - **Код подтверждения** - код из Telegram
   - **Облачный пароль (2FA)** - если у вас включена двухфакторная аутентификация

3. Введите ID чата для спама:
   - Можно использовать числовой ID (например: 7663348900)
   - Или username (например: @username)

4. Скрипт автоматически:
   - Сохранит сессию в папку `session/telegram_account.session`
   - Начнет отправлять слова из `text.txt` в указанный чат

## Сессии

- **Папка `session/` создается автоматически** при первом запуске скрипта (не нужно создавать вручную)
- Сессия автоматически сохраняется в папку `session/` при первой авторизации
- При следующих запусках сессия будет использоваться автоматически (не нужно вводить API credentials и авторизоваться снова)
- Чтобы сменить аккаунт, удалите файл `session/telegram_account.session` и запустите скрипт заново

## Настройка скорости

В файле `main.py` можно изменить переменную `MESSAGE_DELAY`:
- `MESSAGE_DELAY = 0` - максимальная скорость (без задержек)
- `MESSAGE_DELAY = 0.05` - задержка 0.05 секунд между сообщениями
- `MESSAGE_DELAY = 0.2` - задержка 0.2 секунд между сообщениями

## Репозиторий

Репозиторий: [https://github.com/Kidpun/trolokid](https://github.com/Kidpun/trolokid)

## Внимание

- Использование спама может привести к блокировке аккаунта
- Используйте на свой риск
- Не злоупотребляйте отправкой сообщений
