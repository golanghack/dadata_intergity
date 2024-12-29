from pathlib import Path


def is_docker() -> bool:
    """Проверяет, запущен ли код внутри докер-контейнера."""
    path = Path("/proc/self/cgroup")
    return (
        Path.exists(Path(path, "/.dockerenv"))
        or path.is_file()
        and any("docker" in line for line in path.open())
    )
