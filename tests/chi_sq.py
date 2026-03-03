from random import randint
import numpy as np
import secrets as sec
from QRNG import Random
from scipy.stats import chi2

MAX_INT=10;
AMT=100000;


# Prepare
nmp_rdm = np.random.default_rng();
qrng_rdm = Random(MAX_INT);

def calc_chisq(ar, mode=False):
    if not mode:
        ln = len(ar);
        probs = {};

        for c in ar:
            probs[c] = probs.get(c, 0) + 1;

        arp = list(probs.values());
        exp = ln/len(arp);

        return np.round(np.sum([((arp[i]-exp)**2)/exp for i in range(len(arp))]), 2);
    else:
        ln = np.sum(ar);
        exp = ln/len(ar);

        return np.round(np.sum([((i-exp)**2)/exp for i in ar]), 2);


# Collect the data from all four sources
# Sorting because why not
data_random = [randint(0, MAX_INT) for i in range(AMT)];
data_nmp = nmp_rdm.integers(low=0, high=MAX_INT+1, size=AMT).tolist();
data_secrets = [sec.randbelow(MAX_INT+1) for i in range(AMT)];
data_qrng = [qrng_rdm.randint() for i in range(AMT)];
data_real_qrng = [];

# install data from IBMres.txt
with open('IBMres.txt', 'r') as f:
    line = f.read();
    line = line.split("\n");
    for lin in line:
        lin = lin.split(" ");
        data_real_qrng += [int(lin[1])];
data_real_qrng = data_real_qrng[0:MAX_INT+1];

# calculating the entropy
chi_random = calc_chisq(data_random);
chi_nmp = calc_chisq(data_nmp);
chi_secrets = calc_chisq(data_secrets);
chi_qrng = calc_chisq(data_qrng);
chi_real_qrng = calc_chisq(data_real_qrng, True);


print("CHI SQUARED\n==========================\n");
print(f"{chi2.ppf(0.05, MAX_INT)}<IDEAL<{chi2.ppf(0.95, MAX_INT)}\
        \nRANDOM={chi_random}\nNMP={chi_nmp}\nSECRETS={chi_secrets}\
        \nQRNG={chi_qrng}\nREAL QRNG={chi_real_qrng}");
