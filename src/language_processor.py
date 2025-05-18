from openai import OpenAI
import os
import logging

class LanguageProcessor:
    def __init__(self):
        self.language = "en"
        self.client = OpenAI(
            api_key=os.environ.get("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )
        self.model = "Llama-3.1-70b-Versatile"
        logging.basicConfig(filename='language_processor.log', level=logging.INFO)

    def set_language(self, language):
        language_code = {
            "English": "en", "हिन्दी (Hindi)": "hi", "தமிழ் (Tamil)": "ta",
            "తెలుగు (Telugu)": "te", "ಕನ್ನಡ (Kannada)": "kn", "বাংলা (Bengali)": "bn",
            "മലയാളം (Malayalam)": "ml", "ਪੰਜਾਬੀ (Punjabi)": "pa",
            "ગુજરાતી (Gujarati)": "gu", "ଓଡ଼ିଆ (Odia)": "or"
        }
        self.language = language_code.get(language, "en")

    def process(self, text):
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logging.error(f"Error in process: {str(e)}")
            return None

    def translate_to_english(self, text):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are a translator. Translate the following text from {self.language} to English:"},
                    {"role": "user", "content": text}
                ],
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error in translate_to_english: {str(e)}")
            return text  # Return original text if translation fails

    def translate_from_english(self, text, target_language):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are a translator. Translate the following text from English to {target_language}:"},
                    {"role": "user", "content": text}
                ],
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error in translate_from_english: {str(e)}")
            return text  # Return original text if translation fails

    def get_language(self):
        return self.language