"""Download and plot AMZN hourly candlesticks for the last six months."""

from pathlib import Path

import matplotlib.pyplot as plt
import mplfinance as mpf
import yfinance as yf


TICKER = "AMZN"
INTERVAL = "1h"
PERIOD = "6mo"
OUTPUT_FILE = Path("amzn_6m_1h_candles.png")


def download_amzn_data():
	"""Download six months of hourly OHLCV data for Amazon."""
	data = yf.download(
		TICKER,
		period=PERIOD,
		interval=INTERVAL,
		auto_adjust=False,
		progress=False,
		group_by="column",
	)

	if data.empty:
		raise RuntimeError(
			"Yahoo Finance no devolvio datos para AMZN. "
			"Comprueba la conexion o el limite de disponibilidad del intervalo."
		)

	if hasattr(data.columns, "levels"):
		data.columns = data.columns.get_level_values(0)

	required_columns = {"Open", "High", "Low", "Close", "Volume"}
	missing_columns = required_columns.difference(data.columns)
	if missing_columns:
		raise ValueError(f"Faltan columnas OHLCV: {sorted(missing_columns)}")

	return data.dropna(subset=["Open", "High", "Low", "Close"])


def plot_candles(data) -> None:
	"""Render and save the hourly candlestick chart."""
	mpf.plot(
		data,
		type="candle",
		style="yahoo",
		volume=True,
		figsize=(16, 9),
		title=f"{TICKER} | ultimos 6 meses | velas de 1 hora",
		ylabel="Precio (USD)",
		ylabel_lower="Volumen",
		tight_layout=True,
		savefig=dict(fname=OUTPUT_FILE, dpi=150, bbox_inches="tight"),
		show_nontrading=False,
	)
	print(f"Grafica guardada en: {OUTPUT_FILE.resolve()}")
	plt.show()


if __name__ == "__main__":
	plot_candles(download_amzn_data())
