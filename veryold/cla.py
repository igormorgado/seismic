class A(object):
    def go(self):
        print("go A go!")

class B(A):
    def go(self):
        super(B, self).go()
        print("go B go!")

class C(A):
    def go(self):
        super(C, self).go()
        print("go C go!")

class D(B,C):
    def go(self):
        super(D, self).go()
        print("go D go!")

class E(B,C): pass

a = A()
b = B()
c = C()
d = D()
e = E()

# specify output from here onwards

#a.go()
#b.go()
#c.go()
d.go()
#e.go()

