from logger import logger
from pathlib import Path

def query_chain(chain, user_input: str):
    try:
        logger.debug(f"Running chain for input: {user_input}")
        result = chain({"query": user_input})  # returns dict with 'result' and 'source_documents'

        # Extract sources from metadata
        sources = []
        if "source_documents" in result:
            for doc in result["source_documents"]:
                sources.append(doc.metadata.get("source", ""))
        sources = [Path(s).name for s in set(sources)]
        response = {
            "response": result.get("result", ""),
            "sources": sources
        }

        logger.debug(f"Chain response: {response}")
        return response

    except Exception as e:
        logger.exception("Error on query chain")
        raise
