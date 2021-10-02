from os.path import join, dirname, basename

import biblioteca
from mycroft.skills.core import intent_file_handler
from ovos_plugin_common_play.ocp import MediaType
from ovos_workshop.skills.video_collection import VideoCollectionSkill
from pyvod import Collection


class BlackMetalSkill(VideoCollectionSkill):

    def __init__(self):
        super().__init__("TRVEKVLT")
        self.default_image = join(dirname(__file__), "ui", "bg.png")
        self.skill_logo = join(dirname(__file__), "ui", "trvekvlt_icon.png")
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
                                           logo=self.skill_logo, db_path=path)

    def get_intro_message(self):
        self.speak_dialog("intro")

    @intent_file_handler('home.intent')
    def handle_homescreen_utterance(self, message):
        self.handle_homescreen(message)

    # matching
    def match_media_type(self, phrase, media_type):
        score = 0

        if self.voc_match(phrase,
                          "video") or media_type == MediaType.VIDEO:
            score += 1

        if self.voc_match(phrase,
                          "music") or media_type == MediaType.MUSIC:
            score += 10

        if self.voc_match(phrase, "trve"):
            score += 10

        if self.voc_match(phrase, "black-metal"):
            score += 50

        return score


def create_skill():
    return BlackMetalSkill()
