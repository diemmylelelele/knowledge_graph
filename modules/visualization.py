from pyvis.network import Network
import os

def visualize_graph(graph_documents, output_filename="knowledge_graph_with_personality.html"):
    """Visualize the enriched knowledge graph using PyVis."""
    net = Network(
        height="900px",
        width="100%",
        directed=True,
        bgcolor="#222222",
        font_color="white",
        notebook=False,
        filter_menu=True,
        cdn_resources="remote"
    )

    nodes = graph_documents[0].nodes
    relationships = graph_documents[0].relationships

    # Add nodes
    for node in nodes:
        node_type = getattr(node, "type", "Entity")
        traits = []
        # Prefer characteristics stored under properties
        props = getattr(node, "properties", {}) or {}
        if isinstance(props, dict):
            traits = props.get("characteristics") or []
        # Backward compatibility if attribute exists
        if not traits:
            traits = getattr(node, "characteristics", [])
        tooltip = f"Type: {node_type}"
        if traits:
            tooltip += "<br>Traits: " + ", ".join(traits)

        net.add_node(
            node.id,
            label=node.id,
            title=tooltip,
            group=node_type,
            shape="dot",
            size=20 + len(traits) * 2
        )

    # Add relationships
    for rel in relationships:
        try:
            # Some implementations represent endpoints as objects, others as strings/ids
            src = getattr(rel, "source", None)
            tgt = getattr(rel, "target", None)
            src_id = getattr(src, "id", src)
            tgt_id = getattr(tgt, "id", tgt)
            label = getattr(rel, "type", getattr(rel, "label", ""))
            if src_id is None or tgt_id is None:
                continue
            net.add_edge(str(src_id), str(tgt_id), label=label)
        except Exception:
            continue

    # Physics layout
    net.set_options("""
        {
          "physics": {
            "forceAtlas2Based": {
              "gravitationalConstant": -100,
              "centralGravity": 0.01,
              "springLength": 200,
              "springConstant": 0.08
            },
            "minVelocity": 0.75,
            "solver": "forceAtlas2Based"
          }
        }
    """)

    net.save_graph(output_filename)
    print(f"Knowledge graph saved to: {os.path.abspath(output_filename)}")
    return net
