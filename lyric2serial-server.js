//region Imports and vars
const express = require("express");
const api = express();
//endregion Imports and vars

//region API
api.get("/lyric", (req, res) => {
    // Set variables based on get request information
    const artist = req.query.ar;
    const album = req.query.al;
    const albumCover = req.query.ac;
    const track = req.query.t;
    const currentLyric = req.query.cl;
    const previousLyric = req.query.pl;
    const nextLyric = req.query.nl;
    const progress = req.query.p;
    const trackLength = req.query.tl;

    // Make sure we have all parameters, and send error if we don't (not that the client knows what to do with this, mainly for other services trying to access it)
    if (!artist || !album || !albumCover || !track || currentLyric === undefined || previousLyric === undefined || nextLyric === undefined || !progress || !trackLength) {
        res.status(400).send("Malformed data");
    } else {
        if (artist == "") return; // Probably havent actually started a song yet
        res.status(200).send("OK");
        console.clear();
        console.log("Artist:\t" + artist);
        console.log("Album:\t" + album + " (" + albumCover + ')');
        console.log("Track:\t" + track);
        console.log(generateProgress(trackLength, progress));
        console.log("");
        
        // Dim/brighten lyrics, may not work on all terminals
        console.log("\x1b[2m%s\x1b[0m", previousLyric);
        console.log("\x1b[1m%s\x1b[0m", currentLyric);
        console.log("\x1b[2m%s\x1b[0m", nextLyric);
    }
});
//endregion API

//region Functions
function formatTime(ms) {
    const minutes = Math.floor(ms / 60000);
    const seconds = Math.floor((ms % 60000) / 1000);

    const formattedSeconds = seconds.toString().padStart(2, '0');

    return `${minutes}:${formattedSeconds}`;
}

function generateProgress(trackLength, progress) {
    // Generates a progress bar with neat ASCII symbols, pretty cool!
    progressBar = [];
    for (i = 0; i <= 10; i++) {
        if (i == Math.round(((progress / trackLength) * 100) / 10)) {
            progressBar.push('○');
        } else {
            progressBar.push('―');
        }
    }
    
    return '[' + (progressBar.join('')) + "] (" + formatTime(progress) + '/' + formatTime(trackLength) + ')';
}
//endregion Functions

api.listen(5005, () => {
    console.log("Listening on port: 5005");
});