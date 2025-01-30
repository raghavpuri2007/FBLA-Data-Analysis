import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def pollutant_standards():
    # Read the data from the file
    standards = pd.read_csv('Data/Pollutant_Standards.csv')
    print(standards.head())

    # Create a bar chart
    plt.figure(figsize=(8, 6))
    sns.barplot(x='Pollutant', y='1-Year Standard Level (μg/m3)',
                data=standards, palette='tab10')
    plt.title('Pollutant Standards')
    plt.savefig('Pollutant Standards.png', bbox_inches='tight')


def pollutants_over_time():
    # Read the data from the file
    df = pd.read_csv('Data/Pollutants_Over_Time.csv')

    # Create a line plot with shaded areas
    plt.figure(figsize=(12, 8))

    pollutants = df['Pollutant'].unique()
    palette = sns.color_palette('tab10', len(pollutants))
    color_dict = dict(zip(pollutants, palette))

    for pollutant in pollutants:
        pollutant_df = df[df['Pollutant'] == pollutant]

        # Plot the points as dots
        sns.scatterplot(x='Year', y='Mean μg/m3', data=pollutant_df,
                        label=pollutant, color=color_dict[pollutant])

        # Add the shaded area
        plt.fill_between(pollutant_df['Year'], pollutant_df['10th percentile μg/m3'],
                         pollutant_df['90th percentile μg/m3'],
                         color=color_dict[pollutant], alpha=0.2)

        # Fit and plot a second-degree polynomial regression line
        z = np.polyfit(pollutant_df['Year'], pollutant_df['Mean μg/m3'], 2)
        p = np.poly1d(z)
        plt.plot(pollutant_df['Year'], p(pollutant_df['Year']),
                 color=color_dict[pollutant])

    plt.title('Pollutant Concentrations Over Time')
    plt.legend(title='Pollutant')
    plt.savefig('Pollutants Over Time.png', bbox_inches='tight')


def main():
    pollutants_over_time()


if __name__ == '__main__':
    main()
