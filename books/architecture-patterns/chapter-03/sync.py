import hashlib
import os
import shutil
from pathlib import Path

BLOCK_SIZE: int = 65536


def hash_file(path: str):
    hasher = hashlib.sha1()
    with path.open("rb") as file:
        buf = file.read(BLOCK_SIZE)
        while buf:
            hasher.update(buf)
            buf = file.read(BLOCK_SIZE)
    return hasher.hexdigest()


def read_paths_and_hashes(root):
    hashes = {}
    for folder, _, files in os.walk(root):
        for fn in files:
            hashes[hash_file(Path(folder) / fn)] = fn
    return hashes


def determine_actions(src_hashes, dst_hashes, src_folder, dst_folder):
    for sha, filename in src_hashes.items():
        if sha not in dst_hashes:
            sourcepath = Path(src_folder) / filename
            destpath = Path(dst_folder) / filename
            yield 'copy', sourcepath, destpath

        elif dst_hashes[sha] != filename:
            olddestpath = Path(dst_folder) / dst_hashes[sha]
            newdestpath = Path(dst_folder) / filename
            yield 'move', olddestpath, newdestpath

    for sha, filename in dst_hashes.items():
        if sha not in src_hashes:
            yield 'delete', dst_folder / filename


def sync(source, dest: str):
    # imperative shell step 1, gather inputs
    source_hashes = read_paths_and_hashes(source)
    dest_hashes = read_paths_and_hashes(dest)

    # step 2: call functional core
    actions = determine_actions(source_hashes, dest_hashes, source, dest)

    # imperative shell step 3, apply outputs
    for action, *paths in actions:
        if action == 'copy':
            shutil.copyfile(*paths)
        if action == 'move':
            shutil.move(*paths)
        if action == 'delete':
            os.remove(paths[0])


def synchronise_dirs(reader, filesystem, source_root, dest_root):
    source_hashes = reader(source_root)
    dest_hashes = reader(dest_root)

    for sha, filename in source_hashes.items():
        if sha not in dest_hashes:
            sourcepath = source_root + '/' + filename
            destpath = dest_root + '/' + filename
            filesystem.copy(sourcepath, destpath)

        elif dest_hashes[sha] != filename:
            olddespath = dest_root + '/' + dest_hashes[sha]
            newdestpath = dest_root + '/' + filename
            filesystem.move(olddespath, newdestpath)

    for sha, filename in dest_hashes.items():
        if sha not in source_hashes:
            filesystem.delete(dest_root + '/' + filename)
