from database.connection import get_driver

driver = get_driver()

def _parse_node_name(node):
    if not node: return None
    if node.get("name"): return node.get("name")
    uri = node.get("uri")
    if uri and "#" in uri: return uri.split("#")[-1]
    return "Unknown"

def test_connection():
    with driver.session() as session:
        result = session.run("MATCH (n) RETURN count(n) AS cnt")
        print(f"✅ Database Connected! Total Nodes: {result.single()['cnt']}")

def get_shinobi_info(name: str):
    cypher = """
    MATCH (s:ns0__Shinobi)
    WHERE toLower(s.uri) CONTAINS toLower($name) OR toLower(s.name) CONTAINS toLower($name)
    OPTIONAL MATCH (s)-[:ns0__isFrom]->(v)
    OPTIONAL MATCH (s)-[:ns0__hasElement]->(e)
    RETURN s, s.ns0__status as status, collect(DISTINCT v) as villages, collect(DISTINCT e) as elements, labels(s) as all_labels
    LIMIT 1
    """
    with driver.session() as session:
        rec = session.run(cypher, name=name).single()
        if not rec: return None
        ignored_labels = {'ns0__Shinobi', 'Resource', 'ns0__AkatsukiMember', 'ns0__Jinchuuriki', 'ns0__UchihaClanMember'}
        ranks = [l.replace("ns0__", "") for l in rec["all_labels"] if l not in ignored_labels]
        return {
            "name": _parse_node_name(rec["s"]),
            "status": rec["status"],
            "rank": ranks[0] if ranks else "Unknown",
            "villages": [_parse_node_name(v) for v in rec["villages"]],
            "elements": [_parse_node_name(e) for e in rec["elements"]]
        }

def get_eye_users(eye_name: str):
    cypher = """
    MATCH (s:ns0__Shinobi)
    WHERE 
        EXISTS { (s)-[:ns0__hasEye]->(e) WHERE toLower(coalesce(e.uri, e.name, "")) CONTAINS toLower($eye) }
        OR EXISTS {
            (s)-[:rdf__type|ns0__type]->(r)-[:owl__someValuesFrom]->(c)
            WHERE toLower(coalesce(c.uri, c.name, "")) CONTAINS toLower($eye)
        }
        OR EXISTS {
            (s)-[:rdf__type|ns0__type]->(r)-[:owl__allValuesFrom]->(c)
            WHERE toLower(coalesce(c.uri, c.name, "")) CONTAINS toLower($eye)
        }
    RETURN $eye as eye_name, collect(DISTINCT s) as users
    """
    with driver.session() as session:
        try:
            rec = session.run(cypher, eye=eye_name).single()
            if not rec or not rec["users"]: return None
            return {"eye": eye_name, "users": [_parse_node_name(u) for u in rec["users"]]}
        except Exception as e:
            print(f"[Repo Error] Eye Query: {e}")
            return None

def get_element_users(elem_name: str):
    cypher = """
    MATCH (e:ns0__Elemental)<-[:ns0__hasElement]-(s)
    WHERE toLower(e.uri) CONTAINS toLower($elem)
    RETURN e, collect(s) as users
    """
    with driver.session() as session:
        rec = session.run(cypher, elem=elem_name).single()
        if not rec: return None
        return {"element": _parse_node_name(rec["e"]), "users": [_parse_node_name(u) for u in rec["users"]]}

def get_jutsu_users(jutsu_name: str):
    cypher = """
    MATCH (j)<-[:ns0__masterJutsu]-(s)
    WHERE toLower(j.uri) CONTAINS toLower($jutsu) 
    RETURN j, collect(s) as users
    """
    with driver.session() as session:
        rec = session.run(cypher, jutsu=jutsu_name).single()
        if not rec: return None
        return {"jutsu": _parse_node_name(rec["j"]), "users": [_parse_node_name(u) for u in rec["users"]]}

def get_clan_members(clan_name: str):
    cypher = """
    MATCH (c:ns0__Clan)
    WHERE toLower(c.uri) CONTAINS toLower($clan)
    OPTIONAL MATCH (s)-[:ns0__isClanMemberOf]->(c)
    RETURN c, collect(s) as members
    """
    with driver.session() as session:
        rec = session.run(cypher, clan=clan_name).single()
        if not rec: return None
        return {"clan": _parse_node_name(rec["c"]), "members": [_parse_node_name(m) for m in rec["members"]]}

def get_org_members(org_name: str):
    cypher = """
    MATCH (o:ns0__Organizations)
    WHERE toLower(o.uri) CONTAINS toLower($org)
    OPTIONAL MATCH (s)-[:ns0__isOrgMemberOf]->(o)
    RETURN o, collect(s) as members
    """
    with driver.session() as session:
        rec = session.run(cypher, org=org_name).single()
        if not rec: return None
        return {"org": _parse_node_name(rec["o"]), "members": [_parse_node_name(m) for m in rec["members"]]}

def get_teacher_student(name: str):
    cypher = """
    MATCH (s:ns0__Shinobi)
    WHERE toLower(s.uri) CONTAINS toLower($name)
    OPTIONAL MATCH (s)-[:ns0__hasTeacher]->(t)
    OPTIONAL MATCH (s)-[:ns0__hasStudent]->(st)
    RETURN s, collect(DISTINCT t) as teachers, collect(DISTINCT st) as students
    """
    with driver.session() as session:
        rec = session.run(cypher, name=name).single()
        if not rec: return None
        return {
            "name": _parse_node_name(rec["s"]),
            "teachers": [_parse_node_name(t) for t in rec["teachers"]],
            "students": [_parse_node_name(st) for st in rec["students"]]
        }

def get_bijuu_info(name: str):
    cypher = """
    MATCH (j:ns0__Shinobi)-[:ns0__isJinchuurikiOf]->(b:ns0__Bijuu)
    WHERE toLower(j.uri) CONTAINS toLower($name) OR toLower(b.uri) CONTAINS toLower($name)
    RETURN j, b, b.ns0__tailNumber as tails
    """
    with driver.session() as session:
        rec = session.run(cypher, name=name).single()
        if not rec: return None
        return {"jinchuuriki": _parse_node_name(rec["j"]), "bijuu": _parse_node_name(rec["b"]), "tails": rec["tails"]}