from input_parser import LPParser

lp_parser = LPParser()
print(lp_parser)
lp_parser.parse_file("./problems/sample.lp")
print(lp_parser)
