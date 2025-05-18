import json
import os

class LegalAnalyzer:
    def __init__(self):
        self.labor_laws = self._load_json('labor_laws.json')
        self.case_studies = self._load_json('case_studies.json')

    def _load_json(self, filename):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'data', filename)
        with open(file_path, 'r') as f:
            return json.load(f)

    def analyze(self, query):
        relevant_laws = self._find_relevant_laws(query)
        relevant_cases = self._find_relevant_cases(query)
        
        analysis = f"Relevant Laws:\n{relevant_laws}\n\nRelevant Case Studies:\n{relevant_cases}"
        return analysis

    def _find_relevant_laws(self, query):
        # Simple keyword matching (can be improved with NLP techniques)
        relevant_laws = []
        for law in self.labor_laws['labor_laws']:
            if any(keyword in query.lower() for keyword in law['name'].lower().split()):
                relevant_laws.append(f"{law['name']}: {law['description']}")
        return "\n".join(relevant_laws) if relevant_laws else "No directly relevant laws found."

    def _find_relevant_cases(self, query):
        # Simple keyword matching (can be improved with NLP techniques)
        relevant_cases = []
        for case in self.case_studies['case_studies']:
            if any(keyword in query.lower() for keyword in case['title'].lower().split()):
                relevant_cases.append(f"{case['title']}: {case['summary']}")
        return "\n".join(relevant_cases) if relevant_cases else "No directly relevant case studies found."