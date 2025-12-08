from database import repository as repo
from rag import formatters as fmt

def normalize_entity(text: str) -> str:
    text = text.lower()
    mapping = {
        "naruto": "Naruto_Uzumaki", "sasuke": "Sasuke_Uchiha", "kakashi": "Kakashi_Hatake",
        "jiraiya": "Jiraiya", "sakura": "Sakura_Haruno", "itachi": "Itachi_Uchiha",
        "madara": "Madara_Uchiha", "obito": "Obito_Uchiha", "tobi": "Tobi",
        "nagato": "Nagato", "pain": "Nagato", "konan": "Konan", "kisame": "Kisame",
        "kakuzu": "Kakuzu", "hidan": "Hidan", "deidara": "Deidara", "sasori": "Sasori",
        "zetsu": "Zetsu", "orochimaru": "Orochimaru", "tsunade": "Tsunade", 
        "minato": "Minato_Namikaze", "hashirama": "Hashirama", "tobirama": "Tobirama",
        "hiruzen": "Hiruzen_Sarutobi", "gaara": "Gaara", "killer bee": "Killer_Bee",
        "bee": "Killer_Bee", "guy": "Might_Guy", "lee": "RockLee", "neji": "Neji_Hyuuga",
        "hinata": "Hinata_Hyuuga", "shikamaru": "Shikamaru", "choji": "Choji", "ino": "Ino",
        "tenten": "Tenten", "konohamaru": "Konohamaru_Sarutobi", "shisui": "Shisui_Uchiha",
        "zabuza": "Zabuza", "haku": "Haku", "yagura": "Yagura", "utakata": "Utakata",
        "han": "Han", "roshi": "Roshi", "yugito": "Yugito", "fuu": "Fuu",
        "chojuro": "Chojuro", "mangetsu": "Mangetsu_Hozuki", "fuguki": "Fuguki",
        "konoha": "Konohagakure", "suna": "Sunagakure", "kiri": "Kirigakure",
        "iwa": "Iwagakure", "kumo": "Kumogakure", "ame": "Amegakure",
        "akatsuki": "Akatsuki", "seven swordsmen": "Seven_Swordmans_of_The_Mist",
        "taka": "Taka", "uchiha": "Uchiha", "hyuuga": "Hyuuga", "senju": "Senju",
        "uzumaki": "Uzumaki", "nara": "Nara", "akimichi": "Akimichi", "hozuki": "Hozuki",
        "katon": "Katon", "suiton": "Suiton", "futon": "Futon", 
        "doton": "Doton", "raiton": "Raiton", "mokuton": "Mokuton",
        "rinnegan": "Rinnegan", "sharingan": "Sharingan", "byakugan": "Byakugan",
        "kurama": "Kurama", "kyuubi": "Kurama", "ekor 9": "Kurama",
        "gyuuki": "Gyuuki", "hachibi": "Gyuuki", "ekor 8": "Gyuuki",
        "shukaku": "Shukaku", "ekor 1": "Shukaku",
        "matatabi": "Matatabi", "isobu": "Isobu", "son goku": "Son_Goku",
        "kokuo": "Kokuo", "saiken": "Saiken", "choumei": "Choumei",
        "rasengan": "Rasengan", "chidori": "Chidori", "amaterasu": "Ametarasu", 
        "tsukuyomi": "Tsukoyomi", "izanagi": "Izanagi", "izanami": "Izanami",
        "kamui": "Kamui", "shinra tensei": "Shinra_Tensei", "kotoamatsukami": "Kotoamatsukami",
        "kage bunshin": "Kage_Bunshin_no_Jutsu", "hiraishin": "Hiraishin",
        "8 gates": "Eight_Gates", "drunken fist": "Drunken_Fist"
    }
    for key, value in mapping.items():
        if key in text: return value
    return None

def build_context(question: str) -> str:
    target = normalize_entity(question)
    q = question.lower()
    parts = []

    if not target:
        words = q.split()
        if words: target = words[-1]

    if target in ["Rinnegan", "Sharingan", "Byakugan"]:
        data = repo.get_eye_users(target)
        if data: parts.append(fmt.format_list(f"Pengguna {target}", data['users']))

    elif target in ["Katon", "Suiton", "Futon", "Doton", "Raiton", "Mokuton"]:
        data = repo.get_element_users(target)
        if data: parts.append(fmt.format_list(f"Pengguna Elemen {target}", data['users']))

    elif target in ["Uchiha", "Hyuuga", "Senju", "Uzumaki", "Nara", "Akimichi", "Hozuki"]:
        data = repo.get_clan_members(target)
        if data: parts.append(fmt.format_list(f"Anggota Klan {target}", data['members']))
    
    elif target in ["Akatsuki", "Seven_Swordmans_of_The_Mist", "Taka"]:
        data = repo.get_org_members(target)
        if data: parts.append(fmt.format_list(f"Anggota {target}", data['members']))

    else:
        s_info = repo.get_shinobi_info(target)
        if s_info and s_info['name'] != "Unknown":
            parts.append(fmt.format_shinobi_info(s_info))
            ts = repo.get_teacher_student(target)
            if ts and (ts['teachers'] or ts['students']):
                parts.append(fmt.format_teacher_student(ts))

        bij = repo.get_bijuu_info(target)
        if bij:
            parts.append(f"Info Bijuu: {bij['bijuu']} (Ekor {bij['tails']}) ada di dalam {bij['jinchuuriki']}")

        jutsu = repo.get_jutsu_users(target)
        if jutsu and jutsu['users']:
            parts.append(fmt.format_list(f"Pengguna Jutsu {target}", jutsu['users']))

    if not parts: return "Data tidak ditemukan di Knowledge Graph."
    return "\n\n".join(parts)