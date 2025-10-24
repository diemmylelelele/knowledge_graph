import asyncio
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
# from file_utils import get_input_text

def init_graph_transformer(llm):
    """Initialize the LLMGraphTransformer with the selected LLM."""
    # custom_prompt = ChatPromptTemplate.from_messages(
        
    # )
    return LLMGraphTransformer(
        llm=llm
        # prompt=custom_prompt
    )

async def extract_graph_data(text: str, graph_transformer):
    """
    Asynchronously extracts graph data from input text using LLMGraphTransformer.
    """
    documents = [Document(page_content=text)]
    graph_docs = await graph_transformer.aconvert_to_graph_documents(documents)
    return graph_docs
