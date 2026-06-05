from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from aiohttp import ClientSession
from LyricsFindScrapper import Search, SongData

app = FastAPI()

@app.get("/lyrics")
async def get_lyrics(
    artist: str = Query(...),
    title: str = Query(...)
):
    async with ClientSession() as session:
        client = Search(session=session)
        try:
            query = f"{title} {artist}"
            tracks = await client.get_tracks(query)
            if not tracks:
                return JSONResponse(status_code=404, content={"error": "Not found"})

            track = await client.get_track(trackid=f"lfid:{tracks[0].lfid}")
            lyrics: SongData = await client.get_lyrics(track=track)

            return {
                "title": lyrics.title,
                "artist": lyrics.artist,
                "lyrics": lyrics.lyrics,
                "has_lrc": False
            }
        except Exception as e:
            return JSONResponse(status_code=404, content={"error": str(e)})
