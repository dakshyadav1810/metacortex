# chatbot/citations.py

def collect_citations(path):
    seen = set()
    citations = []

    for node in path.nodes:
        if node.url not in seen:
            citations.append(node.url)
            seen.add(node.url)

    return citations
