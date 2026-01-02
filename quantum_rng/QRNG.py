from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import Aer
from math import log2, ceil, sqrt
from random import randint


class Random:
    def __init__(self, maxrange, real_hardware = False):
        self.maxrange = maxrange;
        self.b_maxrange = bin(maxrange)[2:];
        nb = len(self.b_maxrange);
        self.len = nb;
        self.cachesize = 512;
        self.cache = [];

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
        print(self.circ);
        self.sim = Aer.get_backend("qasm_simulator");
        self._runcirc = transpile(self.circ, self.sim);


        
    def randint(self, mx):
        if mx > self.maxrange:
            return -1;

        if not self.cache:
            self._refill();
        
        test=self.cache.pop();
        #print(test);
        return int(test[:self.len][::-1], 2);

    def _refill(self):
        job = self.sim.run(self._runcirc, shots=self.cachesize, memory=True)
        self.cache = job.result().get_memory();



if __name__ == '__main__':
    test = Random(104);

    q_rand = [];
    c_rand = [];
    for i in range(20):
        q_rand += [test.randint(3)];
        c_rand += [randint(0, 15)];

    print(c_rand);
    print(q_rand);
