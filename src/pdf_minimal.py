import zlib, struct

def build_pdf_mini() -> bytes:
    import struct

    def obj(n: int, body: bytes) -> bytes:
        return f"{n} 0 obj\n".encode() + body + b"\nendobj\n"

    header = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"

    stream = b"BT /F1 12 Tf 72 720 Td (PCG!) Tj ET"
    obj5 = obj(5, b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream")

    obj1 = obj(1, b"<< /Type /Catalog /Pages 2 0 R >>")
    obj2 = obj(2, b"<< /Type /Pages /Count 1 /Kids [3 0 R] >>")
    obj3 = obj(3, b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
                   b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>")
    obj4 = obj(4, b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    objs = [obj1, obj2, obj3, obj4, obj5]

    body = header
    offsets = []
    for o in objs:
        offsets.append(len(body))
        body += o

    xref_start = len(body)
    xref = [b"xref\n0 6\n", b"0000000000 65535 f \n"]
    for off in offsets:
        xref.append(f"{off:010d} 00000 n \n".encode())
    xref_bytes = b"".join(xref)

    trailer = (b"trailer\n<< /Size 6 /Root 1 0 R >>\n"
               b"startxref\n" + str(xref_start).encode() + b"\n%%EOF\n")

    return body + xref_bytes + trailer