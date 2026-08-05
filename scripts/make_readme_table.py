import csv
import sys

def bool_icon(val):
    return "✅" if str(val).strip() == "True" else "❌"

def status_icon(val):
    v = str(val).strip().lower()
    if v == "success":
        return "✅ success"
    elif v == "incomplete":
        return "⚠️ incomplete"
    elif v == "failed":
        return "❌ failed"
    return val

def make_table(csv_path, out_path, only_flagged=False):
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    lines = []
    lines.append("| Formula | Expected | Successful | Count Complete | Heatmap Generated | Status |")
    lines.append("|---|---|---|---|---|---|")

    n_total = len(rows)
    n_complete = sum(1 for r in rows if r["calculation_count_complete"] == "True")
    n_incomplete = n_total - n_complete

    for r in rows:
        if only_flagged and r["calculation_count_complete"] == "True":
            continue
        lines.append(
            f"| {r['formula']} | {r['expected_calculations']} | {r['successful_calculations']} | "
            f"{bool_icon(r['calculation_count_complete'])} | {bool_icon(r['heatmap_generated'])} | "
            f"{status_icon(r['status'])} |"
        )

    summary = (
        f"**Summary:** {n_complete}/{n_total} materials fully converged "
        f"({n_incomplete} incomplete)\n\n"
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
    only_flagged = "--flagged-only" in sys.argv
    make_table(csv_path, out_path, only_flagged)
