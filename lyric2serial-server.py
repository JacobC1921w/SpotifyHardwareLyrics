from uvicorn import run
from fastapi import FastAPI, HTTPException
from subprocess import run as os
from os import name as OSName

api: FastAPI = FastAPI()

@api.get("/lyric")
def parse_query(ar: str = None, al: str = None, t: str = None, cl: str = None, pl: str = None, nl: str = None, p: str = None, tl: str = None):
    if None in (ar, al, t, cl, pl, nl, p, tl):
        raise HTTPException(400, "Malformed data")
    else:
        if ar == "": return # Probably havent actually started a song yet
        clearScreen()
        print("Artist:\t" + ar)
        print("Album:\t" + al)
        print("Track:\t" + t)
        print(generateProgress(int(tl), int(p)))
        print("")
        
        print("\033[2m" + pl + "\x1b[0m")
        print("\033[1m" + cl + "\x1b[0m")
        print("\033[2m" + nl + "\x1b[0m")
        return "OK"

def formatTime(ms: int) -> str:
    minutes = ms // 60000
    seconds = (ms % 60000) // 1000

    return f"{minutes}:{seconds:02d}"

def generateProgress(trackLength: int, progress: int) -> str:
    progressBar = "".join(["○" if i == round(((progress / trackLength) * 100) / 10) else "―" for i in range(11)])

    return f"[{progressBar}] ({formatTime(progress)}/{formatTime(trackLength)})"

def clearScreen() -> None:
    os("cls" if OSName == "nt" else "clear", shell=True)

if __name__ == "__main__":
    run("lyric2serial-server:api", host="127.0.0.1", port=5055, reload=False, log_level="Critical")