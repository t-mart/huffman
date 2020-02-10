from pathlib import Path
import time

from huffman import Compression

def test_file(path: Path):
    with path.open('r') as f:
        text = f.read()

    start_compress = time.time()
    c = Compression.compress(text)
    compress_time = time.time() - start_compress

    start_decompress = time.time()
    decompressed = c.decompress()
    decompress_time = time.time() - start_decompress

    print(f"File: {path}")
    print(f"Compression is lossless?: {'✔️' if decompressed == text else '❌'}")
    print(f"Source size: {len(text)} bytes")
    print(f"Compressed size: {c.data_len/8} bytes")
    print(f"Compression ratio: {(len(text)*8)/(c.data_len):.2f}")
    print(f"Time to compress: {compress_time:.2f}s")
    print(f"Time to decompress: {decompress_time:.2f}s")
    print()

for test_file_path in Path('./tests').iterdir():
    test_file(test_file_path)
