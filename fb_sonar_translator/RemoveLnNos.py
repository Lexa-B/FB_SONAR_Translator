import re
import os

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
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    cleaner = RemoveLnNos()
    cleaner.clean_text_file(
        os.path.join(script_dir, "Examples", "松山鏡ーThe_Mirror_of_Matsuyamaー日本語.txt"),
        os.path.join(script_dir, "InputData", "松山鏡ーThe_Mirror_of_Matsuyamaー日本語_Clean.txt")
    )

    cleaner.clean_text_file(
        os.path.join(script_dir, "Examples", "松山鏡ーThe_Mirror_of_Matsuyamaー英語.txt"),
        os.path.join(script_dir, "InputData", "松山鏡ーThe_Mirror_of_Matsuyamaー英語_Clean.txt")
    )

    print("Cleaning complete! The cleaned files are ready.")
