import re
import requests

# Твоя прямая ссылка на подписку, которая отдает живой заголовок с трафиком
API_URL = "https://pozor.bond/sub/ryz156w0996b"
# Точный путь к твоему файлу конфигурации в репозитории
FILE_NAME = "Vpn-family/Full.yaml"

try:
    # 1. Запрашиваем только заголовки у твоей подписки (HEAD-запрос)
    response = requests.head(API_URL, timeout=10)
    
    # Ищем заголовок подписки
    userinfo = response.headers.get("subscription-userinfo") or response.headers.get("Subscription-Userinfo")

    if userinfo:
        print(f"Поймали живой заголовок с хостинга: {userinfo}")
        
        # Вытаскиваем значение скачанного трафика (download=...)
        download_match = re.search(r"download=(\d+)", userinfo)
        download_bytes = download_match.group(1) if download_match else "0"

        # 2. Читаем твой Full.yaml файл с GitHub
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            content = f.read()

        # 3. Собираем новую строку userinfo для бота (лимит 3 ТБ = 3298534883328 байт)
        new_userinfo = f"# subscription-userinfo: upload=0; download={download_bytes}; total=3298534883328"

        # 4. Заменяем старую строку с userinfo на новую живую
        pattern = r"# subscription-userinfo:.*"
        if re.search(pattern, content):
            updated_content = re.sub(pattern, new_userinfo, content)
        else:
            # Если строки не было, вставляем её самой первой в файл
            updated_content = new_userinfo + "\n" + content

        # 5. Сохраняем обновленный файл обратно в репозиторий
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            f.write(updated_content)

        print(f"Трафик успешно обновлен на Гитхабе! Скачано: {download_bytes} байт.")
    else:
        print("Хостинг не отдал заголовок Subscription-Userinfo. Проверь метки &email=kot_vpn на серверах.")

except Exception as e:
    print(f"Ошибка при выполнении скрипта: {e}")
