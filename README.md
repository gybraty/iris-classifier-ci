# Iris Classifier — исследовательский проект с CI/CD

Учебный проект к Заданию 5: небольшой сервис машинного обучения с
автоматическим тестированием, контейнеризацией и непрерывной доставкой.

Модель — случайный лес, обученный на наборе Iris, встроенном в scikit-learn.
Сервис на FastAPI возвращает предсказанный вид и вероятности по классам.

## Быстрый старт

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest -v
uvicorn app.main:app --reload
```

API: `POST /predict`, `GET /health`, `GET /model/info`. Интерактивная
документация — `http://localhost:8000/docs`.

```bash
curl -X POST http://localhost:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'
```

## Docker

```bash
docker build -t iris-classifier:local .
docker run --rm -p 8000:8000 iris-classifier:local
```

Опубликованный образ: `docker pull gybraty/iris-classifier:latest`.

## CI/CD (GitHub Actions)

`.github/workflows/ci.yml` содержит три задания:

1. `test` — устанавливает зафиксированные зависимости и запускает pytest на
   каждом push и pull request.
2. `build-and-push` — собирает образ, проверяет `/health` внутри контейнера,
   затем публикует образ в Docker Hub, если настроены секреты.
3. `deploy` — опциональное ручное развёртывание на Minikube с self-hosted
   раннера.

Включить публикацию: добавить секреты репозитория `DOCKERHUB_USERNAME` и
`DOCKERHUB_TOKEN`. Включить развёртывание: создать self-hosted раннер с меткой
`minikube` и задать переменную репозитория `ENABLE_CD=true`.

## Kubernetes (Minikube)

```bash
minikube start
kubectl apply -f k8s/
minikube image load iris-classifier:local
kubectl -n iris rollout status deployment/iris-classifier
kubectl -n iris get pods,svc
minikube service iris-classifier -n iris --url
```

## Структура проекта

```
app/                    классификатор и приложение FastAPI
tests/                  модульные и API-тесты (11)
Dockerfile              образ контейнера
.github/workflows/      конвейер CI/CD
k8s/                    namespace, Deployment, Service
diagrams/               исходники draw.io и экспорт PNG
report/                 теоретический и практический отчёты
```

## Отчёты

- [Теоретический отчёт](report/theoretical-report.md) · [DOCX](report/theoretical-report.docx) · [PDF](report/theoretical-report.pdf)
- [Практический отчёт](report/practical-report.md) · [DOCX](report/practical-report.docx) · [PDF](report/practical-report.pdf)

## Замечания о воспроизводимости

Версии зависимостей зафиксированы в `requirements.txt` и
`requirements-dev.txt`, разбиение train/test использует `random_state=42`, а
модель обучается на наборе, встроенном в scikit-learn, поэтому сеть при запуске
не нужна. Образ помечается хешем коммита.
