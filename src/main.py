
from heatmap import Heatmap
from num_table import Numerical_Table
from cat_table import Categorical_Table
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
        hm = Heatmap(file)
        op(hm.heatmap)
        return hm


    elif request == "num_table":
        nt = Numerical_Table(file)
        return nt


    elif request == "cat_table":
        ct = Categorical_Table(file)
        return ct


if __name__ == "__main__":
    main()
    