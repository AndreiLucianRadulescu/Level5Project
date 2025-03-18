from dense_lp_generator import DenseLPGenerator

dense_lp_generator = DenseLPGenerator(precision = 4, allow_negative_rhs=False)
dense_lp_generator.generate_dense_lp('large_test.lp', 3000, 3000)