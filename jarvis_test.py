print(">>> JARVIS REAL SIGNAL BOT INICIADO <<<")

import time
import requests
import pandas as pd
import ta
from pybit.unified_trading import HTTP

# ================= CONFIG =================
API_KEY = "fXRmH51hxcx70dhMe]"
API_SECRET = "tIBnbTcZbArYAestnjrPXg1RXuIZyNdNnrN"

BOT_TOKEN = "8488664972:AAEKBU6EzUXNvU3fVAaFN5пwĞHFbHF2qÅho"
CHAT_ID = "7262713362"

SYMBOL = "BTCUSDT"
TIMEFRAME = "60"  # 1H

# ================= CONEXIÓN =================
session = HTTP(
    testnet=True,
    api_key=API_KEY,
    api_secret=API_SECRET
)

# ================= TELEGRAM =================
def alerta(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=10)

# ================= DATOS =================
def obtener_datos():
    klines = session.get_kline(
        category="linear",
        symbol=SYMBOL,
        interval=TIMEFRAME,
        limit=300
    )

    df = pd.DataFrame(
        klines["result"]["list"],
        columns=["timestamp","open","high","low","close","volume","turnover"]
    )

    df[["open","high","low","close","volume"]] = df[
        ["open","high","low","close","volume"]
    ].astype(float)

    return df

# ================= ESTRATEGIA =================
def analizar_entrada():
    df = obtener_datos()

    df["rsi"] = ta.momentum.RSIIndicator(df["close"], 14).rsi()
    df["ema9"] = ta.trend.EMAIndicator(df["close"], 9).ema_indicator()
    df["ema21"] = ta.trend.EMAIndicator(df["close"], 21).ema_indicator()
    df["ema200"] = ta.trend.EMAIndicator(df["close"], 200).ema_indicator()

    last = df.iloc[-2]  # vela cerrada

    if (
        last["rsi"] < 30 and
        last["close"] > last["ema200"] and
        last["ema9"] > last["ema21"]
    ):
        entrada = last["close"]
        sl = df["low"].tail(10).min()
        tp = entrada + (entrada - sl) * 2

        return {
            "entrada": round(entrada, 2),
            "sl": round(sl, 2),
            "tp": round(tp, 2),
            "rsi": round(last["rsi"], 2)
        }

    return None

# ================= BOT =================
def ejecutar_bot():
    senal = analizar_entrada()

    if senal:
        mensaje = (
            "📊 SEÑAL BTCUSDT 1H\n\n"
            f"Entrada: {senal['entrada']}\n"
            f"SL: {senal['sl']}\n"
            f"TP: {senal['tp']}\n"
            f"RSI: {senal['rsi']}\n\n"
            "Gestión de riesgo obligatoria."
        )
        print(mensaje, flush=True)
        alerta(mensaje)
    else:
        mensaje = "🟡 Jarvis activo: sin señal BTCUSDT 1H en este ciclo."
        print(mensaje, flush=True)
        alerta(mensaje)

from datetime import datetime
import time

def main():
    while True:
        try:
            print(f"[{datetime.utcnow()}] Jarvis vivo. Analizando mercado...", flush=True)

            ejecutar_bot()

            print(f"[{datetime.utcnow()}] Ciclo completado. Esperando siguiente análisis.", flush=True)

            time.sleep(3600)  # 1 hora
        except Exception as e:
            print(f"[{datetime.utcnow()}] ERROR: {e}", flush=True)
            time.sleep(300)

if __name__ == "__main__":
    main()





