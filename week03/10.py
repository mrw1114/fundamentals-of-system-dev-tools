import copy

a = [[1,2],[3,4]]
b = a.copy()
c = copy.deepcopy(a)
print('Before modified: a:', a, 'b:', b, 'c:', c)

a[0][0] = 99
print('After modified: a:', a, 'b:', b, 'c:', c)

c[0][0] = 99
d = 111
e = 111
f = 114510
g = 114519
f += 4
g -= 5

print('Now : c = ', c, 'd =', d, 'e =', e, 'f =', f, 'g =', g)
print('a is b :', a is b, '| a == b', a == b)
print('a is c :', a is c, '| a == c', a == c)
print('d is e :', d is e, '| d == e', d == e)
print('f is g :', f is g, '| f == g', f == g)
