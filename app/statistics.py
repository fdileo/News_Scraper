import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import os


def bar_chart(values : list[int], labels : list[str], filename : str):
    
    """
    Salva il grafico a barre nella cartella static\\images.
    PARAMETRI IN INPUT:
    - values: le frequenze associate alle etichette
    - labels: etichette
    - filename: il nome in cui viene salvato il grafico
    """
    
    os.makedirs("app/static/images", exist_ok=True)
    
    plt.bar(labels, values, color = 'skyblue', alpha = 0.8)
    plt.xticks(rotation = 90)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.savefig(f"app/static/images/{filename}.png", bbox_inches = "tight")
    plt.close()
    