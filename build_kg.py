"""
SDM Lab 2 - Biomedical Knowledge Graph
Generates RDFS triples and exports to Turtle (.ttl) format.
"""

from rdflib import Graph, Namespace, RDF, RDFS

BIO = Namespace("http://www.example.org/biomedical#")

g = Graph()
g.bind("bio", BIO)

# ── Metamodel layer ──────────────────────────────────────────────────────────
# Root classes
g.add((BIO.Drug,    RDF.type, RDFS.Class))
g.add((BIO.Disease, RDF.type, RDFS.Class))

# Drug subclasses
for cls in ("AntiInflammatory", "Antibiotic", "Analgesic", "Antiviral", "Steroid"):
    g.add((BIO[cls], RDF.type,         RDFS.Class))
    g.add((BIO[cls], RDFS.subClassOf,  BIO.Drug))

# Disease subclasses
for cls in ("InflammatoryDisease", "InfectiousDisease", "ChronicDisease", "NeurologicalDisease"):
    g.add((BIO[cls], RDF.type,         RDFS.Class))
    g.add((BIO[cls], RDFS.subClassOf,  BIO.Disease))

# Properties
g.add((BIO.affects, RDF.type,     RDF.Property))
g.add((BIO.affects, RDFS.domain,  BIO.Drug))
g.add((BIO.affects, RDFS.range,   BIO.Disease))

for prop in ("treats", "relieves", "worsens"):
    g.add((BIO[prop], RDF.type,             RDF.Property))
    g.add((BIO[prop], RDFS.subPropertyOf,   BIO.affects))

# ── Facts layer – drug instances (50 total) ──────────────────────────────────
DRUGS = {
    "AntiInflammatory": [
        "Ibuprofen", "Aspirin", "Naproxen", "Celecoxib", "Diclofenac",
        "Indomethacin", "Meloxicam", "Piroxicam", "Ketoprofen", "Sulindac",
    ],
    "Antibiotic": [
        "Amoxicillin", "Penicillin", "Ampicillin", "Ciprofloxacin", "Azithromycin",
        "Doxycycline", "Tetracycline", "Erythromycin", "Clarithromycin", "Metronidazole",
    ],
    "Analgesic": [
        "Paracetamol", "Codeine", "Morphine", "Oxycodone", "Tramadol",
        "Fentanyl", "Hydrocodone", "Buprenorphine", "Dihydrocodeine", "Gabapentin",
    ],
    "Antiviral": [
        "Acyclovir", "Oseltamivir", "Remdesivir", "Lopinavir", "Ritonavir",
        "Tenofovir", "Lamivudine", "Zidovudine", "Valacyclovir", "Ribavirin",
    ],
    "Steroid": [
        "Prednisone", "Cortisone", "Methylprednisolone", "Hydrocortisone", "Dexamethasone",
        "Betamethasone", "Triamcinolone", "Fluticasone", "Budesonide", "Beclomethasone",
    ],
}

# ── Facts layer – disease instances (50 total) ───────────────────────────────
DISEASES = {
    "InflammatoryDisease": [
        "Arthritis", "RheumatoidArthritis", "Lupus", "Psoriasis", "Gout",
        "CrohnsDisease", "UlcerativeColitis", "Asthma", "Eczema", "Fibromyalgia",
        "Spondylitis", "Tendinitis", "Vasculitis",
    ],
    "InfectiousDisease": [
        "Pneumonia", "Tuberculosis", "Malaria", "HIV", "Influenza",
        "COVID19", "Cholera", "Typhoid", "Dengue", "Hepatitis",
        "LymeDisease", "Salmonellosis", "Shigellosis",
    ],
    "ChronicDisease": [
        "Diabetes", "Hypertension", "HeartDisease", "ChronicKidneyDisease", "COPD",
        "Osteoporosis", "MultipleSclerosis", "AlzheimerDisease", "Epilepsy", "Anemia",
        "Hemophilia", "Thalassemia",
    ],
    "NeurologicalDisease": [
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
output = "biomedical_kg.ttl"
g.serialize(destination=output, format="turtle")

drug_count    = sum(len(v) for v in DRUGS.values())
disease_count = sum(len(v) for v in DISEASES.values())
rel_count     = len(TREATS) + len(RELIEVES) + len(WORSENS)

print(f"Serialized to {output}")
print(f"  Drug instances:    {drug_count}")
print(f"  Disease instances: {disease_count}")
print(f"  Total instances:   {drug_count + disease_count}")
print(f"  Relationship triples: {rel_count}")
print(f"  Total triples in graph: {len(g)}")
