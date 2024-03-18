#!/usr/bin/env python3
# -*- codeing: utf-8 -*-

import json
import sys
from jsonschema import validate
from jsonschema.exceptions import ValidationError

# Для своего варианта лабораторной работы 2.8 необходимо дополнительно
# реализовать сохранение и чтение данных из файла формата JSON. Необходимо
# также проследить за тем, чтобы файлы генерируемый этой программой не
# попадали в репозиторий лабораторной работы.

# Использовать словарь, содержащий следующие ключи: фамилия, имя; номер
# телефона; дата рождения (список из трех чисел). Написать программу,
# выполняющую следующие действия: ввод с клавиатуры данных в список, состоящий
# из словарей заданной структуры; записи должны быть размещены по алфавиту;
# вывод на экран информации о людях, чьи дни рождения приходятся на месяц,
# значение которого введено с клавиатуры; если таких нет, выдать на дисплей
# соответствующее сообщение.


def get_worker():
    """
    Запросить данные о работнике.
    """
    surname = input("Фамилия: ")
    name = input("Имя: ")
    phone = input("Номер телефона: ")
    year = input("Дата рождения (пример: 05 07 2004): ")

    # Создать словать
    return {
        "surname": surname,
        "name": name,
        "phone": phone,
        "year": year,
    }


def display_workers(staff):
    """
    Отобразить список работников.
    """
    # Проверить, что список работников не пуст.
    if staff:
        # Заголовок таблицы.
        line = "+-{}-+-{}-+-{}-+-{}-+-{}-+".format(
            "-" * 4, "-" * 20, "-" * 20, "-" * 20, "-" * 15
        )
        print(line)
        print(
            "| {:^4} | {:^20} | {:^20} | {:^20} | {:^15} |".format(
                "№", "Фамилия", "Имя", "Номер телефона", "Дата рождения"
            )
        )
        print(line)

        # Вывести данные о всех сотрудниках
        for idx, worker in enumerate(staff, 1):
            print(
                "| {:>4} | {:<20} | {:<20} | {:<20} | {:>15} |".format(
                    idx,
                    worker.get("surname", ""),
                    worker.get("name", ""),
                    worker.get("phone", ""),
                    worker.get("year", ""),
                )
            )
        print(line)

    else:
        print("Список работников пуст.")


def select_workers(staff, month):
    """
    Выбрать работников у которых день рожения в указанный месяц.
    """
    # Сформировать список работников.
    result = [
        employee
        for idx, employee in enumerate(staff)
        if int(employee.get("year").split()[1]) == month
    ]

    # Возвратить список выбранных работников.
    return result


def save_workers(file_name, staff):
    """
    Сохранить всех работников в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_workers(file_name):
    """
    Загрузить всех работников из файла JSON.
    """
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as f:
        document = json.load(f)

    if all(list(map(lambda x: check_validation_json(x), document))):
        return document
    else:
        False


def check_validation_json(file_name):
    with open('worker-schema.json') as f:
        schema = json.load(f)

    try:
        validate(instance=file_name, schema=schema)
        return True
    except ValidationError:
        return False


def main():
    """
    Главная функция программы.
    """
    # Список работников.
    workers = []
    # Организовать бесконечный цикл запроса команд.
    while True:
        # Запросить команду из терминала.
        command = input(">>> ").lower()

        # Выполнить действие в соответствие с командой.
        if command == "exit":
            break

        elif command == "add":
            # Запросить данные о работнике.
            worker = get_worker()
            # Добавить словарь в список.
            workers.append(worker)
            # Отсортировать список в случае необходимости.
            if len(workers) > 1:
                workers.sort(key=lambda item: item.get("name", ""))

        elif command == "list":
            # Отобразить всех работников.
            display_workers(workers)

        elif command.startswith("select "):
            # Разбить команду на части для выделения стажа.
            parts = command.split(maxsplit=1)
            # Получить требуемый месяц.
            period = int(parts[1])

            # Выбрать работников с заданным стажем.
            selected = select_workers(workers, period)
            # Отобразить выбранных работников.
            display_workers(selected)

        elif command.startswith("save "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]

            # Сохранить данные в файл с заданным именем.
            save_workers(file_name, workers)

        elif command.startswith("load "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]

            # Сохранить данные в файл с заданным именем.
            if load_workers(file_name):
                workers = load_workers(file_name)
            else:
                print("Error Validation JSON")

        elif command == "help":
            # Вывести справку о работе с программой.
            print("Список команд:\n")
            print("add - добавить работника;")
            print("list - вывести список работников;")
            print("select <месяц> - запросить работников у которых день"
                  "рождения совподает с указанным месяцем;")
            print("help - отобразить справку;")
            print("load - загрузить данные из файла;")
            print("save - сохранить данные в файл;")
            print("exit - завершить работу с программой.")

        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)


if __name__ == "__main__":
    main()
