import logging
import os
import requests
from typing import List
from bs4 import BeautifulSoup
from fpdf import FPDF

def download_quora_answers(author_id: str) -> None:
    """Downloads all Quora answers"""
    try:
        url = f"https://www.quora.com/profile/{author_id}"
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        answers = soup.find_all("div", class_="q-box qu-pt--medium qu-borderBottom")

        if not answers:
            logging.warning("No answers found for the given author ID: {author_id}")
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for i, answer in enumerate(answers):
            logging.info(f"Downloading answer {i}")
            answer_text = answer.find("span", class_="q-box qu-mb--tiny").text.strip()
            pdf.cell(200, 10, f"Answer {i+1}:", ln=True)
            pdf.multi_cell(200, 10, answer_text)
            pdf.ln()

        filename = f"{author_id}_answers.pdf"
        logging.info("Downloading into PDF file")
        
        pdf.output(filename)
        logging.info(f"Downloaded answers into {filename}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred while downloading answers: {str(e)}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")


def main():
    logging.basicConfig(filename="output.log", level=logging.INFO)

    try:
        # author_id = input("Enter the Quora author ID: ")
        author_id = ""
        download_quora_answers(author_id)

    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()
