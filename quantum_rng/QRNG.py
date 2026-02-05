from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import Aer
from math import log2, ceil, sqrt
from random import randint
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2


class Random:
    def __init__(self, maxrange, real_hardware = False):
        self.maxrange = maxrange;
        self.b_maxrange = bin(maxrange)[2:];
        nb = len(self.b_maxrange);
        self.len = nb;
        self.cachesize = 1024;
        self.cache = [];
        self.real_hardware=real_hardware;

        qreg = QuantumRegister(nb, 'q'); 
        creg = ClassicalRegister(nb, 'c');  
        self.circ = QuantumCircuit(qreg, creg);

        if real_hardware and nb > 5: # choose what algorithm based on the maxrange
            self.circ.h(qreg);
        else:
            prob = sqrt(1/(maxrange+1));
            probs = [prob for i in range(0, maxrange+1)] + [0]*(2**nb-maxrange-1);

            self.circ.initialize(probs);
        
        self.circ.measure(qreg, creg);
        if real_hardware:
            service = QiskitRuntimeService();
            self.sim = service.least_busy(operational=True, simulator=False, min_num_qubits=nb+2);
            self._runcirc = transpile(self.circ, self.sim, optimization_level=2);
            self.sampler = SamplerV2(mode=self.sim);
        else:
            self.sim = Aer.get_backend("qasm_simulator");
            self._runcirc = transpile(self.circ, self.sim);

        
    def randint(self):

        if not self.cache:
            self._refill();
        
        test=self.cache.pop();
        #print(test);
        return int(test[:self.len], 2);

    def get_counts(self, amt=1024):
        if self.real_hardware:
            job = self.sampler.run([self._runcirc], shots=amt).result();
            return job[0].data.c.get_counts();
        else:
            job = self.sim.run(self._runcirc, shots=amt, memory=True);
            return job.result().get_counts();

    def _refill(self):
        if self.real_hardware:
            job = self.sampler.run([self._runcirc], shots=self.cachesize).result();
            print(job);
            self.cache = job[0].data.c.get_bitstrings();
        else:
            job = self.sim.run(self._runcirc, shots=self.cachesize, memory=True);
            self.cache = job.result().get_memory();

        



if __name__ == '__main__':
    flag = True;
    number = 10;
    amt = 50000;

    if flag:  # real hardware implementation
        test = Random(number, flag);
    
        rt = test.get_counts(amt);
        with open('IBMres.txt', 'w') as f:
            for k in rt.keys():
                f.write(f'{k} {rt[k]}\n');        
    else:
        test = Random(number, flag);
        rt = [test.randint() for i in range(amt)];
        print(rt);
