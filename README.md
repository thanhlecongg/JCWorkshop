# Before the Workshop: Test Your Laptop (about 45–60 minutes)

**Workshop:** Build with AI: Make It Work, Make It Reliable
**Do this by:** [DATE, 5 days before the workshop]
**Stuck? Contact:** [NAME / EMAIL / CHAT LINK]. Tell us early. Nothing is wrong with you if setup fails. Laptops differ, and we have backup options.

---

## What is this for?

In the workshop you will use an **AI coding agent**. It can write code, run commands, and change files. That is powerful but also risky, so we run it inside a **sandbox**: a sealed box on your laptop (a program called Docker). The agent can only touch one folder you give it. It cannot see your photos, school files, or the rest of your laptop. Using AI responsibly starts with limiting what it can touch.

This folder is a **test**. You will set up the box, open it in VS Code, and run a few checks. You do **not** need any coding experience and you do **not** need an AI account or an access key. We give you the key on the workshop day. The AI agent is a program called **Codex** that you start by typing `codex` in the terminal; you will use it on the workshop day.

**What you need:** your own laptop (Windows 10/11 or a Mac), your charger, home Wi-Fi, about 10 GB free disk space, and at least 8 GB of RAM. You need permission to install software (ask the owner of the laptop, for example a parent). Do **not** sign up for any AI service for this workshop.

---

## Step 0. Check your laptop (2 minutes)

**Windows:** press **Windows key + R**, type `winver`, press Enter. You need **Windows 10 version 22H2** or newer, or **Windows 11**. Then press **Ctrl + Shift + Esc** → **Performance** tab → **CPU**. Look for **Virtualization: Enabled**. If it says *Disabled*, see Problem 2 below.

**Mac:** click the **Apple menu → About This Mac**. Note whether it says **Apple M1/M2/M3/…** (Apple silicon) or **Intel**. You need a recent macOS (Docker supports the current macOS and the two before it).

Check free disk space (Windows: File Explorer → This PC; Mac: About This Mac → Storage). You need about 10 GB free.

---

## Step 1. Install Docker Desktop (10–20 minutes)

1. Go to **https://www.docker.com/products/docker-desktop/** and download Docker Desktop for your system.
   - Mac: choose **Apple chip** or **Intel chip** to match Step 0.
   - Windows: choose **Windows (AMD64)**, which is correct for almost all laptops.
2. Open the installer and follow the prompts.
   - **Windows:** keep **"Use WSL 2 instead of Hyper-V"** ticked if you see it. You will be asked for administrator permission. The installer may ask you to **restart** the laptop; do it, then open Docker Desktop again.
   - **Mac:** drag Docker into **Applications** and open it. It may ask for your Mac password. On an Apple silicon Mac you may be offered Rosetta; accept it.
3. If Docker asks you to **sign in or create an account**, look for **Skip** and use it. You do not need an account. Accept the terms if asked.
4. Wait until Docker Desktop shows **"Engine running"** (a green status at the bottom left). The first start can take a few minutes.

## Step 2. Test that Docker works (2 minutes)

Open a terminal: **Windows:** press the Windows key, type **PowerShell**, open **Windows PowerShell**. **Mac:** press **Cmd + Space**, type **Terminal**, press Enter.

Type this and press Enter:

```
docker run hello-world
```

You should see a message that starts with **"Hello from Docker!"**. If you see an error, go to the Problems section.

## Step 3. Install VS Code and the Dev Containers extension (5–10 minutes)

1. Go to **https://code.visualstudio.com/** and install **Visual Studio Code** (free). Open it once.
2. Click the **Extensions** icon in the left bar (four squares). Search for **Dev Containers** (by Microsoft). Click **Install**.

## Step 4. Download the sandbox and this folder (10–20 minutes)

This is a large download, so **do it on home Wi-Fi, not at school**. Keep the laptop plugged in.

In the terminal from Step 2, type:

```
docker pull [IMAGE NAME, e.g. ghcr.io/ORG/jc-workshop:1.0]
```

Then download this folder: [DOWNLOAD LINK / GIT LINK for the **environment** package]. Unzip it to a place you can find, for example **C:\JCWorkshop** (Windows) or **Documents/JCWorkshop** (Mac). **Windows: do not put it inside OneDrive or Desktop**; those are synced and can cause errors.

## Step 5. Open it in the sandbox (5–10 minutes, the first time)

1. In VS Code: **File → Open Folder…** and choose the folder you unzipped (the one that contains `check_env.py`). Tick "Trust" if asked.
2. A pop-up at the bottom right says **"Reopen in Container"**. Click it. (If you miss it: press **Ctrl/Cmd + Shift + P**, type `Reopen in Container`, press Enter.)
3. **The first time takes a few minutes**, because VS Code installs its tools inside the box. Wait until the bottom-left corner shows **Dev Container: Workshop environment check**. Next time it will be much faster.

## Step 6. Run the checks (5 minutes)

Open the terminal inside VS Code: **Terminal → New Terminal**. Type:

```
python check_env.py
```

You will see a list of checks marked **OK**, **WARN** or **FAIL**.

- **OK** everywhere means you are ready.
- **FAIL** means something must be fixed. Take a screenshot and send it to us.

The check also makes a small **replay**: look in the left bar for the folder **out** and click **robot_demo.gif**. You will see a delivery robot carry lunch to a hungry student: it goes around a cart, keeps out of a no-entry room, and waits for a student who walks across its way. At the end the student smiles. In the workshop you will build a robot like this one, step by step, with an AI coding agent.

## Step 7. What to bring on the workshop day

- Your laptop, **fully charged**, and your charger
- Docker Desktop already installed and **opened once** (just start it before the session so it is running)
- VS Code installed, with the Dev Containers extension

**On the workshop day:** we will give you a **link to the workshop project (Git)** and a short **access key**. You will download the project, open it in VS Code the same way as in Step 5 ("Reopen in Container"), and paste the key into the file named **.env** in the project folder, replacing `paste-your-key-here`. **Keep the key private:** do not post it, photograph it, or share it. We can cancel it at any time, and it has a spending limit.

---

## Problems and fixes

| # | What you see | What to try |
|---|---|---|
| 1 | Installer says **administrator permission** is needed | Ask the owner of the laptop (a parent) to type their password / approve. Do not change security settings yourself. |
| 2 | Windows says **virtualization is disabled** (Task Manager shows *Disabled*), or Docker says "Virtualization support not detected" | Virtualization must be switched on in the laptop's BIOS/UEFI settings. Search your laptop brand + "enable virtualization" (for example "Lenovo enable virtualization"), or **contact us**. Do not guess in BIOS. |
| 3 | Docker says **WSL 2** is missing or needs updating | In PowerShell run `wsl --update`, then restart the laptop and open Docker Desktop again. If that fails, contact us. |
| 4 | Docker Desktop is stuck on **"Starting…"** for more than 10 minutes | Restart the laptop, open Docker Desktop. Check that you have at least 8 GB RAM and about 10 GB free disk. |
| 5 | VS Code does not show **Reopen in Container** | Check that the **Dev Containers** extension is installed (Step 3) and Docker Desktop shows "Engine running". Then press Ctrl/Cmd + Shift + P and run **Dev Containers: Reopen in Container**. Make sure you opened the folder that contains `.devcontainer`. |
| 6 | **"Cannot connect to the Docker daemon"** / **"docker: command not found"** | Docker Desktop is not running or not installed properly. Open Docker Desktop, wait for "Engine running", then try again. On Windows, close and reopen PowerShell. |
| 7 | Download is very slow or fails | Try again on home Wi-Fi or a mobile hotspot. Keep the laptop awake and plugged in. Tell us if it fails twice. |
| 8 | Not enough disk space | Free about 10 GB (empty Downloads, remove big videos). Ask us if you are unsure what is safe to delete. |
| 9 | Chromebook, tablet, or an old laptop | Docker and VS Code containers will not work. **Tell us now**; we will arrange a loan laptop or share a partner's laptop. |
| 10 | `python check_env.py` shows **FAIL** for "Codex's safety sandbox starts" | Take a screenshot and send it to us. Do not try to change settings yourself. |
| 11 | `check_env.py` says it **cannot reach openrouter.ai** | Your network may block it. Try a phone hotspot. Tell us if it still fails. |
| 12 | VS Code stays on "Setting up dev container" or "Starting" for more than 15 minutes | Wait a bit more on a good connection. If nothing changes: press Ctrl/Cmd + Shift + P → **Developer: Reload Window**, or restart Docker Desktop. Tell us if it still fails. |
| 13 | Anything else | Take a screenshot of the error and send it to **[CONTACT]**. Tell us your laptop type (Windows version or Mac chip). |

**Rule of thumb:** If you have spent more than 20 minutes on one problem, stop and message us.

---

## After the workshop: remove everything (optional)

- Run `docker system prune -a` to delete the downloaded images.
- Uninstall **Docker Desktop** like any other program (Windows: Settings → Apps; Mac: drag it from Applications to the Bin).
- Uninstall **Visual Studio Code** if you do not want it.
- Delete the workshop folders when you are finished with them. Please keep your work until the challenge ends.

---

## A note for parents / guardians

Your child will install **Docker Desktop** and **Visual Studio Code**, widely used free tools (Docker runs programs inside an isolated container), and download a workshop image of about [SIZE]. Installation needs administrator permission and may need a restart. The workshop access key is issued and controlled by the organisers, is spending-limited, and is cancelled after the challenge. Students are asked not to type personal information into the AI tool. [ADD: data/privacy statement, whether prompts or chat logs are stored, who can see them, and your contact details, to be confirmed with the school.]
