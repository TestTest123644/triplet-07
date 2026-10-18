# Humanized Writing Guide: Anti-AI Style Standard

This document sets the tone and editorial rules for all Twin Layer documentation. It draws directly from the Wikipedia field guide on identifying AI-generated text (*Wikipedia: Signs of AI writing*) to eliminate artificial fluff, inflated vocabulary, and formulaic sentence structures.

Our goal is simple: write like a pragmatic software engineer speaking directly to other engineers who need to run, debug, and build on this system.

---

## 1. Forbidden AI Habits & Human Replacements

### A. Ban the "AI Vocabulary" Repertoire
Large language models reflexively use specific words to make ordinary things sound grandiose. Avoid these words and replace them with direct, everyday technical descriptions:

| AI Cliche to Avoid | Why It Fails | Human Replacement |
| :--- | :--- | :--- |
| *serves as / stands as* | Pretentious copulative | Just use **is**, **runs on**, or **acts as**. |
| *is a testament to* | Emotional puffery | "Shows that", "proves that", or state the data directly. |
| *pivotal / vital / crucial / key* | Meaningless hype | Explain *why* something matters instead of declaring it vital. |
| *underscores the importance* | Inflated commentary | "Highlights", "demonstrates", or cut the phrase entirely. |
| *delve into / explore* | Classic LLM filler | "Review", "examine", "read", "trace", or "inspect". |
| *evolving landscape* | Vague marketing jargon | Name the specific components changing. |
| *focal point / indelible mark* | Dramatic literature flourish | Cut. Focus on the actual component or result. |
| *tapestry / rich tapestry* | Instant AI hallmark | Cut. Use "architecture", "structure", or "dataset". |
| *beacon of / spearheading* | Corporate PR hype | Describe what the code actually does. |

### B. Eliminate Formulaic Negative Parallelisms
LLMs rely heavily on rigid contrast patterns to sound nuanced:
- **Avoid:** *"Not only does the Twin Layer stream Kafka telemetry, but it also provides an MCP server."*
- **Human:** *"The Twin Layer streams telemetry over Kafka and exposes an MCP server for control commands."*
- **Avoid:** *"This is not a simple simulator, but a comprehensive cyber-physical twin."*
- **Human:** *"This simulator generates synthetic physical telemetry and logs actual sensor values to SQLite."*

### C. Break the "Rule of Three"
Do not pad descriptions with three adjectives or three verbs just to fill space:
- **Avoid:** *"A robust, scalable, and resilient architecture."*
- **Human:** *"Built to sustain 420 messages per second on a single machine."*
- **Avoid:** *"Detect, contain, and mitigate adversarial attacks."*
- **Human:** *"Quarantine compromised sensors and roll back false readings."*

### D. Avoid Canned Hedging and Didactic Preambles
- **Avoid:** *"It is important to remember that simulation time is different from wall-clock time."*
- **Human:** *"Simulation time is distinct from wall-clock time. Every payload timestamp (`ts`) reflects the virtual clock."*
- **Avoid:** *"One must ensure that Docker is running before executing commands."*
- **Human:** *"Start Docker Desktop before running the compose script."*

### E. Avoid Superficial Summaries at the End of Every Section
LLMs close sections with platitudes like:
- *"In conclusion, this setup ensures optimal performance and seamless integration across all layers."*
Cut these entirely. End each section with the command, output, or table that finishes the point.

---

## 2. Core Traits of Human Technical Documentation

1. **Concrete Decisions & Reasons:** Say *why* we chose something. 
   *(Example: "We configured SQLite with WAL mode (`PRAGMA journal_mode = WAL`) because default rollback journals threw `database is locked` errors during concurrent 10 Hz simulation writes and Streamlit dashboard reads.")*
2. **Real Troubleshooting Steps:** Include the exact errors an engineer might encounter, why they happen, and how to fix them in 10 seconds.
3. **Active Voice & Direct Verbs:** Write "Run `docker compose up -d`" instead of "The user can proceed by executing the docker compose command".
4. **Varied Sentence Length:** Mix short, punchy sentences with technical explanations. Avoid uniform paragraph rhythms.
5. **Accurate Scope:** Do not oversell. Clearly state what the code does, what it mocks, and where its boundaries lie.
