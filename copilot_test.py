import os
import platform

def print_system_uptime():
    system = platform.system()
    if system == "Windows":
        # Windows does not have /proc/uptime, use 'net stats srv'
        try:
            output = os.popen('net stats srv').read()
            for line in output.split('\n'):
                if "Statistics since" in line:
                    print("System uptime since:", line.split("Statistics since")[1].strip())
                    return
            print("Could not determine uptime on Windows.")
        except Exception as e:
            print("Error getting uptime:", e)
    elif system in ["Linux", "Darwin"]:
        try:
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
                uptime_string = "{} days, {} hours, {} minutes, {} seconds".format(
                    int(uptime_seconds // 86400),
                    int((uptime_seconds % 86400) // 3600),
                    int((uptime_seconds % 3600) // 60),
                    int(uptime_seconds % 60)
                )
                print("System uptime:", uptime_string)
        except FileNotFoundError:
            # For Mac OS X (Darwin), use 'sysctl'
            if system == "Darwin":
                try:
                    output = os.popen('sysctl -n kern.boottime').read()
                    import re, time, datetime
                    m = re.search(r'{ sec = (\d+),', output)
                    if m:
                        boot_time = int(m.group(1))
                        uptime_seconds = int(time.time()) - boot_time
                        uptime_string = "{} days, {} hours, {} minutes, {} seconds".format(
                            int(uptime_seconds // 86400),
                            int((uptime_seconds % 86400) // 3600),
                            int((uptime_seconds % 3600) // 60),
                            int(uptime_seconds % 60)
                        )
                        print("System uptime:", uptime_string)
                        return
                except Exception as e:
                    print("Error getting uptime on Mac:", e)
            print("Could not determine uptime.")
    else:
        print("Unsupported operating system.")

if __name__ == "__main__":
    print_system_uptime()
