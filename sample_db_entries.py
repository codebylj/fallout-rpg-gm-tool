"""Initiates database and loads sample data"""
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import *

sample = {
    "1": {
        "title": "ENTRY #201",
        "population": "512",
        "date": "12/03/2241",
        "body": "[OVERSEER M. CLARKE]: The Vault thrives, at least on the "
                "surface. Food production cycles remain steady, "
                "water purifiers hum faithfully, and the hydroponics team "
                "even reported a surplus of beans last week. But beneath the "
                "neat rows of inventory charts lies something less tidy. I "
                "hear whispers from maintenance crews about long shifts and "
                "faulty parts. The filtration system is older than most of "
                "our children, and while the engineers assure me it’s "
                "manageable, their eyes tell me otherwise. I must balance "
                "transparency with stability: reveal too much and morale "
                "collapses, hide too much and resentment festers. Tonight, "
                "I walked the main atrium. Laughter echoed from the "
                "schoolroom, and two teenagers tried to impress one another "
                "by racing along the balcony rail. For a brief moment, "
                "I saw the Vault as it should be: a place where the past’s "
                "mistakes do not reach us. I cling to that image, though my "
                "gut insists trouble brews in the machinery and, perhaps, "
                "in the people."
    },
    "2": {
        "title": "ENTRY #202",
        "population": "509",
        "date": "03/07/2241",
        "body": "[OVERSEER M. CLARKE]: Three lost in a single night. The "
                "filtration alarm screamed through the halls at 02:14, "
                "rousing half the Vault. A rupture in the secondary pipe "
                "filled Corridor C with foul, choking air. Two guards died "
                "trying to reach the valve, and one child succumbed before "
                "medics could evacuate her family. I delivered the news "
                "personally this morning—her father looked at me as though I "
                "had stolen the very air from his lungs. Repair crews worked "
                "tirelessly, and by dawn the system was patched, but the "
                "damage is more than mechanical. Trust erodes like corroded "
                "steel. Some citizens demand we ration water further, others "
                "whisper of opening the Vault door. The very word ‘outside’ "
                "spreads like a disease in conversation. I convened the "
                "Council this afternoon and urged calm. I reminded them that "
                "the wastes offer only death. Yet as I spoke, I wondered if I "
                "believed my own words. The Vault walls feel thinner every day."
    },
    "3": {
        "title": "ENTRY #203",
        "population": "507",
        "date": "21/10/2241",
        "body": "[OVERSEER M. CLARKE]: The vote concluded at midnight. For "
                "the first time since the Vault sealed, we faced the question "
                "openly: remain within, or send an expedition beyond the "
                "door. The result was narrow, painfully so—two votes shy of a "
                "tie. Preparations have begun. Volunteers, some too eager, "
                "already pack supplies in the atrium. I see both fear and "
                "hope in their faces. The Council insists I accompany the "
                "expedition, if only to witness the wasteland firsthand and "
                "judge its dangers with my own eyes. I hesitate. My duty is "
                "here, within these walls, but perhaps duty has shifted. The "
                "children I once watched play are grown now, restless and "
                "hungry for a world they have never seen. The Vault cannot be "
                "a tomb. I record this in case I do not return. If the "
                "outside is as hostile as we were taught, then let history "
                "know: we tried, not out of defiance, but out of necessity. "
                "The air grows thin, and so does time."
    }
}

engine = create_engine("sqlite:///resources/database/vault.db")
Base.metadata.create_all(engine)


def add_vault():
    with Session(engine) as session:
        vault = Vault(
            vault_number="84",
            status="active",
            security_level=4,
            door_status="open",
            overseer_password="h7q#"
        )
        session.add(vault)
        session.commit()
        print("Vault added")


def add_entry():
    with Session(engine) as session:
        data = sample
        number_of_entries = len(data)
        for n in map(str, range(1, number_of_entries + 1)):
            entry = LogEntry(
                title=data[n]["title"],
                date=data[n]["date"],
                population=data[n]["population"],
                text=data[n]["body"],
                vault_id=1
            )
            session.add(entry)
            session.commit()
            print(f"{data[n]["title"]} added")


try:
    add_vault()
    add_entry()
except Exception as e:
    print(e)
