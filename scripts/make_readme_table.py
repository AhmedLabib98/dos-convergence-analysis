import csv
import sys
import os

MATERIALS_PENDING_REVIEW = {"Cs2", "Cu4"}

VOLUME_SUBFOLDER = {
    "1": "1_volume",
    "2": "2_volumes",
    "3": "3_volumes",
}

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

def load_volume_counts(volume_counts_path):
    counts = {}
    with open(volume_counts_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            counts[row["formula"]] = row["n_volume_groups"]
    return counts

def heatmap_link(formula, n_groups, heatmap_dir, repo_relative_path):
    if n_groups not in VOLUME_SUBFOLDER:
        return "—"
    subfolder = VOLUME_SUBFOLDER[n_groups]
    svg_name = f"{formula}_volume_split_row_sorted.svg"
    svg_path = os.path.join(heatmap_dir, subfolder, svg_name)
    if os.path.exists(svg_path):
        return f"[view]({repo_relative_path}/{subfolder}/{svg_name})"
    return "—"

def make_section(rows, heading, heatmap_dir, repo_relative_path, volume_counts):
    lines = [f"## {heading}\n"]
    lines.append("| Formula | Expected | Successful | Count Complete | Heatmap Generated | Status | Row-Sorted Heatmap |")
    lines.append("|---|---|---|---|---|---|---|")
    for r in rows:
        formula = r["formula"]
        n_groups = volume_counts.get(formula, "")
        lines.append(
            f"| {formula} | {r['expected_calculations']} | {r['successful_calculations']} | "
            f"{bool_icon(r['calculation_count_complete'])} | {bool_icon(r['heatmap_generated'])} | "
            f"{status_icon(r['status'], formula)} | "
            f"{heatmap_link(formula, n_groups, heatmap_dir, repo_relative_path)} |"
        )
    lines.append("")
    return lines

def make_table(csv_path, out_path, heatmap_dir, repo_relative_path, volume_counts_path, only_flagged=False):
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    volume_counts = load_volume_counts(volume_counts_path)

    n_total = len(rows)
    n_complete = sum(1 for r in rows if r["calculation_count_complete"] == "True")
    n_incomplete = n_total - n_complete
    n_pending = sum(1 for r in rows if r["formula"] in MATERIALS_PENDING_REVIEW)
    n_row_sorted = n_complete - n_pending

    n_1vol = sum(1 for v in volume_counts.values() if v == "1")
    n_2vol = sum(1 for v in volume_counts.values() if v == "2")
    n_3vol = sum(1 for v in volume_counts.values() if v == "3")

    summary = (
        f"**Summary:** {n_complete}/{n_total} materials fully converged "
        f"({n_incomplete} incomplete)\n\n"
        f"**Row-sorted run (grid fix + volume split + row-similarity sort):** "
        f"{n_row_sorted}/{n_total} materials processed "
        f"({n_pending} pending review: {', '.join(sorted(MATERIALS_PENDING_REVIEW))}, "
        f"{n_incomplete} excluded as incomplete)\n\n"
        f"**Breakdown by volume-group count:** "
        f"{n_1vol} single-volume, {n_2vol} two-volume, {n_3vol} three-volume\n\n"
    )

    if only_flagged:
        flagged_rows = [r for r in rows if r["calculation_count_complete"] != "True"]
        lines = make_section(flagged_rows, "Incomplete Materials", heatmap_dir, repo_relative_path, volume_counts)
    else:
        rows_1vol = [r for r in rows if volume_counts.get(r["formula"]) == "1"]
        rows_2vol = [r for r in rows if volume_counts.get(r["formula"]) == "2"]
        rows_3vol = [r for r in rows if volume_counts.get(r["formula"]) == "3"]
        rows_other = [r for r in rows if r["formula"] not in volume_counts]

        lines = []
        lines += make_section(rows_1vol, f"Single-Volume Materials ({n_1vol})", heatmap_dir, repo_relative_path, volume_counts)
        lines += make_section(rows_2vol, f"Two-Volume Materials ({n_2vol})", heatmap_dir, repo_relative_path, volume_counts)
        lines += make_section(rows_3vol, f"Three-Volume Materials ({n_3vol})", heatmap_dir, repo_relative_path, volume_counts)
        if rows_other:
            lines += make_section(rows_other, "Excluded (Incomplete / Pending Review)", heatmap_dir, repo_relative_path, volume_counts)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(summary)
        f.write("\n".join(lines))
        f.write("\n")

    total_rows_written = sum(1 for l in lines if l.startswith("|") and not l.startswith("|---"))
    print(f"Wrote {total_rows_written} rows to {out_path}")
    print(summary)

if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "results/full_run/all_materials_results.csv"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "results/full_run/RESULTS_TABLE.md"
    heatmap_dir = sys.argv[3] if len(sys.argv) > 3 else "results/full_run/heatmaps"
    repo_relative_path = sys.argv[4] if len(sys.argv) > 4 else "heatmaps"
    volume_counts_path = sys.argv[5] if len(sys.argv) > 5 else "results/full_run/volume_group_counts.csv"
    only_flagged = "--flagged-only" in sys.argv
    make_table(csv_path, out_path, heatmap_dir, repo_relative_path, volume_counts_path, only_flagged)
