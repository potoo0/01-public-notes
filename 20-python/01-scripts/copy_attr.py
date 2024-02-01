

def copy_attr(source: object | dict, dest: object, attrs: list = None, copy_all=False, only_none=True):
    """复制对象属性

    :param source        源对象/字典
    :param dest          目的对象
    :param attrs         需要复制的属性
    :param copy_all      是否复制源的所有属性, True 时会忽略指定的 attrs
    :param only_none     是否只覆盖目标的 None 属性
    """
    src_kv = source if isinstance(source, dict) else source.__dict__
    attrs = src_kv.keys() if copy_all is True else attrs
    if attrs is None or len(attrs) < 1:
        return
    for k in attrs:
        if k in src_kv and hasattr(dest, k) and (not only_none or getattr(dest, k) is None):
            setattr(dest, k, src_kv.get(k))


if __name__ == '__main__':
    class Person():
        id_ = -1
        name = None

    class Student(Person):
        age = None
        
    p1 = Person()
    p1.id_ = 1
    p1.name = 'name-1'

    s1 = Student()
    s1.name = 's1'
    copy_attr(p1, s1, copy_all=True, only_none=True)
