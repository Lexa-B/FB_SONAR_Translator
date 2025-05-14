# SONAR Japanese to English Translator - Complete Version

from sonar.inference_pipelines.text import TextToEmbeddingModelPipeline
from transformers import MarianMTModel, MarianTokenizer
import re
import os

class SONARJapaneseToEnglishTranslator:
    def __init__(self):
        # Initialize SONAR for Japanese sentence processing
        self.sonar = TextToEmbeddingModelPipeline(
            encoder='text_sonar_basic_encoder',
            tokenizer='text_sonar_basic_encoder'
        )
        # Initialize MarianMT for Japanese to English translation
        self.tokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ja-en")
        self.model = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-ja-en")

    def clean_text(self, text):
        # Remove line numbers, URLs, and extra spaces
        text = re.sub(r"^\d+\s+", "", text)
        text = re.sub(r"<https?://[^\s]+>", "", text)
        text = text.replace("\n", " ").strip()
        return text

    def split_sentences(self, text):
        # Split using Japanese and English sentence-ending punctuation
        sentences = re.split(r'(?<=[。！？\.\?\!])\s*', text)
        return [s.strip() for s in sentences if s.strip()]

    def translate_sentence(self, sentence):
        # Translate a single Japanese sentence to English using MarianMT
        inputs = self.tokenizer(sentence, return_tensors="pt", truncation=True)
        translated_tokens = self.model.generate(**inputs)
        translated_text = self.tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
        return translated_text

    def translate_text(self, input_file, output_file):
        # Load and clean Japanese text
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()
        cleaned_text = self.clean_text(text)
        sentences = self.split_sentences(cleaned_text)
        print(f"Loaded {len(sentences)} sentences from {input_file}.")

        # Translate each sentence
        translated_sentences = []
        for sentence in sentences:
            english_text = self.translate_sentence(sentence)
            translated_sentences.append(english_text)
            print(f"Translated: {sentence} → {english_text}")

        # Save translated text
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(translated_sentences))
        print(f"Translation complete! English text saved to {output_file}")

# Example usage
if __name__ == "__main__":
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    translator = SONARJapaneseToEnglishTranslator()
    translator.translate_text(
        os.path.join(script_dir, "InputData", "松山鏡ーThe_Mirror_of_Matsuyamaー日本語_Clean.txt"),
        os.path.join(script_dir, "OutputData", "松山鏡ーThe_Mirror_of_Matsuyamaー英語_Translated.txt")
    )
