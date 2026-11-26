# Set Up Your Laptop for the Workshop

**Build with AI: Make It Work, Make It Reliable**

| | |
|---|---|
| **Do this by** | Sunday, 29 November 2026 |
| **Time needed** | About 45-60 minutes, plus download time. Do it on home Wi-Fi, not at school, with your charger plugged in. |
| **Stuck? Contact** | Please contact congthanh_le@sutd.edu.sg if you have any troubles. Tell us early. If a step fails, it may be not your fault: laptops are different and we have backup options. |

In the workshop you will build a delivery robot together with an AI coding agent: a software that can write code, run commands and change files when you ask it to. You will work in small steps, predict what will happen, test it, and learn how to use AI responsibly.

This guide gets your laptop ready. You do **not** need any coding experience. You do **not** need an AI account or an access key: we give you the key on the workshop day. Please do **not** sign up for any AI service for this workshop.

A Word version of this guide with pictures is in this folder: `Student_Setup_Guide.docx`.

---

## 1. What you are setting up, and why

An AI agent is powerful, but it can also make mistakes. So, we do not let it run directly on your laptop. We put it inside a **sandbox**: a sealed box on your laptop. The AI can only touch **one folder** that you share with the box. It cannot see your photos, school files, passwords or anything else. Using AI responsibly starts with limiting what it can touch.

You will install two programs. Everything else comes inside the box.

| Program | What it does for you |
|---|---|
| **Docker Desktop** | Builds and runs the sealed box (called a **container**) on your laptop. |
| **Visual Studio Code (VS Code)** | A free editor. It shows your files and gives you a **terminal** (a place to type commands). With the Dev Containers extension, it opens your folder **inside** the box. |
| **Dev Containers** (extension) | The small add-on that lets VS Code work inside the docker. |
| **Codex** | The AI coding agent. It lives inside the box. On the workshop day you start it by typing `codex` in the VS Code terminal. |
| **MiniGrid** | The library that makes the robot world. It is already inside the box. |

## 2. Before you start

**What you need**

- Your own laptop: Windows 10 (version 22H2 or newer) or Windows 11 or Ubuntu, or a Mac with a recent macOS.
- At least **8 GB of RAM** and about **15 GB of free disk space**.
- Your charger and home Wi-Fi. The downloads are large, so please do it with stable internet connection.
- **Permission to install software.** Ask the owner of the laptop (for example a parent) if you are not sure. Windows may ask for an administrator password.

## 3. Step by step

### Step 1. Install Docker Desktop (10 to 20 minutes)

1. Go to **https://www.docker.com/products/docker-desktop/** and download Docker Desktop for your system.
2. Open the installer and follow the official instructions.
3. If Docker asks you to **sign in or create an account**, look for **Skip** and use it. You do not need an account. Accept the terms if asked.
4. Wait until Docker Desktop shows **"Engine running"** (a green dot at the bottom left). The first start can take a few minutes.

### Step 2. Test that Docker works (2 minutes)

Open a terminal. **Windows:** press the Windows key, type **PowerShell** and open **Windows PowerShell**. **Mac:** press **Cmd + Space**, type **Terminal** and press Enter.

Type this and press Enter:

```
docker run hello-world
```

You should see a message that starts with **"Hello from Docker!"**. The first time, Docker downloads a tiny test program, so you will also see some lines about pulling an image.

> **If you see an error:** read the message. "Cannot connect to the Docker daemon" usually means Docker Desktop is not running yet: open it and wait for "Engine running".

### Step 3. Install VS Code and the Dev Containers extension (5 to 10 minutes)

1. Go to **https://code.visualstudio.com/** and install **Visual Studio Code** (it is free). Open it once.
2. Click the **Extensions** icon in the left bar (it looks like four squares). Search for **Dev Containers** (by Microsoft) and click **Install**.

### Step 4. Download the sandbox and the workshop folder (10 to 20 minutes)

This is a large download. **Use home Wi-Fi, keep the laptop plugged in, and keep Docker Desktop open.**

1. In the terminal from Step 2, type the command below and press Enter. It downloads the sandbox (called an **image**). Wait until it finishes.

   ```
   docker pull ghcr.io/thanhlecongg/jc-workshop:1.0
   ```

2. Download the workshop folder from **https://github.com/thanhlecongg/JCWorkshop**
3. Unzip it to a place you can find, for example **C:\JCWorkshop** (Windows) or **Documents/JCWorkshop** (Mac). **Windows: do not put it inside OneDrive or Desktop.** Those folders are synced and can cause errors.

### Step 5. Open it in the sandbox (a few minutes, the first time)

1. Make sure Docker Desktop is running. In VS Code choose **File, then Open Folder...** and select the folder you unzipped (the one that contains `check_env.py`). If VS Code asks whether you trust the authors, choose **Yes, I trust the authors**.
2. A pop-up appears at the bottom right. Click **Reopen in Container**. If you miss it, press **Ctrl/Cmd + Shift + P**, type `Reopen in Container` and press Enter.
3. **Wait.** The first time takes a few minutes because VS Code installs its tools inside the box. When it is finished, the bottom-left corner of VS Code shows **Dev Container: Workshop environment check**.

> **Why we do this at home:** the first start downloads a lot. Doing it now means that on the workshop day opening the box is much faster.

### Step 6. Run the check (5 minutes)

1. Open the terminal **inside VS Code**: choose **Terminal, then New Terminal**. Check that the bottom-left still says Dev Container.
2. Type this and press Enter:

   ```
   python check_env.py
   ```

You will see a list of checks. Each line is marked **OK**, **WARN** or **FAIL**.

| Mark | What it means |
|---|---|
| **OK** | This part works. |
| **WARN** | Something is not perfect, but it is not a problem yet. Read the message. If you changed something, run the check again. |
| **FAIL** | Something must be fixed. Take a screenshot and send it to us. Do not try to change settings yourself. |

**Watch the demo robot.** The check also makes a small replay. In the VS Code left bar, open the **out** folder and click **robot_demo.gif**. You will see a delivery robot carry lunch to a hungry student. It goes around a cart, keeps out of a no-entry room, and waits for a student who walks across its way. At the end the student smiles.

> **You are done!** Close VS Code and Docker Desktop if you like. Nothing else is needed until the workshop day.

---

## 4. If something goes wrong

**Rule of thumb:** if you have spent more than 20 minutes on one problem, stop and message us. Take a screenshot of the error first.

| # | What you see | What to try |
|---|---|---|
| 1 | The installer says **administrator permission** is needed | Ask the owner of the laptop (a parent) to type their password or approve. Do not change security settings yourself. |
| 2 | Windows says **virtualization is disabled** (Task Manager shows Disabled), or Docker says "Virtualization support not detected" | Virtualization must be switched on in the laptop's BIOS/UEFI settings. Search your laptop brand plus "enable virtualization" (for example "Lenovo enable virtualization"), or **contact us**. Do not guess in the BIOS. |
| 3 | Docker says **WSL 2** is missing or needs updating | In PowerShell run `wsl --update`, restart the laptop and open Docker Desktop again. If that fails, contact us. |
| 4 | Docker Desktop is stuck on **"Starting..."** for more than 10 minutes | Restart the laptop and open Docker Desktop. Check that you have at least 8 GB of RAM and about 15 GB of free disk space. |
| 5 | VS Code does not show **Reopen in Container** | Check that the **Dev Containers** extension is installed (Step 3) and Docker Desktop says "Engine running". Then press Ctrl/Cmd + Shift + P and run **Dev Containers: Reopen in Container**. Make sure you opened the folder that contains `.devcontainer`. |
| 6 | "Cannot connect to the Docker daemon" or "docker: command not found" | Docker Desktop is not running or not installed properly. Open Docker Desktop, wait for "Engine running" and try again. On Windows, close and reopen PowerShell. |
| 7 | A download is very slow or fails | Try again on home Wi-Fi or a mobile hotspot. Keep the laptop awake and plugged in. Tell us if it fails twice. |
| 8 | Not enough disk space | Free about 15 GB (empty Downloads, remove big videos). Ask us if you are unsure what is safe to delete. |
| 9 | `python check_env.py` shows **FAIL** for "Codex's safety sandbox starts" | Take a screenshot and send it to us. Do not try to change settings yourself. |
| 10 | `check_env.py` says it **cannot reach openrouter.ai** | Your network may block it. Try a phone hotspot. Tell us if it still fails. |
| 11 | VS Code stays on "Setting up dev container" for more than 15 minutes | Wait a bit more on a good connection. If nothing changes, press Ctrl/Cmd + Shift + P and choose **Developer: Reload Window**, or restart Docker Desktop. Tell us if it still fails. |
| 12 | Anything else | Take a screenshot of the error and send it to congthanh_le@sutd.edu.sg. Tell us your laptop type. |

---

## 5. On the workshop day

**Bring**

- Your laptop, **fully charged**, and your charger.
- Docker Desktop already installed and **opened once**. Start it before the session so it says "Engine running".
- VS Code installed, with the Dev Containers extension.

**We will give you** a link to the **workshop project** (on Git) and a short **access key**.

1. Download the workshop project from the link and unzip it (again: not in OneDrive or Desktop).
2. Paste your key into the file named **.env** in the project folder, replacing `paste-your-key-here`. The line must look like `OPENROUTER_API_KEY=` followed by your key, with no spaces and no quotes. (If you cannot see `.env`, open the folder once in VS Code, paste the key, then choose **Dev Containers: Rebuild Container**.)
3. Open the project folder in VS Code and choose **Reopen in Container**, the same way as in Step 5.
4. In the VS Code terminal, you start the AI agent by typing `codex`. We will show you how.

> **Keep your access key private.** Do **not** post it, photograph it, share it, or paste it into a chat or a file you upload. We can cancel it at any time, and it has a spending limit. If you think someone saw it, tell us straight away. We will give you a new one.