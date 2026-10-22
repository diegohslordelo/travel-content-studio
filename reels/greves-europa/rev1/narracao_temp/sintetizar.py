import asyncio, json, ssl, sys, edge_tts, edge_tts.communicate
edge_tts.communicate._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
texto, saida, rate = open(sys.argv[1], encoding="utf-8").read().strip(), sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "+0%"
async def main():
    c = edge_tts.Communicate(texto, "pt-BR-AntonioNeural", rate=rate, boundary="WordBoundary")
    palavras = []
    with open(saida + ".mp3", "wb") as f:
        async for ch in c.stream():
            if ch["type"] == "audio": f.write(ch["data"])
            elif ch["type"] == "WordBoundary":
                palavras.append({"t": ch["offset"] / 1e7, "d": ch["duration"] / 1e7, "w": ch["text"]})
    json.dump(palavras, open(saida + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(len(palavras), "palavras; fim", round(palavras[-1]["t"] + palavras[-1]["d"], 2), "s")
asyncio.run(main())
