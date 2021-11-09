# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import psycopg2
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
    if 'fakultas' in fakultas:
        return fakultas.replace("fakultas ","").capitalize()
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
        return fakultas.capitalize()

def getProgram(program: Text):
    program = program.upper()
    if program in ['S1', 'S2', 'S3', 'D3', 'SP', 'SP1', 'SP2']:
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
    else:
        return program.capitalize()

def getRektor(rektor: Text):
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

def getGambar(gambar:Text):
    GAMBAR = {
        'Lambang Universitas Sriwijaya' : 'Lambang Universitas Sriwijaya',
        'Bendera Universitas Sriwijaya' : 'Bendera Universitas Sriwijaya',
        'Bendera Fakultas Ekonomi': 'Bendera Fakultas Ekonomi',
        'Bendera Fakultas Hukum': 'Bendera Fakultas Hukum',
        'Bendera Fakultas Kedokteran': 'Bendera Fakultas Kedokteran',
        'Bendera Fakultas Teknik': 'Bendera Fakultas Teknik',
        'Bendera Fakultas Pertanian': 'Bendera Fakultas Pertanian',
        'Bendera Fakultas Keguruan dan Ilmu Pendidikan': 'Bendera Fakultas Keguruan dan Ilmu Pendidikan',
        'Bendera Fakultas MIPA': 'Bendera Fakultas MIPA',
        'Bendera Fakultas Ilmu Sosial dan Ilmu Politik': 'Bendera Fakultas Ilmu Sosial dan Ilmu Politik',
        'Bendera Fakultas Ilmu Komputer': 'Bendera Fakultas Ilmu Komputer',
        'Bendera Fakultas Kesehatan Masyarakat': 'Bendera Fakultas Kesehatan Masyarakat',
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
            {"payload":'/ide_dibentuk', "title":"Sejarah"},
            {"payload":'/i_unsur_lambang_universitas_sriwijaya', "title":"Unsur Lambang"},
            {"payload":'/makna_lambang', "title":"Makna Lambang"},
            {"payload":'/fasilitas_pendidikan_kampus_indralaya', "title":"Zona"},
	        {"payload":'/daftar_rektor', "title":"Rektor"},
            {"payload":'/daftar_fakultas', "title":"Fakultas"},
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
            
            query = f"SELECT link FROM gambar WHERE nama_gambar = '{gambar}'"

            print(query)

            queryResult = querySQL(query)

            # dispatcher.utter_message(text=str(queryResult))
            # dispatcher.utter_message(
            #     image="---")
            dispatcher.utter_message(image=queryResult[0][0])

            return []