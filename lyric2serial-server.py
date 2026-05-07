from threading import Thread
from uvicorn import run
from fastapi import FastAPI
from tkinter import Tk, Label

api = FastAPI()

class Overlay:
    def __init__(self):
        self.root = Tk()
        self.root.overrideredirect(True)
        self.root.geometry("+10+10")
        self.root.lift()
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-disabled", True)
        self.root.wm_attributes("-toolwindow", True)
        self.root.config(bg="black")
        self.root.attributes("-alpha", 0.75)

        self.labels = {}
        fields = ["artist", "album", "track", "progress", "previousLyric", "currrentLyric", "nextLyric"]
        
        for field in fields:
            label = Label(self.root, text=f"{field}: ...", font=("Arial", 11, ("bold" if field == "currrentLyric" else "normal")), fg="white", bg="black", anchor='w', justify="left")
            label.pack(anchor='w', fill='x', padx=10)
            self.labels[field] = label

    def updateUI(self, data: dict[str, str]) -> None:
        self.labels["artist"].config(text=f"Artist: {data["ar"]}")
        self.labels["album"].config(text=f"Album: {data["al"]}")
        self.labels["track"].config(text=f"Track: {data['t']}")
        self.labels["progress"].config(text=data["progressString"])
        self.labels["previousLyric"].config(text=data["pl"])
        self.labels["currrentLyric"].config(text=data["cl"])
        self.labels["nextLyric"].config(text=data["nl"])

overlay = None

@api.get("/lyric")
async def parseQuery(ar: str, al: str, t: str, cl: str, pl: str, nl: str, p: str, tl: str) -> dict[str, str]:
    
    progressString = generateProgress(int(tl), int(p))
    
    data = { "ar": ar, "al": al, 't': t, "progressString": progressString, "pl": pl, "cl": cl, "nl": nl }
    
    if overlay:
        overlay.root.after(0, overlay.updateUI, data)
    
    return {"status": "OK"}

def generateProgress(trackLength: int, progress: int) -> str:
    minutes_p, seconds_p = divmod(progress // 1000, 60)
    minutes_t, seconds_t = divmod(trackLength // 1000, 60)
    percent = (progress / trackLength) if trackLength > 0 else 0
    dots = round(percent * 10)
    bar = "".join(['○' if i == dots else '―' for i in range(11)])
    return f"[{bar}] ({minutes_p}:{seconds_p:02d}/{minutes_t}:{seconds_t:02d})"

def runServer() -> None:
    run(api, host="127.0.0.1", port=5005, log_level="critical")

if __name__ == "__main__":
    serverThread = Thread(target=runServer, daemon=True)
    serverThread.start()

    overlay = Overlay()
    overlay.root.mainloop()