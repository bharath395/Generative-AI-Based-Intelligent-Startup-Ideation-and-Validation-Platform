import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go


def build_market_projection(base_value=4.2, annual_growth=0.224, years=None):
    years = years or list(range(2023, 2029))
    values = np.array([
        round(base_value * ((1 + annual_growth) ** index), 2)
        for index, _ in enumerate(years)
    ])
    frame = pd.DataFrame({"year": years, "market_value_billion": values})
    return frame.to_dict(orient="records")


def build_plotly_market_projection(projection):
    frame = pd.DataFrame(projection)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=frame["year"],
        y=frame["market_value_billion"],
        mode="lines+markers",
        name="Market Value ($B)",
        line={"color": "#2563EB", "width": 3},
    ))
    fig.update_layout(
        template="plotly_white",
        margin={"l": 32, "r": 16, "t": 24, "b": 32},
        xaxis_title="Year",
        yaxis_title="Market Value ($B)",
        height=320,
    )
    return json.loads(fig.to_json())


def generate_matplotlib_projection_chart(projection, output_filepath):
    frame = pd.DataFrame(projection)
    path = Path(output_filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(7, 3.4))
    plt.plot(frame["year"], frame["market_value_billion"], marker="o", color="#2563EB")
    plt.fill_between(frame["year"], frame["market_value_billion"], alpha=0.15, color="#2563EB")
    plt.title("Market Growth Projection")
    plt.xlabel("Year")
    plt.ylabel("Market Value ($B)")
    plt.tight_layout()
    plt.savefig(path, dpi=140)
    plt.close()
    return str(path)
