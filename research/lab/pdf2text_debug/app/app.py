from flask import Flask, request, send_file, render_template
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
import os, io, traceback, logging, time, gzip, pickle, builtins

from pdfutils import pdf_to_text

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

LOGFILE  = os.path.join(app.config['UPLOAD_FOLDER'], "_trace.txt")
OPENLOG  = os.path.join(app.config['UPLOAD_FOLDER'], "_openlog.txt")
HEADBIN  = os.path.join(app.config['UPLOAD_FOLDER'], "_last_upload_head.bin")

def _append(path, msg):
    with open(path, "a", encoding="utf-8", errors="ignore") as f:
        f.write(msg)

_orig_open = builtins.open
def _spy_open(file, *args, **kwargs):
    try:
        path = file if isinstance(file, (str, bytes, os.PathLike)) else None
        if path:
            s = str(path)
            if s.endswith(".pickle.gz") or "/cmap/" in s or s.endswith(".pickle"):
                _append(OPENLOG, f"[open] {s} mode={kwargs.get('mode', args[0] if args else 'r')}\n")
                try:
                    with _orig_open(file, "rb") as rb:
                        head = rb.read(16)
                    _append(OPENLOG, f"  head={head!r}\n")
                except Exception as e:
                    _append(OPENLOG, f"  open(head) failed: {e}\n")
    except Exception:
        pass
    return _orig_open(file, *args, **kwargs)

builtins.open = _spy_open

_orig_gzip_open = gzip.open
def _spy_gzip_open(filename, *args, **kwargs):
    _append(OPENLOG, f"[gzip.open] {filename}\n")
    return _orig_gzip_open(filename, *args, **kwargs)
gzip.open = _spy_gzip_open

_orig_pickle_loads = pickle.loads
def _spy_pickle_loads(b, *args, **kwargs):
    _append(OPENLOG, f"[pickle.loads] len={len(b)} bytes\n")
    return _orig_pickle_loads(b, *args, **kwargs)
pickle.loads = _spy_pickle_loads

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        if 'file' not in request.files:
            return 'No file part', 400

        file = request.files['file']
        filename = file.filename or ''
        if filename == '':
            return 'No selected file', 400
        if '..' in filename or '/' in filename:
            return 'directory traversal is not allowed', 403

        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        pdf_content = file.stream.read()

        with open(HEADBIN, 'wb') as hb:
            hb.write(pdf_content[:64])

        try:
            parser = PDFParser(io.BytesIO(pdf_content))
            doc = PDFDocument(parser)
        except Exception as e:
            tb = traceback.format_exc()
            _append(LOGFILE, f"\n[{ts}] PDF check failed for {filename}:\n{tb}\n")
            return tb, 500

        with open(pdf_path, 'wb') as f:
            f.write(pdf_content)

        md_filename = os.path.splitext(filename)[0] + '.txt'
        txt_path = os.path.join(app.config['UPLOAD_FOLDER'], md_filename)

        try:
            pdf_to_text(pdf_path, txt_path)
        except Exception as e:
            tb = traceback.format_exc()
            _append(LOGFILE, f"\n[{ts}] pdf_to_text failed for {filename}:\n{tb}\n")
            return tb, 500

        return send_file(txt_path, as_attachment=True)

    except Exception:
        tb = traceback.format_exc()
        _append(LOGFILE, f"\n[{ts}] unhandled:\n{tb}\n")
        return tb, 500

@app.route('/_dbg/<name>')
def dbg(name):
    safe = {'trace': LOGFILE, 'openlog': OPENLOG, 'head': HEADBIN}
    if name not in safe:
        return "bad dbg name", 400
    return send_file(safe[name], as_attachment=True)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("pdfminer").setLevel(logging.DEBUG)
    app.run(host='0.0.0.0', port=5000)

