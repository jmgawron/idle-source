from idle.idle_core import *
import sys


def main():
    if len(sys.argv) != 3:
        usage()
        exit(1)

    filename = sys.argv[1]
    mode = sys.argv[2]

    if 'offline' in mode:
        print(sys.argv[0], 'running in offline mode.')

        myRunner = TaskRunner(filename)
        myRunner.get_build_tasks()

    elif 'online' in mode:
        print(sys.argv[0], 'running in online mode.')

        myRunner = TaskRunner(filename)
        myRunner.connector.get_service_token()
        myRunner.get_build_tasks()
        myRunner.process_tasks()
        myRunner.print_report()

    elif 'debug' in mode:
        myRunner = TaskRunner(filename)
        myRunner.connector.get_service_token()
        myRunner.get_build_tasks()
        myRunner.process_tasks_debug()

    else:
        print('Invalid argument!')
        usage()


def usage():
    print('Usage:')
    print(' idle.py <xls filename> <offline/online>')


if __name__ == "__main__":
    main()
