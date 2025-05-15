# SONAR Translator - Complete Version

import warnings
# Filter torchaudio backend warning from skops
warnings.filterwarnings('ignore', category=UserWarning, module='skops.io._utils')
warnings.filterwarnings('ignore', message='.*Torchaudio\'s I/O functions.*')

from sonar.inference_pipelines.text import TextToEmbeddingModelPipeline
from sonar.inference_pipelines.text import EmbeddingToTextModelPipeline
from wtpsplit import SaT
import torch
import re
import os
import argparse

class SONARJapaneseToEnglishTranslator:
    def __init__(self, LangSource, LangTarget, Verbose, Sequential):
        # Initialize SONAR for Japanese sentence processing
        self.SONAR_Vec2Text = EmbeddingToTextModelPipeline(
            decoder="text_sonar_basic_decoder",
            tokenizer="text_sonar_basic_encoder",
            device=torch.device("cuda"),
            dtype=torch.float16,)
        self.SONAR_Text2Vec = TextToEmbeddingModelPipeline(
            encoder="text_sonar_basic_encoder",
            tokenizer="text_sonar_basic_encoder",
            device=torch.device("cuda"),
            dtype=torch.float16,)
        # Initialize SaT with GPU support if available
        self.Segmenter = SaT("sat-3l-sm")
        if torch.cuda.is_available():
            self.Segmenter.to("cuda")
        self.Args = {
            "lang_source": LangSource,
            "lang_target": LangTarget,
            "verbose": Verbose,
            "sequential": Sequential
        }

    def CleanText(self, text):
        # Remove line numbers, URLs, and extra spaces
        text = re.sub(r"^\d+\s+", "", text)
        text = re.sub(r"<https?://[^\s]+>", "", text)
        text = text.replace("\n", " ").strip()
        return text

    def SplitSentences(self, text):
        # Use SaT for sentence segmentation
        return self.Segmenter.split(text)
    
    def Translator(self, sentences):
        # Assume sentences is always a list of sentences, even though it might have a length of 1

        if self.Args["verbose"]:
            print(f"Embedding Sentences: {sentences}")

        embeddings = self.SONAR_Text2Vec.predict(sentences, source_lang=self.Args["lang_source"]) 
        if self.Args["verbose"]:
            print(f"embeddings.shape: {embeddings.shape}")


        reconstructed = self.SONAR_Vec2Text.predict(embeddings, target_lang=self.Args["lang_target"], max_seq_len=512)
        # max_seq_len is a keyword argument passed to the fairseq2 BeamSearchSeq2SeqGenerator.

        if self.Args["verbose"]:
            print(f"Disembedded Sentences: {reconstructed}")

        return reconstructed

    def TranslateSentence(self, sentence):
        # Translate a single sentence
        return self.Translator([sentence])[0]

    def TranslateBatch(self, sentences):
        # Translate a batch of sentences
        return self.Translator(sentences)
    
    def TranslateText(self, input_file, output_file):
        # Load and clean Japanese text
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()
        cleaned_text = self.CleanText(text)
        Sentences = self.SplitSentences(cleaned_text)
        print(f"Loaded {len(Sentences)} sentences from {input_file}.")

        # Translate each sentence
        if self.Args["sequential"]: # Sequential Translation
            TranslatedSentences = []
            for Sentence in Sentences:
                TranslatedSentence = self.TranslateSentence(Sentence)
                TranslatedSentences.append(TranslatedSentence)
                print(f"Translated: {Sentence} → {TranslatedSentence}")
        else: # Batch Translation
            TranslatedSentences = self.TranslateBatch(Sentences)
            for i, Sentence in enumerate(Sentences):
                print(f"Translated: {Sentences[i]} → {TranslatedSentences[i]}")

        # Save translated text
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(TranslatedSentences))
        print(f"Translation complete! English text saved to {output_file}")

# Example usage
if __name__ == "__main__":
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Get the command line arguments
    parser = argparse.ArgumentParser(description='Translate text using SONAR.')
    parser.add_argument('-i', '--input_file', type=str, required=True, help='Input file to translate.')
    parser.add_argument('-s', '--lang_source', type=str, required=True, help='Language to translate from (FLORES-200) (e.g., jpn_Jpan, eng_Latn).')
    parser.add_argument('-t', '--lang_target', type=str, required=True, help='Language to translate to (FLORES-200) (e.g., deu_Latn, zho_Hans).')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output.')
    parser.add_argument('-q', '--sequential', action='store_true', help='Process sentences sequentially.')
    args = parser.parse_args()

    if args.verbose:
        print("Verbose mode enabled.")
        print(f"Language Source: {args.lang_source}")
        print(f"Language Target: {args.lang_target}")
        print(f"Sequential: {args.sequential}")

    translator = SONARJapaneseToEnglishTranslator(LangSource=args.lang_source, LangTarget=args.lang_target, Verbose=args.verbose, Sequential=args.sequential)
    translator.TranslateText(
        os.path.join(script_dir, "2_InputData", args.input_file),
        os.path.join(script_dir, "3_OutputData", f"{args.input_file}_{args.lang_source}_{args.lang_target}.txt")
    )

    print(f"Language Source: {args.lang_source}, Language Target: {args.lang_target}, Verbose: {args.verbose}, Sequential: {args.sequential}")
