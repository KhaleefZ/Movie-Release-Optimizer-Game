import matplotlib
matplotlib.use('Agg')  # Set the backend to non-interactive Agg
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

def generate_bar_chart(x_data, y_data, title, x_label, y_label, color):
    plt.figure(figsize=(14, 8))  # Increased figure size
    plt.clf()
    
    # Create bars with improved styling
    if isinstance(color, list):
        bars = plt.bar(x_data, y_data, color=color, width=0.6)
    else:
        bars = plt.bar(x_data, y_data, color=color, width=0.6)
    
    # Enhanced styling
    plt.title(title, pad=20, fontsize=16, fontweight='bold')
    plt.xlabel(x_label, labelpad=12, fontsize=14)
    plt.ylabel(y_label, labelpad=12, fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.3, axis='y')
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    
    # Enhanced bar labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'₹{int(height)} Cr' if 'Crores' in y_label else f'{int(height)}%',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    
    # Higher DPI for better quality
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=400, bbox_inches='tight', facecolor='white')
    img.seek(0)
    plt.close()
    return base64.b64encode(img.getvalue()).decode()

def generate_line_chart(x_data, y_data, title, x_label, y_label, color):
    plt.figure(figsize=(14, 8))  # Increased figure size
    plt.clf()
    
    # Enhanced line plot
    line = plt.plot(x_data, y_data, color=color, linewidth=3, marker='o', markersize=10)[0]
    plt.fill_between(x_data, y_data, alpha=0.2, color=color)
    
    # Enhanced styling
    plt.title(title, pad=20, fontsize=16, fontweight='bold')
    plt.xlabel(x_label, labelpad=12, fontsize=14)
    plt.ylabel(y_label, labelpad=12, fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    
    # Enhanced data point labels
    for x, y in zip(x_data, y_data):
        plt.text(x, y + 1, f'{int(y)}%',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    
    # Higher DPI for better quality
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=400, bbox_inches='tight', facecolor='white')
    img.seek(0)
    plt.close()
    return base64.b64encode(img.getvalue()).decode()

def generate_pie_chart(labels, values, title, figsize=(12, 12)):  # Increased default size
    plt.figure(figsize=figsize)
    plt.clf()
    
    # Enhanced color scheme
    colors = plt.cm.Paired(np.linspace(0, 1, len(labels)))
    
    # Create pie chart with improved styling
    wedges, texts, autotexts = plt.pie(values, labels=labels, 
                                      autopct='%1.1f%%',
                                      startangle=90, 
                                      colors=colors,
                                      textprops={'fontsize': 12},
                                      wedgeprops={'edgecolor': 'white', 'linewidth': 2})
    
    # Enhance text properties
    plt.setp(autotexts, size=11, weight="bold")
    plt.setp(texts, size=12)
    
    plt.title(title, pad=20, fontsize=16, fontweight='bold')
    plt.axis('equal')
    
    # Add legend
    plt.legend(wedges, labels,
              title="Categories",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1),
              fontsize=11)
    
    plt.tight_layout()
    
    # Higher DPI for better quality
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=400, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    plt.close()
    
    return f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode('utf-8')}"