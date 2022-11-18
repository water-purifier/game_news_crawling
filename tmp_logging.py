import logging

logging.basicConfig(filename='./logging.py.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')


def set_isnull_to_zero(val):
    if not val:
        return 0
    else:
        if val.isdigit():
            return val
        else:
            return 0


try:
    null = None
    null2 = ''

    print(null.isdigit())
    print(null2.isdigit())

    print(set_isnull_to_zero('34324'))
    print(set_isnull_to_zero('aaa34324'))
    print(set_isnull_to_zero(''))
    print(set_isnull_to_zero(None))
except Exception as e:
    logging.error(e)
