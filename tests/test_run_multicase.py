from aircraft_design import FunctionRunner
from time import time

def calculate_pi(precision):
    a = 1.0
    b = 1.0/(2**0.5)
    t = 1.0/4.0
    p = 1.0

    for i in range(precision):
        new_a = (a + b)/2.0
        new_b = (a * b)**0.5
        new_t = t - p * (a - new_a)**2
        new_p = 2.0 * p

        a, b, t, p = new_a, new_b, new_t, new_p

    pi = (a + b)**2 / (4.0 * t)
    return pi

def test_function_multicase():
    start_time = time()
    [calculate_pi(100_000) for _ in range(1000)]
    single_thread = time() - start_time

    start_time = time()
    FunctionRunner(calculate_pi, [100_000 for _ in range(1000)]).run_all_cases()
    multi_thread = time() - start_time
    assert multi_thread < single_thread, 'Função não funcional'

