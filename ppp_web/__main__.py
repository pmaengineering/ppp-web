"""Main"""
try:
    from ppp_web.ppp_web import run
except ModuleNotFoundError:
    from ppp_web import run


if __name__ == '__main__':
    run()
