from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
import io, pathlib, traceback, json

def validate_main(args: bytes):
    if args.file and args.file.endswith(".pickle.gz"):
        content = pathlib.Path(args.file).read_bytes()
        try:
            result = analysis_gzipdf(content)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        except:
            print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.file and args.file.endswith(".pdf"):
        pass

def analysis_gzipdf(content: bytes) -> str:
    try:
        parser = PDFParser(io.BytesIO(content))
        doc = PDFDocument(parser)
        return {
            "result": True,
            "msg": "Parsed as PDF (pdfminer)",
        }
    except Exception as e:
        ValueError(e)
        info = {
            "result": False,
            "error_type": e.__class__.__name__,
            "error_msg": str(e),
            "traceback": traceback.format_exc(),
        }

        return info