import gzip
import urllib.request
import xml.etree.ElementTree as ET

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

# 1. Combine M3U Playlists
master_playlist = '#EXTM3U x-tvg-url="epg.xml"\n'

for url in m3u_sources:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8', errors='ignore')
            for line in content.splitlines():
                if not line.startswith("#EXTM3U"):
                    master_playlist += line + "\n"
    except Exception as e:
        print(f"Error reading M3U {url}: {e}")

with open("master.m3u", "w", encoding="utf-8") as f:
    f.write(master_playlist)

# 2. Combine all EPG XML Files into a Single XML Document
merged_tv = ET.Element("tv")

for url in epg_sources:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read()
            
            # Decompress if gzipped (.gz)
            if url.endswith(".gz") or content[:2] == b'\x1f\x8b':
                content = gzip.decompress(content)
                
            root = ET.fromstring(content)
            for child in root:
                if child.tag in ["channel", "programme"]:
                    merged_tv.append(child)
    except Exception as e:
        print(f"Error processing EPG {url}: {e}")

tree = ET.ElementTree(merged_tv)
tree.write("epg.xml", encoding="utf-8", xml_declaration=True)
