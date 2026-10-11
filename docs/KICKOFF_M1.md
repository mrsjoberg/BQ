# Kick-off: build Milestone 1 (the journey skeleton) of BQ

You are **Claude Code running inside my WSL** (Ubuntu 26.04, ARM64), in my clone of `mrsjoberg/BQ`. You work with two MCP servers:
- **Godot MCP** (`Coding-Solo/godot-mcp`);
- the official **Blender Lab MCP**, talking to Blender 5.2 LTS on the Windows side.

You are building Milestone 1 of **BQ**: a portrait mobile game in Godot 4.7.2. The player travels across a 3D map of the UK through history, preparing for the Life in the UK test. The spec in the repo is the source of truth.

## Repo and branch
- The spec is on branch `claude/upbeat-cray-2adgy3`. There is no `main` yet.
- Create a branch `m1-skeleton` from it, and push your work there.

## Read first, in this order
1. `docs/SPEC.md`, all of it. Pay most attention to:
   - the Decisions table and §2 (M1 scope);
   - §3–6: player experience, journey data, map and look, tuning;
   - §8 technical design, **including §8.8 (art pipeline) and §8.9 (AI tooling)**;
   - §9 performance, §10 workflow, §11 CI;
   - §13: the M1 steps and the 11 acceptance criteria.
2. `content-src/README.md` and `content-src/journey_draft.json`: the 78-stop journey data.
3. `docs/LEARNING_DESIGN.md`, §5.4 only: the extension points M1 must leave in place.

## Step 0: tooling check (before anything else)
1. **Godot MCP:** `get_godot_version` must report 4.7.2.
   - If Godot, Node.js or the MCP aren't installed yet, set them up as SPEC §10.1 and §8.9 describe. **Ask me before installing anything.**
   - Add a project-scope `.mcp.json`. Take machine-specific paths from environment variables (for example `${BQ_GODOT_PATH}`) and pin the godot-mcp version.
2. **Blender MCP:** ask Blender for its version and current scene.
   - Blender runs on Windows. Reach it through WSL mirrored networking (`localhost`), or fall back to launching the Windows-side server through WSL interop.
   - Install the server as blender.org/lab/mcp-server describes.
   - If it won't connect, stop and tell me what to check. Don't work around it silently.
3. Report in a few lines: versions, what works, and what doesn't.

## Your job: M1 in the five steps of SPEC §13
1. M1.1 toolchain + MCPs + "hello map"
2. M1.2 terrain + camera
3. M1.3 journey, with the piece, boat and pins made in Blender
4. M1.4 chapters
5. M1.5 tuning + performance

The milestone is done when all 11 acceptance criteria in §13 are met.

## Hard rules
- **Scope:** M1 only. No lessons, quizzes, Passport, audio or final art. Build only the extension points in SPEC §8.6.
- **CI:** never trigger GitHub Actions; nothing may run on push or pull request. The only workflow in M1 is the manual-only fallback `android-test-apk.yml`.
- **Before every push:** run `./tools/test.sh` plus a full debug export. For anything visual, also look at fresh screenshots from `tools/shot.sh`. Never push a broken build.
- **Blender MCP safety:** it runs your Python inside Blender with no safeguards.
  - Only create or change files under `art/`; never delete anything outside it.
  - Keep each script short and readable. I approve every call.
- **Art pipeline (SPEC §8.8):**
  - `.blend` sources go in `art/`.
  - Export with `art/export_glb.py` to `game/assets/models/*.glb`, and commit the result.
  - Vertex colours only: no textures, no skeletons.
  - Stay within the triangle budgets.
  - Render a preview to `art/<asset>/preview.png`.
  - Godot must never import `.blend` files.
- **Godot files:**
  - Scenes and resources are text (`.tscn`, `.tres`).
  - GDScript uses static typing.
  - Review changes made through the MCP as carefully as your own code.
- **Never commit** the handbook PDF or its text, secrets or keystores. Don't open a PR unless I ask.
- **Gameplay questions:** if the spec is unclear or contradicts itself on gameplay, ask me. Small technical choices are yours; note them in the commit message.

## How we work
- After the tooling check, send me a short plan for M1.1 plus any questions the spec doesn't answer. Wait for my go-ahead before writing code.
- After each step, commit and push, then tell me:
  1. what to run;
  2. what to check on the phone (SPEC Appendix A);
  3. what you could not verify.

  `./tools/phone.sh` builds the test APK and installs it on my phone. You may run it yourself, but ask first.

  Then **stop and wait for my phone feedback** before starting the next step.
- **My phone:** a budget Android 11+ phone, paired over Wi-Fi. Ask me for the exact model in M1.2.

## Facts checked in October 2026 (re-check if something fails)

**Tools**
- **Blender:** Blender 5.2 LTS (released 14 Jul 2026) has a Windows ARM64 build but no official Linux ARM64 build, so Blender stays on Windows.
- **Blender Lab MCP:** the add-on (1.0.3) needs Blender 5.1+, and it runs AI-written Python without safeguards.
- **Godot MCP:**
  - Install: `claude mcp add godot -e GODOT_PATH=<path> -- npx @coding-solo/godot-mcp`. Needs Node.js 18+.
  - Tools: `launch_editor`, `run_project`, `get_debug_output`, `stop_project`, `get_godot_version`, `list_projects`, `get_project_info`, `create_scene`, `add_node`, `load_sprite`, `export_mesh_library`, `save_scene`, `get_uid`, `update_project_uids`.
  - It takes no screenshots; that's why `tools/shot.sh` exists. The game windows it opens appear through WSLg.
- **WSL mirrored networking:** in `%UserProfile%\.wslconfig`, put `networkingMode=mirrored` under `[wsl2]`, then run `wsl --shutdown`. After that, WSL reaches Windows services on `localhost`.
- **Paths between WSL and Windows:** Windows sees the repo at `\\wsl.localhost\Ubuntu\home\<user>\BQ`. Translate paths with `wslpath -w` and `wslpath -u`.

**Godot 4.7.2-stable downloads**
- URL pattern: `https://github.com/godotengine/godot/releases/download/4.7.2-stable/Godot_v4.7.2-stable_<suffix>`.
- Suffixes: `linux.arm64.zip`, `linux.x86_64.zip`, `export_templates.tpz` (1.28 GB). Checksums are in `SHA512-SUMS.txt` in the same release.
- The `.tpz` is a zip. Fetch only `templates/android_debug.apk`, `templates/android_release.apk` and `templates/version.txt`, using HTTP range requests (about 232 MB). Put them in `~/.local/share/godot/export_templates/4.7.2.stable/`.

**Android export without Gradle**
- Godot checks that `<java>/bin/java` exists, and that the Android SDK folder contains `platform-tools/adb` and `build-tools/<version>/apksigner` (it prefers 36.x).
- Godot zipaligns the APK itself, so no zipalign is needed.
- Set `rendering/textures/vram_compression/import_etc2_astc=true` in the project settings.
- Debug keystore via the environment variables `GODOT_ANDROID_KEYSTORE_DEBUG_PATH`, `GODOT_ANDROID_KEYSTORE_DEBUG_USER` and `GODOT_ANDROID_KEYSTORE_DEBUG_PASSWORD`. The keystore password and key password must be the same.
- Defaults are minSdk 24 and targetSdk 36. New export presets enable only arm64-v8a, so add armeabi-v7a.
- AAB bundles need the Gradle build, which only runs in CI on x86-64.

**Godot command line**
- Import: `godot --headless --path game --import`
- Export: `--export-debug "<preset>" <output path>`. The output folder must already exist.

**Ubuntu 26.04 arm64 packages**
- `adb` (version 34.0.5) has no mDNS discovery. Pair with `adb pair IP:PORT CODE`, connect by IP:port, then run `adb tcpip 5555` to get a fixed port that lasts until the phone reboots.
- `apksigner` is Java-based and pulls in `default-jre`.
- Also needed: `openjdk-17-jdk-headless`, `python3-numpy` and `nodejs`.
- Google ships no Linux ARM64 Android SDK binaries. Point Godot at a tiny SDK folder that symlinks to these packages.

**Compatibility renderer**
- Mesh LOD and visibility ranges work, but without fading.
- Depth and height fog work but show banding (8-bit).
- `scaling_3d_scale` works (bilinear).
- There is no shader precompilation, so warm up every material while loading.
- MSAA causes grey artifacts on the PowerVR GE8320; keep it off on PowerVR GPUs.
- The Swappy frame-pacing library is Vulkan-only, so it doesn't help this renderer.

**Terrain data**
- Use GEBCO_2026: public domain, credit GEBCO, DOI `10.5285/4f68d5c7-45eb-f999-e063-7086abc036fa`. One request fetches the UK subset:
  `https://dap.ceda.ac.uk/thredds/wcs/bodc/gebco/global/gebco_2026/ice_surface_elevation/netcdf/GEBCO_2026.nc?service=WCS&version=1.0.0&request=GetCoverage&coverage=elevation&crs=OGC:CRS84&bbox=-11,49,2.6,61&format=GeoTIFF_Float`
  The `crs` must be `OGC:CRS84`. This interface is undocumented by GEBCO; the documented fallback is OPeNDAP on the same server.
- Do **not** use NOAA ETOPO 2022: its UK land layer comes from FABDEM, which is licensed for non-commercial use only.
- UK land mask: Natural Earth 1:10m admin-0 countries (public domain), `https://naciscdn.org/naturalearth/10m/cultural/ne_10m_admin_0_countries.zip`.

**Font**
- Atkinson Hyperlegible Next, OFL 1.1: `https://raw.githubusercontent.com/google/fonts/main/ofl/atkinsonhyperlegiblenext/AtkinsonHyperlegibleNext%5Bwght%5D.ttf`
- Ship `OFL.txt` with the game.

**Start now:** run the tooling check, read the files above, then send me the results, your M1.1 plan and your questions.
