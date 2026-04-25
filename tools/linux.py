import shutil
import subprocess


def disk_usage(path: str = "/") -> dict:
    total, used, free = shutil.disk_usage(path)
    return {
        "total_gb": round(total / 1e9, 2),
        "used_gb": round(used / 1e9, 2),
        "free_gb": round(free / 1e9, 2),
        "percent": round(used / total * 100, 1),
    }


def memory_info() -> dict:
    with open("/proc/meminfo") as f:
        data = {}
        for line in f:
            if ":" in line:
                key, val = line.split(":", 1)
                data[key.strip()] = int(val.split()[0])
    total = data.get("MemTotal", 0)
    available = data.get("MemAvailable", 0)
    used = total - available
    return {
        "total_mb": round(total / 1024, 1),
        "used_mb": round(used / 1024, 1),
        "free_mb": round(available / 1024, 1),
        "percent": round(used / total * 100, 1) if total else 0,
    }


def cpu_info() -> dict:
    result = subprocess.run(
        ["grep", "-c", "^processor", "/proc/cpuinfo"],
        capture_output=True, text=True,
    )
    cores = int(result.stdout.strip()) if result.returncode == 0 else 0
    with open("/proc/loadavg") as f:
        parts = f.read().split()
    return {
        "cores": cores,
        "load_1m": float(parts[0]),
        "load_5m": float(parts[1]),
        "load_15m": float(parts[2]),
    }


def top_processes(limit: int = 5) -> list[dict]:
    result = subprocess.run(
        ["ps", "aux", "--sort=-%cpu"],
        capture_output=True, text=True,
    )
    rows = []
    for line in result.stdout.strip().splitlines()[1 : limit + 1]:
        parts = line.split(None, 10)
        if len(parts) >= 11:
            rows.append({
                "pid": parts[1],
                "cpu_pct": parts[2],
                "mem_pct": parts[3],
                "command": parts[10][:60],
            })
    return rows
