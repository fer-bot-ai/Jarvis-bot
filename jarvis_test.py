print(">>> ARCHIVO JARVIS_TEST.PY EJECUTÁNDOSE <<<")
import requests
import pandas as pd
import ta
from pybit.unified_trading import HTTP

# ================= CONFIGURACIÓN =================
API_KEY = "fXRmHS1hxcx7OdhMeJ"
API_SECRET ="tIBnbTcZbArYAestnjrPXglRXuIZyNdWNnrN"

BOT_TOKEN = "8488664972:AAEKBU6EzUXNvU3fVAaFNSnwGHFbHF2qAho"
CHAT_ID = "7262713362"

SYMBOL = "BTCUSDT"
TIMEFRAME = "60"  # 1H

# ================= CONEXIÓN TESTNET =================
session = HTTP(
    testnet=True,
    api_key=API_KEY,
    api_secret=API_SECRET
)

# ================= TELEGRAM =================
def alerta(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=10)
    except:
        pass

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

# ================= SEÑAL =================
def analizar_entrada():
    df = obtener_datos()

    df["ema50"] = ta.trend.ema_indicator(df["close"], 50)
    df["ema200"] = ta.trend.ema_indicator(df["close"], 200)
    df["rsi"] = ta.momentum.rsi(df["close"], 14)
    df["vol_avg"] = df["volume"].rolling(20).mean()

    ultima = df.iloc[-1]

    tendencia = ultima["ema50"] > ultima["ema200"]
    rsi_ok = 30 <= ultima["rsi"] <= 70
    volumen_ok = ultima["volume"] > ultima["vol_avg"]

    if tendencia and rsi_ok and volumen_ok:
        entrada = ultima["close"]
        sl = df["low"].iloc[-2]
        tp = entrada + (entrada - sl) * 2

        return {
            "entrada": round(entrada, 2),
            "sl": round(sl, 2),
            "tp": round(tp, 2),
            "rsi": round(ultima["rsi"], 2)
        }

    return None

# ================= EJECUCIÓN =================
def ejecutar_bot():
    alerta("Jarvis Testnet activo")

    senal = analizar_entrada()

    if senal:
        mensaje = (
            "Señal BTCUSDT 1H\n"
            f"Entrada: {senal['entrada']}\n"
            f"SL: {senal['sl']}\n"
            f"TP: {senal['tp']}\n"
            f"RSI: {senal['rsi']}"
        )
        print(mensaje)
        alerta(mensaje)
    else:
        print("Entrada no válida. Se mantiene disciplina.")
        alerta("Entrada no válida. Se mantiene disciplina.")

import time

print("Jarvis en ejecución 24/7")

while True:
    try:
        ejecutar_bot()
        time.sleep(60)  # corre cada 60 segundos
    except Exception as e:
        print("Error:", e)
        time.sleep(30)
