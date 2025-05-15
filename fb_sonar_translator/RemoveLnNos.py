import re
import os
import argparse

class RemoveLnNos:
    def clean_text_file(self, input_file: str, output_file: str):
        with open(input_file, "r", encoding="utf-8") as infile:
            lines = infile.readlines()

        cleaned_lines = []
        for line in lines:
            # Remove line numbers (1, 2, 3, ...) at the start of each line
            clean_line = re.sub(r"^\d+\s+", "", line.strip())
            # Remove URLs (like <https://...>)
            clean_line = re.sub(r"<https?://[^\s]+>", "", clean_line)
            if clean_line:  # Skip empty lines
                cleaned_lines.append(clean_line)

        with open(output_file, "w", encoding="utf-8") as outfile:
            outfile.write("\n".join(cleaned_lines))

# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Remove line numbers from a text file.')
    parser.add_argument('-i', '--input_file', type=str, required=True, help='Input file to remove line numbers from.')
    args = parser.parse_args()

    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    cleaner = RemoveLnNos()
    cleaner.clean_text_file(
        os.path.join(script_dir, "1_RawExamples", args.input_file),
        os.path.join(script_dir, "2_InputData", f"{args.input_file}_Clean.txt")
    )

    print("Cleaning complete! The cleaned file is ready.")
