import mplfinance as mpf
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

def plot_signal(df: pd.DataFrame, levels: dict, abnormal_idx: int | None = None) -> bytes:
    """Return PNG bytes for chart with volume histogram and S/R lines.

    `df` is expected to be the window to plot (e.g., `df.tail(200)`).
    `abnormal_idx` may be an integer index (relative or absolute) or a pandas.Timestamp.
    The function normalizes it to the plotted window.
    """
    hlines = [v for v in levels.values() if v is not None]
    style = mpf.make_mpf_style(base_mpf_style='classic')
    add_plot = mpf.make_addplot(df['volume'], panel=1, type='bar', color='blue')
    fig, axes = mpf.plot(df, type='candle', style=style, addplot=add_plot, returnfig=True, volume=False)
    ax = axes[0]
    for lvl in hlines:
        ax.hlines(lvl, df.index[0], df.index[-1], colors='grey', linestyles='--')

    # normalize abnormal_idx to plotted window
    pos = None
    if abnormal_idx is not None:
        try:
            import pandas as _pd
            if isinstance(abnormal_idx, (_pd.Timestamp,)):
                # locate timestamp in index
                try:
                    pos = int(df.index.get_loc(abnormal_idx))
                except Exception:
                    pos = None
            else:
                # treat as integer; allow negative indexing
                ai = int(abnormal_idx)
                if ai < 0:
                    ai = len(df) + ai
                if 0 <= ai < len(df):
                    pos = ai
        except Exception:
            pos = None

    if pos is not None:
        ax.scatter(df.index[pos], df['high'].iloc[pos], color='red', zorder=10)

    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=150)
    plt.close(fig)
    buf.seek(0)
    return buf.read()
