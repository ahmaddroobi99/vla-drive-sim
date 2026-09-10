# VLA Drive Sim

Browser simulation of a Vision Language Action driving loop.

Camera patches and a language instruction enter one transformer style policy. The policy outputs steer, throttle, and brake on a forked road with two exits.

## Live demo

https://vla-drive-sim.vercel.app

## What it shows

- Vision tokens: 3x3 camera patches plus a forward camera crop
- Text tokens: natural language tasks (`take the second exit`, `stay in lane`, ...)
- Action chunk: steer deg, throttle in [0,1], brake in [0,1]
- Top down world with a LiDAR style sweep
- Auto policy or manual WASD

The controller is pedagogical. Language selects a reference path. Vision is a nearest point plus heading error. A PD law emits actions. This is not a trained ACT or SmolVLA checkpoint.

## Run locally

Open `index.html` or serve the folder:

```bash
python3 -m http.server 4173
```

Then visit http://localhost:4173

## Demo GIFs

![second exit](gifs/take-second-exit.gif)

![first exit](gifs/take-first-exit.gif)

![lane hold](gifs/stay-in-lane.gif)

Regenerate:

```bash
python3 make_gifs.py
```

## Stack

Static HTML, CSS, and canvas JavaScript. No build step. Vercel serves the folder as a static site.

## Related

- Course: https://vla.vizuara.ai/
- Hardware stack: https://github.com/sreedath/turbovla

## License

MIT
