import csv
import sys
import os

MATERIALS_PENDING_REVIEW = {"Cs2", "Cu4"}

def bool_icon(val):
    return "✅" if str(val).strip() == "True" else "❌"

def status_icon(val, formula):
    if formula in MATERIALS_PENDING_REVIEW:
        return "⏸️ pending review (Martin)"
    v = str(val).strip().lower()
    if v == "success":
        return "✅ success"
    elif v == "incomplete":
        return "⚠️ incomplete"
    elif v == "failed":
        return "❌ failed"
    return val

def heatmap_link(formula, heatmap_dir, repo_relative_path):
    """Return a markdown link to the row-sorted heatmap SVG if it exists, else a dash."""
    svg_name = f"{formula}_volume_split_row_sorted.svg"
    svg_path = os.path.join(heatmap_dir, svg_name)
    if os.path.exists(svg_path):
        return f"[view]({repo_relative_path}/{svg_name})"
    return "—"

def make_table(csv_path, out_path, heatmap_dir, repo_relative_path, only_flagged=False):
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    lines = []
    lines.append("| Formula | Expected | Successful | Count Complete | Heatmap Generated | Status | Row-Sorted Heatmap |")
    lines.append("|---|---|---|---|---|---|---|")

    n_total = len(rows)
    n_complete = sum(1 for r in rows if r["calculation_count_complete"] == "True")
    n_incomplete = n_total - n_complete
    n_pending = sum(1 for r in rows if r["formula"] in MATERIALS_PENDING_REVIEW)
    n_row_sorted = n_complete - n_pending

    for r in rows:
        if only_flagged and r["calculation_count_complete"] == "True":
            continue
        formula = r["formula"]
        lines.append(
            f"| {formula} | {r['expected_calculations']} | {r['successful_calculations']} | "
            f"{bool_icon(r['calculation_count_complete'])} | {bool_icon(r['heatmap_generated'])} | "
            f"{status_icon(r['status'], formula)} | "
            f"{heatmap_link(formula, heatmap_dir, repo_relative_path)} |"
        )

    summary = (
        f"**Summary:** {n_complete}/{n_total} materials fully converged "
        f"({n_incomplete} incomplete)\n\n"
        f"**Row-sorted run (grid fix + volume split + row-similarity sort):** "
        f"{n_row_sorted}/{n_total} materials processed "
        f"({n_pending} pending review: {', '.join(sorted(MATERIALS_PENDING_REVIEW))}, "
        f"{n_incomplete} excluded as incomplete)\n\n"
    )

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(summary)
        f.write("\n".join(lines))
        f.write("\n")

    print(f"Wrote {len(lines)-2} rows to {out_path}")
    print(summary)

if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "results/full_run/all_materials_results.csv"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "results/full_run/RESULTS_TABLE.md"
    heatmap_dir = sys.argv[3] if len(sys.argv) > 3 else "results/full_run/heatmaps"
    repo_relative_path = sys.argv[4] if len(sys.argv) > 4 else "heatmaps"
    only_flagged = "--flagged-only" in sys.argv
    make_table(csv_path, out_path, heatmap_dir, repo_relative_path, only_flagged)
