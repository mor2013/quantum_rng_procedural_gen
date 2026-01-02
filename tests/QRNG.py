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

        qreg = QuantumRegister(nb+2, 'q');  # two more qbits for flag control
        creg = ClassicalRegister(nb, 'c');  
        self.circ = QuantumCircuit(qreg, creg);

        # flip cib to |1>
        self.circ.x(qreg[nb+1]);
        
        # count probability for the first bit to be 1
        prob = (maxrange & ((1 << (nb-1))-1))+1;
        prob = prob/(prob+2**(nb-1));
        state = [sqrt(1-prob), sqrt(prob)];

        self.circ.initialize(state, 0);

        self.circ.x(qreg[0]);
        self.circ.ccx(qreg[0], qreg[nb+1], qreg[nb]);
        self.circ.cx(qreg[nb], qreg[nb+1]);
        self.circ.x(qreg[0]);

        for i in range(1, nb):
            if self.b_maxrange[i] == '1':
                self.circ.h(qreg[i]);

                self.circ.x(qreg[i]);
                self.circ.ccx(qreg[i], qreg[nb+1], qreg[nb]);
                self.circ.cx(qreg[nb], qreg[nb+1]);
                self.circ.x(qreg[i]);
        
            else:
                self.circ.ch(qreg[nb], qreg[i]);


    
        self.circ.measure(qreg[:nb], creg);
        #print(self.circ);
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
        return int(test[:self.len][::-1], 2);

    def _refill(self):
        if self.real_hardware:
            job = self.sampler.run([self._runcirc], shots=self.cachesize).result();
            print(job);
            self.cache = job[0].data.c.get_bitstrings();
        else:
            job = self.sim.run(self._runcirc, shots=self.cachesize, memory=True);
            self.cache = job.result().get_memory();

        



if __name__ == '__main__':
    """test = Random(13, True);

    rt = [test.randint() for i in range(500)];

    with open('IBMres.txt', 'w') as f:
        for n in rt:
            f.write(f'{n}\n');

    """
    test = Random(2, True);
print(test.randint());
