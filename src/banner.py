
__prog__ = "pcg"
__version__ = "0.1.0#dev"
__author__ = "By L1nq"
BANNER = f"""
          ___
 |  _ \ / ___/ ___|   {{{__version__}}}
 | |_) | |  | |  _ 
 |  __/| |__| |_| |   Pdfminer-CMap-Generator (pcg)
 |_|    \____\____|   {__author__}

Usage: python3 pcg.py [options] --help
       python3 pcg.py build -t gzip -p "echo 111 >> uploads/1.txt"
       python3 pcg.py build -t pdf -ep "/proc/self/cwd/uploads/l1"
"""

def banner():
    return BANNER