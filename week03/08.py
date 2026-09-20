def make_counter():
    cnt = 0
    def inc():
        nonlocal cnt
        cnt+=1
        return cnt
    return inc

a = make_counter()
b = make_counter()
print('First use a:', a())
print('Second use a:', a())
print('First use b:', b())
