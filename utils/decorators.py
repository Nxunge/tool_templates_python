def skip(func):
    """标记函数跳过执行"""
    func.skip = True
    return func