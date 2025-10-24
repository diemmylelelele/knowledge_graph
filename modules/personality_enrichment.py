import json
async def enrich_with_personality(graph_docs, context_text: str, llm):
    """
    For each node in the graph, infer descriptive characteristics or personality traits.
    Adds a 'characteristics' field to each node.
    """
    nodes = graph_docs[0].nodes
    for node in nodes:
        name = node.id
        entity_type = getattr(node, "type", "Entity")

        prompt = f"""
        You are analyzing a knowledge graph extracted from text.
        Identify the key characteristics or descriptive traits that best describe the {entity_type.lower()} "{name}".
        Return a JSON list of 1-3 concise descriptive traits [e.g., "curious", "empathetic", "analytical"].
        Context:
        {context_text}
        
        *** Note: if the context does not provide any relevant information that can help describe the entity's personality, return an empty list.
        
        """

        try:
            response = await llm.ainvoke(prompt)  
            traits_json = response.content.strip() # Extract the content from the response object

            try:
                traits = json.loads(traits_json)  # Parse JSON response
            except Exception:
                traits = [t.strip(' "') for t in traits_json.strip("[]").split(",") if t.strip()]

            props = getattr(node, "properties", None)
            if props is None:
                try:
                    node.properties = {"characteristics": traits}
                except Exception:
                    # Fallback: cannot set new attributes; skip but warn
                    print(f"[WARN] Cannot set properties on node '{name}', skipping traits attachment.")
            else:
                node.properties["characteristics"] = traits
        except Exception as e:
            print(f"[WARN] Personality extraction failed for {name}: {e}")
            # still set empty characteristics if possible
            props = getattr(node, "properties", None)
            if props is None:
                try:
                    node.properties = {"characteristics": []}
                except Exception:
                    pass
            else:
                node.properties["characteristics"] = []

    return graph_docs
