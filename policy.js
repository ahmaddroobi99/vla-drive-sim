const Policy = (() => {
  const TASKS = [
    { id: "exit2", text: "take the second exit", tags: ["route", "exit", "now"], path: "exit2" },
    { id: "exit1", text: "take the first exit", tags: ["route", "exit"], path: "exit1" },
    { id: "straight", text: "stay in lane", tags: ["route", "now"], path: "straight" },
    { id: "slow", text: "slow down and hold lane", tags: ["now"], path: "straight", slow: true }
  ];
  function step(car, task, manual) {
    const path = World.PATHS[task.path];
    const n = World.nearest(path, car);
    const look = Math.min(path.length - 1, n.i + 8);
    const wantYaw = World.headingAt(path, look);
    let yawErr = wrap(wantYaw - car.yaw);
    const lat = signedLat(path[n.i], path[Math.min(path.length - 1, n.i + 1)], car);
    yawErr += 0.012 * lat;
    let throttle = task.slow ? 0.18 : 0.42;
    let brake = 0;
    if (Math.abs(yawErr) > 0.35) { throttle *= 0.55; brake = 0.12; }
    if (car.v > (task.slow ? 18 : 34) / 3.6) brake = Math.max(brake, 0.2);
    let steerDeg = clamp(yawErr * 42, -28, 28);
    if (manual) {
      steerDeg = car.manualSteer;
      throttle = car.manualThr;
      brake = car.manualBrk;
    }
    const conf = clamp(1 - Math.abs(lat) / 80 - Math.abs(yawErr) * 0.4, 0.35, 0.98);
    return { steerDeg, throttle: clamp(throttle, 0, 1), brake: clamp(brake, 0, 1), conf, patch: n.i % 9, lat, yawErr };
  }
  function integrate(car, act, dt) {
    const acc = act.throttle * 7.5 - act.brake * 11 - 0.6 * car.v;
    car.v = clamp(car.v + acc * dt, 0, 16);
    const steer = (act.steerDeg * Math.PI) / 180;
    car.yaw += (car.v / 2.6) * Math.tan(steer) * dt;
    car.x += Math.cos(car.yaw) * car.v * dt * 18;
    car.y += Math.sin(car.yaw) * car.v * dt * 18;
    car.t += dt;
    if (car.x > 1080) reset(car);
  }
  function reset(car) {
    car.x = 70; car.y = 250; car.yaw = 0; car.v = 6; car.t = 0;
    car.manualSteer = 0; car.manualThr = 0.3; car.manualBrk = 0;
  }
  function wrap(a) {
    while (a > Math.PI) a -= Math.PI * 2;
    while (a < -Math.PI) a += Math.PI * 2;
    return a;
  }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function signedLat(a, b, p) {
    const dx = b.x - a.x; const dy = b.y - a.y;
    return (dx * (p.y - a.y) - dy * (p.x - a.x)) / (Math.hypot(dx, dy) + 1e-6);
  }
  return { TASKS, step, integrate, reset };
})();
