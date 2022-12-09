from scanner import Scanner
from utils import read_file

if __name__ == '__main__':
        sc = Scanner(read_file())
        sc.tokenizer()
