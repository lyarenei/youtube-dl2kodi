# youtube-dl2kodi

A simple script to parse JSON produced by `--write-info-json` option in youtube-dl/yt-dlp.

For the episode number to work correctly, you need to use `--playlist-reverse` option.

For example:
```shell
yt-dlp --write-info-json --playlist-reverse --exec before_dl:'youtube-dl2kodi.py -f {}' <playlist_url>
```
Note: exec `before_dl` is not necessary, but it is useful if you want to skip downloading and only generate metadata.
