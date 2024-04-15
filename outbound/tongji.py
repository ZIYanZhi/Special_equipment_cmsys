import statistics

data = [54, 51, 55, 53, 53, 54, 52]
sample_std_dev = statistics.stdev(data)
mean = statistics.mean(data)
population_std_dev = statistics.pstdev(data)
zhi = sample_std_dev / mean

print("平均数:", mean)
print("样本标准偏差:", sample_std_dev)
print("值等于:", zhi*100)