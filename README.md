# Performance-engineer
- Поднял виртуальную машину на OS Linux (Ubuntu 20.04) и PostgreSQL 16
- Создал базу и добавил таблицу
 ```bash
CREATE TABLE имя_твоей таблицы (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    address VARCHAR(255)
);
```
где : 
1) CREATE TABLE имя_твоей таблицы - это начало команды, которое указывает СУБД на то, что вы хотите создать новую таблицу с именем имя_твоей таблицы.
2) (id SERIAL PRIMARY KEY) - это определение столбца id. Столбец id представляет собой уникальный идентификатор для каждой строки в таблице. Ключевое слово SERIAL указывает на то, что это столбец с автоинкрементным значением, который генерируется автоматически. Ключевое слово PRIMARY KEY определяет столбец id в качестве первичного ключа таблицы, что означает, что каждое значение в этом столбце должно быть уникальным и не может быть NULL.
3) name VARCHAR(255), email VARCHAR(255), address VARCHAR(255) - это определения столбцов name, email и address. Каждый из них имеет тип данных VARCHAR, что означает переменную длину строки, и максимальную длину 255 символов.
- Написал программу вставки данных в PostgreSQL на Python название.py
- перед запуском нужно установить зависимости
  ```bash
  pip install --upgrade pip &&
  pip install --no-binary :all: psycopg2  &&
  sudo apt-get install python3-psycopg2 &&
  sudo apt-get install faker 
  ```
```bash import psycopg2
import time
import argparse
import concurrent.futures
from faker import Faker

# Функция для вставки данных в базу данных
def insert_data(thread_id, duration):
    conn = psycopg2.connect(database="имя_базы", user="рользователь_базы", password="пароль_базы", host="адрес_host", port="порт_базы")
    cur = conn.cursor()
    fake = Faker()
    start_time = time.time()
    while (time.time() - start_time) < duration:
        data = (fake.name(), fake.email(), fake.address())
        cur.execute("INSERT INTO имя_твоей таблицы (name, email, address) VALUES (%s, %s, %s)", data)
        conn.commit()
    cur.close()
    conn.close()

# Функция для запуска параллельных потоков
def main(num_threads, duration):
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_thread = {executor.submit(insert_data, thread_id, duration): thread_id for thread_id in range(num_threads)}
        for future in concurrent.futures.as_completed(future_to_thread):
            thread_id = future_to_thread[future]
            try:
                future.result()
            except Exception as exc:
                print(f"Thread {thread_id} generated an exception: {exc}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Insert fake data into PostgreSQL")
    parser.add_argument("--threads", type=int, help="Number of parallel threads")
    parser.add_argument("--duration", type=int, help="Duration of insertion in seconds")
    args = parser.parse_args()
    main(args.threads, args.duration)
```
где:
1) psycopg2 - библиотека Python для работы с PostgreSQL.
2) time - модуль для работы со временем.
3) argparse - модуль для парсинга аргументов командной строки.
4) concurrent.futures -  модуль для запуска параллельных задач.
5) Faker - библиотека для генерации фальшивых данных.
6) insert_data(thread_id, duration) -  отвечает за вставку данных в базу данных, открывает соединение с базой данных PostgreSQL, создает курсор для выполнения SQL-запросов, генерирует фальшивые данные с помощью Faker, вставляет их в таблицу имя_твоей таблицы и закрывает соединение.
7) main(num_threads, duration) -  создает пул параллельных потоков с помощью ThreadPoolExecutor, запускает функцию insert_data в каждом потоке и ожидает завершения всех потоков.
8) main - определяет, как скрипт будет обрабатывать аргументы командной строки, такие как количество потоков (--threads) и длительность вставки (--duration). Затем он вызывает функцию main с переданными аргументами
- Запускаем скрипт

   ```bash
  python3 название.py --threads 5 --duration 600
   ```
  

 где:
1) python3 название.py - это команда для запуска скрипта с помощью интерпретатора Python 3
2) --threads 5 - этот аргумент указывает количество параллельных потоков, которые будут использоваться для вставки данных. В данном случае установлено значение 5, что означает, что скрипт будет запущен с использованием 5 потоков.
3) --duration 600 - этот аргумент указывает длительность вставки данных в секундах. В данном случае установлено значение 600 секунд, что означает, что вставка данных будет продолжаться в течение 10 минут.

- Установим Perf

Для установки инструмента Perf в Ubuntu 22.04 вы можете выполнить следующие шаги:
1) Установите пакет linux-tools
```bash
sudo apt update &&
sudo apt install linux-tools
```
2) Убедитесь, что у вас установлены заголовки вашего ядра. Вы можете установить соответствующий пакет для вашего текущего ядра
```bash
sudo apt install linux-headers-$(uname -r)
```
3) После установки заголовков перезагрузите вашу систему
```bash
sudo reboot
```
4) После перезагрузки проверьте, доступен ли Perf
```bash
perf --version
```
- Узнаем  pid postgresa
```bash
ps -ef | grep postgres
```
- Запускаем perf после заускае скрипт описанный выше
```bash
sudo perf record -g -p пид postgresa
```
эта команда записывает данные профилирования в файл perf.data в текущем каталоге, включая информацию о стеке вызовов (-g).  

- Создание Flame Graph
1) осле сбора данных профилирования с помощью Perf, используйте утилиту FlameGraph для создания графического представления стека вызовов в виде Flame Graph. Для этого выполните следующие команды
```bash
git clone https://github.com/brendangregg/FlameGraph.git &&
cd FlameGraph &&
sudo perf script | ./stackcollapse-perf.pl | ./flamegraph.pl > perf2.svg
```
- Но в моем случае я не мог запустить  perf, у меня выдавал ошибку
  WARNING: perf not found for kernel 5.15.0-69

  You may need to install the following packages for this specific kernel:
    linux-tools-5.15.0-69-generic
    linux-cloud-tools-5.15.0-69-generic

  You may also want to install one of the following packages to keep up to date:
    linux-tools-generic
    linux-cloud-tools-generic

  1) Пробывал установить общие пакеты для инструмента Perf
  ```bash
  sudo apt-get install linux-tools-generic linux-cloud-tools-generic
  ```
  без результатно  
2) Рещил найти исполняемый файл perf напрямую в системе
```bash
sudo find / -name perf
```
/usr/lib/linux-tools-5.15.0-107/perf --version
perf version 5.15.149

3) Запуск Flame Graph у меня отличался, пришлось указывать файл perf.data в домашней директории через -i
```bash
/usr/lib/linux-tools-5.15.0-107/perf script -i /home/rizik/perf.data | ./stackcollapse-perf.pl | ./flamegraph.pl > perf2.svg
```
- Итог: очень мало времени было на задание , perf2.svg скачать и запустить в браузере 
