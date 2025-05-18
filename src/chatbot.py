from openai import OpenAI
import os
import logging

class Chatbot:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )
        self.model = "Llama-3.1-70b-Versatile"
        logging.basicConfig(filename='chatbot.log', level=logging.INFO)

    def generate_response(self, legal_analysis):
        prompt = f"""
        You are an AI assistant specializing in employment rights and labor laws.
        Based on the following legal analysis, provide a clear and concise response to the user's query:
        {legal_analysis}
        Remember to:
        1. Be informative but not overly technical
        2. Provide actionable advice when appropriate
        3. Encourage the user to seek professional legal counsel for complex issues
        Response:
        """
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
                max_tokens=500,
                temperature=0.7
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            logging.error(f"Error in generate_response: {str(e)}")
            return "I apologize, but I encountered an error while processing your request. Please try again later or contact support if the issue persists."
