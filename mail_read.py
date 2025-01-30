import imaplib
import email
from email.header import decode_header
import time
from bs4 import BeautifulSoup
from login import *
from API_send_answer import send_answer


def mark_as_unread(mail, num):
    try:
        status = mail.store(num, "+FLAGS", "\\Seen")
        if status[0] != "OK":
            print(f"Ошибка при установке флага 'Seen': {status[0]}")
            return
        status = mail.store(num, "-FLAGS", "\\Seen")
        if status[0] != "OK":
            print(f"Ошибка при сбросе флага 'Seen': {status[0]}")
        else:
            print(f"Письмо снова помечено как непрочитанное.")
    except imaplib.IMAP4.error as e:
        print(f"Ошибка IMAP: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")


def start_sending_answers():
    # Подключение к серверу
    print("Подключаюсь к почтовому северу.")
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(IMAP_USERNAME, IMAP_PASSWORD)

    # Выбор почтового ящика (INBOX - это стандартное имя для входящих писем)
    mail.select("INBOX")

    # Поиск непрочитанных писем
    status, message_ids = mail.search(None, "UNSEEN")

    # Обработка каждого непрочитанного письма
    for num in message_ids[0].split():
        print("Начинаю обработку непрочитанных писем.")
        status, msg_parts = mail.fetch(num, "(RFC822)")
        raw_email = msg_parts[0][1]

        # Парсинг письма
        msg = email.message_from_bytes(raw_email)

        # Игнорирование ответных писем
        if msg.get_content_type() == "message/rfc822":
            continue

        # Получение отправителя
        sender = msg["Return-path"]

        # Получение темы письма
        subject = decode_header(msg["Subject"])[0][0]
        # Декодирую байтовую строку в обычную строку
        subject = subject.decode("utf-8")

        # Получение содержимого письма
        content = ""
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/html":
                content = (
                    part.get_payload(decode=True)
                    .decode(part.get_content_charset())
                    .split("\n")[0]
                    .strip()
                )
        from_mail = sender

        if from_mail == TRUSTED_MAIL:
            subject_tema = subject.replace("Re: ", "")

            html_content = content.split("_____")

            # Функция для удаления HTML-тегов из строки
            def remove_html_tags(html_str):
                soup = BeautifulSoup(html_str, "html.parser")
                return soup.get_text(separator=" ", strip=True)

            # Применяю функцию ко всем элементам списка
            cleaned_content = [remove_html_tags(part) for part in html_content]

            content_telo = cleaned_content[1]
            answer_otvet = cleaned_content[0]
            if (
                send_answer(from_mail, subject_tema, content_telo, answer_otvet)
                == "ERROR"
            ):
                mark_as_unread(mail, num)
        else:
            print(
                f"Неподтвержденный email {from_mail}. Отправка ответа по API произведена не будет."
            )
        print("-" * 30)
        time.sleep(4)
    print("Непрочитанных писем нет. Отключаюсь от сервера.")
    print("******************STOP******************")
    mail.close()
    mail.logout()


def start_checking_mail():
    print("******************START******************")
    start_sending_answers()
