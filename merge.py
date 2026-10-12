import gzip
import urllib.request
import xml.etree.ElementTree as ET
import re
import tempfile
import shutil

# ----------------------------------------------------------------------
# SETTINGS
# ----------------------------------------------------------------------
# False = keep every channel (use the report in the log to see coverage).
# True  = drop channels that have no guide data from master.m3u.
REMOVE_CHANNELS_WITHOUT_EPG = False

# Full URL to your merged EPG, so IPTV apps can find it
EPG_URL = "https://raw.githubusercontent.com/silvern0va/silveriptvcustom/main/epg.xml.gz"

# M3U playlist sources
m3u_sources = [
    # Samsung TV Plus (has Divorce Court). Replaces the dead i.mjh.nz Samsung/Stirr links.
    "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/main/playlists/samsungtvplus_us.m3u",
    # Tubi (guide link is built into this playlist's header)
    "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/main/playlists/tubi_all.m3u",
    "https://www.apsattv.com/localnow.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/RakutenTV/main/playlist.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/roku-playlist-generator/refs/heads/main/roku.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/xumo-playlist-generator/refs/heads/main/playlists/xumo_playlist.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/lg-playlist-generator/refs/heads/main/lg_channels_us.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/airy-playlist-generator/refs/heads/main/airy_channels.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/tcl-playlist-generator/refs/heads/main/tcl.m3u8",
    # Pluto from the generator that uses the jmp2.uk proxy (should fix streams that stopped working)
    "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/main/playlists/plutotv_us.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/plex/refs/heads/main/playlists/plex_us.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/plex/refs/heads/main/playlists/plex_gb.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/plex/refs/heads/main/playlists/plex_au.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/plex/refs/heads/main/playlists/plex_ca.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/plex/refs/heads/main/playlists/plex_nz.m3u",
]

# Explicit EPG sources (more get added from playlist headers automatically)
epg_sources = [
    "https://raw.githubusercontent.com/dp247/Freeview-EPG/master/epg.xml",
    "https://raw.githubusercontent.com/BuddyChewChew/localnow-playlist-generator/refs/heads/main/epg.xml",
    "https://raw.githubusercontent.com/BuddyChewChew/airy-playlist-generator/main/airy_channels.xml",
]


def get_attr(line, attr):
    m = re.search(attr + r'=["\']([^"\']*)["\']', line)
    return m.group(1) if m else None


def short(url):
    return url.replace("https://", "").replace("raw.githubusercontent.com/", "")[-70:]


# ----------------------------------------------------------------------
# STEP 1: READ PLAYLISTS
# ----------------------------------------------------------------------
print("Reading M3U playlists...")
entries = []  # each channel: source, lines, id, name

for url in m3u_sources:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            content = response.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"  ERROR reading M3U {url}: {e}")
        continue

    current = None
    count = 0
    header_epgs = []
    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("#EXTM3U"):
            hdr = get_attr(line, "x-tvg-url") or get_attr(line, "url-tvg")
            if hdr:
                for u in hdr.split(","):
                    u = u.strip()
                    if u:
                        header_epgs.append(u)
                        if u not in epg_sources:
                            epg_sources.append(u)
            continue
        if line.startswith("#EXTINF"):
            current = {
                "source": url,
                "lines": [line],
                "id": get_attr(line, "tvg-id"),
                "name": get_attr(line, "tvg-name"),
            }
            entries.append(current)
            count += 1
        elif current is not None:
            current["lines"].append(line)

    print(f"  {short(url)}: {count} channels, EPG in header: {header_epgs if header_epgs else 'NONE'}")

valid_ids = set()
for e in entries:
    if e["id"]:
        valid_ids.add(e["id"])
    if e["name"]:
        valid_ids.add(e["name"])

print(f"\nTotal channels: {len(entries)}")
print(f"Unique channel identifiers: {len(valid_ids)}")
print(f"Total EPG sources: {len(epg_sources)}")

# ----------------------------------------------------------------------
# STEP 2: MERGE EPG
# ----------------------------------------------------------------------
print("\nMerging, filtering, and compressing EPG XMLs...")

seen_channels = set()
seen_programmes = set()
guided = set()  # channel ids that actually have programme data
epg_stats = {}

with gzip.open("epg.xml.gz", "wb") as out_f:
    out_f.write(b'<?xml version="1.0" encoding="utf-8"?>\n<tv>\n')

    for url in epg_sources:
        print(f"Processing EPG: {url}")
        stats = {"channels": 0, "programmes": 0}
        epg_stats[url] = stats
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with tempfile.NamedTemporaryFile(delete=True) as temp:
                with urllib.request.urlopen(req, timeout=120) as response:
                    shutil.copyfileobj(response, temp)
                temp.seek(0)

                # Detect gzip by file header instead of URL ending
                magic = temp.read(2)
                temp.seek(0)
                if magic == b"\x1f\x8b":
                    f_in = gzip.GzipFile(fileobj=temp)
                else:
                    f_in = temp

                for event, elem in ET.iterparse(f_in, events=("end",)):
                    if elem.tag == "channel":
                        cid = elem.get("id")
                        if cid in valid_ids and cid not in seen_channels:
                            seen_channels.add(cid)
                            stats["channels"] += 1
                            out_f.write(ET.tostring(elem, encoding="utf-8"))
                            out_f.write(b"\n")
                        elem.clear()
                    elif elem.tag == "programme":
                        cid = elem.get("channel")
                        key = (cid, elem.get("start"))
                        if cid in valid_ids and key not in seen_programmes:
                            seen_programmes.add(key)
                            guided.add(cid)
                            stats["programmes"] += 1
                            out_f.write(ET.tostring(elem, encoding="utf-8"))
                            out_f.write(b"\n")
                        elem.clear()
        except Exception as e:
            print(f"  ERROR processing EPG {url}: {e}")

    out_f.write(b"</tv>\n")

# ----------------------------------------------------------------------
# STEP 3: WRITE PLAYLIST
# ----------------------------------------------------------------------
remove = REMOVE_CHANNELS_WITHOUT_EPG
if remove and not guided:
    print("WARNING: no guide data found at all, so not removing any channels.")
    remove = False

master_playlist = f'#EXTM3U x-tvg-url="{EPG_URL}"\n'
kept = 0
for e in entries:
    if remove and e["id"] not in guided:
        continue
    master_playlist += "\n".join(e["lines"]) + "\n"
    kept += 1

with open("master.m3u", "w", encoding="utf-8") as f:
    f.write(master_playlist)

# ----------------------------------------------------------------------
# REPORT
# ----------------------------------------------------------------------
print("\n================ REPORT ================")
print("Guide coverage per playlist (channels with guide data / total channels):")
by_source = {}
for e in entries:
    s = by_source.setdefault(e["source"], [0, 0])
    s[0] += 1
    if e["id"] in guided:
        s[1] += 1
for url, (total, ok) in by_source.items():
    pct = round(100 * ok / total) if total else 0
    print(f"  {ok:5d} / {total:5d} ({pct:3d}%)  {short(url)}")

total_ok = sum(1 for e in entries if e["id"] in guided)
print(f"\nOVERALL: {total_ok} of {len(entries)} channels have guide data")

print("\nWhat each EPG source contributed:")
for url, s in epg_stats.items():
    print(f"  {s['channels']:5d} channels, {s['programmes']:7d} programmes  {short(url)}")

print(f"\nChannels written to master.m3u: {kept}"
      + (" (channels without guide data removed)" if remove else ""))
print("All done!")
