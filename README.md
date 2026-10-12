# Video Downloader (authorized sources only)

GitHub Actions workflow to download videos from URLs you are authorized to access, using yt-dlp where the source supports it, and upload the result as a ZIP artifact.

## Setup
1. Create a GitHub repository and upload these files.
2. Open **Actions** and enable workflows if prompted.
3. Run **Download authorized videos** → **Run workflow**.
4. Paste one authorized URL per line into the `urls` input.
5. Download `videos-zip` from the workflow run's Artifacts section.

## Notes
- This does not bypass logins, DRM, paywalls, or access controls.
- 720p is preferred when the source provides it; otherwise the best available format up to 720p is selected.
- Large downloads may exceed GitHub Actions runtime or artifact limits.
- Only use URLs for content you own or have permission to download.
