import matplotlib.pyplot as plt

def plot_multiple_solutions(solutions):
    labels = [f"A={a}, B={b}" for a, b, obj in solutions]
    values = [obj for a, b, obj in solutions]
    plt.figure(figsize=(10,6))
    bars = plt.bar(labels, values, color='skyblue')
    plt.ylabel('Valor en función objetivo')
    plt.title('Soluciones factibles y su valor objetivo')
    plt.xticks(rotation=45)
    for bar in bars:
        height = bar.get_height()
        plt.annotate(f'{height:.2f}',
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3),
                     textcoords="offset points",
                     ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig('Grafico.png') 
    plt.close()
