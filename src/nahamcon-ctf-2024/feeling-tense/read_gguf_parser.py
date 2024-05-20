from gguf_parser import GGUFParser

parser = GGUFParser("/Users/konstantinp/Downloads/codellama-7b-python.Q4_K_M.gguf")
parser.parse()
parser.print()