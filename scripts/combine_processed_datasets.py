#!/usr/bin/env python3
import csv
from pathlib import Path


DATASETS = [
    ("AGP", Path("processed/AGP")),
    ("GGMP", Path("processed/GGMP")),
]


def read_header(path):
    with path.open(newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        return next(reader)


def read_ids(path):
    ids = []
    with path.open(newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        next(reader)
        for row in reader:
            if row:
                ids.append(row[0])
    return ids


def build_labeled_otu_columns():
    labeled_cols = []
    dataset_positions = {}

    for dataset_name, dataset_dir in DATASETS:
        header = read_header(dataset_dir / "otu.tsv")[1:]
        positions = []
        for source_idx, col in enumerate(header, start=1):
            output_idx = len(labeled_cols)
            labeled_cols.append((dataset_name, col, f"{dataset_name}__{col}"))
            positions.append((output_idx, source_idx))
        dataset_positions[dataset_name] = positions

    return labeled_cols, dataset_positions


def combine_meta(output_path):
    base_header = None
    total_rows = 0

    with output_path.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t")

        for dataset_name, dataset_dir in DATASETS:
            meta_path = dataset_dir / "meta.tsv"
            otu_path = dataset_dir / "otu.tsv"
            otu_ids = set(read_ids(otu_path))

            with meta_path.open(newline="") as meta_handle:
                reader = csv.reader(meta_handle, delimiter="\t")
                header = next(reader)
                if base_header is None:
                    base_header = header + ["dataset"]
                    writer.writerow(base_header)

                for row in reader:
                    if not row:
                        continue
                    sample_id = row[0]
                    if sample_id in otu_ids:
                        writer.writerow(row + [dataset_name])
                        total_rows += 1

    return total_rows


def combine_otu(output_path, labeled_cols, dataset_positions):
    total_rows = 0

    with output_path.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["id"] + [label for _, _, label in labeled_cols])

        for dataset_name, dataset_dir in DATASETS:
            meta_ids = set(read_ids(dataset_dir / "meta.tsv"))
            otu_path = dataset_dir / "otu.tsv"
            positions = dataset_positions[dataset_name]

            with otu_path.open(newline="") as otu_handle:
                reader = csv.reader(otu_handle, delimiter="\t")
                next(reader)
                for row in reader:
                    if not row:
                        continue
                    sample_id = row[0]
                    if sample_id not in meta_ids:
                        continue

                    combined_values = ["0"] * len(labeled_cols)
                    for output_idx, source_idx in positions:
                        combined_values[output_idx] = row[source_idx]
                    writer.writerow([sample_id] + combined_values)
                    total_rows += 1

    return total_rows


def main():
    output_dir = Path("processed/AGP_GGMP")
    output_dir.mkdir(parents=True, exist_ok=True)

    labeled_cols, dataset_positions = build_labeled_otu_columns()
    meta_rows = combine_meta(output_dir / "meta.tsv")
    otu_rows = combine_otu(output_dir / "otu.tsv", labeled_cols, dataset_positions)

    print(f"Created {output_dir}")
    print(f"Combined samples: {meta_rows}")
    print(f"Combined OTU features: {len(labeled_cols)}")
    print(f"Meta rows written: {meta_rows}")
    print(f"OTU rows written: {otu_rows}")


if __name__ == "__main__":
    main()
