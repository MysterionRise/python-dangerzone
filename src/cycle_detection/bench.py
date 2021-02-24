import timeit

from node import generate_linked_list


def floyd():
    linked_list = generate_linked_list(1000, 0.1)
    from floyd_algo_detection import detect_cycle

    return detect_cycle(linked_list)


print(timeit.timeit("[func() for func in (floyd, floyd)]", globals=globals()))
