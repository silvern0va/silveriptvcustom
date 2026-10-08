import gzip
import urllib.request
import xml.etree.ElementTree as ET
import re
import tempfile
import shutil

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
    "https://raw.githubusercontent.com/BuddyChewChew/localnow-playlist-generator/refs/heads/main/epg.xml"
]

# Point the master playlist to the new compressed file
master_playlist = '#EXTM3U x-tvg-url="epg.xml.gz"\n'
valid_ids = set()

print("Merging M3U lists and extracting valid IDs...")
for url in m3u_sources:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8', errors='ignore')
            for line in content.splitlines():
import gzip
import urllib.request
import xml.etree.ElementTree as ET
import re
import tempfile
import shutil

# Updated list focused strictly on US and non-geoblocked international lists
m3u_sources = [
    "https://i.mjh.nz/SamsungTVPlus/us.m3u8",
    "https://raw.githubusercontent.com/BuddyChewChew/tubi-scraper/refs/heads/main/tubi_playlist.m3u",
    "https://www.apsattv.com/localnow.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/roku-playlist-generator/refs/heads/main/roku.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/xumo-playlist-generator/refs/heads/main/playlists/xumo_playlist.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/lg-playlist-generator/refs/heads/main/lg_channels_us.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/airy-playlist-generator/main/airy_channels.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/tcl-playlist-generator/refs/heads/main/tcl.m3u8",
    "https://raw.githubusercontent.com/BuddyChewChew/pluto/main/pluto_us.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/sports/refs/heads/main/liveeventsfilter.m3u8",
    "https://raw.githubusercontent.com/BuddyChewChew/plex/main/playlists/plex_us.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/plex/main/playlists/plex_gb.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/plex/main/playlists/plex_ca.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/plex/main/playlists/plex_au.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/plex/main/playlists/plex_nz.m3u"
]

# Explicit EPGs that might not be declared in playlist headers
epg_sources = [
    "https://raw.githubusercontent.com/dp247/Freeview-EPG/master/epg.xml",
    "https://i.mjh.nz/SamsungTVPlus/us.xml.gz",
    "https://raw.githubusercontent.com/BuddyChewChew/localnow-playlist-generator/refs/heads/main/epg.xml",
    "https://raw.githubusercontent.com/BuddyChewChew/airy-playlist-generator/main/airy_channels.xml"
]

# Output target
master_playlist = '#EXTM3U x-tvg-url="epg.xml.gz"\n'
valid_ids = set()

print("Merging M3U lists and extracting valid IDs...")
for url in m3u_sources:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8', errors='ignore')
            for line in content.splitlines():
                if line.startswith("#EXTM3U"):
                    # Catch both EPG header formats dynamically
                    match = re.search(r'(?:x-tvg-url|url-tvg)=["\']([^"\']+)["\']', line)
                    if match:
                        for u in match.group(1).split(','):
                            u = u.strip()
                            if u and u not in epg_sources:
                                epg_sources.append(u)
                else:
                    if line.startswith("#EXTINF"):
                        # Cache both tvg-id and tvg-name to prevent missing guides
                        id_match = re.search(r'tvg-id=["\']([^"\']+)["\']', line)
                        if id_match:
                            valid_ids.add(id_match.group(1))
                        name_match = re.search(r'tvg-name=["\']([^"\']+)["\']', line)
                        if name_match:
                            valid_ids.add(name_match.group(1))
                    master_playlist += line + "\n"
    except Exception as e:
        print(f"Error reading M3U {url}: {e}")

with open("master.m3u", "w", encoding="utf-8") as f:
    f.write(master_playlist)

print(f"Found {len(valid_ids)} unique channel identifiers.")
print(f"Total EPG sources found: {len(epg_sources)}")

print("Merging, Filtering, and Compressing EPG XMLs...")
with gzip.open("epg.xml.gz", "wb") as out_f:
    out_f.write(b'<?xml version="1.0" encoding="utf-8"?>\n<tv>\n')
    
    for url in epg_sources:
        print(f"Processing EPG: {url}")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with tempfile.NamedTemporaryFile(delete=True) as temp:
                with urllib.request.urlopen(req) as response:
                    shutil.copyfileobj(response, temp)
                
                temp.seek(0)
                f_in = gzip.GzipFile(fileobj=temp) if url.endswith(".gz") else temp
                
                context = ET.iterparse(f_in, events=("end",))
                for event, elem in context:
                    if elem.tag == "channel":
                        if elem.get("id") in valid_ids:
                            out_f.write(ET.tostring(elem, encoding="utf-8"))
                            out_f.write(b'\n')
                        elem.clear()
                    elif elem.tag == "programme":
                        if elem.get("channel") in valid_ids:
                            out_f.write(ET.tostring(elem, encoding="utf-8"))
                            out_f.write(b'\n')
                        elem.clear()
        except Exception as e:
            print(f"Error processing EPG {url}: {e}")

    out_f.write(b'</tv>\n')

print("All done!")

   
                context = ET.iterparse(f_in, events=("end",))
                for event, elem in context:
                    if elem.tag == "channel":
                        if elem.get("id") in valid_ids:
                            out_f.write(ET.tostring(elem, encoding="utf-8"))
                            out_f.write(b'\n')
                        elem.clear()
                    elif elem.tag == "programme":
                        if elem.get("channel") in valid_ids:
                            out_f.write(ET.tostring(elem, encoding="utf-8"))
                            out_f.write(b'\n')
                        elem.clear()
        except Exception as e:
            print(f"Error processing EPG {url}: {e}")

    out_f.write(b'</tv>\n')

print("All done!")
