import os
import re
import ssl
import requests
import xml.etree.ElementTree as ET
from requests.adapters import HTTPAdapter
from requests_ntlm import HttpNtlmAuth
from urllib3.poolmanager import PoolManager
from converter import extract_block
from config import USERNAME, PASSWORT

class LegacySSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.options |= 0x00000004
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        kwargs["ssl_context"] = ctx
        self.poolmanager = PoolManager(*args, **kwargs)

def download_rss_and_save_xml(server_num):
    server_prefix = f"{int(server_num):02}"
    base_url = f"https://{server_prefix}.ml-schulung.de"
    overview_url = f"{base_url}/trainerseite/Lists/Lehrgangsbewertung/overview.aspx"

    session = requests.Session()
    session.mount("https://", LegacySSLAdapter())
    session.auth = HttpNtlmAuth(USERNAME, PASSWORT)
    session.verify = False
    session.headers.update({"User-Agent": "DokMBW/NTLM"})

    try:
        # Lade Seite
        res = session.get(overview_url, timeout=10)
        res.raise_for_status()

        # Debug-HTML speichern (optional)
        with open(f"{server_prefix}_overview_debug.html", "w", encoding="utf-8") as f:
            f.write(res.text)

        # Alle GUIDs im HTML suchen
        guids = re.findall(r'\{[0-9a-fA-F\-]{36}\}', res.text)
        guids = list(set(guids))
        if not guids:
            raise Exception("Keine GUIDs im HTML gefunden.")

        # Alle GUIDs durchprobieren
        for guid in guids:
            feed_url = f"{base_url}/trainerseite/_layouts/15/listfeed.aspx?List={guid}"
            try:
                feed_res = session.get(feed_url, timeout=10)
                feed_res.raise_for_status()

                xml_filename = f"{server_prefix}_feed.xml"
                with open(xml_filename, "w", encoding="utf-8") as f:
                    f.write(feed_res.text)

                root = ET.fromstring(feed_res.text)
                trainer = extract_block(
                    root.find("channel").find("item").find("description").text,
                    "Name des Trainers"
                )

                return {
                    "server": server_prefix,
                    "trainer": trainer,
                    "xml_file": xml_filename
                }

            except Exception:
                continue

        raise Exception("Keine funktionierende Feed-URL mit gültiger GUID gefunden.")

    except Exception as e:
        raise Exception(f"[{server_prefix}] Fehler: {e}")

