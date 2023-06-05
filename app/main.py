from Holiday_and_season import travel_place
import pandas as pd

fsho = travel_place()
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
def main():
    fsho.fstvlHolYear([2023])

if __name__ == "__main__":
    main()