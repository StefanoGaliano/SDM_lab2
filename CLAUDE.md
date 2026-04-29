# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Knowledge Graph Lab Assignment (Lab 2)** — Build and query an RDFS knowledge graph for biomedical data modeling, emphasizing best practices and semantic reasoning versus property graph approaches.


## Approach
- Think before acting. Read existing files before writing code.
- Be concise in output but thorough in reasoning.
- Prefer editing over rewriting whole files.
- Do not re-read files you have already read unless the file may have changed.
- Skip files over 100KB unless explicitly required.
- Suggest running /cost when a session is running long to monitor cache ratio.
- Recommend starting a new session when switching to an unrelated task.
- Test your code before declaring done.
- No sycophantic openers or closing fluff.
- Keep solutions simple and direct.
- User instructions always override this file.

## Domain & Concepts

**Biomedical Domain**: Model relationships between drugs and diseases.
- **Entities**: Drug, Disease (with subcategories like AntiInflammatory, Antibiotic, InflammatoryDisease, InfectiousDisease)
- **Relations**: `treats`, `relieves`, `worsens` (all subproperties of a general `affects` relation)
- **Scale**: ~100 instances across drug and disease classes
- **Key Semantic Principle**: Property graphs (Neo4j) assert only facts; RDFS KGs add ontological layers (taxonomy, inheritance, property abstraction) that enable reasoning

## Architecture & Deliverables

**Three interconnected sections:**

1. **Section A (Modeling)** — RDFS model design
   - Graphical representation of metamodel (schema classes, properties), model layer (taxonomy hierarchy), and facts layer (instances) done in the "rdfs_biomedical_kg_three_layers.svg"
   - Design choices: (Three-Layer Architecture
Metamodel Layer (top, purple/teal) — This layer contains the RDFS vocabulary constructs themselves: rdfs:Class, rdf:Property, rdfs:subClassOf, rdfs:domain, rdfs:range, and rdfs:subPropertyOf. These are not invented concepts — they are the W3C-standardized building blocks that give the model its formal semantics and reasoning power.
Model Layer (middle, blue) — This is the ontology schema. It defines bio:Drug and bio:Disease as rdfs:Classes, their subclasses (bio:AntiInflammatory, bio:Antibiotic, bio:InflammatoryDisease, bio:InfectiousDisease), and the property hierarchy with bio:affects as the super-property and bio:treats, bio:relieves, bio:worsens declared as rdfs:subPropertyOf bio:affects.
Facts Layer (bottom, green) — Concrete named individuals: bio:Ibuprofen, bio:Amoxicillin, bio:Arthritis, bio:BacterialInfection, and bio:GastricUlcer, each linked by rdf:type to their class, and connected by the specific properties.

Key Modeling Decisions
Property hierarchy (rdfs:subPropertyOf): bio:treats, bio:relieves, and bio:worsens are all declared as sub-properties of bio:affects. This means any triple using one of the specific properties automatically entails the more general bio:affects triple via RDFS inference — a query for "all drug–disease pairs where the drug affects the disease" returns results even if only bio:relieves was asserted. Neo4J cannot express this: its RELIEVES, TREATS, and WORSENS edge types are flat and unrelated; there is no mechanism to group them under a common abstraction.
Class hierarchy (rdfs:subClassOf): bio:AntiInflammatory rdfs:subClassOf bio:Drug means that any instance typed as AntiInflammatory is automatically also inferred to be a Drug. A query for "all drugs" returns bio:Ibuprofen even though it was only asserted as AntiInflammatory. Neo4J uses multiple labels on nodes (:Drug:AntiInflammatory) which is not a formal hierarchy — it is manual duplication, not inference.
rdfs:domain and rdfs:range: The super-property bio:affects is declared with rdfs:domain bio:Drug and rdfs:range bio:Disease. This lets GraphDB infer the type of any entity that participates in this property, even without explicit rdf:type assertions — enabling data quality validation and richer reasoning.
Minimizing redundancy: Thanks to inference, we assert only the most specific facts (e.g., bio:Ibuprofen rdf:type bio:AntiInflammatory) and let RDFS derive the rest (rdf:type bio:Drug, bio:affects bio:Arthritis, etc.). Neo4J requires all facts to be explicitly written.
Global IRIs: All terms are given proper namespace-qualified IRIs (e.g., bio:Drug), following Linked Data best practices for interoperability. Neo4J labels are plain strings with no formal identity.)
   - Identify what RDFS does that Neo4j property graphs don't (ontological structure, inference)

2. **Section B (Implementation)** — RDFLib + GraphDB
   - Python script generates triples programmatically and exports to .ttl format
   - GraphDB repository with RDFS (Optimized) reasoning enabled
   - Quality criterion: minimize explicit triples—rely on inference to derive subclass/subproperty relations
   - Must include at least subclasses under Drug and Disease, plus ~100 instances

3. **Section C (Querying)** — SPARQL queries + analysis
   - Three queries: list all drugs, list all diseases, find all (drug, disease) pairs where drug affects disease
   - For each: show SPARQL code, compare with Neo4j Cypher equivalent, explain inferences GraphDB applies
   - Document inferred triple patterns and whether they match expectations

## Tools & Stack

- **RDFLib** (Python) — Programmatic graph construction; serialize to Turtle (.ttl) format
- **GraphDB** (http://localhost:7200/) — RDFS-enabled triple store with reasoning
- **SPARQL** — Query language for KGs
- **Drawing tool** (drawio, arrows.app, yED, etc.) — Visualize metamodel/model/facts layers
- **Deliverable format**: PDF (narrative + queries), Python file (code), TTL file (triples)

## Key Constraints & Practices

### GraphDB Setup
- Enable **RDFS (Optimized)** ruleset when creating repository
- Configure JVM settings: `graphdb.workbench.maxUploadSize=40000000000` and `Xmx=2000m`
- Import .ttl file via Workbench UI or programmatically

### RDFLib Best Practices
- Create graph, add triples using `add()`, serialize to .ttl
- **Minimize redundancy**: don't assert `rdfs:subClassOf` or `rdfs:subPropertyOf` triples manually for derived classes—let GraphDB infer them through RDFS rules
- Use proper namespaces (e.g., local domain ontology namespace for classes/properties)

### Modeling Layers
- **Metamodel**: RDF/RDFS vocabulary (rdfs:Class, rdfs:subClassOf, rdfs:Property, rdfs:subPropertyOf, rdfs:range, rdfs:domain)
- **Model**: Domain classes (ex: Drug, AntiInflammatory subClassOf Drug) and properties (ex: affects with subproperties treats, relieves, worsens)
- **Facts**: Instances (ex: Ibuprofen rdf:type AntiInflammatory; Ibuprofen relieves Arthritis)

### Inference & Reasoning
- GraphDB materializes inferred triples when RDFS rules apply
  - `rdf:type` inference: if `Ibuprofen rdf:type AntiInflammatory` and `AntiInflammatory rdfs:subClassOf Drug`, then infer `Ibuprofen rdf:type Drug`
  - Property inheritance: if `treats rdfs:subPropertyOf affects`, then `?drug treats ?disease` implies `?drug affects ?disease`
- Expected behavior: querying for "all drugs" returns instances of Drug *and* all subclasses; querying "affects" returns direct and inferred relationships

## SPARQL Query Patterns

**List all drugs:**
```sparql
SELECT ?drug WHERE { ?drug rdf:type <domain:Drug> }
```

**List all diseases:**
```sparql
SELECT ?disease WHERE { ?disease rdf:type <domain:Disease> }
```

**All (drug, disease) pairs where drug affects disease:**
```sparql
SELECT ?drug ?disease WHERE { ?drug <domain:affects> ?disease }
```

Adjust namespaces and property URIs to match your ontology.

## Comparison: RDFS KG vs Neo4j Property Graph

| Aspect | RDFS KG | Neo4j Property Graph |
|--------|---------|----------------------|
| **Ontology** | Explicit class hierarchy and property taxonomy | Labels and relationship types, no inheritance |
| **Inference** | Automatic (rdf:type, subClassOf, subPropertyOf rules) | Manual (query must list all specific cases) |
| **Generalization** | General `affects` property with specific subproperties; queries on `affects` retrieve all | No built-in hierarchy; must query treats ∪ relieves ∪ worsens separately |
| **Semantics** | W3C RDF/RDFS standard; machine-interpretable | Proprietary graph model; tailored for property assertion |

## Deliverable Checklist

- [ ] PDF report: Section A (diagram + justification + RDFS vs Neo4j gaps), Section B (SPARQL queries), Section C (query analysis)
- [ ] Python file: RDFLib script generating metamodel, model, and ~100 facts
- [ ] TTL file: Serialized RDF triples
- [ ] File naming: `[Group]-[MemberSurname]+.{pdf,py,ttl}`
- [ ] Assumptions documented in PDF sections
- [ ] Group members named in document

## GraphDB Access

**Local**: http://localhost:7200/
**Tutorials**: http://localhost:7200/guides
**Docs**: graphdb.ontotext.com/documentation/

