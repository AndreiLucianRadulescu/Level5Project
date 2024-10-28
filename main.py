from input_parser import LPParser
from tableau import Tableau

lp_parser = LPParser()
# print(lp_parser)
lp_parser.parse_file("./problems/sample.lp")
# print(lp_parser)
tableau = Tableau(lp_parser=lp_parser)
print(tableau)