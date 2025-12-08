def format_shinobi_info(info: dict) -> str:
    if not info: return ""
    lines = [f"Nama: {info.get('name') or '?'}"]
    if info.get("status"): lines.append(f"Status: {info.get('status')}")
    if info.get("rank"): lines.append(f"Rank: {info.get('rank')}")
    if info.get("villages"): lines.append(f"Asal: {', '.join(info['villages'])}")
    if info.get("elements"): lines.append(f"Elemen: {', '.join(info['elements'])}")
    return "\n".join(lines)

def format_clan_info(info: dict) -> str:
    if not info: return ""
    lines = [f"Klan: {info.get('clan')}"]
    if info.get("members"): lines.append(f"Anggota: {', '.join(info['members'])}")
    return "\n".join(lines)

def format_jutsu_info(info: dict) -> str:
    if not info: return ""
    lines = [f"Jutsu: {info.get('jutsu')}"]
    if info.get("users"): lines.append(f"Pengguna: {', '.join(info['users'])}")
    return "\n".join(lines)

def format_org_info(info: dict) -> str:
    if not info: return ""
    lines = [f"Organisasi: {info.get('org')}"]
    if info.get("members"): lines.append(f"Anggota: {', '.join(info['members'])}")
    return "\n".join(lines)

def format_teacher_student(info: dict) -> str:
    if not info: return ""
    lines = [f"Info Relasi: {info.get('name')}"]
    if info.get("teachers"): lines.append(f"Guru: {', '.join(info['teachers'])}")
    if info.get("students"): lines.append(f"Murid: {', '.join(info['students'])}")
    return "\n".join(lines)

def format_list(title, items):
    if not items: return ""
    return f"{title}: {', '.join(items)}"