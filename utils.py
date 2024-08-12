# import fitz
import re


def remove_unreadable_items(text):
  text = text.replace('\n', ' ')
  text = re.sub('\s+', ' ', text)
  text = re.sub(r'\b\d+\b', '', text)  # Remove standalone numbers
  text = re.sub(r'(\w)-\s*(\w)', r'\1\2', text)  # fix line broken words

  text = re.sub(r'\|', '', text)  # Remove '|'

  # Remove citations and references
  text = re.sub(r'\[\d+\]', '', text)

  # Remove any remaining non-alphanumeric characters
  text = re.sub(r'[^\w\s.,?!]', '', text)

  # Remove extra spaces
  text = re.sub(r'\s+', ' ', text).strip()

  # Remove citations like "(Macal, 2016, p. 145)"
  text = re.sub(r'\(\w+((, )\w+)*(, p\. \d+)?\)', '', text)

  # Remove citations like "(Pyka & Fagiolo, 2007)" and "North & Macal, 2007)"
  text = re.sub(r'\([\w\s&]+, \d+\)', '', text)

  # Remove citations like "(Macal, 2016, p. 146, referring to Bankes, 2002)"
  text = re.sub(r'\(\w+, \d+, p\. \d+, referring to \w+, \d+\)', '', text)

  # Remove citations like "(Axtell & Epstein, 1994; Gilbert & Terna, 2000)"
  text = re.sub(r'\([\w\s&]+, \d+;\s[\w\s&]+, \d+\)', '', text)

  # Remove citations like "(Hoog, 2019; Edali & Yücel, 2019; Lamperti, Roventini, & Sani, 2018)"
  text = re.sub(r'\([\w\s&,]+, \d+;\s[\w\s&,]+, \d+;\s[\w\s&,]+, \d+\)', '', text)

  # Remove author names and affiliations like "Bernd Ebersberger\nInnovation Management University of Hohenheim Stuttgart,"
  text = re.sub(r'\w+\s\w+\n[\w\s]+,', '', text)

  text.replace(". ", ".\n")
  return text

def pdf_to_text(file_path):
  doc = fitz.open(file_path)
  total_pages = min(10, doc.page_count)

  text_list = []

  for i in range(0, total_pages):
    text = doc.load_page(i).get_text("text")
    text = remove_unreadable_items(text)
    text_list.append(text)

  doc.close()
  return text_list
