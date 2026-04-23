// The async modifier allows for the user of await, which converts a promise into an object, when not using await, async is not necessary.
(async function lyric2serial() {
    const { Platform, Player } = Spicetify;
    if (!Player || !Platform) {
        setTimeout(lyric2serial, 300);
        return;
    }
    
    let currentLyrics = [];
    let lastLyric;

    
    let artist
    let album
    let track
    let currentLyric
    let previousLyric
    let nextLyric
    let progress
    let trackLength

    Player.addEventListener("songchange", async () => {
        const data = Spicetify.Player.data.item;
        const query = `https://lrclib.net/api/get?artist_name=${encodeURIComponent(data.artists[0].name)}&track_name=${encodeURIComponent(data.name)}`;

        currentLyrics = [];
        artist = data.artists[0].name
        album = data.album.name
        track = data.name
        trackLength = Player.getDuration()
        
        try {
            const res = await fetch(query);
            const json = await res.json();
            // Parse syncedLyrics into an array of {time, text}
            let currentLyricsArray = json.syncedLyrics.split('\n')
            for (lyric of currentLyricsArray) {
                let timestamp = lyric.substring((lyric.indexOf('[') + 1), (lyric.indexOf(']')))

                const [minutes, seconds, ms] = timestamp.split(/[:.]/)
                timestamp = (parseInt(minutes) * 60000) + (parseInt(seconds) * 1000) + (parseInt((ms || '0').padEnd(3, '0')))

                lyric = lyric.substring((lyric.indexOf(']') + 2), lyric.length)

                currentLyrics.push([timestamp, lyric])
            }
        } catch (e) {
            currentLyrics = [[0, "Couldn't find lyrics :p"]];
        }
    });

    setInterval(() => {
        if (!currentLyrics.length) return;
        progress = Player.getProgress();

        if (progress < currentLyrics[0][0]) {
            sendRequest(artist, album, track, "", "", currentLyrics[0][1], progress, trackLength);
        } else {        
            const currentIndex = currentLyrics.findLastIndex(item => item[0] <= progress);

            if (currentIndex !== -1) {
                const match = currentLyrics[currentIndex];
                currentLyric = match[1] ? match[1] : "♪";
                
                previousLyric = currentLyrics[currentIndex - 1] ? currentLyrics[currentIndex - 1][1] : "♪";
                nextLyric = currentLyrics[currentIndex + 1] ? currentLyrics[currentIndex + 1][1] : "♪";

                sendRequest(artist, album, track, currentLyric, nextLyric, previousLyric, progress, trackLength);
            }
        }
    }, 500);
})();

async function sendRequest(artist, album, track, currentLyric, nextLyric, previousLyric, progress, trackLength) {
    await fetch(`http://127.0.0.1:5005/lyric?ar=${artist}&al=${album}&t=${track}&cl=${currentLyric}&pl=${previousLyric}&nl=${nextLyric}&p=${progress}&tl=${trackLength}`, {
        mode: 'no-cors'
    });
}