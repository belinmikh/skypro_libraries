from src.fileio import read_xlsx
from src.reports import spending_by_category
from src.services import phone_search, search_individuals, simple_search
from src.views import main_page


def main() -> None:
    print("main_page('2021-12-01 15:20:00')")
    print()
    response = main_page("2021-12-01 15:20:00")
    print(response)
    print("ops = read_xlsx('operations.xlsx')")
    ops = read_xlsx("operations.xlsx")
    print("spending_by_category(ops, 'Супермаркеты', '2021-12-01 12:20:00', mode='dict')")
    print()
    result = spending_by_category(ops, "Супермаркеты", "2021-12-01 12:20:00", mode="dict")
    print(result)
    print("ops = read_xlsx('operations.xlsx')")
    ops = read_xlsx("operations.xlsx")
    print("simple_search(ops, 'банк', mode='dict')")
    print()
    result = simple_search(ops, "банк", mode="dict")
    print(result)
    print("ops = read_xlsx('operations.xlsx')")
    ops = read_xlsx("operations.xlsx")
    print("phone_search(ops, mode='dict')")
    print()
    result = phone_search(ops, mode="dict")
    print(result)
    print("ops = read_xlsx('operations.xlsx')")
    ops = read_xlsx("operations.xlsx")
    print("search_individuals(ops, mode='dict')")
    print()
    result = search_individuals(ops, mode="dict")
    print(result)


if __name__ == "__main__":
    main()
