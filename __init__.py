import random
from os.path import join, dirname

from ovos_plugin_common_play.ocp import MediaType, PlaybackType
from ovos_utils.log import LOG
from ovos_workshop.skills.common_play import OVOSCommonPlaybackSkill, \
    ocp_search, ocp_featured_media
from youtube_archivist import YoutubeMonitor


class BlackMetalSkill(OVOSCommonPlaybackSkill):

    def __init__(self):
        super().__init__("TRVEKVLT")
        self.skill_icon = join(dirname(__file__), "ui", "trvekvlt_icon.png")
        self.default_bg = join(dirname(__file__), "ui", "bg.png")
        self.supported_media = [MediaType.GENERIC,
                                MediaType.AUDIO,
                                MediaType.MUSIC]
        self.archive = YoutubeMonitor(db_name="TrveKvlt", logger=LOG)

    def initialize(self):
        bootstrap = f"https://github.com/JarbasSkills/skill-trve-kvlt/raw/dev/bootstrap.json"
        self.archive.bootstrap_from_url(bootstrap)
        self.schedule_event(self._sync_db, random.randint(3600, 24 * 3600))

    def _sync_db(self):
        urls = [
            "https://www.youtube.com/watch?v=kU0pOmzj70o",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfWTRkRauhAjPh0h3ddMJin0",
            "https://www.youtube.com/playlist?list=PLoul9rkF5MasLz-yl4ZLXymHkYrpFz7Bs",
            "https://www.youtube.com/playlist?list=PLnFvfzGgiy7_3Hk2ikc6vd4HvzSdp7ft6",
            "https://www.youtube.com/user/NihiLizTikVoiD",
            "https://www.youtube.com/user/Adnan3098",
            "https://www.youtube.com/c/Werwolf/videos",
            "https://www.youtube.com/watch?v=7njdEm4-7MU",
            "https://www.youtube.com/watch?v=uNtO0_CYeaI",
            "https://www.youtube.com/playlist?list=PLbkph_GtwePZmD-bruvFbuaDnmIJMBjyZ",
            "https://www.youtube.com/playlist?list=PLm7wnjUQm_FC0AClRhesJXfviQ0A4IvPq",
            "https://www.youtube.com/channel/UCVEf05n0AptM-N1RzeYJn-g/videos",
            "https://www.youtube.com/channel/UCJs_uIwVoNCKZAQ5jDqTlkw/videos",
            "https://www.youtube.com/c/NoSolace/videos",
            "https://www.youtube.com/watch?v=UGOwy3fgnUE",
            "https://www.youtube.com/c/AtmosphericBlackMetalAlbumsOfficial/videos",
            "https://www.youtube.com/c/666unholymartyr666/videos",
            "https://www.youtube.com/playlist?list=OLAK5uy_kQ_YuC4aoOYiblVOXDKOzglBELweOtfyM",
            "https://www.youtube.com/playlist?list=OLAK5uy_kUM73tmSd1Ds20-R1DDHUXG1UXaGYRmBw",
            "https://www.youtube.com/playlist?list=PLJmjhSfzVjAMadhqNAs_PznWhKDyxnxtd",
            "https://www.youtube.com/playlist?list=PLJmjhSfzVjAPijd95sOH3x9bzMIxloz8j",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfW6kmo4Io16o9eCpsR1fe7R",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfUOPubujWEeh1fMJnL9DWSi",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfUZpRNS4O72txUzPW6NQCOO",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfUkXyyncMaTokT27WdkyMYg",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfXXqr1QWJ_h3l4RTrPlgxAv",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfXjYUvYqzvQLVPFMSFTUabS",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfVbG03H0pw72T623z4rSXmb",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfXEkgCh0X-KY62chUVAgRSH",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfWHT_OQmnnkj3FnwTR5xYtk",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfW8utcSHKtDudFjqTSX82yf",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfUONxfFCEGKCi4Uq676skR7",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfV18spo8YlL0Ayu9MqVrxKx",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfUHYqFB5HnY5uhYSKPSYBnQ",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfXxVouOUh_GZjLJP9_Esgig",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfWLSZlBqixP54DoTrrPPn_F",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfVKfruimJtofLGX-tUGlhWT",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfXywfjIDudxv5Dwe_R1kHCI",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfUAUmsV4qcyDbBuvE2qO57V",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfVjl_ar1Jto9lQlr5zRiq21",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfUJBLyMV6upmrMOVNDtBuWt",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfUcCDcAKE_SqPMg5vfRjD1h",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfVU2JYRqzT4fttLCqmn9h1u",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfWTLQqFMFHLNdNMWXEzfCRt",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfWmlKgInvh5t6QzmAMmkJQu",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfWfPJCBPs6Jjj8NqgoOI-4o",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfUB1RJOUUq_Za4kKeToEmsA",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfVzMTtxPb1ny4L4cBdNgF2J",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfXvQGPDKyqnyuKYJu3XHYVT",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfW6E5-g9kJy1y7LKO6veU4w",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfVJOEE550anPrXbl0mdRcS3",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfX1wBNu-xzWrXnIIcta2kMq",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfVypjq7JW-Ep3iceVoaHfW4",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfWFUqmxptBtKc9gT9bhRzRz",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfUwGEasW2T_DLGPFj6E-EgZ",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfVwSNl_ZYDK4Iq3MPKf2jNE",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfWzxSRA1kRmIOnqCr6k69bG",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfVfdKf7bgQ-4kAQ2_N2JBSB",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfUcaEY9lsaZ3meoVzY1M97O",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfUkkzHxv_aSHAHCqLaGz_Mn",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfVrinRqF5sLNXOEHUIqqwf0",
            "https://www.youtube.com/playlist?list=PLykNNMVjCDfUKFWDRi6mc4M7FA4eCjGaT",
            "https://www.youtube.com/watch?v=rSHf81j_PQE",
            "https://www.youtube.com/watch?v=ChGALXClzH4",
            "https://www.youtube.com/watch?v=MiCLnDDZ4w0",
            "https://www.youtube.com/watch?v=BJAnJ8b6q5M",
            "https://www.youtube.com/watch?v=D50XrYiinNc",
            "https://www.youtube.com/c/bmpromotion/videos",
        ]
        for url in urls:
            self.archive.parse_videos(url)
        self.schedule_event(self._sync_db, random.randint(3600, 24*3600))

    # matching
    def match_skill(self, phrase, media_type):
        score = 0
        if self.voc_match(phrase, "music") or media_type == MediaType.MUSIC:
            score += 10
        if self.voc_match(phrase, "trve"):
            score += 10
        if self.voc_match(phrase, "black-metal"):
            score += 90
        return score

    def get_playlist(self, score=50, num_entries=100, idx=1):
        entries = list(self.archive.db.items())
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
        base_score = self.match_skill(phrase, media_type)
        if base_score >= 50:
            for i in range(5):
                yield self.get_playlist(base_score, idx=i + 1)

    @ocp_featured_media()
    def featured_media(self, num_entries=250):
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
                   } for entry in self.archive.sorted_entries()
               ][:num_entries]


def create_skill():
    return BlackMetalSkill()
