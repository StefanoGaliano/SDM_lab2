"""
SDM Lab 2 - Biomedical Knowledge Graph
Generates RDFS triples, exports to Turtle (.ttl), and loads into GraphDB.
"""

import sys
import time
import requests
from rdflib import Graph, Namespace, RDF, RDFS

GRAPHDB_URL  = "http://localhost:7200"
REPO_ID      = "biomedical"
TTL_FILE     = "biomedical_kg.ttl"

BIO = Namespace("http://www.example.org/biomedical#")

g = Graph()
g.bind("bio", BIO)

# ── Metamodel layer ──────────────────────────────────────────────────────────

# Drug subclasses
for cls in ("antiinflammatory", "antibiotic", "analgesic", "antiviral", "steroid"):
    g.add((BIO[cls], RDFS.subClassOf,  BIO.Drug))

# Disease subclasses
for cls in ("inflammatory", "infectious", "chronic", "neurological"):
    g.add((BIO[cls], RDFS.subClassOf,  BIO.Disease))

# Properties
g.add((BIO.affects, RDFS.domain,  BIO.Drug))
g.add((BIO.affects, RDFS.range,   BIO.Disease))

# SubProperties
for prop in ("treats", "relieves", "worsens"):
    g.add((BIO[prop], RDFS.subPropertyOf,   BIO.affects))

# ── Facts layer – drug instances (50 total) ──────────────────────────────────
DRUGS = {
    "antiinflammatory": [
        "Ibuprofen", "Aspirin", "Naproxen", "Celecoxib", "Diclofenac",
        "Indomethacin", "Meloxicam", "Piroxicam", "Ketoprofen", "Sulindac",
    ],
    "antibiotic": [
        "Amoxicillin", "Penicillin", "Ampicillin", "Ciprofloxacin", "Azithromycin",
        "Doxycycline", "Tetracycline", "Erythromycin", "Clarithromycin", "Metronidazole",
    ],
    "analgesic": [
        "Paracetamol", "Codeine", "Morphine", "Oxycodone", "Tramadol",
        "Fentanyl", "Hydrocodone", "Buprenorphine", "Dihydrocodeine", "Gabapentin",
    ],
    "antiviral": [
        "Acyclovir", "Oseltamivir", "Remdesivir", "Lopinavir", "Ritonavir",
        "Tenofovir", "Lamivudine", "Zidovudine", "Valacyclovir", "Ribavirin",
    ],
    "steroid": [
        "Prednisone", "Cortisone", "Methylprednisolone", "Hydrocortisone", "Dexamethasone",
        "Betamethasone", "Triamcinolone", "Fluticasone", "Budesonide", "Beclomethasone",
    ],
}

# ── Facts layer – disease instances (50 total) ───────────────────────────────
DISEASES = {
    "inflammatory": [
        "Arthritis", "RheumatoidArthritis", "Lupus", "Psoriasis", "Gout",
        "CrohnsDisease", "UlcerativeColitis", "Asthma", "Eczema", "Fibromyalgia",
        "Spondylitis", "Tendinitis", "Vasculitis",
    ],
    "infectious": [
        "Pneumonia", "Tuberculosis", "Malaria", "HIV", "Influenza",
        "COVID19", "Cholera", "Typhoid", "Dengue", "Hepatitis",
        "LymeDisease", "Salmonellosis", "Shigellosis",
    ],
    "chronic": [
        "Diabetes", "Hypertension", "HeartDisease", "ChronicKidneyDisease", "COPD",
        "Osteoporosis", "MultipleSclerosis", "AlzheimerDisease", "Epilepsy", "Anemia",
        "Hemophilia", "Thalassemia",
    ],
    "neurological": [
        "Migraine", "Neuropathy", "Meningitis", "Encephalitis", "Stroke",
        "ALS", "Sciatica", "ParkinsonsDisease", "Narcolepsy", "Vertigo",
        "Dystonia", "TouretteSyndrome",
    ],
}

for cls, members in DRUGS.items():
    for name in members:
        g.add((BIO[name], RDF.type, BIO[cls]))

for cls, members in DISEASES.items():
    for name in members:
        g.add((BIO[name], RDF.type, BIO[cls]))

# ── Relationship triples ─────────────────────────────────────────────────────
TREATS = [
    ("Amoxicillin",       "Pneumonia"),
    ("Amoxicillin",       "Cholera"),
    ("Ampicillin",        "Pneumonia"),
    ("Ciprofloxacin",     "Typhoid"),
    ("Ciprofloxacin",     "Shigellosis"),
    ("Azithromycin",      "Pneumonia"),
    ("Azithromycin",      "Salmonellosis"),
    ("Doxycycline",       "Malaria"),
    ("Doxycycline",       "LymeDisease"),
    ("Tetracycline",      "Cholera"),
    ("Metronidazole",     "CrohnsDisease"),
    ("Metronidazole",     "UlcerativeColitis"),
    ("Erythromycin",      "Pneumonia"),
    ("Clarithromycin",    "Tuberculosis"),
    ("Oseltamivir",       "Influenza"),
    ("Remdesivir",        "COVID19"),
    ("Lopinavir",         "HIV"),
    ("Ritonavir",         "HIV"),
    ("Tenofovir",         "HIV"),
    ("Lamivudine",        "Hepatitis"),
    ("Zidovudine",        "HIV"),
    ("Ribavirin",         "Hepatitis"),
    ("Acyclovir",         "Meningitis"),
    ("Valacyclovir",      "Encephalitis"),
    ("Prednisone",        "Lupus"),
    ("Prednisone",        "Vasculitis"),
    ("Dexamethasone",     "Meningitis"),
    ("Methylprednisolone","MultipleSclerosis"),
    ("Penicillin",        "Pneumonia"),
]

RELIEVES = [
    ("Ibuprofen",         "Arthritis"),
    ("Ibuprofen",         "Migraine"),
    ("Ibuprofen",         "Fibromyalgia"),
    ("Aspirin",           "HeartDisease"),
    ("Naproxen",          "RheumatoidArthritis"),
    ("Naproxen",          "Gout"),
    ("Naproxen",          "Spondylitis"),
    ("Celecoxib",         "Arthritis"),
    ("Celecoxib",         "RheumatoidArthritis"),
    ("Diclofenac",        "RheumatoidArthritis"),
    ("Diclofenac",        "Tendinitis"),
    ("Meloxicam",         "Arthritis"),
    ("Indomethacin",      "Gout"),
    ("Paracetamol",       "Migraine"),
    ("Codeine",           "Neuropathy"),
    ("Morphine",          "Sciatica"),
    ("Oxycodone",         "Sciatica"),
    ("Tramadol",          "Fibromyalgia"),
    ("Tramadol",          "Neuropathy"),
    ("Gabapentin",        "Neuropathy"),
    ("Gabapentin",        "Epilepsy"),
    ("Gabapentin",        "Sciatica"),
    ("Buprenorphine",     "Neuropathy"),
    ("Prednisone",        "Asthma"),
    ("Budesonide",        "Asthma"),
    ("Budesonide",        "CrohnsDisease"),
    ("Fluticasone",       "Asthma"),
    ("Fluticasone",       "Eczema"),
    ("Hydrocortisone",    "Psoriasis"),
    ("Hydrocortisone",    "Eczema"),
    ("Betamethasone",     "Psoriasis"),
    ("Triamcinolone",     "RheumatoidArthritis"),
    ("Beclomethasone",    "Asthma"),
]

WORSENS = [
    ("Ibuprofen",     "ChronicKidneyDisease"),
    ("Naproxen",      "HeartDisease"),
    ("Aspirin",       "Asthma"),
    ("Indomethacin",  "HeartDisease"),
    ("Codeine",       "Epilepsy"),
    ("Tramadol",      "Epilepsy"),
    ("Metronidazole", "Epilepsy"),
    ("Doxycycline",   "HeartDisease"),
    ("Cortisone",     "Diabetes"),
    ("Cortisone",     "Hypertension"),
    ("Prednisone",    "Osteoporosis"),
    ("Prednisone",    "Diabetes"),
    ("Dexamethasone", "Osteoporosis"),
    ("Hydrocortisone","Hypertension"),
]

for drug, disease in TREATS:
    g.add((BIO[drug], BIO.treats,   BIO[disease]))
for drug, disease in RELIEVES:
    g.add((BIO[drug], BIO.relieves, BIO[disease]))
for drug, disease in WORSENS:
    g.add((BIO[drug], BIO.worsens,  BIO[disease]))

# ── Serialize ────────────────────────────────────────────────────────────────
g.serialize(destination=TTL_FILE, format="turtle")

drug_count    = sum(len(v) for v in DRUGS.values())
disease_count = sum(len(v) for v in DISEASES.values())
rel_count     = len(TREATS) + len(RELIEVES) + len(WORSENS)

print(f"Serialized to {TTL_FILE}")
print(f"  Drug instances:    {drug_count}")
print(f"  Disease instances: {disease_count}")
print(f"  Total instances:   {drug_count + disease_count}")
print(f"  Relationship triples: {rel_count}")
print(f"  Total triples in graph: {len(g)}")

# ── Upload to GraphDB ─────────────────────────────────────────────────────────

def wait_for_graphdb(timeout=180):
    print(f"Waiting for GraphDB at {GRAPHDB_URL} ...", end="", flush=True)
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(f"{GRAPHDB_URL}/rest/repositories", timeout=3)
            if r.status_code == 200:
                print(" ready.")
                return True
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            pass
        print(".", end="", flush=True)
        time.sleep(2)
    print(" timed out.")
    return False


def create_repository():
    repos = requests.get(f"{GRAPHDB_URL}/rest/repositories").json()
    if any(r["id"] == REPO_ID for r in repos):
        print(f"Repository '{REPO_ID}' already exists, skipping creation.")
        return

    config_ttl = f"""
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix rep:  <http://www.openrdf.org/config/repository#> .
@prefix sr:   <http://www.openrdf.org/config/repository/sail#> .
@prefix sail: <http://www.openrdf.org/config/sail#> .
@prefix graphdb: <http://www.ontotext.com/config/graphdb#> .

[] a rep:Repository ;
    rep:repositoryID "{REPO_ID}" ;
    rdfs:label "Biomedical KG" ;
    rep:repositoryImpl [
        rep:repositoryType "graphdb:SailRepository" ;
        sr:sailImpl [
            sail:sailType "graphdb:Sail" ;
            graphdb:ruleset "rdfsplus-optimized" ;
            graphdb:disable-sameAs "true" ;
            graphdb:check-for-inconsistencies "false" ;
            graphdb:entity-id-size "32" ;
            graphdb:enable-context-index "false" ;
            graphdb:enablePredicateList "true" ;
            graphdb:enable-fts-index "false" ;
            graphdb:query-timeout "0" ;
            graphdb:query-limit-results "0" ;
            graphdb:throw-QueryEvaluationException-on-timeout "false" ;
            graphdb:base-URL "http://www.example.org/biomedical#" ;
            graphdb:defaultNS "" ;
            graphdb:imports "" ;
            graphdb:repository-type "file-repository" ;
            graphdb:storage-folder "storage" ;
            graphdb:entity-index-size "10000000" ;
            graphdb:in-memory-literal-properties "true" ;
            graphdb:enable-literal-index "true" ;
        ]
    ] .
"""
    r = requests.post(
        f"{GRAPHDB_URL}/rest/repositories",
        files={"config": ("config.ttl", config_ttl.encode(), "text/turtle")},
    )
    if r.status_code in (200, 201):
        print(f"Repository '{REPO_ID}' created.")
    else:
        print(f"Failed to create repository: {r.status_code} {r.text}")
        sys.exit(1)


def upload_triples():
    with open(TTL_FILE, "rb") as f:
        r = requests.post(
            f"{GRAPHDB_URL}/repositories/{REPO_ID}/statements",
            data=f,
            headers={"Content-Type": "text/turtle"},
        )
    if r.status_code in (200, 204):
        print(f"Uploaded {TTL_FILE} to repository '{REPO_ID}'.")
    else:
        print(f"Upload failed: {r.status_code} {r.text}")
        sys.exit(1)


if not wait_for_graphdb():
    print("GraphDB not reachable. Is Docker running?")
    sys.exit(1)

create_repository()
upload_triples()
print("Done. Open http://localhost:7200 to explore the graph.")
