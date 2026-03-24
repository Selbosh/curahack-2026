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


def build_union_otu_columns():
    union_cols = []
    seen = set()
    for _, dataset_dir in DATASETS:
        header = read_header(dataset_dir / "otu.tsv")[1:]
        for col in header:
            if col not in seen:
                seen.add(col)
                union_cols.append(col)
    return union_cols


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


def combine_otu(output_path, union_cols):
    total_rows = 0

    with output_path.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["id"] + union_cols)

        for _, dataset_dir in DATASETS:
            meta_ids = set(read_ids(dataset_dir / "meta.tsv"))
            otu_path = dataset_dir / "otu.tsv"

            source_header = read_header(otu_path)
            source_col_to_idx = {col: idx for idx, col in enumerate(source_header[1:], start=1)}
            reorder_indices = [source_col_to_idx.get(col) for col in union_cols]

            with otu_path.open(newline="") as otu_handle:
                reader = csv.reader(otu_handle, delimiter="\t")
                next(reader)
                for row in reader:
                    if not row:
                        continue
                    sample_id = row[0]
                    if sample_id not in meta_ids:
                        continue

                    combined_row = [sample_id]
                    for idx in reorder_indices:
                        combined_row.append(row[idx] if idx is not None else "0")
                    writer.writerow(combined_row)
                    total_rows += 1

    return total_rows


def main():
    output_dir = Path("processed/AGP_GGMP")
    output_dir.mkdir(parents=True, exist_ok=True)

    union_cols = build_union_otu_columns()
    meta_rows = combine_meta(output_dir / "meta.tsv")
    otu_rows = combine_otu(output_dir / "otu.tsv", union_cols)

    print(f"Created {output_dir}")
    print(f"Combined samples: {meta_rows}")
    print(f"Combined OTU features: {len(union_cols)}")
    print(f"Meta rows written: {meta_rows}")
    print(f"OTU rows written: {otu_rows}")


if __name__ == "__main__":
    main()
