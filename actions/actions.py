# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import re
import sqlite3
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

def querySQL(query: Text):

    conn = sqlite3.connect('db/chatbot.db')

    cur = conn.execute(query)
    result = cur.fetchall()

    cur.close()
    conn.close()
    
    return result



def getFakultas(fakultas: Text):
    fakultas = fakultas.lower()
    fakultas = fakultas.lstrip('fakultas').lstrip()

    if fakultas in ['hukum', 'kedokteran', 'teknik', 'pertanian', 'ekonomi']:
        return fakultas.capitalize()
    elif fakultas[0] == 'f':
        FAKULTAS = {
        'fh': 'Hukum',
        'fk': 'Kedokteran',
        'ft': 'Teknik',
        'fp': 'Pertanian',
        'fe': 'Ekonomi'
        }
        return FAKULTAS.get(fakultas, None)
    else:
        pass


def getProgram(program: str):
    if program.upper() in ['S1', 'S2', 'S3', 'D3', 'SP', 'SP1', 'SP2']:
        PROGRAM = {
            'S1': 'Sarjana',
            'S2': 'Magister',
            'S3': 'Doktor',
            'D3': 'Diploma Tiga',
            'SP': 'Spesialis 1',
            'SP1': 'Spesialis 1',
            'SP2': 'Spesialis 2 (Subspesialis)'
        }
        return PROGRAM.get(program, None)
    elif program.lower() in ['sarjana', 'magister', 'doktor', 'diploma tiga', 'spesialis 1', 'spesialis 2 (subspesialis)']:
        return program.capitalize()
    else:
        pass

def getRektor(rektor: str):
    rektor = rektor.lower()
    cek = "".join(re.split('\D', rektor))
    if cek:
        return int(re.sub('\D*', '', rektor))
    else:
        REKTOR = {
            'pertama': 1,
            'kedua': 2,
            'ketiga': 3,
            'keempat': 4,
            'kelima': 5,
            'keenam': 6,
            'ketujuh': 7,
            'kedelapan': 8,
            'kesembilan': 9,
            'kesepuluh': 10
        }
    return REKTOR.get(rektor, None)

def getGambar(gambar: str):
    gambar = gambar.lower()
    GAMBAR = {
        'lambang universitas sriwijaya' : 'Lambang Universitas Sriwijaya',
        'bendera universitas sriwijaya' : 'Bendera Universitas Sriwijaya',
        'bendera fakultas ekonomi': 'Bendera Fakultas Ekonomi',
        'bendera fakultas hukum': 'Bendera Fakultas Hukum',
        'bendera fakultas kedokteran': 'Bendera Fakultas Kedokteran',
        'bendera fakultas teknik': 'Bendera Fakultas Teknik',
        'bendera fakultas pertanian': 'Bendera Fakultas Pertanian',
        'bendera fakultas keguruan dan ilmu pendidikan': 'Bendera Fakultas Keguruan dan Ilmu Pendidikan',
        'bendera fakultas mipa': 'Bendera Fakultas MIPA',
        'bendera fakultas ilmu sosial dan ilmu politik': 'Bendera Fakultas Ilmu Sosial dan Ilmu Politik',
        'bendera fakultas ilmu komputer': 'Bendera Fakultas Ilmu Komputer',
        'bendera fakultas kesehatan masyarakat': 'Bendera Fakultas Kesehatan Masyarakat',
        'lambang unsri' : 'Lambang Universitas Sriwijaya',
        'bendera unsri' : 'Bendera Universitas Sriwijaya',
        'bendera fe': 'Bendera Fakultas Ekonomi',
        'bendera fh': 'Bendera Fakultas Hukum',
        'bendera fk': 'Bendera Fakultas Kedokteran',
        'bendara ft': 'Bendera Fakultas Teknik',
        'bendera fp': 'Bendera Fakultas Pertanian',
        'bendera fkip': 'Bendera Fakultas Keguruan dan Ilmu Pendidikan',
        'bendera fmipa': 'Bendera Fakultas MIPA',
        'bendera fisip': 'Bendera Fakultas Ilmu Sosial dan Ilmu Politik',
        'bendera fasilkom': 'Bendera Fakultas Ilmu Komputer',
        'bendera fkm': 'Bendera Fakultas Kesehatan Masyarakat',
    }
    return GAMBAR.get(gambar, None)


class ActionDaftarIsi(Action):
    def name(self) -> Text:
        return "action_daftar"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        buttons=[
            {"payload":'ide pertama', "title":"Sejarah"},
            {"payload":'unsur lambang universitas sriwijaya', "title":"Unsur Lambang"},
            {"payload":'makna lambang', "title":"Makna Lambang"},
            {"payload":'fasilitas pendidikan kampus indralaya', "title":"Zona"},
	        {"payload":'daftar rektor', "title":"Rektor"},
            {"payload":'daftar fakultas', "title":"Fakultas"},
        ]

        dispatcher.utter_message(text="Daftar isi dari chatbot", buttons=buttons)

        return []

class ActionProgram(Action):
    def name(self) -> Text:
        return "action_program"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        fakultas = next(tracker.get_latest_entity_values("fakultas"), None)

        fakultas = getFakultas(fakultas)

        if(fakultas is None):
            dispatcher.utter_message("Nama fakultas tidak valid")
            return []

        query = f"SELECT program FROM program_pendidikan WHERE fakultas LIKE '{fakultas}' GROUP BY program"

        print(query)

        queryResult = querySQL(query)

        result = f'Jurusan dari Fakultas {fakultas} terdiri dari: '
        for f in queryResult:
            result += f'\n {f[0]}'

        dispatcher.utter_message(text=str(result))

        return []


class ActionJurusan(Action):
    def name(self) -> Text:
        return "action_jurusan"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        fakultas = next(tracker.get_latest_entity_values("fakultas"), None)
        program = next(tracker.get_latest_entity_values("program"), None)

        if program is None:
            program = "sarjana"

        fakultas = getFakultas(fakultas)
        program = getProgram(program)

        if(fakultas is None or program is None):
            dispatcher.utter_message("Nama fakultas / program tidak valid")
            return []

        query = f"SELECT program_studi FROM program_pendidikan WHERE fakultas LIKE '{fakultas}' AND program LIKE '{program}'"

        print(query)

        queryResult = querySQL(query)

        result = f"Jurusan dari Fakultas {fakultas} Program {program} terdiri dari: "
        for j in queryResult:
            result += f'\n {j[0]}'

        dispatcher.utter_message(text=str(result))
        return []


class ActionGelar(Action):
    def name(self) -> Text:
        return "action_gelar"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        jurusan = next(tracker.get_latest_entity_values("jurusan"), None)
        program = next(tracker.get_latest_entity_values("program"), None)

        if program is None:
            program = "sarjana"

        jurusan = ' '.join(part.capitalize() for part in jurusan.split())
        program = getProgram(program)

        if(program is None):
            dispatcher.utter_message("Nama program tidak valid")
            return []

        query = f"SELECT gelar, singkatan FROM program_pendidikan WHERE program_studi LIKE '{jurusan}' AND program LIKE '{program}'"

        gelar, singkatan = querySQL(query)[0]
        result = f'{gelar} ({singkatan})'

        dispatcher.utter_message(text=str(result))

        return []

class ActionFakultas(Action):
    def name(self) -> Text:
        return "action_fakultas"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        fakultas = next(tracker.get_latest_entity_values("fakultas"), None)

        fakultas = getFakultas(fakultas)

        if(fakultas is None):
            dispatcher.utter_message("Nama fakultas tidak valid")
            return []

        query = f"SELECT program_studi, program FROM program_pendidikan WHERE fakultas = '{fakultas}'";

        queryResult = querySQL(query)

        result = f"Jurusan dari Fakultas {fakultas} teridiri dari: "
        for jurusan, program in queryResult:
            result += f"\n {jurusan} ({program})"

        dispatcher.utter_message(text=str(result))

        return []

class ActionRektor(Action):

    def name(self) -> Text:
        return "action_rektor"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        rektor = next(tracker.get_latest_entity_values("rektor"), None)

        rektor = getRektor(rektor)

        if rektor is None:
            dispatcher.utter_message("Nomor rektor tidak valid")
            return []

        query = f"SELECT nama_rektor FROM rektor WHERE id = '{rektor}'"

        print(query)

        queryResult = querySQL(query)

        result = f"Rektor ke-{rektor} Universitas Sriwijaya adalah {queryResult[0][0]}"

        dispatcher.utter_message(text=result)

        return []

    class ActionDaftarRektor(Action):
        def name(self) -> Text:
            return "action_daftar_rektor"

        async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
        ) -> List[Dict[Text, Any]]:

            buttons=[
                {"payload":'siapa rektor pertama unsri ?', "title":"Drg. M. Isa"},
                {"payload":'siapa rektor kedua unsri ?', "title":"Kol. Pol. Amir Datuk Palindih, S.H."},
                {"payload":'siapa rektor ketiga unsri', "title":"Kol. CDM. dr. Noesmir"},
                {"payload":'siapa rektor keempat unsri', "title":"Prof. H. Djuaini Mukti, M.A."},
                {"payload":'siapa rektor kelima unsri', "title":"Drs. Sjafran Sjamsuddin"},
                {"payload":'siapa rektor keenam unsri', "title":"Prof. Dr. Amran Halim, M.A."},
                {"payload":'siapa rektor ketujuh unsri', "title":"Prof. Ir. H.Machmud Hasjim, MME"},
                {"payload":'siapa rektor kedelapan unsri', "title":"Prof.Dr.Ir. H. Zainal Ridho Djafar"},
                {"payload":'siapa rektor kesembilan unsri', "title":"Prof.Dr.Badia Perizade, M.B.A"},
                {"payload":'siapa rektor kesepuluh unsri', "title":"Prof. Dr. Ir. H. Anis Saggaff, MSCE"}
            ]

            dispatcher.utter_message(text="Rektor Universitas Sriwijaya", buttons=buttons)

            return []
    
    class ActionDaftarFakultas(Action):
        def name(self) -> Text:
            return "action_daftar_fakultas"

        async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
        ) -> List[Dict[Text, Any]]:
            buttons = [
                {"payload" : "jurusan dan program di fakultas ekonomi", "title" : "Fakultas Ekonomi"},
                {"payload" : "jurusan dan program di fakultas hukum", "title" : "Fakultas Hukum"},
                {"payload" : "jurusan dan program di fakultas teknik", "title" : "Fakultas Teknik"},
                {"payload" : "jurusan dan program di fakultas kedokteran" , "title" : "Fakultas Kedokteran"},
                {"payload" : "jurusan dan program di fakultas pertanian" , "title" : "Fakultas Pertanian"}
            ]
            dispatcher.utter_message(text="Fakultas yang ada di UNSRI", buttons=buttons)

            return []

    class ActionGambar(Action):
        def name(self) -> Text:
            return "action_gambar"

        async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
        ) -> List[Dict[Text, Any]]:
            gambar = next(tracker.get_latest_entity_values("gambar"), None)
            gambar = getGambar(gambar)

            if gambar is None:
                dispatcher.utter_message("Gambar tidak ditemukan")
                return []
            
            query = f"SELECT link FROM gambar WHERE nama_gambar = '{gambar}'"

            print(query)

            queryResult = querySQL(query)

            # dispatcher.utter_message(text=str(queryResult))
            # dispatcher.utter_message(
            #     image="---")
            dispatcher.utter_message(image=queryResult[0][0])

            return []