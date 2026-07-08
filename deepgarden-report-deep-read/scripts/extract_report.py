#!/usr/bin/env python3
"""DeepGarden 公司研报精读 — PDF 文本抽取（带 [Pxx] 页码标记）。

用法:
    python extract_report.py --src "<研报.pdf>" --out "<工作目录/_extract>"

说明:
    - 每页文本前加 [Pxx]，便于下游用 Grep 定位 + Read 局部读取，避免大文本灌入上下文。
    - 依赖 pdfplumber；缺失时尝试自动 pip install。
"""
import sys
import os
import subprocess
import argparse


def ensure_pdfplumber():
    try:
        import pdfplumber  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pdfplumber"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="研报 PDF 路径")
    ap.add_argument("--out", required=True, help="输出目录")
    args = ap.parse_args()

    ensure_pdfplumber()
    import pdfplumber

    os.makedirs(args.out, exist_ok=True)
    base = os.path.splitext(os.path.basename(args.src))[0]
    out_txt = os.path.join(args.out, base + ".txt")

    total_chars = 0
    pages = 0
    with open(out_txt, "w", encoding="utf-8") as fout, pdfplumber.open(args.src) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            txt = page.extract_text() or ""
            txt = txt.rstrip()
            if txt:
                fout.write(f"\n[P{i}]\n")
                fout.write(txt + "\n")
                total_chars += len(txt)
                pages += 1

    print(f"pages_with_text={pages} total_chars={total_chars} out={out_txt}")


if __name__ == "__main__":
    main()
