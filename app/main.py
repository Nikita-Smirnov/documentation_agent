import asyncio
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.agents import generate_and_validate_documentation
from app.health import check_all_services
from app.logger import logger
from app.rag import (
    add_document_to_index,
    initialize_rag_from_docs,
    search_documentation,
)
from app.schemas import GenerateRequest, GenerateResponse, SearchRequest, SearchResponse
from app.storage import save_document


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Инициализация RAG из docs/")

    # Выполняем загрузку эмбедингов в отдельном потоке
    loop = asyncio.get_event_loop()

    with ThreadPoolExecutor() as pool:
        await loop.run_in_executor(pool, initialize_rag_from_docs)

    logger.info("Сервис готов к работе")

    yield


app = FastAPI(title="AI Docs Assistant", lifespan=lifespan)


@app.get("/health")
async def health_check():
    return await check_all_services()


@app.post("/search", response_model=SearchResponse)
def search_docs(req: SearchRequest):
    result = search_documentation(req.query)

    if not result:
        return SearchResponse(
            found=False,
            message="Документация не найдена. Используйте /generate для создания новой.",
        )

    return SearchResponse(found=True, content=result)


@app.post("/generate", response_model=GenerateResponse)
def generate_docs(req: GenerateRequest):
    if search_documentation(req.query, similarity_threshold=0.75):
        return GenerateResponse(
            success=False, message="Документ уже существует. Используйте /search."
        )

    try:
        content = generate_and_validate_documentation(req.query)
        if not content.strip().startswith("###"):
            logger.error(
                f"Сгенерированный документ не соответствует формату для запроса: {req.query}"
            )
            return GenerateResponse(
                success=False, message="Ошибка генерации: неверный формат документа."
            )

        file_path = save_document(content, req.query)

        add_document_to_index(file_path)

        return GenerateResponse(
            success=True,
            message="Документ успешно создан и сохранён.",
            content=content,
            file_path=file_path,
        )

    except Exception as e:
        logger.error(f"Ошибка генерации документа: {e}", exc_info=True)
        return GenerateResponse(success=False, message=f"Ошибка генерации: {e!s}")
