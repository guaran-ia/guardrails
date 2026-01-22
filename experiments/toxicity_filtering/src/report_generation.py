from utils import read_json, make_markdown_table
import os
from collections import Counter
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

COLOR_PALETTE = px.colors.sequential.Agsunset

def compile_summaries(data_path:str):
    summaries = []
    for directory in os.listdir(data_path):
        summary_path = os.path.join(data_path, directory, f"{directory}_toxic_term_filtering_report.json")
        summaries.append(read_json(summary_path))
    
    return summaries

def get_general_statistics(summaries:list[dict]):
    number_of_corpora = 0
    total_documents = 0
    affected_documents = 0
    toxic_term_counter = Counter()

    for summary in summaries:
        number_of_corpora += 1
        total_documents += summary["total_documents"]
        affected_documents += summary['affected_documents']
        toxic_term_counter.update(summary['toxic_term_counts'])


    general_statistics = {
        'number_of_corpora':number_of_corpora,
        'total_documents':total_documents,
        'affected_documents':affected_documents,
        'percentage_affected_documents':f"{affected_documents/total_documents*100:.2f}",
        'toxic_terms':toxic_term_counter.total(),
        'toxic_terms_distinct':len(toxic_term_counter),
        'toxic_term_density_all':f"{toxic_term_counter.total()/total_documents:.4f}",
        'toxic_term_density_affected':f"{toxic_term_counter.total()/affected_documents:.4f}"
    }

    return general_statistics


def create_corpus_level_table(summaries:list[dict]):
    corpus_level_rows = []

    for summary in summaries:
        total_docs = summary["total_documents"]
        affected_docs = summary["affected_documents"]
        toxic_terms = summary["toxic_terms"]

        row = {
            "Corpus Name": summary["corpus_name"],
            "Total Documents": total_docs,
            "Affected Documents": affected_docs,
            "Percentage of Affected Documents": summary["ratio_affected_documents"],
            "Toxic Terms": toxic_terms,
            "Toxic Term Density (All Documents)": (
                toxic_terms / total_docs if total_docs > 0 else 0
            ),
            "Toxic Term Density (Affected Documents)": (
                toxic_terms / affected_docs if affected_docs > 0 else 0
            ),
        }

        corpus_level_rows.append(row)

    corpus_level_table = make_markdown_table(
        corpus_level_rows,
        order_by="Total Documents",
        highlights={
            "Affected Documents": "max",
            "Percentage of Affected Documents": "max",
            "Toxic Terms": "max",
            "Toxic Term Density (All Documents)": "max",
            "Toxic Term Density (Affected Documents)": "max"
        },
        totals={
            "Total Documents": "sum",
            "Affected Documents": "sum",
            "Percentage of Affected Documents": lambda rows: (
                sum(r["Affected Documents"] for r in rows)
                / sum(r["Total Documents"] for r in rows)
            ),
            "Toxic Terms": "sum",
            "Toxic Term Density (All Documents)": lambda rows: (
                sum(r["Toxic Terms"] for r in rows)
                / sum(r["Total Documents"] for r in rows)
            ),
            "Toxic Term Density (Affected Documents)": lambda rows: (
                sum(r["Toxic Terms"] for r in rows)
                / sum(r["Affected Documents"] for r in rows)
            ),
        },
        formatters={
            "Percentage of Affected Documents": lambda x: f"{x:.2%}",
            "Toxic Term Density (All Documents)": lambda x: f"{x:.4f}",
            "Toxic Term Density (Affected Documents)": lambda x: f"{x:.4f}",
        },
        align="center",
    )

    return corpus_level_table, corpus_level_rows

def create_term_level_table(summaries: list[dict]):
    term_level_rows = []

    term_counter = Counter()

    for summary in summaries:
        term_counter.update(summary['toxic_term_counts'])

    total = sum(term_counter.values())

    for term, count in term_counter.items():
        row = {
            'Term': term,
            'Occurrences':count,
            'Percentage of All Occurrences': count/total
        }

        term_level_rows.append(row)

    term_level_table = make_markdown_table(
        term_level_rows,
        order_by="Occurrences",
        highlights={
            "Occurrences": "max",
            "Percentage of All Occurrences": "max",
        },
        totals={
            "Occurrences": "sum",
        },
        formatters={
            "Percentage of All Occurrences": lambda x: f"{x:.2%}",
        },
        align="center",
    )

    return term_level_table, term_level_rows

def create_source_level_table(summaries:list[dict]):
    source_level_rows = []
    total_documents_source = Counter()
    affected_documents_source = Counter()
    toxic_terms_source = Counter()
    total_affected_documents = 0


    for summary in summaries:
        total_affected_documents += summary['affected_documents']
        total_documents_source.update(summary['total_documents_by_source'])
        affected_documents_source.update(summary['affected_documents_by_source'])
        toxic_terms_source.update(summary['toxic_terms_by_source'])

    total_documents_sources_no_affected_documents = 0
    sources_no_affected_documents = 0

    for source, total_documents in total_documents_source.items():
        affected_documents = affected_documents_source[source]

        if affected_documents == 0:
            total_documents_sources_no_affected_documents += total_documents
            sources_no_affected_documents += 1
            continue

        percentage_from_source_documents = affected_documents/total_documents
        percentage_from_affected_documents = affected_documents/total_affected_documents
        toxic_terms = toxic_terms_source[source]
        toxic_term_density_total_documents = toxic_terms/total_documents
        toxic_term_density_affected_documents = toxic_terms/affected_documents if affected_documents > 0 else 0

        row = {
            'Source Name': source,
            'Total Documents': total_documents,
            'Affected Documents': affected_documents,
            'Percentage from Source Documents': percentage_from_source_documents,
            'Percentage from Affected Documents': percentage_from_affected_documents,
            'Toxic Terms': toxic_terms,
            'Toxic Term Density (Total Documents)': toxic_term_density_total_documents,
            'Toxic Term Density (Affected Documents)': toxic_term_density_affected_documents
        }

        source_level_rows.append(row)

    row = {
        'Source Name': "Others",
        'Total Documents': total_documents_sources_no_affected_documents,
        'Affected Documents': 0,
        'Percentage from Source Documents': 0.0,
        'Percentage from Affected Documents': 0.0,
        'Toxic Terms': 0,
        'Toxic Term Density (Total Documents)': 0.0,
        'Toxic Term Density (Affected Documents)': 0.0
    }

    source_level_rows.append(row)

    source_level_table = make_markdown_table(
        source_level_rows,
        order_by=["Affected Documents", "Total Documents"],
        highlights={
            'Affected Documents': "max",
            'Percentage from Source Documents': "max",
            'Percentage from Affected Documents': "max",
            'Toxic Terms': "max",
            'Toxic Term Density (Total Documents)': "max",
            'Toxic Term Density (Affected Documents)': "max",
        },
        totals={
            "Affected Documents": "sum",
            'Toxic Terms': "sum",
            'Percentage from Source Documents': lambda rows: (
                sum(r['Affected Documents'] for r in rows)/ sum(r['Total Documents'] for r in rows)
            ),
            'Toxic Term Density (Total Documents)': lambda rows: (
                sum(r['Toxic Terms'] for r in rows)/sum(r['Total Documents'] for r in rows)
            ),
            'Toxic Term Density (Affected Documents)': lambda rows: (
                sum(r['Toxic Terms'] for r in rows)/ sum(r["Affected Documents"] for r in rows)
            ),
        },
        formatters={
            'Percentage from Source Documents': lambda x:f"{x:.2%}",
            'Percentage from Affected Documents': lambda x:f"{x:.2%}",
            'Toxic Term Density (Total Documents)': lambda x:f"{x:.4f}",
            'Toxic Term Density (Affected Documents)': lambda x:f"{x:.4f}",
        },
        align="center",
    )

    return source_level_table, source_level_rows

def create_domain_level_table(summaries:list[dict]):
    domain_level_rows = []
    total_documents_domain = Counter()
    affected_documents_domain = Counter()
    toxic_terms_domain = Counter()
    total_affected_documents = 0

    for summary in summaries:
        total_affected_documents += summary['affected_documents']
        total_documents_domain.update(summary['total_documents_by_domain'])
        affected_documents_domain.update(summary['affected_documents_by_domain'])
        toxic_terms_domain.update(summary['toxic_terms_by_domain'])

    total_documents_domains_no_affected_documents = 0
    domains_no_affected_documents = 0

    for domain, total_documents in total_documents_domain.items():
        affected_documents = affected_documents_domain[domain]

        if affected_documents == 0:
            total_documents_domains_no_affected_documents += total_documents
            domains_no_affected_documents += 1
            continue

        percentage_from_domain_documents = affected_documents/total_documents
        percentage_from_affected_documents = affected_documents/total_affected_documents
        toxic_terms = toxic_terms_domain[domain]
        toxic_term_density_total_documents = toxic_terms/total_documents
        toxic_term_density_affected_documents = toxic_terms/affected_documents if affected_documents > 0 else 0

        row = {
            'Domain': domain,
            'Total Documents': total_documents,
            'Affected Documents': affected_documents,
            'Percentage from Domain Documents': percentage_from_domain_documents,
            'Percentage from Affected Documents': percentage_from_affected_documents,
            'Toxic Terms': toxic_terms,
            'Toxic Term Density (Total Documents)': toxic_term_density_total_documents,
            'Toxic Term Density (Affected Documents)': toxic_term_density_affected_documents
        }

        domain_level_rows.append(row)    

    row = {
        'Domain': "Others",
        'Total Documents': total_documents_domains_no_affected_documents,
        'Affected Documents': 0,
        'Percentage from Domain Documents': 0.0,
        'Percentage from Affected Documents': 0.0,
        'Toxic Terms': 0,
        'Toxic Term Density (Total Documents)': 0.0,
        'Toxic Term Density (Affected Documents)': 0.0
    }

    domain_level_rows.append(row)
    
    domain_level_table = make_markdown_table(
        domain_level_rows,
        order_by=["Affected Documents", "Total Documents"],
        highlights={
            'Affected Documents': "max",
            'Percentage from Domain Documents': "max",
            'Percentage from Affected Documents': "max",
            'Toxic Terms': "max",
            'Toxic Term Density (Total Documents)': "max",
            'Toxic Term Density (Affected Documents)': "max",
        },
        totals={
            "Affected Documents": "sum",
            'Toxic Terms': "sum",
            'Percentage from Domain Documents': lambda rows: (
                sum(r['Affected Documents'] for r in rows)/ sum(r['Total Documents'] for r in rows)
            ),
            'Toxic Term Density (Total Documents)': lambda rows: (
                sum(r['Toxic Terms'] for r in rows)/sum(r['Total Documents'] for r in rows)
            ),
            'Toxic Term Density (Affected Documents)': lambda rows: (
                sum(r['Toxic Terms'] for r in rows)/ sum(r["Affected Documents"] for r in rows)
            ),
        },
        formatters={
            'Percentage from Domain Documents': lambda x:f"{x:.2%}",
            'Percentage from Affected Documents': lambda x:f"{x:.2%}",
            'Toxic Term Density (Total Documents)': lambda x:f"{x:.4f}",
            'Toxic Term Density (Affected Documents)': lambda x:f"{x:.4f}",
        },
        align="center",
    )

    return domain_level_table, domain_level_rows, domains_no_affected_documents

def create_tables(summaries:list[dict]):
    tables = {}
    rows = {}

    tables['corpus_level_breakdown_table'], rows['corpus_level_rows'] = create_corpus_level_table(summaries=summaries)
    tables['term_level_breakdown_table'], rows['term_level_rows'] = create_term_level_table(summaries=summaries)
    tables['source_level_breakdown_table'], rows['source_level_rows'] = create_source_level_table(summaries=summaries)
    tables['domain_level_breakdown_table'], rows['domain_level_rows'], domains_no_affected_documents = create_domain_level_table(summaries=summaries)
    
    return tables, rows, domains_no_affected_documents

def create_corpus_size_vs_toxicity_plot(corpus_level_rows:list[dict]):
    corpus_level_df = pd.DataFrame(corpus_level_rows)
    corpus_level_df["Percentage of Affected Documents (%)"] = corpus_level_df["Percentage of Affected Documents"] * 100
    corpus_level_df_zero = corpus_level_df[corpus_level_df["Affected Documents"] == 0]
    corpus_level_df_nonzero = corpus_level_df[corpus_level_df["Affected Documents"] > 0]
    largest = corpus_level_df.nlargest(4, "Total Documents")
    most_toxic = corpus_level_df.nlargest(4, "Percentage of Affected Documents (%)")
    labels = pd.concat([largest, most_toxic]).drop_duplicates()
    
    corpus_size_vs_toxicity = go.Figure()

    #Corpora with Affected Documents
    corpus_size_vs_toxicity.add_trace(
        go.Scatter(
            x=corpus_level_df_nonzero['Total Documents'],
            y=corpus_level_df_nonzero['Percentage of Affected Documents (%)'],
            mode="markers",
            marker=dict(
                size=corpus_level_df_nonzero['Affected Documents'],
                sizemode="area",
                sizeref=2.*max(corpus_level_df_nonzero['Affected Documents'])/(40.**2),
                opacity=0.8,
                line=dict(width=1),
            ),
            showlegend=False
        )
    )

    #Corpora without Affected Documents
    corpus_size_vs_toxicity.add_trace(
        go.Scatter(
            x=corpus_level_df_zero["Total Documents"],
            y=corpus_level_df_zero['Percentage of Affected Documents (%)'],
            mode="markers",
            marker=dict(
                symbol="x",
                size=8,
                line=dict(width=0)
            ),
            showlegend=False
        )
    )

    corpus_size_vs_toxicity.add_trace(
        go.Scatter(
            x=labels["Total Documents"],
            y=labels['Percentage of Affected Documents (%)'],
            mode="text",
            text=labels["Corpus Name"],
            textposition="top center",
            showlegend=False
        )
    )

    corpus_size_vs_toxicity.update_layout(
        template = "plotly_dark",
        xaxis=dict(
            title=dict(
                text = "Total Documents"
            ),
            type="log",
        ),
        yaxis=dict(
            title=dict(
                text = "Percentage of Affected Documents"
            ),
        ),
        width = 1000,
        height = 550,
        margin=dict(l=80, r=40, t=40, b=80),
    )

    return corpus_size_vs_toxicity

def create_pareto_chart_terms(term_level_rows:list[dict]):
    term_level_df = pd.DataFrame(term_level_rows)
    term_level_df = term_level_df.sort_values("Occurrences", ascending=False)
    top_n = 20
    term_level_df = term_level_df.head(top_n)
    term_level_df["Rank"] = range(1, len(term_level_df) + 1)
    term_level_df["Cumulative Occurrences"] = term_level_df["Occurrences"].cumsum()
    term_level_df["Cumulative %"] = term_level_df["Cumulative Occurrences"] / term_level_df["Occurrences"].sum() * 100
    total_count = term_level_df["Occurrences"].sum()
    top_5_pct = term_level_df.head(5)["Occurrences"].sum() / total_count * 100
    top_10_pct = term_level_df.head(10)["Occurrences"].sum() / total_count * 100

    terms_pareto_chart = go.Figure()

    terms_pareto_chart.add_trace(go.Bar(
        x=term_level_df["Term"],
        y=term_level_df["Occurrences"],
        name="Occurrences",
        opacity=0.85,
        yaxis="y",
    ))


    terms_pareto_chart.add_trace(go.Scatter(
        x=term_level_df["Term"],
        y=term_level_df["Cumulative %"],
        name="Cumulative %",
        mode="lines+markers",
        line=dict(width=3),
        marker=dict(size=6),
        yaxis="y2",
    ))

    for x, label in [(4, "Top 5"), (9, "Top 10")]:
        terms_pareto_chart.add_shape(
            type="line",
            x0=x,
            x1=x,
            y0=0,
            y1=100,
            yref="y2",
            line=dict(dash="dash", color=COLOR_PALETTE[3])
        )

        terms_pareto_chart.add_annotation(
            x=x,
            y=103,
            yref="y2",
            text=label,
            showarrow=False,
            font=dict(size=12)
        )

    terms_pareto_chart.add_annotation(
        x=4,
        y=term_level_df.loc[term_level_df["Rank"] == 5, "Cumulative %"].values[0],
        yref="y2",
        text=f"{top_5_pct:.1f}% of occurrences",
        showarrow=True,
        arrowhead=2,
    )

    terms_pareto_chart.add_annotation(
        x=9,
        y=term_level_df.loc[term_level_df["Rank"] == 10, "Cumulative %"].values[0],
        yref="y2",
        text=f"{top_10_pct:.1f}% of occurrences",
        showarrow=True,
        arrowhead=2,
    )

    terms_pareto_chart.update_layout(
        template="plotly_dark",
        xaxis=dict(
            title="Toxic Term",
            tickmode="linear",
            dtick=1
        ),
        yaxis=dict(
            title="Number of Occurrences"
        ),
        yaxis2=dict(
            title="Cumulative Percentage of Occurrences",
            overlaying="y",
            side="right",
            griddash="dot"
        ),
        width=1000,
        height=550,
        showlegend=False,
        margin=dict(l=80, r=80, t=40, b=80),
    )

    pareto_chart_dict = {
        'cumulative_percentage_toxic_terms_top_5': f"{top_5_pct:.4f}",
        'cumulative_percentage_toxic_terms_top_10': f"{top_10_pct:.4f}"
    }

    return terms_pareto_chart, pareto_chart_dict

def create_risk_contribution_plot_source(source_level_rows:list[dict]):
    source_level_df = pd.DataFrame(source_level_rows)
    unknown_source_percentage = source_level_df.loc[source_level_df["Source Name"] == 'unknown', "Percentage from Affected Documents"].iloc[0]
    source_level_df = source_level_df[source_level_df['Source Name'] != 'unknown']

    source_level_df['Contribution'] = source_level_df['Percentage from Affected Documents'] * 100
    source_level_df['Risk'] = source_level_df['Percentage from Source Documents'] * 100

    most_contribution = source_level_df.nlargest(3, "Contribution")
    riskiest = source_level_df.nlargest(3, "Risk")

    labels = pd.concat([most_contribution, riskiest]).drop_duplicates()

    risk_contribution_source = go.Figure()
    risk_contribution_source.add_trace(go.Scatter(
        x=source_level_df["Contribution"],
        y=source_level_df["Risk"],
        textposition="top center",
        mode="markers",
        marker=dict(
            size=source_level_df["Total Documents"] / source_level_df["Total Documents"].max() * 40 + 5,
        )
    ))

    for _, row in labels.iterrows():
        risk_contribution_source.add_annotation(
            x=row["Contribution"],
            y=row["Risk"],
            text=row["Source Name"],
            showarrow=True,
            arrowhead=1,
            ax=20,
            ay=-30,
            borderwidth=1,
            font=dict(size=11),
        )

    risk_contribution_source.update_layout(
        template="plotly_dark",
        xaxis=dict(title="Source Contribution (%)"),
        yaxis=dict(title="Source Risk (%)"),
        width=1000,
        height=550,
        margin=dict(l=80, r=40, t=40, b=80),
        showlegend=False
    )

    return risk_contribution_source, f"{unknown_source_percentage*100:.4f}"

def create_risk_contribution_plot_domain(domain_level_rows:list[dict]):
    domain_level_df = pd.DataFrame(domain_level_rows)
    unknown_domain_percentage = domain_level_df.loc[domain_level_df["Domain"] == 'unknown', "Percentage from Affected Documents"].iloc[0]
    domain_level_df = domain_level_df[domain_level_df['Domain'] != 'unknown']

    domain_level_df['Contribution'] = domain_level_df['Percentage from Affected Documents'] * 100
    domain_level_df['Risk'] = domain_level_df['Percentage from Domain Documents'] * 100

    domain_level_df = domain_level_df.nlargest(30, "Total Documents")

    most_contribution = domain_level_df.nlargest(3, "Contribution")
    riskiest = domain_level_df.nlargest(3, "Risk")

    labels = pd.concat([most_contribution, riskiest]).drop_duplicates()

    risk_contribution_domain = go.Figure()
    risk_contribution_domain.add_trace(go.Scatter(
        x=domain_level_df["Contribution"],
        y=domain_level_df["Risk"],
        textposition="top center",
        mode="markers",
        marker=dict(
            size=domain_level_df["Total Documents"] / domain_level_df["Total Documents"].max() * 40 + 5,
        )
    ))

    for _, row in labels.iterrows():
        risk_contribution_domain.add_annotation(
            x=row["Contribution"],
            y=row["Risk"],
            text=row["Domain"],
            showarrow=True,
            arrowhead=1,
            ax=20,
            ay=-30,
            borderwidth=1,
            font=dict(size=11),
        )

    risk_contribution_domain.update_layout(
        template="plotly_dark",
        xaxis=dict(title="Contribution to Affected Documents (%)", automargin=True),
        yaxis=dict(title="Percentage of Affected Documents (%)", automargin=True),
        width=1000,
        height=550,
        margin=dict(l=80, r=40, t=40, b=80),
        showlegend=False
    )

    return risk_contribution_domain, f"{unknown_domain_percentage*100:.4f}"

def create_plots(table_rows:dict[str, dict], plots_data_path:str):
    os.makedirs(plots_data_path, exist_ok=True)

    plots = {}
    plots_data = {}

    #Figure 1: corpus size vs toxicity
    corpus_size_vs_toxicity_file = os.path.join(plots_data_path, "corpus_size_vs_toxicity.png")
    corpus_size_vs_toxicity_plot = create_corpus_size_vs_toxicity_plot(table_rows['corpus_level_rows'])
    corpus_size_vs_toxicity_plot.write_image(corpus_size_vs_toxicity_file, scale=2)

    plots['corpus_size_vs_toxicity_percentage_figure'] = corpus_size_vs_toxicity_file

    #Figure 2: Pareto Chart
    toxic_terms_pareto_chart_file = os.path.join(plots_data_path, "toxic_terms_pareto_chart.png")
    toxic_terms_pareto_chart_plot, toxic_terms_pareto_chart_dict = create_pareto_chart_terms(table_rows['term_level_rows'])
    toxic_terms_pareto_chart_plot.write_image(toxic_terms_pareto_chart_file, scale=2)

    plots['pareto_chart_term_frequency'] = toxic_terms_pareto_chart_file
    plots_data.update(toxic_terms_pareto_chart_dict)

    #Figure 3: Source Risk vs Contribution
    source_risk_vs_contribution_file = os.path.join(plots_data_path, "source_risk_vs_contribution.png")
    source_risk_vs_contribution_plot, unknown_source_percentage = create_risk_contribution_plot_source(table_rows['source_level_rows'])
    source_risk_vs_contribution_plot.write_image(source_risk_vs_contribution_file, scale=2)

    plots['source_risk_vs_contribution'] = source_risk_vs_contribution_file
    plots_data['unknown_source_percentage'] = unknown_source_percentage

    #Figure 4: Domain Risk vs Contribution
    domain_risk_vs_contribution_file = os.path.join(plots_data_path, "domain_risk_vs_contribution.png")
    domain_risk_vs_contribution_plot, unknown_domain_percentage = create_risk_contribution_plot_domain(table_rows['domain_level_rows'])
    domain_risk_vs_contribution_plot.write_image(domain_risk_vs_contribution_file, scale=2)

    plots['domain_risk_vs_contribution'] = domain_risk_vs_contribution_file
    plots_data['unknown_domain_percentage'] = unknown_domain_percentage

    return plots, plots_data
    

def create_report(data_path:str, output_path:str, filename:str, processing_paths:dict):
    #Data paths
    report_template_path = os.path.join(data_path, "report_template.md")
    processing_results_path = os.path.join(data_path, "processing_results")
    plots_output_path = os.path.join(data_path, "plots")

    #Read Report Template
    try:
        with open(report_template_path, 'r', encoding='utf-8') as file:
            report_template = file.read()
    except FileNotFoundError:
        print(f"Error: The file '{report_template_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    #Dictionary with values to insert into the markdown string
    format_dictionary = {}
    format_dictionary.update(processing_paths)

    summaries = compile_summaries(data_path=processing_results_path)

    general_statistics = get_general_statistics(summaries=summaries)

    format_dictionary.update(general_statistics)

    tables_dict, rows_dict, domains_no_affected_documents = create_tables(summaries=summaries)

    format_dictionary.update(tables_dict)

    format_dictionary['number_domains_no_affected_documents'] = domains_no_affected_documents

    plots_path_dict, plots_data = create_plots(rows_dict, plots_output_path)

    for key, value in plots_path_dict.items():
        plots_path_dict[key] = os.path.relpath(value, output_path)

    format_dictionary.update(plots_path_dict)
    format_dictionary.update(plots_data)

    #Add the plots_path_dict to the format dictionary

    #Format template
    report = report_template.format(**format_dictionary)

    output_filename = os.path.join(output_path, filename)

    try:
        with open(output_filename, "w", encoding="utf-8") as md_file:
            md_file.write(report)
        print(f"Successfully wrote content to {output_filename}")
    except IOError as e:
        print(f"Error writing to file: {e}")
