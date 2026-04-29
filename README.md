# SDM Lab 2 — Biomedical RDFS Knowledge Graph

Builds and queries an RDFS knowledge graph of drugs and diseases using RDFLib, GraphDB, and SPARQL.

## Requirements

- [Docker](https://docs.docker.com/get-docker/) (running)
- Python 3

## Run

```bash
./run.sh
```

This will:
1. Pull and start `ontotext/graphdb:10.7.6` on port 7200
2. Install Python dependencies (`rdflib`, `requests`)
3. Generate the knowledge graph and serialize to `biomedical_kg.ttl`
4. Create the `biomedical` repository in GraphDB with RDFS (Optimized) reasoning
5. Upload the triples

Once done, open **http://localhost:7200** and select the `biomedical` repository.

## SPARQL Queries

Run these in the GraphDB SPARQL editor (always include the PREFIX declarations):

**List all drugs (50)**
```sparql
PREFIX bio: <http://www.example.org/biomedical#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?drug WHERE {
    ?drug rdf:type bio:Drug .
} ORDER BY ?drug
```

**List all diseases (50)**
```sparql
PREFIX bio: <http://www.example.org/biomedical#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?disease WHERE {
    ?disease rdf:type bio:Disease .
} ORDER BY ?disease
```

**All drug–disease pairs where the drug affects the disease (76)**
```sparql
PREFIX bio: <http://www.example.org/biomedical#>

SELECT DISTINCT ?drug ?disease WHERE {
    ?drug bio:affects ?disease .
} ORDER BY ?drug ?disease
```

## Graph Structure

| Category | Count |
|---|---|
| Drug instances | 50 |
| Disease instances | 50 |
| `treats` relationships | 29 |
| `relieves` relationships | 33 |
| `worsens` relationships | 14 |
| Total triples (explicit) | 205 |

Drug subclasses: `AntiInflammatory`, `Antibiotic`, `Analgesic`, `Antiviral`, `Steroid`

Disease subclasses: `InflammatoryDisease`, `InfectiousDisease`, `ChronicDisease`, `NeurologicalDisease`

Property hierarchy: `affects` ← `treats`, `relieves`, `worsens`

## Files

| File | Description |
|---|---|
| `run.sh` | Single entry point — starts Docker and loads the graph |
| `build_kg.py` | Builds the RDF graph and uploads it to GraphDB |
| `biomedical_kg.ttl` | Generated Turtle file (created by running the script) |
| `report.tex` | Full lab report (Section A, B, C) |
