from random import randint
import numpy as np
import secrets as sec
from QRNG import Random
import matplotlib.pyplot as plt


MAX_INT=13;
AMT=500;

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
    while line:
        data_real_qrng += [int(n) for n in line.split('\n') if n != ''];
        line = f.read();

data_real_qrng.sort();


"""print(f'REAL={data_real_qrng}');
print(f'RANDOM={data_random}');
print(f'NUMPY={data_nmp}');
print(f'SECRETS={data_secrets}');
print(f'QRNG={data_qrng}');"""

# Analyze the data
dict_random = {};
for n in data_random:
    dict_random[n] = dict_random.get(n, 0) + 1;
dict_nmp = {};
for n in data_nmp:
    dict_nmp[n] = dict_nmp.get(n, 0) + 1;
dict_secrets = {};
for n in data_secrets:
    dict_secrets[n] = dict_secrets.get(n, 0) + 1;
dict_qrng = {};
for n in data_qrng:
    dict_qrng[n] = dict_qrng.get(n, 0) + 1;
dict_real_qrng = {};
for n in data_qrng:
    dict_real_qrng[n] = dict_real_qrng.get(n, 0) + 1;

"""print(f'RANDOM={dict_random}');
print(f'NUMPY={dict_nmp}');
print(f'SECRETS={dict_secrets}');
print(f'QRNG={dict_qrng}');
"""

# Visualising the data
plt.style.use('_mpl-gallery');

x = list(range(0, MAX_INT+1));
y_random = [dict_random.get(i, 0) for i in range(MAX_INT+1)];
y_nmp = [dict_nmp.get(i, 0) for i in range(MAX_INT+1)];
y_secrets = [dict_secrets.get(i, 0) for i in range(MAX_INT+1)];
y_qrng = [dict_qrng.get(i, 0) for i in range(MAX_INT+1)];
y_real_qrng = [dict_real_qrng.get(i, 0) for i in range(MAX_INT+1)];

# plot
fig, axs = plt.subplots();

axs.grid(color='#dfe4ed');
axs.stem(x, y_random, linefmt='#abb5c4', markerfmt='D');
axs.stem([n-0.1 for n in x], y_secrets, linefmt='#abb5c4', markerfmt='D');
axs.stem([n-0.2 for n in x], y_nmp, linefmt='#abb5c4', markerfmt='D');
axs.stem([n+0.1 for n in x], y_qrng, linefmt='#bd5420', markerfmt='D');
axs.stem([n+0.2 for n in x], y_real_qrng, linefmt='red', markerfmt='D');
#axs[1].stem(x, y_nmp, linefmt='red', markerfmt='D');

axs.set(xlim=(0, 8), xticks=np.arange(-1, MAX_INT+2),
    ylim=(0, 8), yticks=np.arange(0, 0.20*AMT))

plt.tight_layout();
plt.show()