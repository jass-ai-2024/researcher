SYSTEM_ROLE = ("You are a researcher who helps to clarify process of development by providing information"
               " and useful insights for each service")
SYSTEM_GUIDE = """
Some Rules:
- You always speak and think english. Any research is done in english
- If you get a service architecture as input, you should select only ml related information
- If you get a ML service information, you shoud generate list of tasks for a up-to-date research
- If you get a list of research tasks, you should send them to refining and processing
"""

test_prompt = """
Сервис предназначен для автоматического определения, к какому классу относится загруженное изображение — к котикам или собакам.
Он должен быть надежным, масштабируемым и обеспечивать низкую задержку обработки.
Компоненты архитектуры

- Пользовательский интерфейс (UI)
Веб-интерфейс или мобильное приложение для загрузки изображений и получения результатов классификации.

- Сервер приложений
Обрабатывает запросы от UI, передает изображения на сервис классификации и возвращает результаты пользователю.

- Сервис классификации
Основной компонент, выполняющий задачу классификации изображений с использованием предобученной нейронной сети.

- Хранилище данных
Хранит изображения, метаданные, результаты классификации и логи.

- Мониторинг и логирование
Система для отслеживания состояния сервиса, производительности модели и анализа логов.
"""