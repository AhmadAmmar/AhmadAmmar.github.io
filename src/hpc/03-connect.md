---
title: Connecting securely
slug: connect
description: SSH keys, passphrases, multi-factor authentication and a login shortcut.
---

## How SSH keys work

**SSH** (Secure Shell) is an encrypted remote terminal (OpenSSH, n.d.). Instead of a password, it can use a matched pair of files. The **public key** is like a padlock: you can give out copies, and the cluster fits one to your account. The **private key** is the only thing that opens it, and it stays on your computer. A **passphrase** locks the private key in case your laptop is stolen.

**Never share your private key, its passphrase or your MFA secret with anybody**, including IT staff or a colleague. Only the file ending in `.pub` is safe to send.

## Step 1: Make a key pair

```powershell
# laptop (PowerShell on Windows 10 or later; on macOS or Linux, use ~/.ssh/ instead)

# Make the folder that SSH looks in. -Force means no error if it exists
mkdir $HOME\.ssh -Force

# -t chooses the key type, -b its size in bits, -f the file name
ssh-keygen -t rsa -b 4096 -f $HOME\.ssh\my-kelvin-key
```

Set a passphrase when asked: Kelvin2 requires one. Nothing appears as you type, which is normal. This creates `my-kelvin-key` (private) and `my-kelvin-key.pub` (public). A forgotten passphrase cannot be recovered: you have to make a new pair.

## Step 2: Give the cluster your public key

Each cluster has its own process. **Kelvin2 only:** apply through the [access page](https://www.qub.ac.uk/sites/ni-hpc/Kelvin2/Access/); the documentation says to allow 48 hours. If you are outside the QUB network, as Ulster University users are, you send NI-HPC the public key, as set out in [their connection guide](https://ni-hpc.github.io/nihpc-documentation/Connecting%20to%20Kelvin2/).

```powershell
# laptop
# Copy the public key to the clipboard, ready to paste
Get-Content $HOME\.ssh\my-kelvin-key.pub | Set-Clipboard
```

## Step 3: Log in, and set up MFA

```powershell
# laptop
# -p: network port. -i: which private key. Then username@address
ssh -p 55890 -i $HOME\.ssh\my-kelvin-key <username>@login.kelvin.alces.network
```

**Kelvin2 only.** Port 55890 and this address are for connecting from outside the QUB network. From inside it, the address is `kelvin2.qub.ac.uk` on the normal port. MFA is mandatory. On first login, generate it:

```bash
# cluster
/opt/flight/bin/flight mfa generate
```

Scan the QR code into an authenticator app. From then on, each login asks for `Verification code:`. If you lose the app, NI-HPC can reset it.

You land on one of four login nodes, shown in your prompt: `[<username>@login1 [kelvin2] ~]$`. The first time you reach a new login node you may see a warning about the host's identity. The connection guide explains what to do; read it rather than clicking through.

## Step 4: Make a shortcut

The file `.ssh/config` on your laptop stores settings under a nickname. Open it with `notepad $HOME\.ssh\config`, and add the lines below. Comments must be on their own line in this file.

```text
# laptop: .ssh/config
# The nickname you will type
Host kelvin
  # The real address
  HostName login.kelvin.alces.network
  Port 55890
  User <username>
  # Your private key
  IdentityFile ~/.ssh/my-kelvin-key
  # Send a small signal every 60 seconds, so that idle sessions stay up
  ServerAliveInterval 60
```

Now `ssh kelvin` is enough, and `scp` understands `kelvin:` as well.

## Step 5: Optional: stop retyping the passphrase

```powershell
# laptop (the first line may need an administrator PowerShell)

# Have the Windows SSH agent start automatically
Get-Service ssh-agent | Set-Service -StartupType Automatic
Start-Service ssh-agent

# Hand it your key: it holds the unlocked key in memory
ssh-add $HOME\.ssh\my-kelvin-key
```

You will still need the MFA code. `exit` ends a session.

If you prefer a graphical program on Windows, NI-HPC's guide also covers MobaXterm and PuTTY.
