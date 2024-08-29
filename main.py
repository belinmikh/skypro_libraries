import json
import sys

from typing import Any

from src.fileio import read_xlsx
from src.reports import spending_by_category
from src.services import simple_search, phone_search, search_individuals
from src.views import main_page


def nice_dict(d: Any, t: str = "") -> None:
    # awesome bools
    """Prints dictionaries in readable way"""
    if isinstance(d, dict):
        print()
        print(f"{t}nice dict:")
        for k, v in d.items():
            print(f"{t}key {type(k)}: {k}:")
            nice_dict(v, t + '\t')
            print(f"{t}_____")
    elif isinstance(d, list):
        print(f"{t}nice list:")
        for i in range(len(d)):
            nice_dict(d[i], t + '\t')
            if i > 3:
                print(f'\n{t}and more...\n')
                break
    else:
        try:
            print(t + str(d))
        except:
            print(f"{t}{type(d)} is not printable")


def main() -> None:
    if len(sys.argv) != 2:
        print("python main.py 'func_name'")
        print("Funcs: main_page, spending_by_category, \n"
              "simple_search, phone_search, search_individuals")
        print("Recommendation: run 'clear' before test")
    elif sys.argv[1] == 'main_page':
        print("main_page('2021-12-01 15:20:00')")
        print()
        response = main_page('2021-12-01 15:20:00')
        nice_dict(json.loads(response))
        print("Recommendation: run 'clear' before next test")
    elif sys.argv[1] == 'spending_by_category':
        print("ops = read_xlsx('operations.xlsx')")
        ops = read_xlsx('operations.xlsx')
        print("spending_by_category(ops, 'Супермаркеты', '2021-12-01 12:20:00', mode='dict')")
        print()
        result = spending_by_category(ops, 'Супермаркеты', '2021-12-01 12:20:00', mode='dict')
        nice_dict(result)
        print("Recommendation: run 'clear' before next test")
    elif sys.argv[1] == 'simple_search':
        print("ops = read_xlsx('operations.xlsx')")
        ops = read_xlsx('operations.xlsx')
        print("simple_search(ops, 'банк', mode='dict')")
        print()
        result = simple_search(ops, 'банк', mode='dict')
        nice_dict(result)
        print("Recommendation: run 'clear' before next test")
    elif sys.argv[1] == 'phone_search':
        print("ops = read_xlsx('operations.xlsx')")
        ops = read_xlsx('operations.xlsx')
        print("phone_search(ops, mode='dict')")
        print()
        result = phone_search(ops, mode='dict')
        nice_dict(result)
        print("Recommendation: run 'clear' before next test")
    elif sys.argv[1] == 'search_individuals':
        print("ops = read_xlsx('operations.xlsx')")
        ops = read_xlsx('operations.xlsx')
        print("search_individuals(ops, mode='dict')")
        print()
        result = search_individuals(ops, mode='dict')
        nice_dict(result)
        print("Recommendation: run 'clear' before next test")
    else:
        print("python main.py 'func_name'")
        print("Funcs: main_page, spending_by_category, \n"
              "simple_search, phone_search, search_individuals")
        print("Recommendation: run 'clear' before test")


if __name__ == '__main__':
    main()
