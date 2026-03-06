from fastapi import FastAPI, HTTPException
from ytmusicapi import YTMusic
import yt_dlp
from typing import List

app = FastAPI(title="Music Engine API")
yt = YTMusic()

# Configuração do extrator
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True,
}

@app.get("/search")
async def search_music(query: str):
    """Busca músicas e retorna metadados e IDs"""
    try:
        results = yt.search(query, filter="songs")
        parsed_results = []
        for res in results[:10]:
            parsed_results.append({
                "id": res['videoId'],
                "title": res['title'],
                "artist": res['artists'][0]['name'],
                "thumbnail": res['thumbnails'][-1]['url'],
                "duration": res.get('duration', '0:00')
            })
        return parsed_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stream/{video_id}")
async def get_stream(video_id: str):
    """Gera a URL direta do áudio para streaming ou download"""
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "stream_url": info['url'],
                "extension": info.get('ext', 'm4a'),
                "title": info.get('title')
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)