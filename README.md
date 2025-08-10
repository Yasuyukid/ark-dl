# Arknights Downloader

A tool for downloading **Arknights** assets quickly and easily. This is meant to be used with [aelurum](https://github.com/aelurum)'s [ArknightsStudio](https://github.com/aelurum/AssetStudio/tree/ArknightsStudio).

## Install requirements

```sh
pip install --upgrade -r requirements.txt
```

## Create the executable

```sh
pyinstaller --noconfirm --onefile --console --icon "Assets/icon.ico" --name ark-dl --collect-datas UnityPy "main.py"
```

## Usage

Download all assets and save them to `Downloads`

```sh
ark-dl --directory "Downloads" --server all
```

Download `hot_update_list.json` from `cn` server

```sh
ark-dl --hot-update-list --server cn
```

Download all assets from `en` server whose names contain `skadi2`

```sh
ark-dl --filter "skadi2"
```

All available options

| Option              | Description                                            |
|---------------------|--------------------------------------------------------|
| `--help/-h`         | show this help message and exit                        |
| `--no-log`          | disable log messages                                   |
| `--hot-update-list` | download hot_update_list.json instead                  |
| `--directory/-d`    | set the output directory (default: arkprts's AppData)  |
| `--filter/-f`       | only download assets whose names contain this string   |
| `--pack-id/-p`      | only download assets whose packIDs contain this string |
| `--type/-t`         | only download assets whose types contain this string   |
| `--server/-s`       | set the download server (default: en)                  |
| `--no-subfolder`    | save all assets in the base directory                  |
| `--force`           | force-overwrite any existing files                     |

## Acknowledgement

- [ashleney](https://github.com/ashleney)'s [ArkPRTS](https://github.com/ashleney/ArkPRTS).
- [aelurum](https://github.com/aelurum)'s [ArknightsStudio](https://github.com/aelurum/AssetStudio/tree/ArknightsStudio).
