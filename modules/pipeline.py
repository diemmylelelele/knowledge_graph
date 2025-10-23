from modules.file_utils import get_input_text
from modules.graph_extraction import init_graph_transformer, extract_graph_data
from modules.personality_enrichment import enrich_with_personality
from modules.visualization import visualize_graph
from langchain_ollama import ChatOllama


async def generate_knowledge_graph(input_path_or_text: str):
    """Complete pipeline: text → graph → enrichment → visualization"""
    # Load input
    print("Reading input...")
    text = get_input_text(input_path_or_text)

    # Initialize LLM and transformer (inside the running loop)
    print("Initializing LLM (Ollama)...")
    llm = ChatOllama(model="llama3.2:latest", temperature=0)
    graph_transformer = init_graph_transformer(llm)

    # Extract knowledge graph
    print("Extracting base knowledge graph...")
    graph_docs = await extract_graph_data(text, graph_transformer)

    # Enrich with personality / characteristics
    print("Enriching graph nodes with inferred traits...")
    enriched_docs = await enrich_with_personality(graph_docs, text, llm)

    # Visualize
    print("Visualizing final graph...")
    visualize_graph(enriched_docs)
