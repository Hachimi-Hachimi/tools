def load_ignore_list(dir_path):
    try:
        f = open(dir_path / ".gitignore", "r")
        print("Loading ignore list from .gitignore")
        return {s[1:] for s in f.readlines() if s[0] == "!" and not "*" in s}
    except:
        return {}