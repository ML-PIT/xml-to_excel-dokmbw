from DBlib import Classroom, HardwareDevice, Session, engine
from tkinter import Toplevel, Label, Entry, Button, StringVar, ttk
from sqlalchemy.orm import joinedload


def add_hardware(device_type, Bezeichnung, Name, serial_number, classroom_number):
    session = Session()

    # Klassenraum anhand der Raumnummer abfragen oder erstellen
    classroom = session.query(Classroom).filter_by(room_number=classroom_number).first()
    if not classroom:
        classroom = Classroom(room_number=classroom_number)

    hardware = HardwareDevice(device_type=device_type, Bezeichnung=Bezeichnung, Name=Name, serial_number=serial_number,
                              assigned_to_classroom=classroom)
    session.add(hardware)
    session.commit()
    session.close()


def remove_hardware(serial_number):
    session = Session()
    hardware = session.query(HardwareDevice).filter_by(serial_number=serial_number).first()
    if hardware:
        session.delete(hardware)
        session.commit()
    session.close()


def edit_hardware(serial_number, device_type, bezeichnung, classroom_id, new_status):
    session = Session()
    hardware = session.query(HardwareDevice).filter_by(serial_number=serial_number).first()

    if hardware:
        hardware.device_type = device_type
        hardware.bezeichnung = bezeichnung

        # Abrufen des Klassenzimmerobjekts basierend auf der übergebenen ID
        classroom = session.query(Classroom).filter_by(id=classroom_id).first()
        if classroom:
            hardware.assigned_to_classroom = classroom
        else:
            # Behandlung, falls kein entsprechendes Klassenzimmer gefunden wird
            pass

        hardware.status = new_status
        session.commit()
    else:
        # Behandlung, falls keine Hardware mit dieser Seriennummer gefunden wird
        pass

    session.close()


def list_hardware():
    def search():
        search_term = search_var.get()

        session = Session()
        query = session.query(HardwareDevice).options(joinedload(HardwareDevice.assigned_to_classroom))
        query = query.filter(
            (HardwareDevice.device_type.contains(search_term)) |
            (HardwareDevice.Bezeichnung.contains(search_term)) |
            (HardwareDevice.serial_number.contains(search_term)) |
            (HardwareDevice.assigned_to_classroom.has(room_number=search_term))
        )

        devices = query.all()
        session.close()

        # Die vorhandenen Einträge im Treeview löschen
        for item in tree.get_children():
            tree.delete(item)

        # Neue Suchergebnisse hinzufügen
        for device in devices:
            classroom_number = device.assigned_to_classroom.room_number if device.assigned_to_classroom else 'N/A'
            tree.insert('', 'end', values=(device.device_type, device.Bezeichnung, device.serial_number, classroom_number))

    def search_and_clear(event=None):  # event-Parameter hinzugefügt für die Kompatibilität mit dem bind-Ereignis
        search()
        search_var.set("")

    search_window = Toplevel()
    search_window.title("Hardware suchen")
    search_window.geometry("720x480")

    Label(search_window, text="Suche:").grid(row=0, column=0)
    search_var = StringVar()
    search_entry = Entry(search_window, textvariable=search_var)
    search_entry.grid(row=0, column=1)
    search_entry.bind("<Return>", search_and_clear)

    Button(search_window, text="Suche", command=search_and_clear).grid(row=0, column=2)

    columns = ('device_type', 'Bezeichnung', 'serial_number', 'classroom_number')
    tree = ttk.Treeview(search_window, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col.title())
    tree.grid(row=1, column=0, columnspan=3, sticky='nsew')

    # Scrollbar für den Treeview
    scrollbar = ttk.Scrollbar(search_window, orient='vertical', command=tree.yview)
    scrollbar.grid(row=1, column=3, sticky='ns')
    tree.configure(yscrollcommand=scrollbar.set)

    # Fenster-Layout für dynamisches Skalieren anpassen
    search_window.grid_rowconfigure(1, weight=1)
    search_window.grid_columnconfigure(1, weight=1)

    return search_window
