# Project TRUTH: Forensic Auditing of Statutory Timeline Compression in Public Procurement

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://truth-procurement-auditor-611.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Forensic Standard: RFC 6962](https://img.shields.io/badge/Integrity-RFC%206962%20Merkle-green.svg)](https://datatracker.ietf.org/doc/html/rfc6962)

**Author:** Piyush Jakhar[cite: 1]  
**Subject Category:** Systems Software (SOFT)[cite: 1]  
**Target Fair:** IRIS National Science Fair 2026[cite: 1]  
**Live Production Dashboard:** [truth-procurement-auditor-611.streamlit.app](https://truth-procurement-auditor-611.streamlit.app/)[cite: 1]

---

## 📌 Project Overview

Project TRUTH (**T**ransparency in **R**oad **U**tilities and **T**enders **H**ub) is an end-to-end civic auditing and digital forensic systems pipeline[cite: 1]. It audits active public procurement notices against statutory transparency mandates defined under Rule 43 of the **Rajasthan Transparency in Public Procurement (RTPP) Rules, 2013**[cite: 1].

The software programmatically ingests semi-structured notice feeds, isolates chronological and financial metadata, runs high-dimensional unsupervised anomaly detection, establishes an unalterable cryptographic chain of custody, and automatically compiles ready-to-file legal petitions under Section 6(1) of the **Right to Information (RTI) Act, 2005**[cite: 1].

---

## 🏗️ Systems Architecture Pipeline

1. **Layer 1: In-Memory Ingestion & Tokenizer Parsing Engine**[cite: 1]
   * Deterministic regular expression tokenizers extract tender identifiers, contract valuations, portal upload timestamps, and administrative tiers[cite: 1].
   * Performance: Macro $F_1$-Score of **0.984** across 200 ground-truth annotated tokens with a mean latency of **18.4 ms** per notice canvas[cite: 1].

2. **Layer 2: Deterministic Regulatory Verification & Procurement Risk Index (PRI)**[cite: 1]
   * Computes the net bidding window ($\Delta t = t_{\text{closing}} - t_{\text{published}}$) and evaluates deficits against statutory thresholds (7, 10, or 20–30 days)[cite: 1].
   * Quantifies non-compliance on a 0–100 risk scale via a weighted PRI formula incorporating window deficit and rural sub-divisional administrative tier weighting[cite: 1].

3. **Layer 3: Unsupervised Multivariate Anomaly Engine**[cite: 1]
   * Deploys an ensemble of 100 Isolation Trees (contamination factor = 0.25) across a 3-dimensional feature space: $[\Delta t_i, \text{Estimated\_Cost}_i, \text{PRI}_i]$[cite: 1].
   * Evaluates anomalous tree-path lengths to detect short-window anomalies independently of static rules, achieving a **Silhouette Coefficient of 0.72**[cite: 1].

4. **Layer 4: Cryptographic Forensic Custody Chain (`generate_ledger.py`)**[cite: 1]
   * Normalizes raw tender metadata into deterministic canonical strings and generates unique 64-character SHA-256 digests (FIPS 180-4 standard)[cite: 1].
   * Recursively aggregates leaf digests into an immutable binary Merkle Tree following the RFC 6962 standard, producing a single root signature that locks audit data integrity against tampering[cite: 1].

5. **Layer 5: Cloud Dashboard & Automated Civic Recourse**[cite: 1]
   * Interactive Streamlit dashboard hosted inside a containerized Linux runtime bounded by a 1.0 GB RAM memory threshold[cite: 1].
   * Dynamically formats and compiles official Form A petitions under Section 6(1) of the RTI Act, 2005, embedding verified timestamps and cryptographic verification hashes[cite: 1].

---

## 🔬 Empirical Ground-Truth Discovery

Evaluating an empirical corpus of **$N = 40$ active civil procurement notices** published across 11 administrative divisions in Rajasthan revealed[cite: 1]:

* **The 5-Day Physical-to-Digital Timestamp Mismatch:** Cross-referencing physical print notices from *Rajasthan Patrika* (Jhunjhunu District Edition, Page 15, September 30, 2026) against server logs on `eproc.rajasthan.gov.in` revealed that physical print claimed bid documents were available from September 25, 2026, whereas the portal server upload timestamp confirmed files were withheld until September 30, 2026 at 15:30:00 IST[cite: 1].
* **Effective Bidding Window:** External contractors were restricted to **4.10 days**, creating an illegal 2.90-day deficit against the mandatory 7-day statutory limit under Rule 43[cite: 1].
* **Spatial Concentration:** 100% of detected violations clustered within rural sub-divisional field offices (Chirawa, Khetri, Mundawar), while district circle headquarters maintained a 100% compliance rate[cite: 1].

---

## 📊 Inferential Statistical Rigor

To verify whether timeline compression is random clerical variation or systematic administrative exclusion, a $2 \times 2$ spatial contingency matrix was evaluated[cite: 1]:

* **Standard Pearson Chi-Square ($\chi^2$):** 40.00, $dof = 1$ (disqualified due to boundary zero-count frequencies)[cite: 1]
* **Yates's Continuity Corrected ($\chi^2$):** **34.84**, $dof = 1$, $p = 3.57 \times 10^{-9}$[cite: 1]
* **Fisher's Exact Test:** Exact two-tailed probability **$p = 1.18 \times 10^{-9} \quad (p < 0.0001)$**[cite: 1]
* **Conclusion:** The null hypothesis ($H_0$) is conclusively rejected, mathematically proving that timeline suppression in rural sub-divisions does not occur by random chance ($p < 0.0001$)[cite: 1].

---

## ⚙️ Repository Structure

```text
├── app.py                 # Streamlit cloud application and interactive forensic UI
├── generate_ledger.py     # SHA-256 and RFC 6962 Merkle root evidence generator
├── requirements.txt       # Production dependencies (streamlit, scikit-learn, scipy)
├── forensic_ledger.json   # Immutable cryptographic audit trail of the 40 tenders
└── README.md              # Systems architecture and research documentation
