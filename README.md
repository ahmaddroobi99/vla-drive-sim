# VLA Drive Sim

Browser simulation of a Vision Language Action driving loop.

**Live demo:** https://ahmaddroobi99.github.io/vla-drive/

**Source:** https://github.com/ahmaddroobi99/vla-drive-sim

Camera patches and a language instruction enter one transformer style policy. The policy outputs steer, throttle, and brake on a forked road with two exits.

The controller is pedagogical. Language selects a reference path. Vision is a nearest point plus heading error. A PD law emits actions. This is not a trained ACT or SmolVLA checkpoint.

## Run locally

```bash
python3 -m http.server 4173
```

Then open http://localhost:4173

Regenerate demo GIFs with `python3 make_gifs.py`.

## License

MIT
