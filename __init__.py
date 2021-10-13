from os.path import join, dirname, basename

import biblioteca
from mycroft.skills.core import intent_file_handler
from ovos_plugin_common_play.ocp import MediaType, PlaybackType
from ovos_workshop.skills.common_play import ocp_search
from ovos_workshop.skills.video_collection import VideoCollectionSkill
from pyvod import Collection
import random


class BlackMetalSkill(VideoCollectionSkill):

    def __init__(self):
        super().__init__("TRVEKVLT")
        self.default_image = join(dirname(__file__), "ui", "bg.png")
        self.skill_icon = join(dirname(__file__), "ui", "trvekvlt_icon.png")
        self.default_bg = join(dirname(__file__), "ui", "bg.png")
        self.message_namespace = basename(dirname(__file__)) + ".jarbasskills"
        self.supported_media = [MediaType.GENERIC,
                                MediaType.VIDEO,
                                MediaType.MUSIC]
        base_folder = biblioteca.download("ytcat_trveKvlt")
        path = join(base_folder, "trveKvlt.jsondb")
        # load video catalog
        self.media_collection = Collection("TrveKvlt",
                                           logo=self.skill_icon, db_path=path)
        self.n_mixes = 3

    @intent_file_handler('home.intent')
    def handle_homescreen_utterance(self, message):
        self.handle_homescreen(message)

    # matching
    def get_base_score(self, phrase):
        score = 0

        if self.voc_match(phrase, "trve"):
            score += 15

        if self.voc_match(phrase, "black-metal"):
            score += 70

        return score

    @ocp_search()
    def ocp_blackmetal(self, phrase):
        if self.voc_match(phrase, "black-metal", exact=True):
            score = 100
        else:
            score = self.get_base_score(phrase)

        if score < 50:
            return
        pl = [
            {
                "match_confidence": score,
                "media_type": MediaType.MUSIC,
                "uri": "youtube//" + entry["url"],
                "playback": PlaybackType.AUDIO,
                "image": entry["logo"],
                "bg_image": self.default_bg,
                "skill_icon": self.skill_icon,
                "title": entry["title"]
            } for entry in self.videos  # VideoCollectionSkill property
        ]
        for i in range(self.n_mixes):
            random.shuffle(pl)
            yield {
                "match_confidence": score,
                "media_type": MediaType.MUSIC,
                "playlist": pl[:50],
                "playback": PlaybackType.AUDIO,
                "skill_icon": self.skill_icon,
                "image": self.skill_icon,
                "bg_image": self.default_bg,
                "title": f"Trve Kvlt Black Metal (Mix {i + 1})"
            }


def create_skill():
    return BlackMetalSkill()
