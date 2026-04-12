# le-vibe bootstrap report

Generated: 2026-04-12T00:04:46.242719+00:00

## OS

- **Type:** linux
- **Name:** Linux
- **Version:** 6.17.0-20-generic
- **Arch:** x86_64

## Hardware

- **CPU:** AMD Ryzen 9 6900HS with Radeon Graphics
- **RAM total:** 30.6 GiB
- **RAM available:** 18.3 GiB
- **Disk free:** 56.4 GiB
- **Acceleration:** gpu
- **Apple Silicon:** False

### GPUs

- NVIDIA NVIDIA GeForce RTX 3080 Ti Laptop GPU VRAM: 16.0 GiB



## Prerequisites


- **internet:** ok — reachable https://ollama.com

- **curl:** ok — /usr/bin/curl

- **tar:** ok — /usr/bin/tar

- **systemctl:** ok — present


## Tier assessment


- **Selected tier:** `tier_32b_possible_but_slow`
- **Notes:** ram=30.6GB avail=18.3GB; disk_free=56.4GB; max_vram≈16.0GB; accel=gpu
- **Scores:** ram=0.24, vram=0.20, cpu=0.75, disk=0.28


### Rejected higher tiers


- `tier_70b_candidate`: insufficient VRAM/unified memory or RAM for 70B-class comfortable run

- `tier_32b_comfortable`: not enough comfortable memory headroom for 32B




## Model decision


- **Model:** `deepseek-r1:14b`
- **Tier:** `tier_32b_possible_but_slow`
- **Comfortable:** True
- **Reason:** First available model in deepseek-r1 ladder matching tier tier_32b_possible_but_slow. ram=30.6GB avail=18.3GB; disk_free=56.4GB; max_vram≈16.0GB; accel=gpu


### Rejected candidates


- `deepseek-r1:70b`: 70B requires tier_70b_candidate

- `deepseek-r1:32b`: 32B is possible-but-slow on this machine; use --allow-slow for 32B




## Ollama

- **Installed:** True
- **Version:** ollama version is 0.12.9
- **Was running before:** True
- **Started by script:** False
- **Port in use before:** 
- **API verified:** True
- **Endpoint:** `http://127.0.0.1:11434`
- **Dry run:** False




### Pull log (excerpt)

```
ok
```


## Continue

Import `output/continue-config.yaml` into the Continue extension. apiBase should be `http://localhost:11434`.

## Start / stop / status

See `README.md` for OS-specific `scripts/` helpers.