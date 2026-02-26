import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def visualize_pollution_data(df_long):
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(12, 6))

    kyiv_dust = df_long[(df_long['city'] == 'Київ') & (df_long['nameImpurity'] == 'Завислі речовини')]
    
    plt.subplot(1, 2, 1)
    sns.lineplot(data=kyiv_dust, x='day', y='value', marker='o', color='royalblue')
    plt.title('Тренд пилу в Києві (Січень 2026)')
    plt.xlabel('День місяця')
    plt.ylabel('Концентрація')

    target_cities = ['Київ', 'Херсон', 'Вінниця', 'Суми']
    comparison_data = df_long[(df_long['city'].isin(target_cities)) & (df_long['nameImpurity'] == 'Дiоксид сiрки')]
    
    plt.subplot(1, 2, 2)
    sns.boxplot(data=comparison_data, x='city', y='value', palette='Set2')
    plt.title('Розподіл SO2: Стабільність vs Сплески')
    plt.xlabel('Місто')
    plt.ylabel('Концентрація')

    plt.tight_layout()
    plt.show()
