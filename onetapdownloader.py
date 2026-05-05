#!/usr/bin/env python3
"""
oneTapDownloader
----------------
Scarica foto e video dai social (YouTube, Instagram, TikTok, Facebook)
con un solo comando, senza server a pagamento.

Download photos and videos from social platforms (YouTube, Instagram,
TikTok, Facebook) with a single command — no paid servers needed.

Powered by yt-dlp  <https://github.com/yt-dlp/yt-dlp>
"""

import argparse
import os
import sys
from typing import Optional
from urllib.parse import urlparse

try:
    import yt_dlp
    from colorama import Fore, Style, init as colorama_init
except ImportError as exc:
    print(
        f"[ERROR] Missing dependency: {exc}\n"
        "Run:  pip install -r requirements.txt",
        file=sys.stderr,
    )
    sys.exit(1)

colorama_init(autoreset=True)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SUPPORTED_DOMAINS = (
    "youtube.com",
    "youtu.be",
    "instagram.com",
    "tiktok.com",
    "facebook.com",
    "fb.watch",
)

QUALITY_MAP = {
    "best":  "bestvideo+bestaudio/best",
    "worst": "worstvideo+worstaudio/worst",
    "1080":  "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    "720":   "bestvideo[height<=720]+bestaudio/best[height<=720]",
    "480":   "bestvideo[height<=480]+bestaudio/best[height<=480]",
    "360":   "bestvideo[height<=360]+bestaudio/best[height<=360]",
}


def _detect_platform(url: str) -> str:
    try:
        hostname = urlparse(url).hostname or ""
    except ValueError:
        hostname = ""
    hostname = hostname.lower()
    # strip leading 'www.' for cleaner matching
    if hostname.startswith("www."):
        hostname = hostname[4:]

    if hostname in ("youtube.com", "youtu.be") or hostname.endswith(".youtube.com"):
        return "YouTube"
    if hostname == "instagram.com" or hostname.endswith(".instagram.com"):
        return "Instagram"
    if hostname == "tiktok.com" or hostname.endswith(".tiktok.com"):
        return "TikTok"
    if hostname in ("facebook.com", "fb.watch") or hostname.endswith(".facebook.com"):
        return "Facebook"
    return "Unknown"


def _print_info(msg: str) -> None:
    print(f"{Fore.CYAN}[ℹ]  {msg}{Style.RESET_ALL}")


def _print_success(msg: str) -> None:
    print(f"{Fore.GREEN}[✔]  {msg}{Style.RESET_ALL}")


def _print_error(msg: str) -> None:
    print(f"{Fore.RED}[✖]  {msg}{Style.RESET_ALL}", file=sys.stderr)


def _progress_hook(d: dict) -> None:
    if d["status"] == "downloading":
        percent = d.get("_percent_str", "?%").strip()
        speed = d.get("_speed_str", "?/s").strip()
        eta = d.get("_eta_str", "?").strip()
        print(
            f"\r{Fore.YELLOW}  ↓  {percent}  @ {speed}  ETA {eta}   {Style.RESET_ALL}",
            end="",
            flush=True,
        )
    elif d["status"] == "finished":
        print()  # newline after progress


# ---------------------------------------------------------------------------
# Core download function
# ---------------------------------------------------------------------------


def download(
    url: str,
    output_dir: str = "./downloads",
    quality: str = "best",
    audio_only: bool = False,
    no_watermark: bool = False,
    list_formats: bool = False,
    cookies: Optional[str] = None,
    verbose: bool = False,
) -> int:
    """
    Download media from *url* using yt-dlp.

    Returns 0 on success, 1 on error.
    """
    platform = _detect_platform(url)
    _print_info(f"Platform detected: {platform}")
    _print_info(f"URL: {url}")

    os.makedirs(output_dir, exist_ok=True)

    ydl_opts: dict = {
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "progress_hooks": [_progress_hook],
        "quiet": not verbose,
        "no_warnings": not verbose,
        "verbose": verbose,
    }

    if list_formats:
        ydl_opts["listformats"] = True

    elif audio_only:
        ydl_opts["format"] = "bestaudio/best"
        ydl_opts["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ]
        _print_info("Mode: audio-only (MP3)")

    else:
        fmt = QUALITY_MAP.get(quality, QUALITY_MAP["best"])
        ydl_opts["format"] = fmt
        _print_info(f"Quality: {quality}  →  format spec: {fmt}")

    # TikTok no-watermark: use the embed URL trick supported by yt-dlp
    if no_watermark and platform == "TikTok":
        ydl_opts["extractor_args"] = {"tiktok": {"webpage_download": ["1"]}}
        _print_info("No-watermark mode enabled for TikTok")

    if cookies:
        if not os.path.isfile(cookies):
            _print_error(f"Cookies file not found: {cookies}")
            return 1
        ydl_opts["cookiefile"] = cookies
        _print_info(f"Using cookies from: {cookies}")

    _print_info(f"Saving to: {os.path.abspath(output_dir)}")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ret = ydl.download([url])
        if ret == 0:
            _print_success("Download completed successfully.")
        return ret
    except yt_dlp.utils.DownloadError as exc:
        _print_error(f"Download failed: {exc}")
        return 1
    except KeyboardInterrupt:
        print()
        _print_error("Interrupted by user.")
        return 1


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="onetapdownloader",
        description=(
            "📥  oneTapDownloader — scarica foto/video dai social con un solo comando.\n"
            "     Powered by yt-dlp  <https://github.com/yt-dlp/yt-dlp>"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("url", help="URL del contenuto da scaricare / URL to download")
    parser.add_argument(
        "--output", "-o",
        default="./downloads",
        metavar="DIR",
        help="Cartella di destinazione (default: ./downloads)",
    )
    parser.add_argument(
        "--quality", "-q",
        default="best",
        choices=list(QUALITY_MAP.keys()),
        help="Qualità video (default: best)",
    )
    parser.add_argument(
        "--audio-only", "-a",
        action="store_true",
        help="Scarica solo la traccia audio in MP3",
    )
    parser.add_argument(
        "--no-watermark",
        action="store_true",
        help="Rimuovi la watermark (dove supportato, es. TikTok)",
    )
    parser.add_argument(
        "--list-formats",
        action="store_true",
        help="Elenca i formati disponibili senza scaricare",
    )
    parser.add_argument(
        "--cookies",
        metavar="FILE",
        help="File cookies Netscape (utile per contenuti privati/age-restricted)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Output dettagliato",
    )
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    print(
        f"\n{Fore.MAGENTA}{'─'*50}\n"
        f"  📥  oneTapDownloader\n"
        f"{'─'*50}{Style.RESET_ALL}\n"
    )

    ret = download(
        url=args.url,
        output_dir=args.output,
        quality=args.quality,
        audio_only=args.audio_only,
        no_watermark=args.no_watermark,
        list_formats=args.list_formats,
        cookies=args.cookies,
        verbose=args.verbose,
    )
    sys.exit(ret)


if __name__ == "__main__":
    main()
