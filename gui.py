import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from rss_downloader import download_rss_and_save_xml
from converter import convert_xml_to_excel
from mailer import sende_auswertung_per_mail
from urllib3.exceptions import InsecureRequestWarning
import urllib3
urllib3.disable_warnings(InsecureRequestWarning)

def run_gui_process(server_list):
    erfolge = []
    fehler = []

    for server in server_list:
        try:
            result = download_rss_and_save_xml(server)
            datum = datetime.now().strftime("%d%m%Y")
            excel_file = f"{datum}_{result['server']}_{result['trainer']}.xlsx"
            convert_xml_to_excel(result["xml_file"], excel_file)
            erfolge.append(excel_file)
        except Exception as e:
            fehler.append(str(e))

    if erfolge:
        sende_auswertung_per_mail(erfolge)
        messagebox.showinfo("Erfolg", f"{len(erfolge)} Dateien erfolgreich versendet.")
    else:
        messagebox.showerror("Fehler", "\n".join(fehler))

def start_gui():
    root = tk.Tk()
    root.title("DokMBW Serverauswahl")
    vars = []

    tk.Label(root, text="Wähle die Server aus:").pack(pady=(10, 0))

    for i in range(1, 11):
        var = tk.IntVar()
        tk.Checkbutton(root, text=f"{i:02}", variable=var).pack(anchor="w")
        vars.append((i, var))

    def starten():
        selected = [i for i, var in vars if var.get()]
        if not selected:
            messagebox.showwarning("Hinweis", "Bitte mindestens einen Server auswählen.")
            return
        run_gui_process(selected)

    tk.Button(root, text="Auswertung starten", command=starten).pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    start_gui()
