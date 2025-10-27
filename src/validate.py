from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
import io, pathlib, traceback, json

def validate_main(args: bytes):
    if not args.file:
        print("[!] Error: No file specified")
        return 1

    if not pathlib.Path(args.file).exists():
        print(f"[!] Error: File not found: {args.file}")
        return 1

    if args.file.endswith(".pickle.gz"):
        content = pathlib.Path(args.file).read_bytes()
        result = analysis_gzipdf(content)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result.get("result") else 1
    elif args.file.endswith(".pdf"):
        content = pathlib.Path(args.file).read_bytes()
        result = analysis_pdf(content)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result.get("result") else 1
    else:
        print(f"[!] Error: Unsupported file type: {args.file}")
        print("[*] Supported types: .pickle.gz, .pdf")
        return 1

def analysis_gzipdf(content: bytes) -> dict:
    try:
        parser = PDFParser(io.BytesIO(content))
        doc = PDFDocument(parser)
        return {
            "result": True,
            "msg": "Parsed as PDF - polyglot GZIP/PDF valid",
        }
    except Exception as e:
        return {
            "result": False,
            "error_type": e.__class__.__name__,
            "error_msg": str(e),
            "traceback": traceback.format_exc(),
        }

def analysis_pdf(content: bytes) -> dict:
    try:
        parser = PDFParser(io.BytesIO(content))
        doc = PDFDocument(parser)
        return {
            "result": True,
            "msg": "Valid PDF file",
        }
    except Exception as e:
        return {
            "result": False,
            "error_type": e.__class__.__name__,
            "error_msg": str(e),
            "traceback": traceback.format_exc(),
        }