import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    # Read the data from the file
    standards = pd.read_csv('Data/Pollutant_Standards.csv')
    print(standards.head())

    # Create a bar chart
    plt.figure(figsize=(8, 6))
    sns.barplot(x='Pollutant', y='1-Year Standard Level (μg/m3)',
                data=standards, palette='viridis')
    # plt.xlabel('Pollutant')
    # plt.ylabel('1-Year Standard Level (μg/m3)')
    plt.title('Pollutant Standards')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()


if __name__ == '__main__':
    main()
