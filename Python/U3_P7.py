from google import  genai
from dotenv import load_dotenv
import os, argparse, logging

try:
    load_dotenv()

    logging.basicConfig(
        format= "%(asctime)s %(name)s [%(levelname)s] %(message)s",
        level= logging.DEBUG,
        handlers=[logging.FileHandler("U3_P7.log")],
        force= True
    )

    CLIENT = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    MODEL = "gemini-3.5-flash-lite"

    parser = argparse.ArgumentParser(description="Taking input and output file name.")

    parser.add_argument("--input", type= str, help=".txt Input File Name")
    parser.add_argument("--output", type= str, help=".txt Output File Name")

    logging.log(level=20, msg="Program started.")
    arguments = parser.parse_args()
    input_file = str(arguments.input).strip()
    output_file = str(arguments.output).strip()

    if input_file or input_file == "":
        logging.log(level=20, msg=f"Processing {input_file}.")
        if os.path.exists(input_file) and os.path.isfile(input_file):
            if input_file.rsplit(".",2)[-1] == "txt":

                if output_file or output_file == "":
                    if input_file.rsplit(".",2)[-1] == "txt":
                        pass
                    else:
                        raise Exception(f"{output_file} is not a valid '.txt'(text) file.")
                else:
                    raise Exception("Output file not provided.")

                with open(input_file, "r", encoding="utf-8") as file:
                    file_text = file.read()

                if file_text == "":
                    raise Exception(f"{input_file} is empty!")
                else:
                    logging.log(level=20, msg="Generating summary...")
                    interaction = CLIENT.interactions.create(
                        model= MODEL,
                        input= f"Generate a 5-6 lines short summary for the given text.\nTEXT:{file_text}",
                        store= False
                    )

                    if interaction.output_text:
                        logging.log(level=20, msg="Summary Generated...")

                        with open(output_file, "w", encoding="utf-8") as file:
                            logging.log(level=20, msg="Committing the generated summary into output file.")
                            file.write(str(interaction.output_text))
                            logging.log(level=20, msg="Saved the generated summary into output file.")

                    else:
                        raise Exception("Summary gneration failed.")
            else:
                raise Exception(f"{input_file} is not a valid '.txt'(text) file.")
        else:
            raise Exception(f"Provided file: {input_file} does not exists in the given directory.")
    else:
        raise Exception("Input file not provided.")

except Exception as e:
    print("ERROR:",e)
    logging.log(level=40, msg=e)

finally:
    logging.log(level=20, msg="Program ended.")
