import argparse
import subprocess
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Download authorized video URLs.")
    parser.add_argument("--input", default="urls.txt")
    parser.add_argument("--output", default="videos")
    args = parser.parse_args()

    source = Path(args.input)
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)

    if not source.exists():
        print(f"Input file not found: {source}", file=sys.stderr)
        return 2

    urls = [
        line.strip() for line in source.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    if not urls:
        print("No URLs found. Add one authorized URL per line to urls.txt.")
        return 0

    # Prefer 720p or lower; merge separate video/audio streams when available.
    fmt = "bv*[height<=720]+ba/b[height<=720]/best[height<=720]/best"
    failed = 0
    for index, url in enumerate(urls, start=1):
        print(f"[{index}/{len(urls)}] Processing URL")
        command = [
            sys.executable, "-m", "yt_dlp",
            "--no-playlist",
            "--format", fmt,
            "--merge-output-format", "mp4",
            "--output", str(output / "%(title).180B [%(id)s].%(ext)s"),
            "--no-overwrites",
            url,
        ]
        result = subprocess.run(command, check=False)
        if result.returncode != 0:
            failed += 1
            print(f"Download failed for entry {index}; see yt-dlp output above.")
    print(f"Finished. Failed entries: {failed}/{len(urls)}")
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
