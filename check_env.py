"""Checks that your laptop + the workshop sandbox work. Run in the VS Code terminal (inside the container).
The AI agent in this workshop is the Codex CLI: you start it by typing `codex` in the terminal.

    python check_env.py          # all checks (no key needed)
    python check_env.py --ai     # also asks the AI one tiny question (needs a real key in .env; the key comes on the workshop day)

If something shows FAIL, take a screenshot and send it to the organisers.
"""
import glob
import os
import platform
import shutil
import subprocess
import sys
import tomllib
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
results = []  # (status, name, detail)


def record(status, name, detail=""):
    results.append((status, name, detail))
    print(f"  [{status:4s}] {name}" + (f": {detail}" if detail else ""))


def run(cmd, timeout=60):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout + p.stderr).strip()
    except Exception as e:  # noqa: BLE001
        return 1, str(e)


def section(title):
    print(f"\n{title}")


# ---------------------------------------------------------------- 1. your computer / container
def check_system():
    section("1. The sandbox (the box your robot and the AI live in)")
    record("OK", "Python", platform.python_version())
    record("OK", "Machine", f"{platform.system()} {platform.machine()}, user {os.environ.get('USER') or 'student'}")
    try:
        mem_kb = int(next(line for line in open("/proc/meminfo") if line.startswith("MemTotal")).split()[1])
        gb = mem_kb / 1024 / 1024
        if gb < 2.5:
            record("WARN", "Memory for Docker", f"{gb:.1f} GB. Low. Docker Desktop -> Settings -> Resources: give it at least 4 GB.")
        else:
            record("OK", "Memory for Docker", f"{gb:.1f} GB")
    except Exception:  # noqa: BLE001
        record("WARN", "Memory for Docker", "could not read")
    free_gb = shutil.disk_usage(HERE).free / 1024**3
    record("OK" if free_gb >= 2 else "WARN", "Free disk space", f"{free_gb:.1f} GB")
    try:
        out_dir = os.path.join(HERE, "out")
        os.makedirs(out_dir, exist_ok=True)
        test = os.path.join(out_dir, ".write_test")
        with open(test, "w") as f:
            f.write("ok")
        os.remove(test)
        record("OK", "Can write to your project folder")
    except Exception as e:  # noqa: BLE001
        record("FAIL", "Can write to your project folder", str(e))


# ---------------------------------------------------------------- 2. MiniGrid + replay
def check_minigrid():
    section("2. MiniGrid (the robot world) and replay")
    try:
        import gymnasium as gym
        import minigrid

        env = gym.make("MiniGrid-Empty-5x5-v0")
        env.reset(seed=0)
        env.step(2)  # move forward once
        env.close()
        record("OK", "MiniGrid installed and a robot world runs", minigrid.__version__)
    except Exception as e:  # noqa: BLE001
        record("FAIL", "MiniGrid installed and a robot world runs", str(e))
        return
    try:
        sys.path.insert(0, HERE)
        import demo_robot

        n, ok, steps, waits = demo_robot.make_demo()
        size = os.path.getsize(demo_robot.OUT)
        if ok and size > 0:
            record("OK", "Demo robot delivered the lunch, replay GIF saved", f"{os.path.relpath(demo_robot.OUT, HERE)} ({n} pictures, {size // 1024} KB; {steps} steps, waited {waits}x)")
            print("         -> Open out/robot_demo.gif in the VS Code Explorer (left bar) and watch the robot.")
        else:
            record("FAIL", "Demo robot", "did not deliver safely or the GIF is empty")
    except Exception as e:  # noqa: BLE001
        record("FAIL", "Demo robot and replay", str(e))


# ---------------------------------------------------------------- 3. Codex (the AI coding agent)
def check_codex():
    section("3. Codex (the AI coding agent)")
    code, out = run(["codex", "--version"], 30)
    record("OK" if code == 0 else "FAIL", "Codex installed", out.splitlines()[-1] if out else "not found")
    cfg_path = os.path.expanduser("~/.codex/config.toml")
    try:
        cfg = tomllib.load(open(cfg_path, "rb"))
        provider = cfg.get("model_provider")
        ok = provider == "openrouter" and cfg.get("sandbox_mode") == "read-only" and cfg.get("approval_policy") == "on-request"
        record("OK" if ok else "WARN", "Codex settings", f"model {cfg.get('model')}, provider {provider}, sandbox {cfg.get('sandbox_mode')}, approvals {cfg.get('approval_policy')}")
    except Exception as e:  # noqa: BLE001
        record("FAIL", "Codex settings file", f"{cfg_path}: {e}")
    code, out = run(["codex", "sandbox", "echo", "SANDBOX_OK"], 60)
    if "SANDBOX_OK" in out:
        record("OK", "Codex's safety sandbox starts", "the AI will have to ask before changing files")
    else:
        record("FAIL", "Codex's safety sandbox starts", "it did not start. Ask a teaching assistant. (Details: " + out.replace("\n", " ")[:120] + ")")


# ---------------------------------------------------------------- 4. network and key
def check_network_and_key(ai):
    section("4. Internet and access key")
    try:
        with urllib.request.urlopen("https://openrouter.ai/api/v1/models", timeout=15) as r:
            record("OK" if r.status == 200 else "WARN", "Can reach the AI service (openrouter.ai)", f"HTTP {r.status}")
    except Exception as e:  # noqa: BLE001
        record("FAIL", "Can reach the AI service (openrouter.ai)", f"{e}. A school or home network may block it. Try a phone hotspot.")
    key = os.environ.get("OPENROUTER_API_KEY", "")
    if not key or key.startswith("paste"):
        record("OK", "Access key", "not set yet. That is normal: you get the key on the workshop day.")
        if ai:
            record("WARN", "AI test", "skipped: no real key in .env")
        return
    record("OK", "Access key", "found (never share or photograph it)")
    if ai:
        code, out = run(["codex", "exec", "--skip-git-repo-check", "Reply with just the word pong."], 150)
        record("OK" if "pong" in out.lower() else "FAIL", "AI test (asks the AI to say 'pong')", "answered" if "pong" in out.lower() else out.replace("\n", " ")[-160:])
    else:
        record("OK", "AI test", "not run. Use: python check_env.py --ai")


def main():
    print("Workshop environment check")
    print("=" * 26)
    ai = "--ai" in sys.argv
    check_system()
    check_minigrid()
    check_codex()
    check_network_and_key(ai)
    fails = [r for r in results if r[0] == "FAIL"]
    warns = [r for r in results if r[0] == "WARN"]
    print("\n" + "=" * 26)
    if not fails and not warns:
        print("ALL GOOD. Your laptop is ready for the workshop.")
    elif not fails:
        print(f"MOSTLY GOOD with {len(warns)} warning(s) above. Read them, then run this check again if you changed something.")
    else:
        print(f"{len(fails)} problem(s) to fix (marked FAIL). Take a screenshot of this screen and send it to the organisers.")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
