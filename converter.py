import pandas as pd
import xml.etree.ElementTree as ET
import re
from datetime import datetime

def get_value_from_rating(rating_str, label):
    match = re.search(fr"{re.escape(label)};#(\d+)#", rating_str)
    return int(match.group(1)) if match else None

def extract_block(description_raw, label):
    match = re.search(fr"<b>{label}:</b>(.*?)</div>", description_raw.replace("\n", ""))
    return re.sub(r"<.*?>", "", match.group(1).strip()) if match else ""

def convert_xml_to_excel(xml_file_path, output_excel_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    channel = root.find("channel")
    entries = []

    for item in channel.findall("item"):
        author = "***"
        pub_date = item.find("pubDate").text
        pub_date = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %Z").strftime("%d.%m.%Y")
        description_raw = item.find("description").text

        seminar = extract_block(description_raw, "Titel des Seminars")
        ort = extract_block(description_raw, "Ort der Schulung")
        beginn = extract_block(description_raw, "Schulungszeitraum (Beginn)")
        ende = extract_block(description_raw, "Schulungszeitraum (Ende)")
        trainer = extract_block(description_raw, "Name des Trainers")
        themen = extract_block(description_raw, "Folgende Themen haben mich besonders interessiert:")
        zu_kurz = extract_block(description_raw, "Diese Themen kamen meiner Meinung nach zu kurz/habe ich nicht verstanden:")
        bewertung = extract_block(description_raw, "Lehrgangsbewertung")
        zufriedenheit = extract_block(description_raw, "Zufriedenheit")
        vorschlaege = extract_block(description_raw, "Haben Sie noch Wünsche, Vorschläge, Anregungen?")

        entries.append({
            "Erstellt von": author,
            "Titel des Seminars": seminar,
            "Ort der Schulung": ort,
            "Schulungszeitraum (Beginn)": beginn,
            "Schulungszeitraum (Ende)": ende,
            "Name des Trainers": trainer,
            "Folgende Themen haben mich besonders interessiert:": themen,
            "Diese Themen kamen meiner Meinung nach zu kurz/habe ich nicht verstanden:": zu_kurz,
            "Haben Sie noch Wünsche, Vorschläge, Anregungen?": vorschlaege,
            "Zufriedenheit_Ich würde das Seminar weiterempfehlen": get_value_from_rating(zufriedenheit, "Ich würde das Seminar weiterempfehlen"),
            "Zufriedenheit_Zufriedenheit mit Seminar": get_value_from_rating(zufriedenheit, "Zufriedenheit mit Seminar"),
            "Zufriedenheit_Zufriedenheit mit Trainer/in": get_value_from_rating(zufriedenheit, "Zufriedenheit mit Trainer/in"),
            "Lehrgangsbewertung_Teilnehmerunterlagen": get_value_from_rating(bewertung, "Teilnehmerunterlagen"),
            "Lehrgangsbewertung_Praxisanteil des Seminars (erster Eindruck)": get_value_from_rating(bewertung, "Praxisanteil des Seminars (erster Eindruck)"),
            "Lehrgangsbewertung_Präsentation der Inhalte (Nachvollziehbarkeit)": get_value_from_rating(bewertung, "Präsentation der Inhalte (Nachvollziehbarkeit)"),
            "Lehrgangsbewertung_Durchführung durch Trainer/in (Methodisch)": get_value_from_rating(bewertung, "Durchführung durch Trainer/in (Methodisch)"),
            "Lehrgangsbewertung_Durchführung durch Trainer/in (Fachlich)": get_value_from_rating(bewertung, "Durchführung durch Trainer/in (Fachlich)"),
            "Lehrgangsbewertung_Struktur des Seminars (Roter Faden)": get_value_from_rating(bewertung, "Struktur des Seminars (Roter Faden)"),
            "Lehrgangsbewertung_Allgemeine Atmosphäre": get_value_from_rating(bewertung, "Allgemeine Atmosphäre"),
            "Elementtyp": "Element",
            "Pfad": ""
        })

    df = pd.DataFrame(entries)
    df.to_excel(output_excel_path, index=False)
