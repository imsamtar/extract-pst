# extract-pst

Extract emails and attachments from Microsoft Outlook `.pst` files — fully Dockerized, no local dependencies.

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Docker](https://img.shields.io/badge/Docker-required-2496ED?logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)

## Features

- **Batch extraction** — drop any number of `.pst` files into `pst_files/` and run a single command
- **Deep extraction** — powered by `readpst` (`libpst`) to walk every folder in the archive
- **mbox → EML conversion** — every message is written as a standard `.eml` file, openable in any mail client
- **Attachment extraction** — attachments are saved alongside their message in `<message>-attachments/` folders
- **Zero setup** — everything runs in a container; inputs and outputs live on your host via mounted volumes

## Quick start

1. Place your `.pst` files in the `pst_files/` directory
2. Run:

   ```bash
   docker compose up --build
   ```

3. Find your extracted emails in `output_emails/<pst-file-name>/`

Each archive gets its own folder, with the original folder hierarchy preserved:

```
output_emails/
└── my-archive/
    ├── Inbox/
    │   ├── message_1.eml
    │   ├── message_1-attachments/
    │   │   └── invoice.pdf
    │   └── message_2.eml
    └── Sent/
        └── message_3.eml
```

## How it works

```
.pst ──readpst──▶ .mbox (per folder) ──mbox_to_eml.py──▶ .eml + attachments
```

| Stage | Tool |
|---|---|
| PST → mbox | `readpst -D` ([pst-utils](https://packages.debian.org/stable/pst-utils)) |
| mbox → EML + attachments | [`mbox_to_eml.py`](mbox_to_eml.py) (Python stdlib only) |

Re-running the container wipes previous extraction folders and starts fresh.

## Project structure

```
extract-pst/
├── pst_files/           # drop your .pst files here (gitignored)
├── output_emails/       # extracted emails land here (gitignored)
├── extract.sh           # orchestration: clean → extract → convert
├── mbox_to_eml.py       # mbox → eml + attachment extraction
├── Dockerfile
└── docker-compose.yaml
```

## Privacy

Your `.pst` files and extracted emails are gitignored, mounted from your host, and never leave your machine — nothing user-specific is baked into the image.

## License

[MIT](LICENSE)
