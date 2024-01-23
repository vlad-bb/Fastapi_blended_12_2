from time import time
from multiprocessing import Pool, cpu_count
import logging
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - (%(filename)s).%(funcName)s(%(lineno)d) - "
                           "[%(threadName)s] - %(message)s")


def factorize(numbers: list):
    result = []
    for i in numbers:
        lst = []
        for num in range(1, i + 1):
            if i % num == 0:
                lst.append(num)
        result.append(lst)
    return result


def multifactorize(number: int):
    lst = []
    for num in range(1, number + 1):
        if number % num == 0:
            lst.append(num)
    logging.debug(lst)
    return lst


if __name__ == '__main__':
    input_data = [128, 255, 99999, 10651060]
    start = time()
    a, b, c, d = factorize(input_data)
    end = time()
    print(f'Single proc: {end - start}')
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]

    core_counts = cpu_count()

    start = time()
    with Pool(processes=2) as pool:
        pool.map(multifactorize, input_data)
    end = time()
    print(f'Multiproc proc: {end - start}')

    start = time()
    with ProcessPoolExecutor(2) as executor:
        executor.map(multifactorize, input_data)
    end = time()
    print(f'Multiproc concurrent: {end - start}')
