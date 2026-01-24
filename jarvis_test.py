print(">>> ARCHIVO JARVIS_TEST.PY EJECUTÁNDOSE <<<")

import time
import requests
import pandas as pd
import ta
from pybit.unified_trading import HTTP

# ================= CONFIGURACIÓN =================
API_KEY = "fXRmHS1hxcx7OdhMeJ"
API_SECRET = "tIBnbTcZbArYAestnjrPXglRXuIZyNdWNnrN"

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
    # Por ahora no hay lógica → solo prueba estabilidad
    return None

# ================= BOT =================
def ejecutar_bot():
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

# ================= MAIN =================
print("Jarvis en ejecución 24/7")
alerta("Jarvis Testnet activo. Bot en ejecución 24/7.")

def main():
    while True:
        try:
            ejecutar_bot()
            time.sleep(3600)  # 1 hora
        except Exception as e:
            print("Error:", e)
            alerta(f"Error Jarvis Testnet: {e}")
            time.sleep(300)

if __name__ == "__main__":
    main()
