from pyvod import Collection
from os.path import join, dirname, basename
from mycroft.skills.core import intent_file_handler
from pyvod import Collection, Media
from os.path import join, dirname, basename
from ovos_workshop.frameworks.playback import CommonPlayMediaType, CommonPlayPlaybackType, \
    CommonPlayMatchConfidence
from ovos_workshop.skills.video_collection import VideoCollectionSkill
import biblioteca


class BlackMetalSkill(VideoCollectionSkill):

    def __init__(self):
        super().__init__("TRVEKVLT")
        self.default_image = join(dirname(__file__), "ui", "bg.png")
        self.skill_logo = join(dirname(__file__), "ui", "trvekvlt_icon.png")
        self.skill_icon = join(dirname(__file__), "ui", "trvekvlt_icon.png")
        self.default_bg = join(dirname(__file__), "ui", "bg.png")
        self.message_namespace = basename(dirname(__file__)) + ".jarbasskills"
        self.supported_media = [CommonPlayMediaType.GENERIC,
                                CommonPlayMediaType.VIDEO,
                                CommonPlayMediaType.MUSIC]
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
                          "video") or media_type == CommonPlayMediaType.VIDEO:
            score += 1

        if self.voc_match(phrase,
                          "music") or media_type == CommonPlayMediaType.MUSIC:
            score += 10

        if self.voc_match(phrase, "trve"):
            score += 10

        if self.voc_match(phrase, "black-metal"):
            score += 50

        return score


def create_skill():
    return BlackMetalSkill()
