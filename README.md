Прогнозирование
=======================
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/19--WMSzriGl00XM5FgEpx3QTaxfY0XI2)


Приложение может предсказывать на конкретную дату на 24 интервала просто выбирая дату в форме. Также можно подавать файл в csv формата с колонками date и time_interval. Если в файле больше столбцов, то это не проблема. На выходе получите файл с дополнительной колонкой `predictions`.
Если хотите поднять свою инфраструктуру с MlFlow, Minio(S3), [мониторингом моделей](https://www.evidentlyai.com/) и мониторингом приложений, то запустите `docker-compose.yml` из [этого](https://github.com/vdmitrii/mlinfra) репозитория.


Для запуска пайплайна необходимы следующие шаги:
1. Клонировать репозиторий командой `git clone`
2. Перейти в него и установить все зависимости командой `poetry install --no-interaction --no-ansi`
3. Положить свой файл по пути `data/raw/`. Для справки образец `data.csv`
4. Запустить из корневой директории на  выбор `make` или `poetry run dvc repro` (для этого варианта предварительно нужно выполнить команду `dvc init`)
5. Итоговый прогноз будет находиться в файле `data/predictions/preds.csv`
--- 
Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Простой способ запуска с `make`
    ├── README.md          <- Описание структуру проекта
    ├── data
    │   ├── processed      <- Данные, предобработанные для моделирования
    │   └── raw            <- Сюда класть сырые данные для предсказания
    │
    ├── models             <- Тренированные модели
    │
    ├── notebooks          <- Jupyter ноутбуку
    │
    │
    ├── requirements.txt   <- Файл с библиотеками для воспроизводимости
    │
    ├── src                <- Source code
    │   ├── __init__.py    <- Делает src Python модуелем
    │   │
    │   ├── data           <- Скрипты для загрузки датасета
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Скрипты для генерации признаков
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Скрипты для тренировки и предскания моделей
    │   │   │                
    │   │   ├── predict_model.py
    │   │   └── train_model.py

