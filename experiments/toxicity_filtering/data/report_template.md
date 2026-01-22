# Toxicity Filtering Experiments Report🤬📋

This report presents and analyses the results of a keyword-based toxicity filtering experiment conducted across multiple text corpora. The goal of the experiment is to evaluate the performance of the filtering method.

## Methodology⚙️
This section describes the datasets, toxic term list, and filtering procedure used throughout the experiment.

### Source Data

The source data [**`🗂️data`**]({relative_data_directory}) consist on **{number_of_corpora} corpora** sourced from the [**`🗃️Existing Corpora Repository`**](https://github.com/guaran-ia/existing-guarani-corpora.git), which compiles available Guarani corpora into files of a standardised form. For more information on the contents of this corpora, read their [report](https://github.com/guaran-ia/existing-guarani-corpora/blob/main/report.md).

### Toxic Term List

The words and phrases used for filtering, hereafter referred to as **toxic terms** [**`📃toxic_terms.txt`**]({toxic_term_path}), were manually copied from the SPL's list of [**`📘Palabras Vulgares u Ofensivas en Guarani`**](https://docs.google.com/document/d/1xXF2OvHNfR0nEbkKZYitx2OA15e0AesvNMZnZZN_ruc/edit?usp=sharing), which includes a combination of single-word and multi-word expressions. 

### Filtering Criterion

A document is considered an **affected document** if it contains **at least one term** from the list. 

Toxic terms are identified using regular expression matching with word boundaries to reduce false positives from partial matches. The individual occurrences of each term are counted independendly, so that multiple toxic terms can be identified in a singular document. Refer to [**`📄utils.py`**]({utils_path}) for the matching function.

## Summary of Results 📊

The following is a global overview of the results of the filtering process. More in-depth analyses are presented in the following sections.

- **Number of analysed corpora:** {number_of_corpora}
- **Number of documents analysed:** {total_documents}
- **Number of affected documents:** {affected_documents} ({percentage_affected_documents}%)
- **Total number of toxic terms:** {toxic_terms}
- **Number of distinct toxic terms:** {toxic_terms_distinct}
- **Toxic term density across all documents:** {toxic_term_density_all}
- **Toxic term density across affected documents:** {toxic_term_density_affected}

## Corpus-Level Analysis 📚

This section examines how toxicity is distributed across individual corpora. 

### Table 1: Corpus-Level Breakdown

The table below summarizes toxicity-related statistics for each corpus. The table is ordered by corpus size, from largest to smallest, and the highest values for each column are highlighted.

{corpus_level_breakdown_table}

### Figure 1: Corpus Size vs. Toxicity Prevalence

![Corpus Size vs. Toxicity Percentage]({corpus_size_vs_toxicity_percentage_figure})

> The scatter plot above compares corpus size (X-axis, log normalised) with the percentage of affected documents in the corpus (Y-axis). The dot sizes represent the number (raw count) of affected documents, while the **x** markers represent corpora without affected documents.

## Term-Level Analysis 🔤

This section focuses on the distribution and frequency of individual toxic terms.

### Table 2: Term-Level Breakdown

The table below shows the frequency of the detected toxic terms. The table is ordered from most to least frequent term, and terms from the list that were not detected are omitted.

{term_level_breakdown_table}

### Figure 2. Pareto Curve of Term Frequency (Top-20)

![Pareto Curve of Term Frequency]({pareto_chart_term_frequency})

> The Pareto Curve shows the cumulative distribution of the detected toxic terms. The Top-5 toxic terms account for **{cumulative_percentage_toxic_terms_top_5}%** of all occurrences, while the Top-10 toxic terms account for **{cumulative_percentage_toxic_terms_top_10}%** of occurrences. Terms outside the Top-20 most frequent terms are excluded for clarity. Refer to **Table 2** for the complete breakdown.

## Attribution Analysis 📑

This section explores the origins of the identified toxic terms and affected documents, in terms of their source and domain.

>[NOTE] As seen in their respective sections, many documents have the source and/or domain labelled as *'unknown'*, while this is included in the complete breakdowns (**Tables 3 & 4**), the unknown sources are excluded from other forms of analysis.


### Table 3: Source-Level Breakdown

This table showcases the complete stats of the sources where affected documents were found. The sources are ordered by amount of affected documents attributed to them, with the sources without affected documents being left at the bottom of the table.

{source_level_breakdown_table}

### Figure 3: Source Toxicity Risk vs. Contributiobn

![Source Risk vs. Contribution]({source_risk_vs_contribution})

> The graph shows each source's toxicity risk (the percentage of the documents attributed to that source that are affected) plotted against its toxicity contribution (the percentage from all the affected documents attributed to that source). As previously mentioned, documents with their sources labelled as *'unknown'*, which represent **{unknown_source_percentage}%** of the affected documents, are excluded from this analysis. The Top-3 sources with the most contribution and most risk are labelled.

### Table 4: Domain-Level Breakdown

This table showcases the complete stats of the domains where affected documents were found. Domains without affected documents are grouped into the 'Others' category to prevent the table from becoming, in total {number_domains_no_affected_documents} compose this category. The domains are ordered by amount of affected documents attributed to them, with the domains without affected documents being left at the bottom of the table.

{domain_level_breakdown_table}

### Figure 4: Domain Toxicity vs. Contribution (Top-20)

![Domain Risk vs. Contribution]({domain_risk_vs_contribution})

> The graph shows each domain's toxicity risk (the percentage of the documents attributed to that domain that are affected) plotted against its toxicity contribution (the percentage from all the affected documents attributed to that source). The plot includes only the Top-20 domains with the most overall documents. Furthermore and as previously mentioned the documents for which the domain was labelled as *'unknown'*, which represent the **{unknown_domain_percentage}%** of all affected documents, are excluded from the analysis.

## Limitations and Future Work

The current keyword matching method relies on unified spelling of the toxic terms. As a result, instances of these terms where the spelling is different (e.g. different apostrophe or nasal tilde) are likely not matched. 

### False Positive Identification
This report doesn't account for false positive or false negative cases, as that is work that should be manually done. For false positive identification, this spreadsheet [**`Toxic Content Filtering`**](https://docs.google.com/spreadsheets/d/1vet809FK5yo7RdrYuhVrYkK19pzOHbfDl0OOck_nyxk/edit?usp=sharing) has been made available.

### Toxic Term Severity

The list of toxic terms used for identification contains vocabulary with varying degrees of offensiveness. This report doesn't account for this aspect of the affected documents. The proposal is to assign an offensiveness score to each term, and use those to calculate a similar score for each affected document to then integrate said scores into the report. The labels can be assigned in this spreadsheet [**`Toxic Term Score Assignment`**](https://docs.google.com/spreadsheets/d/13xCHU2A_ys-l5oYV_NFZbYtXZWsFd3tAXjWPte90VYY/edit?usp=sharing)