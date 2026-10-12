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

    # Template: put downloaded files into the output directory
    outtmpl = str(output / "%(title).180B [%(id)s].%(ext)s")

    # Common yt-dlp options: continue on errors and be verbose enough for debugging
    base_cmd = [
        sys.executable, "-m", "yt_dlp",
        "--no-playlist",
        "--format", fmt,
        "--merge-output-format", "mp4",
        "--output", outtmpl,
        "--no-overwrites",
        "--ignore-errors",
        "--no-warnings",
    ]

    total_downloaded = 0
    for index, url in enumerate(urls, start=1):
        print(f"[{index}/{len(urls)}] Processing URL: {url}")
        before = sum(1 for _ in output.rglob("*"))
        command = base_cmd + [url]
        # Run yt-dlp and let it print its output to the workflow logs for debugging
        result = subprocess.run(command, check=False)
        after = sum(1 for _ in output.rglob("*"))
        added = after - before
        if added > 0:
            total_downloaded += added
            print(f"Downloaded {added} new file(s) for this URL.")
        else:
            # If yt-dlp returned non-zero, print a warning; keep going.
            if result.returncode != 0:
                print(f"Warning: download command exited with code {result.returncode} for {url}", file=sys.stderr)
            else:
                print(f"No files created by yt-dlp for {url}; it may be an unsupported URL or no media found.")

    print(f"Finished. Total downloaded files: {total_downloaded}")

    # Exit with success even if some URLs failed so the workflow can continue to create artifacts conditionally.
    # If you prefer the job to fail when nothing was downloaded, change this behavior to return 1 when total_downloaded == 0.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
