# TgExportParser

## English

TgExportParser is a Python script designed to convert Telegram export HTML files into Markdown format. It parses chat exports from Telegram, extracting messages, authors, timestamps, and links, and saves them in a readable Markdown format along with a separate file containing all found links.

### Features
- Converts HTML exports to Markdown
- Extracts message text, author names, and timestamps
- Collects and saves all links found in messages
- Handles service messages (e.g., user joined/left)
- Safe filename generation for Windows compatibility
- Comprehensive logging with loguru

### Installation
1. Clone the repository:
   ```
   git clone https://github.com/alex-lik/TgExportParser.git
   cd TgExportParser
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Usage
1. Place your Telegram export HTML files in the `exports/` directory.
2. Run the script:
   ```
   python main.py
   ```
3. Processed Markdown files and link lists will be saved in the `results/` directory.

### Example
Assuming you have an export file `MyChat.html` in `exports/`:
- Input: `exports/MyChat.html`
- Output: `results/MyChat.md` (Markdown with messages)
- Output: `results/MyChat_links.txt` (list of links, if any)

### Dependencies
- beautifulsoup4
- loguru

### License
MIT License

## Русский

TgExportParser - это Python-скрипт, предназначенный для конвертации HTML-файлов экспорта Telegram в формат Markdown. Он анализирует экспорты чатов из Telegram, извлекает сообщения, имена авторов, время и ссылки, и сохраняет их в читаемом формате Markdown вместе с отдельным файлом, содержащим все найденные ссылки.

### Возможности
- Конвертирует HTML-экспорты в Markdown
- Извлекает текст сообщений, имена авторов и время
- Собирает и сохраняет все ссылки, найденные в сообщениях
- Обрабатывает сервисные сообщения (например, пользователь присоединился/покинул)
- Безопасная генерация имен файлов для совместимости с Windows
- Комплексное логирование с использованием loguru

### Установка
1. Клонируйте репозиторий:
   ```
   git clone https://github.com/yourusername/TgExportParser.git
   cd TgExportParser
   ```
2. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```

### Использование
1. Поместите HTML-файлы экспорта Telegram в папку `exports/`.
2. Запустите скрипт:
   ```
   python main.py
   ```
3. Обработанные файлы Markdown и списки ссылок будут сохранены в папке `results/`.

### Пример
Предположим, у вас есть файл экспорта `MyChat.html` в `exports/`:
- Вход: `exports/MyChat.html`
- Выход: `results/MyChat.md` (Markdown с сообщениями)
- Выход: `results/MyChat_links.txt` (список ссылок, если есть)

### Зависимости
- beautifulsoup4
- loguru

### Лицензия
Лицензия MIT