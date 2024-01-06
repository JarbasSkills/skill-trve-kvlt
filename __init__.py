import random
from os.path import join, dirname

import requests
from json_database import JsonStorageXDG

from ovos_utils.ocp import MediaType, PlaybackType
from ovos_workshop.decorators.ocp import ocp_search, ocp_featured_media
from ovos_workshop.skills.common_play import OVOSCommonPlaybackSkill


class BlackMetalSkill(OVOSCommonPlaybackSkill):

    def __init__(self, *args, **kwargs):
        self.skill_icon = join(dirname(__file__), "ui", "trvekvlt_icon.png")
        self.default_bg = join(dirname(__file__), "ui", "bg.png")
        self.supported_media = [MediaType.AUDIO,
                                MediaType.MUSIC]
        self.archive = JsonStorageXDG("TrveKvlt", subfolder="OCP")
        super().__init__(*args, **kwargs)

    def initialize(self):
        self._sync_db()
        self.load_ocp_keywords()

    def load_ocp_keywords(self):
        albums = []
        artists = []
        songs = []
        genre = ["Black Metal"]

        for url, data in self.archive.items():
            t = data["title"].split("(")[0].split("|")[0].split("[")[0].strip() \
                .replace("‎-", "-")
            if "-" in t:
                artist, title = t.split("-")[:2]
                artists.append(artist.strip())
                if "album" in data["title"].lower():
                    albums.append(title.strip())
                else:
                    songs.append(title.strip())

        self.register_ocp_keyword(MediaType.MUSIC,
                                  "artist_name", artists)
        self.register_ocp_keyword(MediaType.MUSIC,
                                  "album_name", albums)
        self.register_ocp_keyword(MediaType.MUSIC,
                                  "music_genre", genre)
        self.register_ocp_keyword(MediaType.MUSIC,
                                  "song_name", songs)

    def _sync_db(self, message=None):
        bootstrap = f"https://github.com/JarbasSkills/skill-trve-kvlt/raw/dev/bootstrap.json"
        data = requests.get(bootstrap).json()
        self.archive.merge(data)
        self.schedule_event(self._sync_db, random.randint(3600, 24 * 3600))

    def get_playlist(self, score=50, num_entries=100, idx=1):
        entries = list(self.archive.items())
        random.shuffle(entries)
        entries = entries[:num_entries]
        pl = [{
            "title": video["title"],
            "image": video["thumbnail"],
            "match_confidence": 70,
            "media_type": MediaType.MUSIC,
            "uri": "youtube//" + url,
            "playback": PlaybackType.AUDIO,
            "skill_icon": self.skill_icon,
            "bg_image": video["thumbnail"],
            "skill_id": self.skill_id
        } for url, video in entries]
        return {
            "match_confidence": score,
            "media_type": MediaType.MUSIC,
            "playlist": pl,
            "playback": PlaybackType.AUDIO,
            "skill_icon": self.skill_icon,
            "image": self.skill_icon,
            "bg_image": self.default_bg,
            "title": f"Black Metal Mix {idx}"
        }

    @ocp_search()
    def search_db(self, phrase, media_type):
        base_score = 15 if media_type == MediaType.MUSIC else 0
        entities = self.ocp_voc_match(phrase)

        base_score += 30 * len(entities)

        candidates = list(self.archive.values())
        artist = entities.get("artist_name")
        album = entities.get("album_name")
        song = entities.get("song_name")

        if artist or song or album:
            # filter valid results
            if album:
                candidates = [video for video in candidates
                              if album.lower() in video["title"].lower()]
            elif artist:
                candidates = [video for video in candidates
                              if artist.lower() in video["title"].lower()]
            elif song:
                candidates = [video for video in candidates
                              if song.lower() in video["title"].lower()]

            for video in candidates:
                yield {
                    "title": video["title"],
                    "author": artist or video["author"],
                    "album": album,
                    "match_confidence": min(100, base_score),
                    "media_type": MediaType.MUSIC,
                    "uri": "youtube//" + video["url"],
                    "playback": PlaybackType.AUDIO,
                    "skill_icon": self.skill_icon,
                    "skill_id": self.skill_id,
                    "image": video["thumbnail"],
                    "bg_image": self.default_bg
                }

        # black metal playlists on black metal request
        if "music_genre" in entities:
            for i in range(5):
                yield self.get_playlist(base_score, idx=i + 1)

    @ocp_featured_media()
    def featured_media(self, num_entries=50):
        return [
                   {
                       "match_confidence": 100,
                       "media_type": MediaType.MUSIC,
                       "uri": "youtube//" + entry["url"],
                       "playback": PlaybackType.AUDIO,
                       "image": entry["thumbnail"],
                       "length": entry.get("duration", 0) * 1000,
                       "bg_image": self.default_bg,
                       "skill_icon": self.skill_icon,
                       "title": entry["title"]
                   } for entry in self.archive.values()
               ][:num_entries]


if __name__ == "__main__":
    from ovos_utils.messagebus import FakeBus

    s = BlackMetalSkill(bus=FakeBus(), skill_id="t.fake")
    for r in s.search_db("burzum", MediaType.MUSIC):
        print(r)

    for r in s.search_db("xasthur", MediaType.MUSIC):
        print(r)
