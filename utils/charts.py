import matplotlib
matplotlib.use('Agg')  # Set the backend to non-interactive Agg
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

def generate_bar_chart(x_data, y_data, title, x_label, y_label, color):
    plt.figure(figsize=(12, 6))
    plt.clf()
    
    # Remove the arbitrary multiplication factor
    y_data = [val if isinstance(val, (int, float)) else 0 for val in y_data]
    
    if isinstance(color, list):
        bars = plt.bar(x_data, y_data, color=color)
    else:
        bars = plt.bar(x_data, y_data, color=color)
    
    plt.title(title, pad=20, fontsize=14, fontweight='bold')
    plt.xlabel(x_label, labelpad=10, fontsize=12)
    plt.ylabel(y_label, labelpad=10, fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'₹{int(height)} Cr',
                ha='center', va='bottom')
    
    plt.tight_layout()
    
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=300, bbox_inches='tight', facecolor='white')
    img.seek(0)
    plt.close()
    return base64.b64encode(img.getvalue()).decode()

def generate_line_chart(x_data, y_data, title, x_label, y_label, color):
    plt.figure(figsize=(12, 6))
    plt.clf()
    
    line = plt.plot(x_data, y_data, color=color, linewidth=3, marker='o', markersize=8)[0]
    plt.fill_between(x_data, y_data, alpha=0.2, color=color)
    
    plt.title(title, pad=20, fontsize=14, fontweight='bold')
    plt.xlabel(x_label, labelpad=10, fontsize=12)
    plt.ylabel(y_label, labelpad=10, fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    
    for x, y in zip(x_data, y_data):
        plt.text(x, y, f'{int(y)}%',
                ha='center', va='bottom')
    
    plt.tight_layout()
    
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=300, bbox_inches='tight', facecolor='white')
    img.seek(0)
    plt.close()
    return base64.b64encode(img.getvalue()).decode()

def generate_pie_chart(labels, values, title, figsize=(10, 6)):
    plt.figure(figsize=figsize)
    
    colors = plt.cm.tab20(np.linspace(0, 1, len(labels)))
    
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    plt.axis('equal')
    plt.title(title)
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    
    return f"data:image/png;base64,{img_str}"