import psutil
ps = psutil.Process()
with ps.oneshot():
    print(
        ps.name(),
        ps.cpu_times(),
        ps.cpu_percent(),
        ps.create_time(),
        ps.ppid(),
        ps.status()
        )