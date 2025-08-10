import arkprts, asyncio, argparse, pathlib, shutil, json
from typing import Literal

def save_file(ab_file_path: arkprts.bundle.PathLike, save_directory: arkprts.bundle.PathLike, *, log: bool = True, subfolder: bool = True, force: bool = False) -> None:
    ab_file_path = pathlib.Path(ab_file_path)
    save_directory = pathlib.Path(save_directory)

    save_path = (save_directory / ab_file_path.relative_to(arkprts.network.TEMP_DIR / "ArknightsAB")) if subfolder else (save_directory / "-".join(ab_file_path.relative_to(arkprts.network.TEMP_DIR / "ArknightsAB").parts))
    save_path.parent.mkdir(parents = True, exist_ok = True)

    should_save = not save_path.exists() or force
    if should_save:
        shutil.move(ab_file_path, save_path)

    if log:
        print(f'Successfully downloaded to "{save_path}"' if should_save else f'Ignored "{save_path}" since it already exists')

async def _download_bundle(bundle: arkprts.BundleAssets, filter: str = "", pack_id: str = "", type: str = "", *, log: bool = True, subfolder: bool = True, force: bool = False) -> None:
    hot_update_list = await bundle._get_hot_update_list(bundle.default_server)
    requested_names = [info["name"] for info in hot_update_list["abInfos"] if filter in info["name"] and pack_id in info.get("pid", "") and type in info.get("type", "")]

    ab_file_paths = await asyncio.gather(*(bundle._download_unity_file(name, server = bundle.default_server) for name in requested_names),)
    for ab_file_path in ab_file_paths:
        save_file(ab_file_path, bundle.directory / bundle.default_server, log = log, subfolder = subfolder, force = force)

async def _download_hot_update_list(bundle: arkprts.BundleAssets, *, log: bool = True, force: bool = False) -> None:
    hot_update_list = await bundle._get_hot_update_list(bundle.default_server)

    save_path = bundle.directory / bundle.default_server / "hot_update_list.json"
    save_path.parent.mkdir(parents = True, exist_ok = True)

    should_save = not save_path.exists() or force
    if should_save:
        with open(save_path, "w") as file:
            json.dump(hot_update_list, file, indent = 4)

    if log:
        print(f'Successfully downloaded to "{save_path}"' if should_save else f'Ignored "{save_path}" since it already exists')

async def download_bundle(directory: arkprts.bundle.PathLike | None, filter: str = "", pack_id: str = "", type: str = "", *, server: arkprts.network.ArknightsServer | Literal["all"] | None = None, hot_update_list: bool = False, log: bool = True, subfolder: bool = True, force: bool = False) -> None:
    bundle = arkprts.BundleAssets(directory, default_server = server)

    if server == "all":
        for server in arkprts.network.NETWORK_ROUTES:
            bundle.default_server = server
            await (_download_hot_update_list(bundle, log = log, force = force) if hot_update_list else _download_bundle(bundle, filter, pack_id, type, log = log, subfolder = subfolder, force = force))
    else:
        await (_download_hot_update_list(bundle, log = log, force = force) if hot_update_list else _download_bundle(bundle, filter, pack_id, type, log = log, subfolder = subfolder, force = force))

    await bundle.network.session.close()

def main(log: bool, hot_update_list: bool, directory: arkprts.bundle.PathLike, filter: str, pack_id: str, type: str, server: str, subfolder: bool, force: bool) -> None:
    asyncio.run(download_bundle(directory, filter, pack_id, type, server = server, hot_update_list = hot_update_list, log = log, subfolder = subfolder, force = force))

parser = argparse.ArgumentParser("ark-dl", description = "A tool for downloading Arknights assets quickly and easily")
parser.add_argument("--no-log", action = "store_false", help = "disable log messages")
parser.add_argument("--hot-update-list", action = "store_true", help = "download hot_update_list.json instead")
parser.add_argument("-d", "--directory", default = arkprts.network.APPDATA_DIR / "Assets", type = str, help = "set the output directory (default: arkprts's AppData)")
parser.add_argument("-f", "--filter", default = "", type = str, help = "only download assets whose names contain this string")
parser.add_argument("-p", "--pack-id", default = "", type = str, help = "only download assets whose packIDs contain this string")
parser.add_argument("-t", "--type", default = "", type = str, help = "only download assets whose types contain this string")
parser.add_argument("-s", "--server", default = "en", type = str, help = "set the download server (default: en)")
parser.add_argument("--no-subfolder", action = "store_false", help = "save all assets in the base directory")
parser.add_argument("--force", action = "store_true", help = "force-overwrite any existing files")

if __name__ == "__main__":
    args = parser.parse_args()
    main(args.no_log, args.hot_update_list, args.directory, args.filter, args.pack_id, args.type, args.server, args.no_subfolder, args.force)