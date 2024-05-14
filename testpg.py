import psycopg2
import time
import argparse
import concurrent.futures
from faker import Faker

# Функция для вставки данных в базу данных
def insert_data(thread_id, duration):
    conn = psycopg2.connect(database="mytest", user="postgres", password="P@$$w0rd21", host="87.242.117.219", port="5432")
    cur = conn.cursor()
    fake = Faker()
    start_time = time.time()
    while (time.time() - start_time) < duration:
        data = (fake.name(), fake.email(), fake.address())
        cur.execute("INSERT INTO test (name, email, address) VALUES (%s, %s, %s)", data)
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

