class A:
    def dada_di_gaddi(self):
        print("Dada di gaddi")
class B(A):
    def abba_di_gaddi(self):
        print("Abba di gaddi")
class C(B):
    def Personal_gaddi(self):
        print("Personal_gaddi")
b = C()
b.dada_di_gaddi()
b.abba_di_gaddi()
b.Personal_gaddi()
class D:
    def Abba_ji(self):
        print("Abba_ji from D")
class E:
    def me(self):
        print("me from D")
e=E()
e.me()
d=D()