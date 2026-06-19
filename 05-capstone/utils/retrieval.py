from pathlib import Path
import re

KB_PATH = Path(__file__).resolve().parent.parent / "knowledge_base" / "support_faq.txt"

STOPWORDS = {
    "the", "and", "for", "are", "with", "that", "this", "from", "your",
    "you", "was", "were", "have", "has", "had", "not", "but", "can",
    "how", "what", "when", "why", "who", "will", "into", "their", "them",
    "then", "than", "too", "out", "get", "got", "our", "his", "her",
    "its", "about", "there", "here", "after", "before", "again"
}


def load_knowledge_base() -> str:
    return KB_PATH.read_text(encoding="utf-8")


def tokenize(text: str):
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    return [word for word in words if word not in STOPWORDS]


def search_knowledge_base(query: str) -> str:
    kb_text = load_knowledge_base()
    query_words = set(tokenize(query))

    sections = kb_text.strip().split("\n\n")
    scored_sections = []

    for section in sections:
        section_words = set(tokenize(section))
        score = len(query_words & section_words)

        if score > 0:
            scored_sections.append((score, section))

    if not scored_sections:
        return "No relevant knowledge base match found."

    scored_sections.sort(key=lambda x: x[0], reverse=True)
    top_sections = [section for _, section in scored_sections[:3]]

    return "\n\n".join(top_sections)