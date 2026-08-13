
from src.heatmap import Heatmap
from src.num_table import Numerical_Table
from src.cat_table import Categorical_Table
from objprint import op


def main():
    request = input("What do you need? [heatmap, num_table, cat_table]: ")
    file = input("Enter file path: ")

    # ========== TESTING ========== #
    #
    request = "heatmap"
    file = "Student_Productivity_Dataset.csv"
    #
    # ========== TESTING ========== #

    if request == "heatmap":
        heatmap = Heatmap(file)
        op(heatmap.heatmap)
        return heatmap


    elif request == "num_table":
        num_table = Numerical_Table(file)
        return num_table


    elif request == "cat_table":
        cat_table = Categorical_Table(file)
        return cat_table


if __name__ == "__main__":
    main()
    