import urllib.request

# 1. Your dynamic M3U links
m3u_sources = [
    "https://www.apsattv.com/localnow.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/tcl-playlist-generator/refs/heads/main/tcl.m3u8",
    "https://raw.githubusercontent.com/BuddyChewChew/airy-playlist-generator/main/airy_channels.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/lg-playlist-generator/refs/heads/main/lg_channels_us.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/sports/refs/heads/main/liveeventsfilter.m3u8",
    "https://raw.githubusercontent.com/BuddyChewChew/plex/main/playlists/plex_all.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/RakutenTV/main/playlist.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plutotv_all.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/xumo-playlist-generator/refs/heads/main/playlists/xumo_playlist.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/tubi-scraper/refs/heads/main/tubi_playlist.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/main/playlists/samsungtvplus_all.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/main/playlists/roku_all.m3u"
]

# 2. Dedicated EPG XML links for every network
epg_sources = [
    "https://epgshare01.online/epgshare01/epg_ripper_ALL_SOURCES1.xml.gz",
    "https://raw.githubusercontent.com/BuddyChewChew/localnow-playlist-generator/refs/heads/main/epg.xml",
    "https://raw.githubusercontent.com/BuddyChewChew/pluto/main/pluto_all_epg.xml",
    "https://raw.githubusercontent.com/BuddyChewChew/tubi-scraper/refs/heads/main/tubi_epg.xml",
    "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/main/epgs/samsungtvplus_all_epg.xml",
    "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/main/epgs/roku_all_epg.xml",
    "https://raw.githubusercontent.com/BuddyChewChew/plex/main/epgs/plex_all_epg.xml",
    "https://raw.githubusercontent.com/BuddyChewChew/xumo-playlist-generator/refs/heads/main/epg.xml",
    "https://raw.githubusercontent.com/BuddyChewChew/lg-playlist-generator/refs/heads/main/lg_epg_us.xml",
    "https://raw.githubusercontent.com/BuddyChewChew/tcl-playlist-generator/refs/heads/main/epg.xml",
    "https://raw.githubusercontent.com/BuddyChewChew/airy-playlist-generator/main/airy_epg.xml"
]

epg_string = ",".join(epg_sources)
master_playlist = f'#EXTM3U x-tvg-url="{epg_string}"\n'

for url in m3u_sources:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            for line in content.splitlines():
                if not line.startswith("#EXTM3U"):
                    master_playlist += line + "\n"
    except Exception as e:
        print(f"Error reading {url}: {e}")

with open("master.m3u", "w", encoding="utf-8") as f:
    f.write(master_playlist)
