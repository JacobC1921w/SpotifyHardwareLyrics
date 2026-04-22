const express = require('express')
const api = express();
const listenPort = 5005;

api.get("/lyric", (req, res) => {
    const artist = req.query.ar;
    const album = req.query.al
    const track = req.query.t;
    const currentLyric = req.query.cl;
    const previousLyric = req.query.pl;
    const nextLyric = req.query.nl;
    const progress = req.query.p;
    const trackLength = req.query.tl;

    if (!artist || !album || !track || currentLyric === undefined || previousLyric === undefined || nextLyric === undefined || !progress || !trackLength) {
        res.status(400).send("Malformed data")
    } else {
        if (artist == "") return; // Probably havent actually started a song yet
        res.status(200).send("OK")
        console.clear()
        console.log("Artist:\t" + artist);
        console.log("Album:\t" + album)
        console.log("Track:\t" + track);
        console.log(generateProgress(trackLength, progress));
        console.log("")
        
        console.log("\x1b[2m%s\x1b[0m", previousLyric)
        console.log("\x1b[1m%s\x1b[0m", currentLyric)
        console.log("\x1b[2m%s\x1b[0m", nextLyric)
    }
})

function formatTime(ms) {
    const minutes = Math.floor(ms / 60000);
    const seconds = Math.floor((ms % 60000) / 1000);

    const formattedSeconds = seconds.toString().padStart(2, '0');

    return `${minutes}:${formattedSeconds}`;
}

function generateProgress(trackLength, progress) {
    progressBar = [];
    for (i = 0; i <= 10; i++) {
        if (i == Math.round(((progress / trackLength) * 100) / 10)) {
            progressBar.push("○")
        } else {
            progressBar.push('―')
        }
    }
    
    return '[' + (progressBar.join('')) + "] (" + formatTime(progress) + "/" + formatTime(trackLength) + ")";
}

api.listen(listenPort, () => {
    console.log("Listening on port: " + listenPort)
})