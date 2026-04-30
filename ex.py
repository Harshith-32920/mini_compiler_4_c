from optimizer import CodeOptimizer

code = [
    "t1 = 2 + 3",
    "t2 = t1 * 4",
    "t3 = t1 * 4",
    "t4 = t2",
    "x = t4"
]

opt = CodeOptimizer(code)
opt.optimize()
opt.print_code()