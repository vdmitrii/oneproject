import schedule
import time
import subprocess


def job():
    try:
        # Запускаем команду
        result = subprocess.run(['poetry', 'run', 'dvc', 'repro'], check=True, text=True, capture_output=True)

        # Выводим результат
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
    except subprocess.CalledProcessError as e:
        # Обрабатываем ошибку, если команда завершилась с ненулевым кодом
        print(f"Ошибка: {e}")
        print(f"Код ошибки: {e.returncode}")
        print(f"STDERR: {e.stderr}")

# schedule.every().day.at("00:00").do(job)
# schedule.every().day.at("12:42", "Europe/Moscow").do(job)


while True:
    schedule.run_pending()
    time.sleep(1)
    