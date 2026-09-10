from merge_sort import merge_sort

# 测试1
def test1():
    input_data = [1, 1, 4, 5, 1, 4]
    result = merge_sort(input_data)
    # 断言期望输出
    assert result == [1, 1, 1, 4, 4, 5]

# 测试2
def test2():
    input_data = [1, 9, 1, 9, 8, 1, 0]
    result = merge_sort(input_data)
    assert result == [0, 1, 1, 1, 8, 9, 9]
