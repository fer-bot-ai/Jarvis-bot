print(">>> ARCHIVO JARVIS_TEST.PY EJECUTÁNDOSE <<<")

import time
import requests
import pandas as pd
import ta
from pybit.unified_trading import HTTP
from datetime import datetime

# ================= CONFIGURACIÓN =================
API_KEY = "fXRmH51hxcx70dhMe]"
API_SECRET = "tIBnbTcZbArYAestnjrPXg1RXuIZyNdNnrN"|

BOT_TOKEN = "8488664972:AAEKBU6EzUXNvU3fVAaFN5пwĞHFbHF2qÅho"
CHAT_ID - *7262713362"

SYMBOL = "BTCUSDT"
TIMEFRAME = "60"  # 1H

# ================= CONEXIÓN BYBIT TESTNET =================
session = HTTP(
    testnet=True,
    api_key=API_KEY,
    api_secret=API_SECRET
)

# ================= TELEGRAM =================
def alerta(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(
            url,
            data={"chat_id": CHAT_ID, "text": msg},
            timeout=10
        )
    except:
        pass

# ================= DATOS =================
def obtener_datos():
    klines = session.get_kline(
        category="linear",
        symbol=SYMBOL,
        interval=TIMEFRAME,
        limit=200
    )

    df = pd.DataFrame(
        klines["result"]["list"],
        columns=["timestamp","open","high","low","close","volume","turnover"]
    )

    df[["open","high","low","close","volume"]] = df[
        ["open","high","low","close","volume"]
    ].astype(float)

    df["timestamp"] = df["timestamp"].astype(int)
    return df

# ================= SEÑAL =================
def analizar_entrada(df):
    df["rsi"] = ta.momentum.RSIIndicator(df["close"], window=14).rsi()

    rsi_actual = df["rsi"].iloc[-1]
    precio = df["close"].iloc[-1]

    if rsi_actual < 30:
        return {
            "tipo": "LONG",
            "entrada": precio,
            "sl": precio * 0.98,
            "tp": precio * 1.04,
            "rsi": round(rsi_actual, 2)
        }

    if rsi_actual > 70:
        return {
            "tipo": "SHORT",
            "entrada": precio,
            "sl": precio * 1.02,
            "tp": precio * 0.96,
            "rsi": round(rsi_actual, 2)
        }

    return None

# ================= BOT =================
ultima_vela = None

def ejecutar_bot():
    global ultima_vela

    df = obtener_datos()

    timestamp_ultima = df["timestamp"].iloc[-1]

    if ultima_vela == timestamp_ultima:
        return  # ya se analizó esta vela

    ultima_vela = timestamp_ultima

    senal = analizar_entrada(df)

    if senal:
        hora = datetime.utcfromtimestamp(timestamp_ultima / 1000)

        mensaje = (
            f"📊 Señal BTCUSDT 1H\n"
            f"Tipo: {senal['tipo']}\n"
            f"Entrada: {senal['entrada']:.2f}\n"
            f"SL: {senal['sl']:.2f}\n"
            f"TP: {senal['tp']:.2f}\n"
            f"RSI: {senal['rsi']}\n"
            f"Hora UTC: {hora}"
        )

        print(mensaje)
        alerta(mensaje)

print("Jarvis en ejecución 24/7")
alerta("Jarvis Testnet activo. Bot en ejecución.")

def main():
    while True:
        try:
            ejecutar_bot()
            time.sleep(60)  # revisa cada minuto
        except Exception as e:
            print("Error:", e)
            alerta(f"Error Jarvis Testnet: {e}")
            time.sleep(300)

if __name__ == "__main__":
    main()
