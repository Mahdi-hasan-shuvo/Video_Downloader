import re
import uuid
import random
from fake_useragent import UserAgent
from urllib.parse import urlparse, parse_qs
def get_video_id(url: str):
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    # print(parsed.path.strip("/") )
    if "youtu.be" in host:
        return parsed.path.strip("/")        # /VIDEOID → VIDEOID
    # 2) youtube.com/watch?v=VIDEOID
    if "youtube.com" in host and parsed.path == "/watch":
        params = parse_qs(parsed.query)
        return params.get("v", [None])[0]

    # 3) youtube.com/shorts/VIDEOID
    if "youtube.com" in host and parsed.path.startswith("/shorts/"):
        return parsed.path.split("/")[2]

    # 4) youtube.com/embed/VIDEOID
    if "youtube.com" in host and parsed.path.startswith("/embed/"):
        return parsed.path.split("/")[2]
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    if match:
        return match.group(1)

    return None
headers_fb = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': UserAgent().random,
        }

YT_headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'dnt': '1',
    'origin': 'https://www.clipto.com',
    'priority': 'u=1, i',
    'referer': 'https://www.clipto.com/media-downloader/free-youtube-video-to-mp4-0607',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': UserAgent().random,
}

def YT_cookie_dict():
    """Generate cookies with specific patterns like the example"""
    
    # Predefined keys with specific value types
    cookie_templates = {
        'NEXT_LOCALE': lambda: random.choice(['en', 'es', 'fr', 'de', 'ja']),
        'traffic-source': lambda: f"stripe-web-ytd-seo-{random.choice(['mp4', 'jpg', 'png'])}",
        'traffic-history': lambda: random.choice(['seo', 'direct', 'social', 'referral']),
        'uu': lambda: str(uuid.uuid4()),
        'country': lambda: random.choice(['US', 'GB', 'BD', 'JP', 'CA', 'AU', 'DE']),
        'merge-video-api': lambda: str(random.choice([0, 1])),
        'vd-down-app': lambda: random.choice(['a', 'b', 'c', 'd']),
        'pwa-install': lambda: random.choice(['a', 'b', 'c', 'd']),
        'intercom-id-vbv7xze7': lambda: str(uuid.uuid4()),
        'intercom-session-vbv7xze7': lambda: random.choice(['', str(uuid.uuid4())]),
        'intercom-device-id-vbv7xze7': lambda: str(uuid.uuid4()),
    }
    
    # Generate cookies (select random subset)
    num_cookies = random.randint(5, len(cookie_templates))
    selected_keys = random.sample(list(cookie_templates.keys()), num_cookies)
    
    cookies = {}
    for key in selected_keys:
        cookies[key] = cookie_templates[key]()
    
    return cookies
headers_ins = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'dnt': '1',
    'dpr': '1',
    'priority': 'u=0, i',
    'sec-ch-prefers-color-scheme': 'dark',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-full-version-list': '"Chromium";v="142.0.7444.176", "Google Chrome";v="142.0.7444.176", "Not_A Brand";v="99.0.0.0"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"19.0.0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'viewport-width': '1014',
}