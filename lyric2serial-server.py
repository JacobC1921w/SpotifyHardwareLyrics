# Appologies for the type hinting, i'm a big fan of it in Python and its my program :p

#region Imports
# Notice how I only import exactly what I need? Not sure how much time this saves, but in previous projects using OpenCV this was a lifechanger!
from threading import Thread
from uvicorn import run
from fastapi import FastAPI
from tkinter import Tk, Label, Frame
from PIL import Image, ImageTk
from io import BytesIO
from requests import get
from ctypes import windll
#endregion Imports

api = FastAPI()

#region TK overlay class
# I hate OOB ;(
class Overlay:
    def __init__(self):
        # Window attributes. Basically we want the window to be on the top at all times and not show up in ALT+TAB menu to make it look nicer. Also setup transparency
        self.root = Tk()
        self.root.overrideredirect(True)
        self.root.geometry("+10+10")
        self.root.lift()
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-disabled", True)
        self.root.wm_attributes("-toolwindow", True)
        self.root.config(bg="black")
        self.root.attributes("-alpha", 0.6)

        self.mainContainer = Frame(self.root, bg="black", padx=0, pady=0, highlightthickness=0)
        self.mainContainer.pack()

        self.imageLabel = Label(self.mainContainer, bg="black", borderwidth=0, highlightthickness=0)
        self.imageLabel.pack(side="left", padx=0, pady=0)

        self.textContainer = Frame(self.mainContainer, bg="black", padx=0, pady=0, highlightthickness=0)
        self.textContainer.pack(side="left", fill="both", expand=True)

        self.makeClickThrough()

        self.labels = {}
        self.currentAlbumCoverUrl = ""
        fields = ["artist", "album", "track", "progress", "previousLyric", "currrentLyric", "nextLyric"]

        # Initialize some labels        
        for field in fields:
            # Setting pady=0 here ensures there is no vertical gap between labels
            label = Label(self.textContainer, text=f"{field}: ...", 
                          font=("Arial", 11, ("bold" if field == "currrentLyric" else "normal")), 
                          fg="white", bg="black", anchor='w', justify="left", highlightthickness=0)
            label.pack(anchor='w', fill='x', padx=(10, 10), pady=0)
            self.labels[field] = label

    # Im not gonna lie i used AI to help with this because I was lost :( - image stuff is funky, im more of a network guy
    def updateImage(self, url: str) -> None:
        if url == self.currentAlbumCoverUrl:
            return
        
        try:
            response = get(url, timeout=5)
            imgData = BytesIO(response.content)
            img = Image.open(imgData)

            self.root.update_idletasks()
            targetHeight = self.textContainer.winfo_height()
            
            if targetHeight < 10:
                targetHeight = 154

            img = img.resize((targetHeight, targetHeight), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            self.imageLabel.config(image=photo)
            self.imageLabel.image = photo 
            self.currentAlbumCoverUrl = url
        except:
            pass

    # Also used AI for this sorry I know it sucks and i genuinely feel bad about it but I'm being transparent about it completely    
    def makeClickThrough(self) -> None:
        # Get the window handle (HWND)
        hwnd = windll.user32.GetParent(self.root.winfo_id())
        
        # Define Windows Constants
        GWL_EXSTYLE = -20
        WS_EX_LAYERED = 0x80000
        WS_EX_TRANSPARENT = 0x20
        
        # Get current styles and add the Layered and Transparent flags
        style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style |= WS_EX_LAYERED | WS_EX_TRANSPARENT
        
        # Apply the new style
        windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)

    # We use this to update the labels lol
    def updateUI(self, data: dict[str, str]) -> None:
        self.labels["artist"].config(text=f"Artist:\t{data["ar"]}")
        self.labels["album"].config(text=f"Album:\t{data["al"]}")
        self.labels["track"].config(text=f"Track:\t{data['t']}")
        self.labels["progress"].config(text=data["progressString"])
        self.labels["previousLyric"].config(text=data["pl"])
        self.labels["currrentLyric"].config(text=data["cl"])
        self.labels["nextLyric"].config(text=data["nl"])
        
        if data["ac"]:
            self.updateImage(data["ac"])
#endregion TK overlay class

overlay = None

#region API
@api.get("/lyric")
async def parseQuery(ar: str, al: str, ac: str, t: str, cl: str, pl: str, nl: str, p: str, tl: str) -> dict[str, str]:
    
    progressString = generateProgress(int(tl), int(p))
    
    data = { "ar": ar, "al": al, "ac": ac, 't': t, "progressString": progressString, "pl": pl, "cl": cl, "nl": nl }
    
    if overlay:
        overlay.root.after(0, overlay.updateUI, data)
    
    return {"status": "OK"}
#endregion API

#region Functions
def generateProgress(trackLength: int, progress: int) -> str:
    minutes_p, seconds_p = divmod(progress // 1000, 60)
    minutes_t, seconds_t = divmod(trackLength // 1000, 60)
    percent = (progress / trackLength) if trackLength > 0 else 0
    dots = round(percent * 10)
    bar = "".join(['○' if i == dots else '―' for i in range(11)])
    return f"[{bar}] ({minutes_p}:{seconds_p:02d}/{minutes_t}:{seconds_t:02d})"

def runServer() -> None:
    run(api, host="127.0.0.1", port=5005, log_level="critical")
#endregion Functions

if __name__ == "__main__":
    # This is just a little "hack" so that we can run the pprogram without having to use the uvicorn command. Also seperate threads because multithreadin is sick in Python
    serverThread = Thread(target=runServer, daemon=True)
    serverThread.start()

    overlay = Overlay()
    try:
        overlay.root.mainloop()
    except KeyboardInterrupt:
        exit(0)