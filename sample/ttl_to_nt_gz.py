#!/usr/bin/env python3
"""
Convert all *.ttl files in the current directory (or a given directory)
into a single gzipped N-Triples file (*.nt.gz).

Requires: pip install rdflib

Usage:
    python ttl_to_nt_gz.py                      # -> merged.nt.gz
    python ttl_to_nt_gz.py -o output.nt.gz      # custom output name
    python ttl_to_nt_gz.py -d /path/to/dir      # custom input directory
"""

import argparse
import glob
import gzip
import os
import sys

from rdflib import Graph


def main():
    parser = argparse.ArgumentParser(description="Merge *.ttl files into one *.nt.gz")
    parser.add_argument("-d", "--directory", default=".", help="Directory with .ttl files (default: current)")
    parser.add_argument("-o", "--output", default="merged.nt.gz", help="Output file (default: merged.nt.gz)")
    args = parser.parse_args()

    ttl_files = sorted(glob.glob(os.path.join(args.directory, "*.ttl")))
    if not ttl_files:
        print(f"No .ttl files found in {os.path.abspath(args.directory)}", file=sys.stderr)
        sys.exit(1)

    total = 0
    # Parse and write file by file so memory stays bounded to one file at a time.
    # Note: blank node IDs are made unique per file by rdflib, so merging is safe.
    with gzip.open(args.output, "wb") as out:
        for path in ttl_files:
            print(f"Processing {path} ...", end=" ", flush=True)
            g = Graph()
            try:
                g.parse(path, format="turtle")
            except Exception as e:
                print(f"FAILED ({e})", file=sys.stderr)
                continue
            data = g.serialize(format="nt")
            if isinstance(data, str):
                data = data.encode("utf-8")
            out.write(data)
            if data and not data.endswith(b"\n"):
                out.write(b"\n")
            total += len(g)
            print(f"{len(g)} triples")

    print(f"\nDone: {total} triples from {len(ttl_files)} file(s) -> {args.output}")


if __name__ == "__main__":
    main()
