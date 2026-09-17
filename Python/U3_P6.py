from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel 
import os, json, logging

load_dotenv()
try:
    CLIENT = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
except Exception as e:
    print("\nERROR: API Connection Failed.")

MODEL = "gemini-3.5-flash-lite"
REPORT_FILE = "reportP6.jsonl"

LOG_FILE = "P6.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE)
    ],
    force=True
)

class ResFormat(BaseModel):
    title: str
    summary: str
    keywords: list
    word_count: int

def api_call(content):
    interaction = CLIENT.interactions.create(
        model = MODEL,
        system_instruction = "You are a content summarizer. You have to summarize the given content strictly in 2-3 lines and return a report of the content strictly in the given JSON format. First the 'title' - Title/Topic of the content, 'summary' - 2-3 lines summary of the content, 'keywords' - list/array of keywords/important words mentioned in the content and then last 'word_count' - total number of words in the original content.",
        input = content,
        response_format = {
            "type": "text",
            "mime_type": "application/json",
            "schema": ResFormat.model_json_schema()
        }
    )

    return interaction.output_text

def mech(i, f, l):
    try:
        f=f.strip()
        print(f"\nProceesing file {i+1} out of {l} files..")
        if f.rsplit(".",2)[-1] == "txt":
            if os.path.exists(f) & os.path.isfile(f):
                with open(f, "r", encoding="utf-8") as file:
                    file_content = file.read().strip()

                if file_content == "":
                    logging.log(level=20, msg=f"{f} is empty.")
                    raise Exception(f"{f} is empty.")
                else:
                    report = json.loads(api_call(file_content))   #API Call

                    if not isinstance(report, dict):
                        logging.log(level=20, msg=f"Invalid JSON response for {f}.")
                        raise Exception(f"Invalid JSON response for {f}.")
                    else:
                        if not (list(report.keys()) == ['title', 'summary', 'keywords', 'word_count']):
                            logging.log(level=20, msg=f"Invalid JSON response structure for {f}.")
                            raise Exception(f"Invalid JSON response structure for {f}.")
                        else:
                            with open(REPORT_FILE, "a", encoding="utf-8") as file:
                                json.dump(report, file, indent=4)
                            print("\nResponse saved in the reportP6.jsonl file.")

                            logging.log(level=20, msg=f"Respnse Status: SUCCESS for {f}.")
            
            else:
                logging.log(level=20, msg=f"{f} does not exist in the given directory.")
                raise Exception(f"{f} does not exist in the given directory.")
            
        else:
            logging.log(level=20, msg=f"{f}: Invalid file type. Only .txt file allowed")
            raise Exception("Invalid file type. Only .txt file allowed")
    except Exception as e:
        print("\nERROR:",e)

def main():
    try:
        FILE = input("\nEnter the txt file name: ").strip().split()

        if len(FILE) <= 0:
            raise Exception("No file provided. Please enter a file name.")

        else:
            for i, f in enumerate(FILE):
                mech(i, f, len(FILE))
            
    except Exception as e:
        print("\nERROR:",e)

if __name__ == "__main__":
    main()