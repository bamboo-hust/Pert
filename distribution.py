from constant import *
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

class Distribution:
    def __init__(self, mu, sigma, sz=DISTRIBUTION_MAX_SIZE):
        self.mu = mu
        self.sigma = sigma
        self.pdf = np.zeros(sz)
        for i in range(sz):
            self.pdf[i] = self.eval(i)
        self.pdf /= np.sum(self.pdf)

    # use for initiation only
    def eval(self, x):
        return 1.0 / (self.sigma * np.sqrt(2.0 * np.pi)) * np.exp(-(x - self.mu)**2 / (2.0 * self.sigma**2))

    def add(self, other):
        pdf = np.convolve(self.pdf, other.pdf)
        mu = np.sum(pdf * np.arange(len(pdf)))
        sigma = np.sqrt(np.sum((pdf * (np.arange(len(pdf)) -mu) ** 2)))
        res = Distribution(mu, sigma, len(pdf))
        res.pdf = pdf
        return res

    def max(self, other):
        cdf1 = self.pdf.copy()
        cdf2 = other.pdf.copy()
        sz = max(len(cdf1), len(cdf2))
        cdf1.resize(sz)
        cdf2.resize(sz)
        for i in range(1, sz):
            cdf1[i] += cdf1[i - 1]
            cdf2[i] += cdf2[i - 1]
        pdf = cdf1 * cdf2
        for i in range(sz - 1, 0, -1):
            pdf[i] -= pdf[i - 1]
        
        mu = np.sum(pdf * np.arange(len(pdf)))
        sigma = np.sqrt(np.sum((pdf * (np.arange(len(pdf)) -mu) ** 2)))
        res = Distribution(mu, sigma, len(pdf))
        res.pdf = pdf
        return res

# a = Distribution(5, 10)
# b = Distribution(5, 10)
# c = Distribution.max(a, b)
# plt.plot(c.pdf, label = "c")
# plt.plot(a.pdf, label = "a")
# # plt.plot(b.pdf, label = "b")
# plt.legend()
# plt.show()