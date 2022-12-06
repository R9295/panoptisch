def get_file_dir(path: str) -> str:
    return '/'.join(path.split('/')[:-1])
