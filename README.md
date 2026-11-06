<p align="center">
  <img src="assets/banner.svg" alt="Jordan Dominick: local AI on AMD hardware: GPUs, NPUs and radios" width="100%">
</p>

<p align="center">
  <b>I make local AI run fast on the AMD hardware on my desk, and build the tools I want along the way.</b><br>
  Two Radeon GPUs, a Ryzen AI NPU and an Ubertooth: inference engines, model quants, dashboards and radio tools.
</p>

<p align="center">
  <a href="https://huggingface.co/jdominick05"><img src="https://img.shields.io/badge/Hugging%20Face-jdominick05-ffb547?style=flat-square&labelColor=1b1e24&logo=huggingface&logoColor=white" alt="Hugging Face: jdominick05"></a>
  <a href="https://pypi.org/project/caminus/"><img src="https://img.shields.io/badge/PyPI-caminus-ffb547?style=flat-square&labelColor=1b1e24&logo=pypi&logoColor=white" alt="PyPI: caminus"></a>
  <a href="mailto:j.dominick2005@proton.me"><img src="https://img.shields.io/badge/email-j.dominick2005%40proton.me-ffb547?style=flat-square&labelColor=1b1e24&logo=protonmail&logoColor=white" alt="email: j.dominick2005@proton.me"></a>
  <img src="https://img.shields.io/badge/Discord-exalted__._-ffb547?style=flat-square&labelColor=1b1e24&logo=discord&logoColor=white" alt="Discord: exalted_._">
  <img src="https://img.shields.io/badge/based%20in-Maryland-8b8f98?style=flat-square&labelColor=1b1e24" alt="based in Maryland">
</p>

## About me

- **I tune local AI for the hardware it runs on.** Mostly large mixture-of-experts language models on two Radeon cards, and vision models on the NPU inside a Ryzen AI chip.
- **I build with AI coding agents.** I decide what to build, write the specs and tests, and run everything on my own machines; agents (Claude Code, and Qwen Code running on my own engine) write most of the code.
- **I publish the evidence.** Benchmarks in these repos come with their method and logs, including the cases where AMD's own stack or upstream llama.cpp still wins.
- **Security background:** CyberPatriot, and the National Cyber League (2021, my team placed in the top 100 in Georgia).
- **Looking for IT support / help desk work**, remote or around Maryland.

## Projects

### Local LLMs on two Radeon GPUs

| Project | What it is | Headline |
|---|---|---|
| [**Caminus**](https://github.com/jdominick05/caminus) | An inference engine written for two RDNA3 GPUs from the kernel up. It serves the Qwen3.8-Flash-Next Coder to Qwen Code, Claude Code and other harnesses over OpenAI- and Anthropic-compatible APIs. | About **104 tok/s**, **123–203 tok/s** with DFlash drafting: about twice llama.cpp on the same two cards. <br><a href="https://pypi.org/project/caminus/"><img src="https://img.shields.io/pypi/v/caminus?style=flat-square&labelColor=1b1e24&color=ffb547&label=pip%20install%20caminus" alt="PyPI version"></a> |
| [**ignite‑llama**](https://github.com/jdominick05/ignite-llama) | My llama.cpp fork, tuned for Qwen3.8 Flash-Next decode on RDNA3 (ROCm/HIP). | **58.7 tok/s** against 36.3 with stock llama.cpp kernels (RX 7900 XTX + 7900 XT). |
| [**Flash-Next REAP-288 GGUF**](https://huggingface.co/jdominick05/Qwen3.8-Flash-Next-REAP-288-44GB-262k-GGUF) | A 288-expert prune of Qwen3.8 Flash-Next, quantized to run its full 262k context on 24 + 20 GB of VRAM. | <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fhuggingface.co%2Fapi%2Fmodels%2Fjdominick05%2FQwen3.8-Flash-Next-REAP-288-44GB-262k-GGUF&query=%24.downloads&label=downloads%2Fmonth&color=ffb547&style=flat-square&labelColor=1b1e24&logo=huggingface&logoColor=white" alt="Hugging Face downloads last month"> |
| [**Qwen3.8-27B GGUF**](https://huggingface.co/jdominick05/Qwen3.8-27B-24GB-262k-GGUF) | Mixed-precision quants that fit the full 262,144-token context on a single 24 GB GPU. | <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fhuggingface.co%2Fapi%2Fmodels%2Fjdominick05%2FQwen3.8-27B-24GB-262k-GGUF&query=%24.downloads&label=downloads%2Fmonth&color=ffb547&style=flat-square&labelColor=1b1e24&logo=huggingface&logoColor=white" alt="Hugging Face downloads last month"> |
| [**llm‑top**](https://github.com/jdominick05/llm-top) | `top` for your local LLM: a live terminal dashboard for llama-server or LM Studio, and the Qwen Code agents using it. Written in Go. | <a href="https://github.com/jdominick05/llm-top/releases/latest"><img src="https://img.shields.io/github/v/release/jdominick05/llm-top?style=flat-square&labelColor=1b1e24&color=ffb547" alt="latest release"></a> |

### AI on the Ryzen AI NPU

| Project | What it is | Headline |
|---|---|---|
| [**Ignition**](https://github.com/jdominick05/Ignition) | Real-time YOLO on the AMD Ryzen AI (XDNA1) NPU, with a one-line install. | Faster end to end than AMD's own runtime on YOLOv8n, YOLO11n, YOLO26n and YOLOv8n-pose, and more accurate, from a fraction of the install size. |
| [**ignite‑xdna**](https://github.com/jdominick05/ignite-xdna) | The research behind Ignition: a bare-metal engine for the XDNA1 NPU, and every measurement behind it. | YOLOv8n in **7.15 ms** against 10.84 on AMD's stack (10.2 once its compiler is tuned), COCO mAP 34.1 against 26.7. Where AMD still wins is on the page too. |
| [**ignite‑scribe**](https://github.com/jdominick05/ignite-scribe) | An MCP server that turns your Windows desktop into redacted text an AI agent can read. | Password fields are never read; secrets are removed before anything leaves your PC. |

### Radio

| Project | What it is | Headline |
|---|---|---|
| [**fang**](https://github.com/jdominick05/fang) | A receive-only Ubertooth One toolkit: 2.4 GHz spectrum analyzer, BLE scanner, tracker detector and Classic Bluetooth survey. | Software CRC checks remove the stock tools' ghost devices; the spectrum view is about 12 dB more sensitive. |

## On my desk

- **GPUs:** AMD Radeon RX 7900 XTX (24 GB) + RX 7900 XT (20 GB), ROCm on Linux
- **NPU:** AMD Ryzen 7 8700G (XDNA1), Windows 11
- **Radio:** Ubertooth One
- **Agents:** Claude Code, Qwen Code

<p align="center"><sub>Every number on this page comes from the linked repo or model card.</sub></p>
