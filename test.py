import json

class A:
    def __init__(self, a, b):
        self.a = a
        self.b = b

sample_A = A(1, 'Alireza')

print(json.dumps(sample_A.__dict__))