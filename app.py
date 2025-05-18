import logging
import traceback
import os
import streamlit as st
from src.chatbot import Chatbot
from src.legal_analyzer import LegalAnalyzer
from src.language_processor import LanguageProcessor
from src.voice_interface import VoiceInterface
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(filename='main.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def generate_process():
    process = """
    1. User selects their preferred language
    2. User chooses input method (text or voice)
    3. User provides their question about employment rights
    4. System processes the input:
       a. Translates input to English if necessary
       b. Analyzes the legal context of the question
       c. Generates a response based on the analysis
    5. System translates the response back to the user's language if necessary
    6. System presents the response to the user (text or voice)
    """
    return process

def main():
    st.title("Employment Rights and Legal Advice Chatbot")
    
    # Check for API key
    if not os.environ.get("GROQ_API_KEY"):
        st.error("GROQ_API_KEY is not set in the environment variables. Please set it and restart the application.")
        return

    try:
        # Initialize components
        chatbot = Chatbot()
        legal_analyzer = LegalAnalyzer()
        language_processor = LanguageProcessor()
        voice_interface = VoiceInterface()

        # Language selection
        languages = [
            "English", "हिन्दी (Hindi)", "தமிழ் (Tamil)", "తెలుగు (Telugu)",
            "ಕನ್ನಡ (Kannada)", "বাংলা (Bengali)", "മലയാളം (Malayalam)",
            "ਪੰਜਾਬੀ (Punjabi)", "ગુજરાતી (Gujarati)", "ଓଡ଼ിಆ (Odia)"
        ]
        language = st.selectbox("Select Language", languages)
        language_processor.set_language(language)

        # Input method selection
        input_method = st.radio("Choose input method", ["Text", "Voice"])

        if input_method == "Text":
            user_input = st.text_input("Enter your question about employment rights:")
        else:
            try:
                user_input = voice_interface.listen()
            except Exception as e:
                logging.error(f"Error in voice input: {str(e)}")
                st.error("Error in voice input. Please try text input instead.")
                user_input = st.text_input("Enter your question about employment rights:")

        if user_input:
            try:
                logging.info(f"Processing user input: {user_input}")
                
                # Process user input
                processed_input = language_processor.process(user_input)
                if processed_input is None:
                    raise ValueError("Failed to process user input")
                
                # Translate to English for analysis if necessary
                if language != "English":
                    english_input = language_processor.translate_to_english(user_input)
                    if english_input == user_input:
                        logging.warning("Translation to English failed, using original input")
                else:
                    english_input = user_input
                
                logging.info(f"Analyzing input: {english_input}")
                legal_analysis = legal_analyzer.analyze(english_input)
                if not legal_analysis:
                    raise ValueError("Legal analysis failed")
                
                logging.info("Generating response")
                english_response = chatbot.generate_response(legal_analysis)
                if not english_response:
                    raise ValueError("Failed to generate response")
                
                # Translate response back to user's language if necessary
                if language != "English":
                    response = language_processor.translate_from_english(english_response, language)
                    if response == english_response:
                        logging.warning("Translation from English failed, using English response")
                else:
                    response = english_response

                # Display response
                st.write("Chatbot:", response)

                if input_method == "Voice":
                    try:
                        voice_interface.speak(response)
                    except Exception as e:
                        logging.error(f"Error in voice output: {str(e)}")
                        st.error("Error in voice output. Please read the text response.")

            except Exception as e:
                logging.error(f"Error in processing user input: {str(e)}")
                logging.error(traceback.format_exc())
                st.error(f"An error occurred while processing your request: {str(e)}. Please try again or contact support.")
                print(f"Detailed error: {traceback.format_exc()}")  # Added for more verbose console output

        # Display the process
        if st.button("Show Process"):
            st.text(generate_process())

    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
        logging.error(traceback.format_exc())
        st.error(f"A critical error occurred: {str(e)}. Please check the logs for more details and ensure all required files and dependencies are in place.")
        print(f"Critical error: {traceback.format_exc()}")  # Added for more verbose console output

if __name__ == "__main__":
    main()