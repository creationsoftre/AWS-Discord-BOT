# AWS Control via Discord (Replit)

**Tagline:** Let trusted friends control specific AWS resources through Discord — **no AWS Console access required**.  
**Stack:** Python • discord.py (Pycord-compatible) • boto3 • Replit env vars • AWS EC2

---

## Reason for this project

I built a Discord bot that exposes a **safe, role‑gated control plane** for AWS. Instead of giving AWS Console access, teammates can use Discord slash commands to **start/stop/reboot** a tagged EC2 instance and view rich **status embeds** (name, state, AZ, launch time). It demonstrates **cloud automation**, **least‑privilege design**, and **user experience** thinking—packaging real AWS operations behind a familiar chat interface with proper constraints, logging, and error handling.

---

## What the bot does

- **EC2 controls:** start, stop, reboot a pre‑selected instance (scoped by tag).
- **Status card:** posts a Discord embed with instance **Name**, **State**, **Availability Zone**, **Launch Time**.
- **Guardrails:** command cool‑downs, required Discord roles, and environment‑based secrets.
- **Ops hygiene:** session reuse, defensive error handling, optional log packaging for purged messages.

**Guide Embed**  
![AWS Guide — Discord Embed](https://github.com/creationsoftre/blob/blob/main/aws_guide.png)

**Status Embed**  
![AWS Status — Discord Embed](https://github.com/creationsoftre/blob/blob/main/aws_status.png)

---

## Architecture at a glance

```
Discord (slash commands) ──> Bot (discord.py) ──> boto3 (EC2 client) ──> AWS
         ▲                         │
         │       Replit Env Vars   │
         └───────────(tokens, keys)┘
```

- **Entry point:** `main.py` loads Cogs, wires error handlers, and runs the bot loop. It also runs a background task that polls EC2 metadata to keep the bot responsive.  
- **Cloud client & config:** `variables.py` centralizes **discord token**, **role IDs**, and constructs a **boto3 Session/EC2 client** from Replit env vars.  
- **AWS/Discord actions:** `functions.py` contains the EC2 operations and the UI helpers (status embed + a small Select‑menu view).

---

## Key files

- `main.py` — bot startup, error handling, Cog loading, and a background status task.  
- `variables.py` — central config/DI: Discord IDs + `boto3` session/client built from env vars (least‑privilege keys).  
- `functions.py` — AWS actions: get instance info, check state, start/stop/reboot, and send a rich status embed; plus admin utilities (purge + log packaging) and a small Select UI.

> Slash command handlers live in Cogs (loaded from `./cogs`). Typical Cogs wire commands like `/ec2_start`, `/ec2_stop`, `/ec2_status` to the functions here.

---

## How commands work (high‑level flow)

1. **User triggers a slash command** (e.g., `/ec2_status`).
2. **Role check & cooldowns** run (e.g., must have “EC2 role”).
3. Bot uses **EC2 tag filtering** to identify the instance and read state.
4. For control commands, the bot **defers ephemerally**, calls the EC2 API, logs the action, and replies with a **clear outcome**.
5. Status uses a **Discord embed** with colored state indicators and metadata.

---

## Setup (Replit)

1. Create a new Replit (Python).  
2. Add **Secrets** (Environment Variables):  
   - `aws-BOT_Token` — your Discord bot token  
   - `aws_access_key_id` — AWS access key (least privilege)  
   - `aws_secret_access_key` — AWS secret key  
3. In `variables.py`, set IDs for your server/roles and the **EC2 tag value** for the instance you want to control.  
4. Ensure the AWS user/role has **only** the following permissions (example minimal policy):  
   - `ec2:DescribeInstances`  
   - `ec2:StartInstances` (restricted to the instance ARN you allow)  
   - `ec2:StopInstances` (restricted)  
   - `ec2:RebootInstances` (restricted)  
5. Invite the Discord bot to your server with the required scopes/permissions.  
6. Run the repl. The bot will load Cogs from `./cogs` and start listening.

---

## Local development

```bash
pip install -r requirements.txt  # discord.py / py-cord, boto3, etc.
python main.py
```

> You’ll need the same env vars locally. On macOS/Linux: `export aws-BOT_Token=...` etc.

---

## Security & Ops Notes

- **Least privilege:** Scope EC2 actions to a single instance by **tag** and restrict IAM by **resource ARN**.  
- **No console exposure:** Users never see the AWS Console or keys; actions happen via the bot.  
- **Role gates:** Only users with the configured **Discord role ID** can run control commands.  
- **Cooldowns & error UX:** Friendly ephemeral responses and cooldown handling improve safety and clarity.  
- **Auditing:** Consider posting an audit embed to a log channel and/or writing structured logs to a durable store.

---

## What I’d improve next

- **Slash command Cogs:** Add typed options (e.g., `/ec2_status instance:<select by tag>`).  
- **Multi‑resource support:** Allow safe operations for SSM docs, SQS purge, or RDS start/stop windows.  
- **Observability:** Structured JSON logs + a small dashboard (e.g., CloudWatch Logs Insights).  
- **Permissions wizard:** A script that autogenerates a least‑privilege IAM policy from the configured instance tag.  
- **Safer discovery:** Replace `Win32_Product`‑style approaches in other contexts with metadata or registry reads.  
- **Testing:** Mocks for boto3 and discord to CI test the command flows.

---

## License

MIT
