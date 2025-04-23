import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
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


def exceeding_pollutants():
    standards = pd.read_csv('Data/Pollutant_Standards.csv')
    df = pd.read_csv('Data/Pollutants_Over_Time.csv')
    df = df[df["Year"] == 2012]
    df = df.merge(standards, left_on="Pollutant", right_on="Pollutant")

    df["% Exceeding Standards"] = 100 * (df['70th percentile μg/m3'] -
                                         df['1-Year Standard Level (μg/m3)']) / df['1-Year Standard Level (μg/m3)']

    plt.figure(figsize=(8, 6))
    colors = ['#d62728', "#61b861", "#61b861", "#e05d5e", '#2ca02c']
    plt.barh(df['Pollutant'], df["% Exceeding Standards"], color=colors)

    # Add a horizontal line at y=0, custom labels
    plt.axvline(0, color='black', linewidth=1, linestyle='--')
    custom_labels = ['PM 2.5', 'NO', 'NO2', 'O3', 'SO2']
    plt.yticks(ticks=range(len(custom_labels)), labels=custom_labels)
    plt.xlabel("Percent Over Quality Standard")

    # Set the title and save the plot
    plt.title('By How Much Do Pollutants Exceed Quality Standards?')
    plt.savefig('Pollutants Relative to Standards.png', bbox_inches='tight')


def pollutants_over_time():
    # Read the data from the files
    df = pd.read_csv('Data/Pollutants_Over_Time.csv')
    standards = pd.read_csv('Data/Pollutant_Standards.csv')
    pollutants = standards['Pollutant'].unique()
    palette = sns.color_palette('tab10', len(pollutants))
    color_dict = dict(zip(pollutants, palette))

    for POLLUTANT in pollutants:
        # Create a line plot with shaded areas
        fig, ax = plt.subplots(figsize=(12, 8))

        for pollutant in pollutants:
            pollutant_df = df[df['Pollutant'] == pollutant]
            alpha_val = 1 if pollutant == POLLUTANT else 0.09
            std_alpha = 1 if pollutant == POLLUTANT else 0.05
            shade_alpha = 0.2 if pollutant == POLLUTANT else 0.035

            # Plot the points as dots
            sns.scatterplot(ax=ax, x='Year', y='Mean μg/m3', data=pollutant_df,
                            label=pollutant, color=color_dict[pollutant], alpha=alpha_val)

            # Add the shaded area
            ax.fill_between(pollutant_df['Year'], pollutant_df['30th percentile μg/m3'],
                            pollutant_df['70th percentile μg/m3'],
                            color=color_dict[pollutant], alpha=shade_alpha)

            # Fit and plot a second-degree polynomial regression line
            z = np.polyfit(pollutant_df['Year'], pollutant_df['Mean μg/m3'], 1)
            p = np.poly1d(z)
            ax.plot(pollutant_df['Year'], p(pollutant_df['Year']),
                    color=color_dict[pollutant], alpha=alpha_val)

            # Add a horizontal dotted line for the pollutant standard
            standard_level = standards.loc[standards['Pollutant']
                                           == pollutant, '1-Year Standard Level (μg/m3)']
            print(standard_level)
            if not standard_level.empty:
                ax.axhline(y=standard_level.values[0], color=color_dict[pollutant],
                           linestyle='--', linewidth=2, label=None, alpha=std_alpha)

        # Add the first legend (pollutant dots only)
        plt.legend(title='Pollutant', loc='upper right')

        # Add the second legend for line types
        best_fit_line = mlines.Line2D(
            [], [], color='black', linestyle='-', linewidth=2, label='Best-Fit Line')
        safety_threshold_line = mlines.Line2D(
            [], [], color='black', linestyle='--', linewidth=2, label='Safety Threshold')
        extra_legend = ax.legend(handles=[best_fit_line, safety_threshold_line],
                                 loc='upper left')
        ax.add_artist(extra_legend)

        plt.title('Pollutant Concentrations Over Time')
        plt.legend(title='Pollutant')
        plt.savefig('Pollutants Over Time/' + POLLUTANT +
                    '.png', bbox_inches='tight')


def main():
    exceeding_pollutants()


if __name__ == '__main__':
    main()
