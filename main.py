import os
import sys
import re
from pathlib import Path
from bs4 import BeautifulSoup
from loguru import logger

EXPORTS_DIR = Path("exports")
RESULTS_DIR = Path("results")
LOGS_DIR = Path("logs")

RESULTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)


def safe_filename(name: str) -> str:
    """Удаляет недопустимые символы из имени файла для Windows"""
    return re.sub(r'[<>:"/\\|?*]', "_", name)[:100]  # Ограничим до 100 символов


def parse_telegram_html(html_content: str, links: list) -> str:
    """Парсит HTML экспорт Telegram в Markdown, собирает ссылки"""
    soup = BeautifulSoup(html_content, "html.parser")
    output_lines = []

    # Заголовок канала/чата
    header = soup.select_one(".page_header .text")
    if header:
        output_lines.append(f"# {header.text.strip()}\n")

    messages = soup.select(".message")

    for msg in messages:
        try:
            # Сервисные сообщения
            if "service" in msg.get("class", []):
                details = msg.select_one(".body.details")
                if details:
                    output_lines.append(f"**_{details.text.strip()}_**\n")
                continue

            # Автор
            from_name = msg.select_one(".from_name")
            author = from_name.text.strip() if from_name else ""

            # Время
            date_div = msg.select_one(".date.details")
            time = date_div.text.strip() if date_div else ""

            # Текст сообщения
            text_div = msg.select_one(".text")
            if text_div:
                for br in text_div.find_all("br"):
                    br.replace_with("\n")
                text = text_div.get_text("\n").strip()
            else:
                text = ""

            if not text:
                continue  # пустые сообщения пропускаем

            # Собираем ссылки
            found_links = re.findall(r'https?://\S+|t\.me/\S+', text)
            links.extend(found_links)

            # Блок сообщения
            block = f"**{author}** ({time})\n{text}\n"
            output_lines.append(block)

        except Exception as e:
            logger.exception(f"Ошибка при обработке сообщения {msg.get('id')}: {e}")

    return "\n".join(output_lines)


def process_file(file_path: Path):
    """Обрабатывает один HTML-файл"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, "html.parser")

        # Определяем имя чата
        header = soup.select_one(".page_header .text")
        chat_name = header.text.strip() if header else file_path.stem

        safe_name = safe_filename(chat_name)

        # Логирование
        log_file = LOGS_DIR / f"{safe_name}.log"
        logger.remove()
        logger.add(sys.stderr, level="INFO")
        logger.add(log_file, level="DEBUG", rotation="1 MB", encoding="utf-8")

        logger.info(f"Обрабатываю файл: {file_path.name}, чат: {chat_name}")

        links = []
        md_output = parse_telegram_html(html_content, links)

        # Markdown файл
        result_file = RESULTS_DIR / f"{safe_name}.md"
        with open(result_file, "w", encoding="utf-8") as f:
            f.write(md_output)

        # Файл ссылок (если есть)
        if links:
            links_file = RESULTS_DIR / f"{safe_name}_links.txt"
            with open(links_file, "w", encoding="utf-8") as f:
                f.write("\n".join(sorted(set(links))))
            logger.info(f"Найдено ссылок: {len(links)} (сохранены в {links_file.name})")

        logger.success(f"Файл {file_path.name} → {result_file.name}")

    except Exception as e:
        logger.exception(f"Ошибка при обработке файла {file_path.name}: {e}")


def main():
    if not EXPORTS_DIR.exists():
        print(f"Папка {EXPORTS_DIR} не найдена")
        return

    files = list(EXPORTS_DIR.glob("*.html"))
    if not files:
        print("Нет файлов для обработки в папке exports")
        return

    for file_path in files:
        process_file(file_path)


if __name__ == "__main__":
    main()
