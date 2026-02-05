from random import randint
import numpy as np
import secrets as sec
from QRNG import Random
from math import log2
import matplotlib.pyplot as plt
import requests
import json

MAX_INT=10;
AMT=100000;

ENT_UNIFORM_DISTRIBUTION = log2(MAX_INT);

def calc_entropy(ar, mode=False):
    if not mode:
        ln = len(ar);
        probs = {};

        for c in ar:
            probs[c] = probs.get(c, 0) + 1;

        arp = list(probs.values());
        arp = [c/ln for c in arp];

        return -np.sum([p*log2(p) for p in arp]);
    else:
        ln = np.sum(ar);
        arp = [c/ln for c in ar];
        return -np.sum([p*log2(p) for p in arp]);


# Prepare
nmp_rdm = np.random.default_rng();
qrng_rdm = Random(MAX_INT);


# Collect the data from all four sources
# Sorting because why not
data_random = [randint(0, MAX_INT) for i in range(AMT)];                            data_random.sort();
data_nmp = nmp_rdm.integers(low=0, high=MAX_INT+1, size=AMT).tolist();              data_nmp.sort();
data_secrets = [sec.randbelow(MAX_INT+1) for i in range(AMT)];                      data_secrets.sort();
data_qrng = [qrng_rdm.randint() for i in range(AMT)];                               data_qrng.sort();
data_real_qrng = [];

# install data from IBMres.txt
with open('IBMres.txt', 'r') as f:
    line = f.read();
    line = line.split("\n");
    for lin in line:
        lin = lin.split(" ");
        data_real_qrng += [int(lin[1])];

# calculating the entropy
ent_random = calc_entropy(data_random);
ent_nmp = calc_entropy(data_nmp);
ent_secrets = calc_entropy(data_secrets);
ent_qrng = calc_entropy(data_qrng);
ent_real_qrng = calc_entropy(data_real_qrng, True);

print("SHANNON ENTROPY\n==========================\n");
print(f"IDEAL ENTROPY={ENT_UNIFORM_DISTRIBUTION}\
        \nRANDOM={ent_random}\nNMP={ent_nmp}\nSECRETS={ent_secrets}\
        \nQRNG={ent_qrng}\nREAL QRNG={ent_real_qrng}");
