from sqlalchemy import create_engine, Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base
import os

# Pfad zur Datenbankdatei auf dem Netzwerklaufwerk
db_path = r'M:\MLC-Work\pit\hardware_inventory.db'
# db_path = 'hardware_inventory.db'

# Erstelle eine Instanz von declarative_base()
Base = declarative_base()

engine = create_engine(f'sqlite:///{db_path}', echo=True)


class Classroom(Base):
    __tablename__ = 'classrooms'

    id = Column(Integer, primary_key=True)
    room_number = Column(String(10), unique=True, nullable=False)


class HardwareDevice(Base):
    __tablename__ = 'hardware_devices'

    id = Column(Integer, primary_key=True)
    project = Column(Enum('KITLos 1', 'KITLos 2', 'DokMBw'), nullable=False)
    device_type = Column(Enum('Drucker', 'Laptop', 'Beamer', 'LTE-Router',
                              'Mängel', 'Schrott'), nullable=False)
    Bezeichnung = Column(Enum('HP ProBook 450 G9', 'Brother HL-L2375DW',
                              'Epson EB-L520U', 'HP Z-Book Fury 16',
                              'ACER Aspire 5', 'Acer P1287', 'Samsung M2026',
                              'Netgear NightHawk M1', 'TP-Link AC750'), nullable=False)
    Name = Column(String(100), nullable=False)
    serial_number = Column(String(50), unique=True, nullable=False)
    assigned_to_classroom_id = Column(Integer, ForeignKey('classrooms.id'))
    assigned_to_classroom = relationship('Classroom', back_populates='devices')
    status = Column(String(150))


Classroom.devices = relationship('HardwareDevice', back_populates='assigned_to_classroom')

Session = sessionmaker(bind=engine)

# Überprüfe, ob die Datenbankdatei vorhanden ist. Wenn nicht, erstelle sie
if not os.path.exists(db_path):
    Base.metadata.create_all(engine)
