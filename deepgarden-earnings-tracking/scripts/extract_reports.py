#!/usr/bin/env python3
"""Extract periodic-report PDFs to page-marked text + build a light cross-year summary.

Usage:
    python extract_reports.py --src "<dir with PDFs>" --out "<extract dir>"

Outputs (in --out):
    <report name>.txt          full text, each page prefixed with [Pxx]
    跨年财务摘要.txt            compact multi-year 主要会计数据 pulled from annual reports
"""
import os
import re
import argparse


def extract_pdfs(src, out):
    os.makedirs(out, exist_ok=True)
    files = sorted(f for f in os.listdir(src) if f.lower().endswith(".pdf"))
    if not files:
        print("No PDFs found in", src)
        return []
    results = []
    for f in files:
        path = os.path.join(src, f)
        base = re.sub(r"\.pdf$", "", f)
        txt_path = os.path.join(out, base + ".txt")
        pages = 0
        chars = 0
        with open(txt_path, "w", encoding="utf-8") as w:
            try:
                import pdfplumber
            except ImportError:
                import subprocess, sys
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "pdfplumber"])
                import pdfplumber
            with pdfplumber.open(path) as pdf:
                pages = len(pdf.pages)
                for i, pg in enumerate(pdf.pages, 1):
                    t = pg.extract_text() or ""
                    w.write(f"\n[P{i}]\n")
                    w.write(t)
                    w.write("\n")
                    chars += len(t)
        results.append((f, pages, chars, os.path.getsize(txt_path)))
        print(f"{f}: pages={pages} chars={chars} txt={os.path.getsize(txt_path)}B")
    return results


def grab_section(txt, *markers, after=90):
    lines = txt.splitlines()
    out = []
    for m in markers:
        for i, ln in enumerate(lines):
            if m in ln:
                out.append(f"--- 命中「{m}」(@line {i+1}) ---")
                out.extend(lines[i:i + after])
                out.append("")
                break
    return "\n".join(out)


def build_cross_year(out, annual_names):
    blocks = []
    for name in annual_names:
        p = os.path.join(out, name + ".txt")
        if not os.path.exists(p):
            continue
        txt = open(p, encoding="utf-8").read()
        blocks.append(f"\n########## {name} ##########")
        blocks.append(grab_section(txt, "主要会计数据", "主要财务指标",
                                    "公司主要会计数据和财务指标"))
        bal = []
        for ln in txt.splitlines():
            if re.search(r"(流动资产合计|非流动资产合计|资产总计|流动负债合计|"
                         r"负债合计|归属于母公司所有者权益合计|所有者权益合计)", ln):
                bal.append(ln.strip())
        blocks.append("--- 资产负债表关键行 ---")
        blocks.append("\n".join(bal[:40]))
    path = os.path.join(out, "跨年财务摘要.txt")
    open(path, "w", encoding="utf-8").write("\n".join(blocks))
    print("跨年摘要:", os.path.getsize(path), "B")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="directory containing report PDFs")
    ap.add_argument("--out", required=True, help="output directory for extracted text")
    args = ap.parse_args()

    results = extract_pdfs(args.src, args.out)
    # annual reports: filenames containing 年年度; used for cross-year summary
    annual = [re.sub(r"\.pdf$", "", f) for f, *_ in results
              if "年年度" in f or "年度报告" in f]
    if annual:
        build_cross_year(args.out, annual)


if __name__ == "__main__":
    main()
