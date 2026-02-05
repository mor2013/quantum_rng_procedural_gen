from random import randint
import numpy as np
import secrets as sec
from QRNG import Random
import matplotlib.pyplot as plt
import requests
import json


MAX_INT=10;
AMT=50000;

# Prepare
nmp_rdm = np.random.default_rng();
qrng_rdm = Random(MAX_INT);


# Collect the data from all four sources
# Sorting because why not
data_random = [randint(0, MAX_INT) for i in range(AMT)];                            data_random.sort();
data_nmp = nmp_rdm.integers(low=0, high=MAX_INT+1, size=AMT).tolist();              data_nmp.sort();
data_secrets = [sec.randbelow(MAX_INT+1) for i in range(AMT)];                      data_secrets.sort();
data_qrng = [qrng_rdm.randint() for i in range(AMT)];                               data_qrng.sort();

dict_real_qrng = {};

# install data from IBMres.txt
with open('IBMres.txt', 'r') as f:
    line = f.read();
    line = line.split("\n");
    for lin in line:
        lin = lin.split(" ");
        dict_real_qrng[int(lin[0],2)] = int(lin[1]);

# request data from outshift API endpoint

url = "https://api.qrng.outshift.com/api/v1/random_numbers";

headers = {
    "Content-Type": "application/json",
    "x-id-api-key": "nY,NCr]!bL8pW]207(oU(r12[S<84D0:]}h)7j13T>:0fYLktGqx01+RfWLkE7[j"
}

data = {
    "encoding": "raw",
    "format": "all",
    "bits_per_block": 4,
    "number_of_blocks": 1000
}

"""for i in range(5):
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        #print("Random numbers generated successfully:")
        #print(json.dumps(result, indent=2))
        
        data_outshift_qrng += [int(n["binary"], 2) for n in result["random_numbers"]];
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

data_outshift_qrng.sort();"""


"""
print(f'REAL={data_real_qrng}');
print(f'RANDOM={data_random}');
print(f'NUMPY={data_nmp}');
print(f'SECRETS={data_secrets}');
print(f'QRNG={data_qrng}');
print(f'OUTSHIFT={data_outshift_qrng}');
"""


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

# Visualising the data
plt.style.use('_mpl-gallery');

x = list(range(0, MAX_INT+1));
y_random = [dict_random.get(i, 0) for i in range(MAX_INT+1)];
y_nmp = [dict_nmp.get(i, 0) for i in range(MAX_INT+1)];
y_secrets = [dict_secrets.get(i, 0) for i in range(MAX_INT+1)];
y_qrng = [dict_qrng.get(i, 0) for i in range(MAX_INT+1)];
y_real_qrng = [dict_real_qrng.get(i, 0) for i in range(MAX_INT+1)];
print(y_real_qrng);

# plot
fig, axs = plt.subplots();

axs.grid(color='#dfe4ed');
axs.stem(x, y_random, linefmt='#abb5c4', markerfmt='D');
axs.stem([n-0.1 for n in x], y_secrets, linefmt='#abb5c4', markerfmt='D');
axs.stem([n-0.2 for n in x], y_nmp, linefmt='#abb5c4', markerfmt='D');
axs.stem([n+0.1 for n in x], y_qrng, linefmt='#bd5420', markerfmt='D');
axs.stem([n+0.3 for n in x], y_real_qrng, linefmt='red', markerfmt='D');
#axs.stem([n+0.2 for n in x], y_outshift_qrng, linefmt='blue', markerfmt='D');
#axs[1].stem(x, y_nmp, linefmt='red', markerfmt='D');

axs.set(xlim=(0, 8), xticks=np.arange(-1, MAX_INT+2),
    ylim=(0, 8), yticks=np.arange(0, 3400))

axs.tick_params(axis='y', which='both', left=False, labelleft=False);
plt.tight_layout();
plt.show()