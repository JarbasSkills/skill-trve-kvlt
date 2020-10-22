from mycroft.skills.common_play_skill import CommonPlaySkill, \
    CPSMatchLevel, CPSTrackStatus, CPSMatchType
from mycroft.skills.core import intent_file_handler
from mycroft.util.parse import fuzzy_match, match_one
from pyvod import Collection, Media
from os.path import join, dirname
import random
from json_database import JsonStorageXDG


class BlackMetalSkill(CommonPlaySkill):

    def __init__(self):
        super().__init__("TRVEKVLT")
        self.supported_media = [CPSMatchType.GENERIC,
                                CPSMatchType.VIDEO,
                                CPSMatchType.MUSIC]

        path = join(dirname(__file__), "res", "trveKvlt.jsondb")
        # load video catalog
        self.blackmetal = Collection("trveKvlt",
                                     logo=join(dirname(__file__), "res",
                                               "trvekvlt_logo.png"),
                                     db_path=path)
        self.videos = [ch.as_json() for ch in self.blackmetal.entries]

    def initialize(self):
        self.add_event('skill-trve-kvlt.jarbasskills.home',
                       self.handle_homescreen)
        self.gui.register_handler("skill-trve-kvlt.jarbasskills.play_event",
                                  self.play_video_event)
        self.gui.register_handler(
            "skill-trve-kvlt.jarbasskills.clear_history",
            self.play_video_event)

    def get_intro_message(self):
        self.speak_dialog("intro")

    @intent_file_handler('trveKvltHome.intent')
    def handle_homescreen_utterance(self, message):
        self.handle_homescreen(message)

    # homescreen
    def handle_homescreen(self, message):
        self.gui.clear()
        random.shuffle(self.videos)
        self.gui["mytvtogoHomeModel"] = self.videos[:500]
        self.gui["historyModel"] = JsonStorageXDG("trve-kvlt-history").get("model", [])
        self.gui.show_page("Homescreen.qml", override_idle=True)

    # play via GUI event
    def play_video_event(self, message):
        video_data = message.data["modelData"]
        self.play_blackmetal(video_data)

    # clear history event
    def clear_history_event(self, message):
        self.historyDB.clear()

    # common play
    def play_blackmetal(self, video_data):
        if not self.gui.connected:
            self.log.error("GUI is required for BlackMetal skill, "
                           "but no GUI connection was detected")
        # add to playback history
        historyDB = JsonStorageXDG("trve-kvlt-history")
        if "model" not in historyDB:
            historyDB["model"] = []
        historyDB["model"].append(video_data)
        historyDB.store()

        self.gui["historyModel"] = historyDB["model"]
        # play video
        video = Media.from_json(video_data)
        url = str(video.streams[0])
        self.gui.play_video(url, video.name)

    def match_media_type(self, phrase, media_type):
        match = None
        score = 0

        if self.voc_match(phrase,
                          "video") or media_type == CPSMatchType.VIDEO:
            score += 0.1
            match = CPSMatchLevel.GENERIC

        if self.voc_match(phrase,
                          "music") or media_type == CPSMatchType.MUSIC:
            score += 0.1
            match = CPSMatchLevel.CATEGORY

        if self.voc_match(phrase, "trve"):
            score += 0.1
            match = CPSMatchLevel.CATEGORY

        if self.voc_match(phrase, "black-metal"):
            score += 0.2
            match = CPSMatchLevel.TITLE

        return match, score

    def CPS_match_query_phrase(self, phrase, media_type):
        leftover_text = phrase
        best_score = 0

        # see if media type is in query, base_score will depend if "scifi"
        # or "video" is in query
        match, base_score = self.match_media_type(phrase, media_type)

        videos = list(self.videos)

        best_video = random.choice(videos)

        # score video data
        for ch in videos:
            score = 0
            # score tags
            tags = list(set(ch.get("tags", [])))
            if tags:
                # tag match bonus
                for tag in tags:
                    if not tag:
                        continue
                    tag = tag.lower().strip()
                    if tag in phrase:
                        match = CPSMatchLevel.CATEGORY
                        score += 0.1
                        leftover_text = leftover_text.replace(tag, "")

            # score description
            words = ch.get("description", "").split(" ")
            for word in words:
                if len(word) > 4 and word in leftover_text:
                    score += 0.05

            if score > best_score:
                best_video = ch
                best_score = score

        # match video name
        for ch in videos:
            title = ch["title"]

            score = fuzzy_match(leftover_text, title)
            if score >= best_score:
                # TODO handle ties
                match = CPSMatchLevel.TITLE
                best_video = ch
                best_score = score
                leftover_text = title

        if not best_video:
            self.log.debug("No BlackMetal matches")
            return None

        if best_score < 0.6:
            self.log.debug("Low score, randomizing results")
            best_video = random.choice(videos)

        score = base_score + best_score

        if self.voc_match(phrase, "black-metal"):
            score += 0.15
        if self.voc_match(phrase, "trve"):
            score += 0.1

        if score >= 0.85:
            match = CPSMatchLevel.EXACT
        elif score >= 0.7:
            match = CPSMatchLevel.MULTI_KEY
        elif score >= 0.5:
            match = CPSMatchLevel.TITLE

        self.log.debug("Best BlackMetal video: " + best_video["title"])

        if match is not None:
            return (leftover_text, match, best_video)
        return None

    def CPS_start(self, phrase, data):
        self.play_blackmetal(data)


def create_skill():
    return BlackMetalSkill()

path = join(dirname(__file__), "res", "trveKvlt.jsondb")
# load video catalog
blackmetal = Collection("trveKvlt",
                             logo=join(dirname(__file__), "res",
                                       "trvekvlt_logo.png"),
                             db_path=path)
videos = [ch.as_json() for ch in blackmetal.entries]