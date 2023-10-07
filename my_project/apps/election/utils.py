import base64
from io import BytesIO
import matplotlib

matplotlib.use("agg")
import matplotlib.pyplot as plt


def get_pie_chart(labels: dict, sizes: dict) -> str:
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%")
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    img = base64.b64encode(image_png).decode("utf-8")
    return img
