from pyvod import Collection
from os.path import join, dirname, basename
from ovos_utils.skills.templates.video_collection import VideoCollectionSkill
from mycroft.skills.core import intent_file_handler
from pyvod import Collection, Media
from os.path import join, dirname, basename
from ovos_utils.playback import CPSMatchType, CPSPlayback, CPSMatchConfidence


class BlackMetalSkill(VideoCollectionSkill):

    def __init__(self):
        super().__init__("TRVEKVLT")
        self.default_image = join(dirname(__file__), "ui", "bg.png")
        self.skill_logo = join(dirname(__file__), "ui", "trvekvlt_icon.png")
        self.skill_icon = join(dirname(__file__), "ui", "trvekvlt_icon.png")
        self.default_bg = join(dirname(__file__), "ui", "bg.png")
        self.message_namespace = basename(dirname(__file__)) + ".jarbasskills"
        self.supported_media = [CPSMatchType.GENERIC,
                                CPSMatchType.AUDIO,
                                CPSMatchType.VIDEO,
                                CPSMatchType.MUSIC]
        self.playback_type = CPSPlayback.AUDIO
        self.media_type = CPSMatchType.MUSIC
        path = join(dirname(__file__), "res", "trveKvlt.jsondb")
        # load video catalog
        self.settings["match_description"] = True
        self.settings["match_tags"] = True
        self.media_collection = Collection("trveKvlt",
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
                          "video") or media_type == CPSMatchType.VIDEO:
            score += 1

        if self.voc_match(phrase,
                          "music") or media_type == CPSMatchType.MUSIC:
            score += 10

        if self.voc_match(phrase, "trve"):
            score += 10

        if self.voc_match(phrase, "black-metal"):
            score += 70
            self.CPS_extend_timeout(0.5)

        return score


def create_skill():
    return BlackMetalSkill()
