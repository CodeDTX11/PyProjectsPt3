from flask import Flask

app = Flask(__name__)

def make_emphasis(func):
    print("start emphasis")
    def wrapper():
        print("emphasis")
        return f"<em>{func()}</em>"
    return wrapper

def make_bold(func):
    print("start bold")
    def wrapper():
        print("bold")
        return f"<b>{func()}</b>"
    return wrapper

def make_underline(func):
    print("start under")
    def wrapper():
        print("under")
        return f"<u>{func()}</u>"
    return wrapper

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/b")
@make_emphasis
@make_bold
@make_underline
def bye():
    return "Bye"

# print(bye())

# bye = make_emphasis(bye)
# print(bye())
# bye = make_bold(bye)
# print(bye())
# bye = make_underline(bye)
# print(bye())

def add_sprinkles(f):
    print("s")
    def wrapper():
        print("add sprinkles")
        f()
    return wrapper

def add_fudge(f):
    print("f")
    def wrapper():
        print("add fudge")
        f()
    return wrapper

# @add_sprinkles
# @add_fudge
# def get_ice():
#     print("ice cream")
#
# get_ice()

# if __name__ == "__main__":
#     app.run(debug=True)

def create_functions():
    funcs = []
    for i in range(3):
        def make_func(x):
            def func():
                return x  # 'x' is captured at creation time
            return func
        funcs.append(make_func(i))
    return funcs

f0, f1, f2 = create_functions()
print(f0())  # Output: 0
print(f1())  # Output: 1
print(f2())  # Output: 2