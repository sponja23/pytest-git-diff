from absolute_imports.a import a_func


def c_func():
    print("c_func() called")
    a_func()
    print("c_func() finished")
