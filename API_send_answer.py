import requests
from login import *
import time


def send_answer(from_mail, subject_tema, content_telo, answer_otvet):
    if answer_otvet == "[Ответить]":
        print(
            f"По API ОТВЕТ id: {subject_tema} текст: '{content_telo}'. Тип ответа: {answer_otvet}"
        )
        return answer_question(subject_tema, content_telo)

    elif answer_otvet == "[Отклонить]":
        print(
            f"По API ОТКЛОНИТЬ id: {subject_tema} коммент: '{content_telo}'. Тип ответа: {answer_otvet}"
        )
        return reject_question(subject_tema, content_telo)
    else:
        print(f"По API НЕ отправляю. Т.к. не нашел тип ответа в письме.")


url = "https://feedbacks-api.wildberries.ru/api/v1/questions"
headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Authorization": API_KEY,
}


# отклонить
def reject_question(id, text):
    data = {
        "id": id,
        "answer": {"text": text},
        "state": "none",
    }
    for attempt in range(3):  # Всего 3 попытки
        try:
            response = requests.patch(url, headers=headers, json=data)
            print(
                f"Запрос отправлен статус-код: {response.status_code}. Ответ json: {response.json()}"
            )
            break  # Выход из цикла, если запрос успешен
        except requests.exceptions.RequestException as e:
            if attempt < 2:  # Если это не последняя попытка
                print(
                    f"Ошибка при отправке запроса: {e}. Повторная попытка через 10 секунд..."
                )
                time.sleep(10)
            else:
                print(f"Все попытки завершились неудачно. ID вопроса = {id}")
                return "ERROR"
    return "OK"


# ответить
def answer_question(id, text):
    data = {
        "id": id,
        "answer": {"text": text},
        "state": "wbRu",
    }
    for attempt in range(3):  # Всего 3 попытки
        try:
            response = requests.patch(url, headers=headers, json=data)
            print(
                f"Запрос отправлен статус-код: {response.status_code}. Ответ json: {response.json()}"
            )
            break  # Выход из цикла, если запрос успешен
        except requests.exceptions.RequestException as e:
            if attempt < 2:  # Если это не последняя попытка
                print(
                    f"Ошибка при отправке запроса: {e}. Повторная попытка через 10 секунд..."
                )
                time.sleep(10)
            else:
                print(f"Все попытки завершились неудачно. ID вопроса = {id}")
                return "ERROR"
    return "OK"
