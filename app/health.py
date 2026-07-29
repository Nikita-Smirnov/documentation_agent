import httpx

from app.logger import logger
from app.rag import search_documentation
from app.settings import settings


async def check_qdrant() -> bool:
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(f"{settings.qdrant_url}/collections")
            return resp.status_code == 200
    except Exception as e:
        logger.error(f"Qdrant недоступен: {e}")
        return False


async def check_ollama() -> bool:
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(f"{settings.ollama_url}/api/tags")
            return resp.status_code == 200
    except Exception as e:
        logger.error(f"Ollama недоступен: {e}")
        return False


def check_docs() -> bool:
    from pathlib import Path

    return len(list(Path("docs").glob("*.md"))) > 0


def run_rag_canary_check() -> bool:
    query = "Эндпоинт для получения профиля"
    result = search_documentation(query, similarity_threshold=0.6)
    if not result:
        return False
    return "GET /api/v1/profile" in result


async def check_all_services() -> dict:
    qdrant = await check_qdrant()
    ollama = await check_ollama()
    docs = check_docs()
    rag_canary = run_rag_canary_check()

    status = "healthy" if all([qdrant, ollama, docs, rag_canary]) else "unhealthy"

    return {
        "status": status,
        "checks": {
            "qdrant": qdrant,
            "ollama": ollama,
            "docs": docs,
            "rag_canary": rag_canary,
        },
    }
