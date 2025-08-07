print("Loading config/api.py...")  # <-- Вот эту строку
from ninja import NinjaAPI
from transactions_app.api.routers import router as transactions_router
# Создаём объект API с уникальным пространством имён

# Добавляем уникальное пространство имён 'main_api'
api_1 = NinjaAPI(
    title='Budget API',
    version='1.0',
    docs_url='/docs/',
    urls_namespace='api_1', 
)

# Регистрируем роутеры
api_1.add_router('/transactions/', transactions_router)