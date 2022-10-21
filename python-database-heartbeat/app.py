import multiprocessing
import time

def test_db_alive(conn):
    try:
        print("db_alive")
        print(f"arg: {conn}")
        time.sleep(5)
        return True
    except:
        return False


def test_db_performance_1(conn):
    try:
        print("performance_1")
        print(f"arg: {conn}")
        time.sleep(5)
        return True
    except:
        return False


def test_db_performance_2(conn):
    try:
        print("performance_2")
        print(f"arg: {conn}")
        time.sleep(5)
        return True
    except:
        return False


def config_tests():
    jobs = []
    for f in [test_db_alive, test_db_performance_1, test_db_performance_2]:
        job = multiprocessing.Process(target=f, args=('argumento',))
        jobs.append(job)
        job.start()

    exited = 0
    while exited < len(jobs):
        for job in jobs:
            if not job.is_alive():
                exited += 1

    print('Terminado')

if __name__ == '__main__':
    config_tests()