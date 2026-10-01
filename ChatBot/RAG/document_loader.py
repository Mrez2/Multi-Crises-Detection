import os
import json

class DocumentLoader:
    def __init__(self, file_path="ChatBot/RAG/knowledge_base.json"):
        self.file_path = file_path

    def load_documents(self):
        """Load safety knowledge base documents from JSON file."""
        if not os.path.exists(self.file_path):
            print(f"[⚠️ DocumentLoader Warning]: File not found at {self.file_path}")
            return []
        
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"[⚠️ DocumentLoader Error]: Failed to load documents: {e}")
            return []