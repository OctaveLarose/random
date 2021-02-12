import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def get_methods_qty_plot():
    # class_csv_path = "/home/octavel/bordel/ck_data/class/"
    # csv_filenames = os.listdir(class_csv_path)
    #
    # df = None
    # for idx, csv_name in enumerate(csv_filenames):
    #     csv_path = os.path.join(class_csv_path, csv_name)
    #     new_df = pd.read_csv(csv_path)
    #     if df is not None:
    #         df = pd.concat((df, new_df))
    #     else:
    #         df = new_df
    #     print(f"Progress: {idx + 1}/{len(csv_filenames)}")
    #
    # df.to_csv("mega_class.csv", sep=',', encoding='utf-8')

    df = pd.read_csv("mega_class.csv")
    # df = pd.read_csv("/home/octavel/bordel/ck_data/class/class_jwtk_jjwt.csv")

    METHOD_GRAPH_CAP = 30
    print(f"Classes with nbr methods <= {METHOD_GRAPH_CAP}: {len(df.loc[df['totalMethodsQty'] <= METHOD_GRAPH_CAP])}")
    print(f"Classes with nbr methods > {METHOD_GRAPH_CAP}: {len(df.loc[df['totalMethodsQty'] > METHOD_GRAPH_CAP])}")

    df = df.loc[df["totalMethodsQty"] <= METHOD_GRAPH_CAP]

    # max_class = df[df["totalMethodsQty"] == df["totalMethodsQty"].max()]

    sns.set_theme(style="darkgrid")
    bins = np.arange(-0.5, METHOD_GRAPH_CAP + 1, 1)
    plot = sns.displot(data=df, x="totalMethodsQty", bins=bins)
    plot.set(xlabel='Number of methods', ylabel='Number of classes')
    # plt.xlim(-1, 30)
    plt.margins(x=0)
    plt.tight_layout()
    plt.show()


def main():
    get_methods_qty_plot()


if __name__ == "__main__":
    main()
