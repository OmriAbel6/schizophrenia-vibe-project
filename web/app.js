/* ==========================================================================
   Schizophrenia capstone presentation
   – deck navigation (RTL-aware)
   – slide 8: first-person doorway hallucination scene (Three.js) with a
     synthesized spatial-audio anxiety layer (Web Audio API)
   – slide 16: live clinical AI simulation – a liquid-glass chat with the
     FastAPI patient agent (../python/main.py), with an offline fallback
   ========================================================================== */
(() => {
  'use strict';

  const TOTAL = 18;
  const SIM_SLIDE = 8;
  const CHAT_SLIDE = 16;
  const FINALE_SLIDE = 18;
  const COLORS = { pos: '#059669', posFill: '#10B981', neg: '#E11D48', sky: '#0284C7', skyLight: '#0EA5E9', teal: '#0D9488', slate: '#64748B', ink: '#0F172A' };
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ------------------------------------------------------------------ */
  /* Deck navigation                                                     */
  /* ------------------------------------------------------------------ */
  const slides = Array.from(document.querySelectorAll('.slide'));
  const counter = document.getElementById('counter');
  const progressBar = document.getElementById('progressBar');
  const slideTitle = document.getElementById('slideTitle');
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  const fsBtn = document.getElementById('fsBtn');
  let current = -1;
  const hooks = { onEnter: {}, onLeave: {} };

  function readHash() {
    const n = parseInt((location.hash || '').replace(/\D/g, ''), 10);
    return Number.isFinite(n) && n >= 1 && n <= TOTAL ? n - 1 : 0;
  }

  function goTo(index) {
    const next = Math.max(0, Math.min(TOTAL - 1, index));
    if (next === current) return;
    const previous = current;
    slides.forEach((s, i) => {
      s.classList.toggle('is-active', i === next);
      s.classList.toggle('is-prev', i < next);
    });
    current = next;
    counter.textContent = `${next + 1} / ${TOTAL}`;
    progressBar.style.width = `${((next + 1) / TOTAL) * 100}%`;
    slideTitle.textContent = slides[next].dataset.title || '';
    prevBtn.disabled = next === 0;
    nextBtn.disabled = next === TOTAL - 1;
    history.replaceState(null, '', `#${next + 1}`);
    if (previous >= 0 && hooks.onLeave[previous + 1]) hooks.onLeave[previous + 1]();
    if (hooks.onEnter[next + 1]) hooks.onEnter[next + 1](previous + 1);
  }

  const goNext = () => goTo(current + 1);
  const goPrev = () => goTo(current - 1);
  nextBtn.addEventListener('click', goNext);
  prevBtn.addEventListener('click', goPrev);

  document.addEventListener('keydown', (e) => {
    const tag = (e.target.tagName || '').toLowerCase();
    if (tag === 'input' || tag === 'textarea' || tag === 'select') return;      // typing / sliders own the keys
    if (tag === 'button' && e.key !== 'ArrowLeft' && e.key !== 'ArrowRight' && e.key !== 'Home' && e.key !== 'End') return;
    if (!document.getElementById('brainBridge').hidden) return;
    switch (e.key) {
      case 'ArrowLeft': case 'PageDown': case ' ': case 'Enter':
        e.preventDefault(); goNext(); break;              // RTL: left = forward
      case 'ArrowRight': case 'PageUp': case 'Backspace':
        e.preventDefault(); goPrev(); break;              // RTL: right = back
      case 'ArrowDown': e.preventDefault(); goNext(); break;
      case 'ArrowUp': e.preventDefault(); goPrev(); break;
      case 'Home': e.preventDefault(); goTo(0); break;
      case 'End': e.preventDefault(); goTo(TOTAL - 1); break;
      case 'f': case 'F': toggleFullscreen(); break;
      default: break;
    }
  });
  window.addEventListener('hashchange', () => goTo(readHash()));

  let touchX = null;
  document.addEventListener('touchstart', (e) => { touchX = e.touches[0].clientX; }, { passive: true });
  document.addEventListener('touchend', (e) => {
    if (touchX === null) return;
    const dx = e.changedTouches[0].clientX - touchX;
    touchX = null;
    if (Math.abs(dx) < 60) return;
    if (dx > 0) goNext(); else goPrev();
  });

  function toggleFullscreen() {
    const el = document.documentElement;
    if (!document.fullscreenElement) (el.requestFullscreen || el.webkitRequestFullscreen || function () {}).call(el);
    else (document.exitFullscreen || document.webkitExitFullscreen || function () {}).call(document);
  }
  fsBtn.addEventListener('click', toggleFullscreen);

  /* ------------------------------------------------------------------ */
  /* Simplex noise (Gustavson) – organic warping                         */
  /* ------------------------------------------------------------------ */
  const noise3 = (() => {
    const grad3 = [[1, 1, 0], [-1, 1, 0], [1, -1, 0], [-1, -1, 0], [1, 0, 1], [-1, 0, 1],
      [1, 0, -1], [-1, 0, -1], [0, 1, 1], [0, -1, 1], [0, 1, -1], [0, -1, -1]];
    const p = new Uint8Array(256);
    for (let i = 0; i < 256; i++) p[i] = i;
    let seed = 1337;
    const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
    for (let i = 255; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); const t = p[i]; p[i] = p[j]; p[j] = t; }
    const perm = new Uint8Array(512); const perm12 = new Uint8Array(512);
    for (let i = 0; i < 512; i++) { perm[i] = p[i & 255]; perm12[i] = perm[i] % 12; }
    const F3 = 1 / 3; const G3 = 1 / 6;
    const dot = (g, x, y, z) => g[0] * x + g[1] * y + g[2] * z;
    const corner = (gi, x, y, z) => { let t = 0.6 - x * x - y * y - z * z; if (t < 0) return 0; t *= t; return t * t * dot(grad3[gi], x, y, z); };
    return (xin, yin, zin) => {
      const s = (xin + yin + zin) * F3;
      const i = Math.floor(xin + s); const j = Math.floor(yin + s); const k = Math.floor(zin + s);
      const t = (i + j + k) * G3;
      const x0 = xin - (i - t); const y0 = yin - (j - t); const z0 = zin - (k - t);
      let i1, j1, k1, i2, j2, k2;
      if (x0 >= y0) {
        if (y0 >= z0) { i1 = 1; j1 = 0; k1 = 0; i2 = 1; j2 = 1; k2 = 0; }
        else if (x0 >= z0) { i1 = 1; j1 = 0; k1 = 0; i2 = 1; j2 = 0; k2 = 1; }
        else { i1 = 0; j1 = 0; k1 = 1; i2 = 1; j2 = 0; k2 = 1; }
      } else if (y0 < z0) { i1 = 0; j1 = 0; k1 = 1; i2 = 0; j2 = 1; k2 = 1; }
      else if (x0 < z0) { i1 = 0; j1 = 1; k1 = 0; i2 = 0; j2 = 1; k2 = 1; }
      else { i1 = 0; j1 = 1; k1 = 0; i2 = 1; j2 = 1; k2 = 0; }
      const x1 = x0 - i1 + G3; const y1 = y0 - j1 + G3; const z1 = z0 - k1 + G3;
      const x2 = x0 - i2 + 2 * G3; const y2 = y0 - j2 + 2 * G3; const z2 = z0 - k2 + 2 * G3;
      const x3 = x0 - 1 + 3 * G3; const y3 = y0 - 1 + 3 * G3; const z3 = z0 - 1 + 3 * G3;
      const ii = i & 255; const jj = j & 255; const kk = k & 255;
      return 32 * (
        corner(perm12[ii + perm[jj + perm[kk]]], x0, y0, z0)
        + corner(perm12[ii + i1 + perm[jj + j1 + perm[kk + k1]]], x1, y1, z1)
        + corner(perm12[ii + i2 + perm[jj + j2 + perm[kk + k2]]], x2, y2, z2)
        + corner(perm12[ii + 1 + perm[jj + 1 + perm[kk + 1]]], x3, y3, z3));
    };
  })();

  /* ------------------------------------------------------------------ */
  /* First-person doorway scene (Three.js)                               */
  /* ------------------------------------------------------------------ */
  const WAYPOINTS = [7.0, 5.6, 4.2, 2.8, 1.4, -0.2, -2.0, -4.2];

  function createPOVScene(host, vignette, callbacks) {
    const THREE = window.THREE;
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.shadowMap.enabled = false;
    host.appendChild(renderer.domElement);
    const canvas = renderer.domElement;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x07080c);
    scene.fog = new THREE.FogExp2(0x07080c, 0.055);

    const camera = new THREE.PerspectiveCamera(70, 1, 0.05, 80);
    camera.rotation.order = 'YXZ';
    camera.position.set(0, 1.6, WAYPOINTS[0]);

    const ambient = new THREE.AmbientLight(0x6a6256, 0.75);
    scene.add(ambient);
    const ceilingLight = new THREE.PointLight(0xfff0d6, 1.25, 14, 1.6);
    ceilingLight.position.set(0, 2.85, 4);
    scene.add(ceilingLight);
    const fixture = new THREE.Mesh(new THREE.SphereGeometry(0.12, 12, 12), new THREE.MeshBasicMaterial({ color: 0xfff6e0 }));
    fixture.position.copy(ceilingLight.position);
    scene.add(fixture);

    // --- The home interior: 5 m wide, 3 m high, 8 m deep (z 0..8) ----------
    const plaster = new THREE.MeshStandardMaterial({ color: 0xd9cfbf, roughness: 0.95, side: THREE.DoubleSide });
    const plasterDark = new THREE.MeshStandardMaterial({ color: 0xc7bca8, roughness: 0.95, side: THREE.DoubleSide });
    const wood = new THREE.MeshStandardMaterial({ color: 0x6e5540, roughness: 0.8 });
    const breathing = [];
    function wall(w, h, segs, mat) {
      const geo = new THREE.PlaneGeometry(w, h, segs, Math.round(segs * h / w) || 4);
      const mesh = new THREE.Mesh(geo, mat);
      breathing.push({ mesh, base: Float32Array.from(geo.attributes.position.array) });
      return mesh;
    }
    const leftWall = wall(8, 3, 28, plaster); leftWall.rotation.y = Math.PI / 2; leftWall.position.set(-2.5, 1.5, 4); scene.add(leftWall);
    const rightWall = wall(8, 3, 28, plaster); rightWall.rotation.y = -Math.PI / 2; rightWall.position.set(2.5, 1.5, 4); scene.add(rightWall);
    const ceiling = wall(5, 8, 18, plasterDark); ceiling.rotation.x = Math.PI / 2; ceiling.position.set(0, 3, 4); scene.add(ceiling);
    const backWall = new THREE.Mesh(new THREE.PlaneGeometry(5, 3), plaster); backWall.rotation.y = Math.PI; backWall.position.set(0, 1.5, 8); scene.add(backWall);
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(5, 8), wood); floor.rotation.x = -Math.PI / 2; floor.position.set(0, 0, 4); scene.add(floor);
    // Skirting and a few furniture hints so the room reads as a home.
    const rug = new THREE.Mesh(new THREE.PlaneGeometry(2.2, 3.2), new THREE.MeshStandardMaterial({ color: 0x8a5a4a, roughness: 1 }));
    rug.rotation.x = -Math.PI / 2; rug.position.set(0, 0.005, 4.5); scene.add(rug);
    const sideboard = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.9, 0.45), wood); sideboard.position.set(-1.75, 0.45, 2.2); scene.add(sideboard);
    const picture = new THREE.Mesh(new THREE.PlaneGeometry(0.9, 0.6), new THREE.MeshStandardMaterial({ color: 0x3b5a7a })); picture.rotation.y = Math.PI / 2; picture.position.set(-2.48, 1.7, 5.5); scene.add(picture);
    const coat = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 1.8, 8), new THREE.MeshStandardMaterial({ color: 0x2a2a2a })); coat.position.set(2.2, 0.9, 1.0); scene.add(coat);

    // Front wall with the doorway (opening x -0.75..0.75, y 0..2.2).
    const frontL = new THREE.Mesh(new THREE.PlaneGeometry(1.75, 3), plaster); frontL.position.set(-1.625, 1.5, 0); scene.add(frontL);
    const frontR = new THREE.Mesh(new THREE.PlaneGeometry(1.75, 3), plaster); frontR.position.set(1.625, 1.5, 0); scene.add(frontR);
    const lintel = new THREE.Mesh(new THREE.PlaneGeometry(1.5, 0.8), plaster); lintel.position.set(0, 2.6, 0); scene.add(lintel);
    const frameMat = new THREE.MeshStandardMaterial({ color: 0x3a2a1e, roughness: 0.7 });
    [[-0.79, 1.1, 0.08, 2.2], [0.79, 1.1, 0.08, 2.2]].forEach(([x, y, w, h]) => {
      const post = new THREE.Mesh(new THREE.BoxGeometry(w, h, 0.14), frameMat); post.position.set(x, y, 0); scene.add(post);
    });
    const top = new THREE.Mesh(new THREE.BoxGeometry(1.66, 0.08, 0.14), frameMat); top.position.set(0, 2.24, 0); scene.add(top);
    const doorGroup = new THREE.Group(); doorGroup.position.set(-0.75, 0, 0); scene.add(doorGroup);
    const door = new THREE.Mesh(new THREE.BoxGeometry(1.5, 2.2, 0.06), new THREE.MeshStandardMaterial({ color: 0x4a3324, roughness: 0.6 }));
    door.position.set(0.75, 1.1, 0); doorGroup.add(door);
    const knob = new THREE.Mesh(new THREE.SphereGeometry(0.04, 10, 10), new THREE.MeshStandardMaterial({ color: 0xd4af37, metalness: 0.8, roughness: 0.3 }));
    knob.position.set(1.35, 1.05, 0.06); doorGroup.add(knob);

    // --- Outside: pavement, street, buildings, lamps -------------------------
    const asphalt = new THREE.Mesh(new THREE.PlaneGeometry(60, 40), new THREE.MeshStandardMaterial({ color: 0x24262b, roughness: 1 }));
    asphalt.rotation.x = -Math.PI / 2; asphalt.position.set(0, -0.02, -14); scene.add(asphalt);
    const pavement = new THREE.Mesh(new THREE.BoxGeometry(12, 0.1, 3), new THREE.MeshStandardMaterial({ color: 0x4b4d52, roughness: 1 }));
    pavement.position.set(0, -0.05, -1.5); scene.add(pavement);
    const facade = new THREE.Mesh(new THREE.PlaneGeometry(14, 6), new THREE.MeshStandardMaterial({ color: 0x8b8378, roughness: 1, side: THREE.DoubleSide }));
    facade.rotation.y = Math.PI; facade.position.set(0, 3, -0.02); scene.add(facade); // outer face of the home
    const bldgMat = new THREE.MeshStandardMaterial({ color: 0x2a2d36, roughness: 0.9 });
    const winMat = new THREE.MeshBasicMaterial({ color: 0xffe3a3 });
    [[-9, -7, 7, 6], [9, -8, 9, 7], [-10, -16, 11, 7], [10, -17, 8, 7], [0, -24, 10, 16]].forEach(([x, z, h, w]) => {
      const b = new THREE.Mesh(new THREE.BoxGeometry(w, h, 6), bldgMat); b.position.set(x, h / 2, z); scene.add(b);
      for (let r = 0; r < Math.floor(h / 2); r++) {
        for (let c = 0; c < 3; c++) {
          if ((r + c) % 2) continue;
          const win = new THREE.Mesh(new THREE.PlaneGeometry(0.6, 0.8), winMat);
          win.position.set(x + (c - 1) * 1.6, 1.4 + r * 2, z + 3.01); scene.add(win);
        }
      }
    });
    const lamps = [];
    [[-3.2, -3.5], [3.4, -8], [-3.2, -13]].forEach(([x, z]) => {
      const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.07, 3.6, 8), new THREE.MeshStandardMaterial({ color: 0x1a1a1a }));
      pole.position.set(x, 1.8, z); scene.add(pole);
      const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.14, 10, 10), new THREE.MeshBasicMaterial({ color: 0xffd9a0 }));
      bulb.position.set(x, 3.6, z); scene.add(bulb);
      const light = new THREE.PointLight(0xffc98a, 1.1, 16, 1.5); light.position.set(x, 3.5, z); scene.add(light);
      lamps.push({ light, base: 1.1, seed: Math.random() * 10 });
    });

    // --- Hallucinatory elements ------------------------------------------------
    const silhouetteMat = () => new THREE.MeshBasicMaterial({ color: 0x050507, transparent: true, opacity: 0, depthWrite: false });
    const silhouettes = [
      [-2.15, 0.95, 2.6], [2.1, 0.95, 5.4], [-3.6, 0.95, -3.0], [3.9, 0.95, -6.2], [0.9, 0.95, -9.5], [-1.6, 0.95, -12],
    ].map(([x, y, z], i) => {
      const mesh = new THREE.Mesh(new THREE.PlaneGeometry(0.7, 1.9), silhouetteMat());
      mesh.position.set(x, y, z); scene.add(mesh);
      return { mesh, visible: false, timer: 1 + i * 0.7, target: 0 };
    });
    const shadowBlob = new THREE.Mesh(new THREE.CircleGeometry(0.45, 24), new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0, depthWrite: false }));
    shadowBlob.rotation.x = -Math.PI / 2; shadowBlob.position.y = 0.012; scene.add(shadowBlob);
    const fragments = Array.from({ length: 14 }, () => {
      const mesh = new THREE.Mesh(new THREE.PlaneGeometry(0.05 + Math.random() * 0.25, 0.02 + Math.random() * 0.08),
        new THREE.MeshBasicMaterial({ color: Math.random() < 0.5 ? 0x0a0a0c : 0xffffff, transparent: true, opacity: 0, depthWrite: false }));
      scene.add(mesh);
      return { mesh, timer: Math.random() * 2, life: 0 };
    });

    const state = {
      intensity: 0.5, running: false, t: 0, stepIndex: 0, z: WAYPOINTS[0], targetZ: WAYPOINTS[0],
      look: { x: 0, y: 0 }, lookSmooth: { x: 0, y: 0 }, flicker: 0, moving: 0, phase: 'home', lastFilter: 0,
    };
    let last = performance.now();
    const fwd = new THREE.Vector3(); const toObj = new THREE.Vector3();

    function resize() {
      const w = host.clientWidth || 1; const h = host.clientHeight || 1;
      renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
    }
    new ResizeObserver(resize).observe(host); resize();

    host.addEventListener('mousemove', (e) => {
      const r = host.getBoundingClientRect();
      state.look.x = ((e.clientX - r.left) / r.width - 0.5) * 2;
      state.look.y = (0.5 - (e.clientY - r.top) / r.height) * 2;
    });
    host.addEventListener('mouseleave', () => { state.look.x = 0; state.look.y = 0; });

    function phaseFor(z) { return z > 2.4 ? 'home' : z > -0.6 ? 'door' : 'street'; }

    function update(dt) {
      const t = state.t; const a = state.intensity;
      // Movement along the path with head-bob.
      const dz = state.targetZ - state.z;
      state.z += dz * Math.min(1, dt * 2.4);
      state.moving += ((Math.abs(dz) > 0.05 ? 1 : 0) - state.moving) * Math.min(1, dt * 6);
      const doorProximity = Math.max(0, 1 - Math.abs(state.z) / 3.2);
      const dist = a * (0.3 + 0.7 * doorProximity);          // distortion strength peaks at the doorway
      const phase = phaseFor(state.z);
      if (phase !== state.phase) { state.phase = phase; callbacks.onPhase(phase); }

      // Breathing walls.
      breathing.forEach(({ mesh, base }) => {
        const pos = mesh.geometry.attributes.position;
        const amp = 0.22 * dist;
        for (let i = 0; i < pos.count; i++) {
          const ix = i * 3;
          const n = noise3(base[ix] * 0.55 + t * 0.45, base[ix + 1] * 0.55 + t * 0.2, mesh.id * 0.37 + t * 0.3);
          pos.setZ(i, base[ix + 2] + n * amp);
        }
        pos.needsUpdate = true;
        if (dist > 0.02) mesh.geometry.computeVertexNormals();
      });

      // Flickering overhead light.
      if (Math.random() < dist * 0.09) state.flicker = 0.12 + Math.random() * 0.25;
      state.flicker = Math.max(0, state.flicker - dt);
      const flickerDim = state.flicker > 0 ? 0.12 + Math.random() * 0.3 : 1;
      ceilingLight.intensity = 1.25 * flickerDim * (1 - 0.25 * dist * (0.5 + 0.5 * Math.sin(t * 9.3)));
      fixture.material.color.setScalar(flickerDim);
      lamps.forEach((l) => { l.light.intensity = l.base * (1 - dist * 0.35 * Math.max(0, noise3(t * 2.2 + l.seed, 0, 0))); });

      // Door swings open as we approach, then stays open.
      const openness = Math.max(0, Math.min(1, (5.2 - state.z) / 2.4));
      doorGroup.rotation.y = openness * 1.75;

      // Detached, stretching shadow on the floor ahead of us.
      shadowBlob.position.set(camera.position.x + Math.sin(t * 0.7) * 1.4 * dist, 0.012, state.z - 1.3 - dist * 1.2);
      shadowBlob.scale.set(1 + dist * 2.8 * (0.5 + 0.5 * Math.sin(t * 0.9)), 1 + dist * 0.6, 1);
      shadowBlob.material.opacity = 0.55 * dist;

      // Peripheral silhouettes: appear at the edges, vanish when looked at.
      camera.getWorldDirection(fwd);
      silhouettes.forEach((s) => {
        s.timer -= dt;
        if (s.timer <= 0) { s.visible = !s.visible; s.timer = s.visible ? 2 + Math.random() * 4 : 1 + Math.random() * 3; }
        toObj.subVectors(s.mesh.position, camera.position); const d = toObj.length(); toObj.normalize();
        const angle = Math.acos(Math.max(-1, Math.min(1, fwd.dot(toObj))));
        const lookedAt = angle < 0.32;
        s.target = s.visible && !lookedAt && d < 14 ? 0.8 * dist : 0;
        const rate = lookedAt ? 9 : 2.5;
        s.mesh.material.opacity += (s.target - s.mesh.material.opacity) * Math.min(1, dt * rate);
        s.mesh.rotation.y = Math.atan2(camera.position.x - s.mesh.position.x, camera.position.z - s.mesh.position.z);
        s.mesh.scale.y = 1 + 0.25 * dist * Math.sin(t * 3 + s.mesh.id);
      });

      // Intrusive visual fragments darting through the periphery.
      fragments.forEach((f) => {
        f.timer -= dt;
        if (f.timer <= 0) {
          const side = Math.random() < 0.5 ? -1 : 1;
          f.mesh.position.set(camera.position.x + side * (0.9 + Math.random() * 0.8), 1.1 + Math.random() * 1.2, state.z - 1.2 - Math.random() * 2);
          f.mesh.rotation.set(0, Math.random() * Math.PI, Math.random() * Math.PI);
          f.life = 0.15 + Math.random() * 0.4; f.timer = f.life + 0.6 + Math.random() * 3 * (1.2 - a);
        }
        f.life = Math.max(0, f.life - dt);
        f.mesh.material.opacity = f.life > 0 ? 0.9 * dist : 0;
      });

      // Camera: mouse look + perceptual drift, roll and field-of-view pulsing.
      state.lookSmooth.x += (state.look.x - state.lookSmooth.x) * Math.min(1, dt * 4);
      state.lookSmooth.y += (state.look.y - state.lookSmooth.y) * Math.min(1, dt * 4);
      const driftX = noise3(t * 0.35, 1.3, 0) * 0.22 * dist;
      const driftY = noise3(0, t * 0.3, 2.1) * 0.12 * dist;
      const bob = Math.sin(t * 7.5) * 0.035 * state.moving;
      camera.position.set(Math.sin(t * 0.5) * 0.08 * dist, 1.6 + bob + Math.sin(t * 1.3) * 0.02 * dist, state.z);
      camera.rotation.set(state.lookSmooth.y * 0.28 + driftY, -state.lookSmooth.x * 0.6 + driftX, Math.sin(t * 0.6) * 0.07 * dist);
      camera.fov = 70 + Math.sin(t * 0.8) * 9 * dist + 7 * dist * doorProximity + Math.sin(t * 4.1) * 2 * dist;
      camera.updateProjectionMatrix();

      // Outdoor mood: colder ambient and thicker fog once outside.
      const outside = Math.max(0, Math.min(1, (1.5 - state.z) / 3));
      ambient.color.setRGB(0.41 - 0.2 * outside, 0.38 - 0.16 * outside, 0.34 - 0.08 * outside);
      scene.fog.density = 0.055 + 0.03 * outside + 0.04 * dist;

      // Vignette pulse and chromatic fringing (CSS, throttled).
      vignette.style.opacity = (0.15 + dist * 0.7 * (0.65 + 0.35 * Math.sin(t * 2.3))).toFixed(3);
      if (t - state.lastFilter > 0.08) {
        state.lastFilter = t;
        const px = (dist * 5 * (0.7 + 0.3 * Math.sin(t * 3.7))).toFixed(1);
        canvas.style.filter = dist > 0.03
          ? `drop-shadow(${px}px 0 0 rgba(255,0,70,0.35)) drop-shadow(-${px}px 0 0 rgba(0,170,255,0.35)) saturate(${(1 - 0.35 * dist).toFixed(2)})`
          : 'none';
      }
    }

    function frame(now) {
      if (!state.running) return;
      const dt = Math.min((now - last) / 1000, 0.05); last = now;
      state.t += dt;
      update(dt);
      renderer.render(scene, camera);
      requestAnimationFrame(frame);
    }

    return {
      start() { if (state.running) return; state.running = true; last = performance.now(); resize(); requestAnimationFrame(frame); },
      stop() { state.running = false; },
      isRunning() { return state.running; },
      setIntensity(v) { state.intensity = v; },
      step() {
        if (state.stepIndex >= WAYPOINTS.length - 1) return false;
        state.stepIndex += 1; state.targetZ = WAYPOINTS[state.stepIndex];
        callbacks.onStep(state.stepIndex, WAYPOINTS.length - 1, state.targetZ < 0.8 && WAYPOINTS[state.stepIndex - 1] >= 0.8);
        return true;
      },
      reset() {
        state.stepIndex = 0; state.z = WAYPOINTS[0]; state.targetZ = WAYPOINTS[0]; state.t = 0; state.flicker = 0;
        silhouettes.forEach((s) => { s.mesh.material.opacity = 0; s.visible = false; });
        canvas.style.filter = 'none'; vignette.style.opacity = '0';
        callbacks.onStep(0, WAYPOINTS.length - 1, false);
        if (!state.running) renderer.render(scene, camera);
      },
      stepsTotal: WAYPOINTS.length - 1,
    };
  }

  /* Fallback: 2D canvas corridor when Three.js is unavailable. */
  function create2DScene(host, vignette, callbacks) {
    const canvas = document.createElement('canvas'); host.appendChild(canvas);
    const ctx = canvas.getContext('2d');
    const state = { intensity: 0.5, running: false, t: 0, stepIndex: 0, progress: 0 };
    function resize() { canvas.width = host.clientWidth; canvas.height = host.clientHeight; }
    new ResizeObserver(resize).observe(host); resize();
    function frame() {
      if (!state.running) return;
      state.t += 0.016; const { width: w, height: h } = canvas; const a = state.intensity; const t = state.t;
      state.progress += (state.stepIndex / 7 - state.progress) * 0.04;
      ctx.fillStyle = '#0b0b0d'; ctx.fillRect(0, 0, w, h);
      const cx = w / 2; const cy = h / 2; const depth = 6;
      for (let i = depth; i >= 1; i--) {
        const k = (i - state.progress * 3 + 6) % 6 + 0.3; const s = 1 / k;
        const wobble = Math.sin(t * 1.5 + i) * 12 * a;
        ctx.strokeStyle = `rgba(217,207,191,${0.15 + s * 0.5})`; ctx.lineWidth = 2;
        ctx.strokeRect(cx - w * 0.45 * s + wobble, cy - h * 0.45 * s, w * 0.9 * s, h * 0.9 * s);
      }
      ctx.fillStyle = `rgba(0,0,0,${0.3 * a * (0.5 + 0.5 * Math.sin(t * 2))})`; ctx.fillRect(0, 0, w, h);
      vignette.style.opacity = (0.2 + a * 0.6 * (0.6 + 0.4 * Math.sin(t * 2.3))).toFixed(2);
      requestAnimationFrame(frame);
    }
    return {
      start() { if (state.running) return; state.running = true; requestAnimationFrame(frame); },
      stop() { state.running = false; }, isRunning() { return state.running; },
      setIntensity(v) { state.intensity = v; },
      step() { if (state.stepIndex >= 7) return false; state.stepIndex += 1; callbacks.onStep(state.stepIndex, 7, state.stepIndex === 5); callbacks.onPhase(state.stepIndex < 4 ? 'home' : state.stepIndex < 6 ? 'door' : 'street'); return true; },
      reset() { state.stepIndex = 0; state.progress = 0; callbacks.onStep(0, 7, false); callbacks.onPhase('home'); },
      stepsTotal: 7,
    };
  }

  /* ------------------------------------------------------------------ */
  /* Spatial anxiety soundscape (Web Audio API)                          */
  /* ------------------------------------------------------------------ */
  function createPOVAudio() {
    let ctx = null; let master = null; let intensity = 0.5;
    const timers = []; const nodes = []; let whiteBuf = null; let brownBuf = null; let ring = null; let whisperSide = 1;

    const AC = window.AudioContext || window.webkitAudioContext;
    function noiseBuffer(seconds, brown) {
      const len = Math.floor(ctx.sampleRate * seconds); const buf = ctx.createBuffer(1, len, ctx.sampleRate);
      const d = buf.getChannelData(0); let lastV = 0;
      for (let i = 0; i < len; i++) {
        const w = Math.random() * 2 - 1;
        if (brown) { lastV = (lastV + 0.02 * w) / 1.02; d[i] = lastV * 3.5; } else d[i] = w;
      }
      return buf;
    }
    function panner(value) {
      if (!ctx.createStereoPanner) return null;
      const p = ctx.createStereoPanner(); p.pan.value = value; return p;
    }
    function chain(src, ...rest) { let node = src; rest.forEach((n) => { if (n) { node.connect(n); node = n; } }); node.connect(master); }

    function thump(time, gainPeak, freqFrom, freqTo) {
      const o = ctx.createOscillator(); o.type = 'sine';
      o.frequency.setValueAtTime(freqFrom, time); o.frequency.exponentialRampToValueAtTime(freqTo, time + 0.14);
      const g = ctx.createGain(); g.gain.setValueAtTime(0.0001, time);
      g.gain.exponentialRampToValueAtTime(gainPeak, time + 0.012); g.gain.exponentialRampToValueAtTime(0.0001, time + 0.16);
      const lp = ctx.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 140;
      chain(o, lp, g); o.start(time); o.stop(time + 0.2);
    }
    function heartbeat() {
      const now = ctx.currentTime; const strength = 0.35 + intensity * 0.5;
      thump(now, strength, 62, 38); thump(now + 0.19, strength * 0.7, 56, 34);
      const bpm = 62 + intensity * 86;
      timers.push(setTimeout(heartbeat, (60 / bpm) * 1000));
    }
    function whisper() {
      const now = ctx.currentTime; whisperSide *= -1;
      const src = ctx.createBufferSource(); src.buffer = whiteBuf;
      const bp = ctx.createBiquadFilter(); bp.type = 'bandpass'; bp.Q.value = 7 + Math.random() * 9;
      bp.frequency.setValueAtTime(900 + Math.random() * 1500, now); bp.frequency.linearRampToValueAtTime(500 + Math.random() * 2600, now + 0.5);
      const g = ctx.createGain(); const dur = 0.3 + Math.random() * 0.7;
      g.gain.setValueAtTime(0.0001, now); g.gain.exponentialRampToValueAtTime(0.25 + intensity * 0.45, now + 0.07); g.gain.exponentialRampToValueAtTime(0.0001, now + dur);
      chain(src, bp, g, panner(whisperSide * (0.85 + Math.random() * 0.15)));
      src.start(now); src.stop(now + dur + 0.1);
      if (Math.random() < intensity * 0.5) timers.push(setTimeout(whisper, 140));
      timers.push(setTimeout(whisper, 900 + Math.random() * 3200 * (1.35 - intensity)));
    }
    function footstep(delay, side) {
      const time = ctx.currentTime + delay;
      const src = ctx.createBufferSource(); src.buffer = brownBuf;
      const lp = ctx.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 260;
      const g = ctx.createGain(); g.gain.setValueAtTime(0.0001, time); g.gain.exponentialRampToValueAtTime(0.45, time + 0.02); g.gain.exponentialRampToValueAtTime(0.0001, time + 0.22);
      chain(src, lp, g, panner(side * 0.35)); src.start(time); src.stop(time + 0.3);
    }
    function creak() {
      const now = ctx.currentTime;
      const o = ctx.createOscillator(); o.type = 'sawtooth';
      o.frequency.setValueAtTime(160, now); o.frequency.linearRampToValueAtTime(420, now + 1.1); o.frequency.linearRampToValueAtTime(300, now + 1.6);
      const bp = ctx.createBiquadFilter(); bp.type = 'bandpass'; bp.Q.value = 9; bp.frequency.value = 700;
      const trem = ctx.createOscillator(); trem.frequency.value = 23; const tremGain = ctx.createGain(); tremGain.gain.value = 0.5;
      const g = ctx.createGain(); g.gain.setValueAtTime(0.0001, now); g.gain.exponentialRampToValueAtTime(0.14, now + 0.1); g.gain.exponentialRampToValueAtTime(0.0001, now + 1.7);
      trem.connect(tremGain).connect(g.gain); trem.start(now); trem.stop(now + 1.8);
      chain(o, bp, g, panner(-0.4)); o.start(now); o.stop(now + 1.8);
    }

    function start() {
      if (!AC) return false;
      if (!ctx) ctx = new AC();
      if (ctx.state === 'suspended') ctx.resume();
      whiteBuf = whiteBuf || noiseBuffer(1.5, false); brownBuf = brownBuf || noiseBuffer(1.0, true);
      master = ctx.createGain(); master.gain.setValueAtTime(0.0001, ctx.currentTime);
      master.gain.exponentialRampToValueAtTime(0.7, ctx.currentTime + 1.2); master.connect(ctx.destination);
      // Tense high-frequency ring with slow tremolo.
      ring = ctx.createOscillator(); ring.type = 'sine'; ring.frequency.value = 7600;
      const ringGain = ctx.createGain(); ringGain.gain.value = 0.004 + intensity * 0.02;
      const lfo = ctx.createOscillator(); lfo.frequency.value = 0.23; const lfoGain = ctx.createGain(); lfoGain.gain.value = 0.006;
      lfo.connect(lfoGain).connect(ringGain.gain); lfo.start();
      ring.connect(ringGain).connect(master); ring.start(); nodes.push(ring, lfo); ring.userGain = ringGain;
      // Distant muffled street bed.
      const bed = ctx.createBufferSource(); bed.buffer = brownBuf; bed.loop = true;
      const lp = ctx.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 180;
      const bedGain = ctx.createGain(); bedGain.gain.value = 0.18; bed.connect(lp).connect(bedGain).connect(master); bed.start(); nodes.push(bed);
      heartbeat(); whisper();
      return true;
    }
    function stop() {
      timers.splice(0).forEach(clearTimeout);
      if (!ctx || !master) return;
      const m = master; const stopping = nodes.splice(0);
      m.gain.cancelScheduledValues(ctx.currentTime); m.gain.setValueAtTime(m.gain.value, ctx.currentTime);
      m.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.7);
      setTimeout(() => { stopping.forEach((n) => { try { n.stop(); } catch (e) { /* already stopped */ } }); m.disconnect(); }, 800);
      master = null; ring = null;
    }
    return {
      start, stop,
      get active() { return master !== null; },
      setIntensity(v) { intensity = v; if (ring) ring.userGain.gain.value = 0.004 + v * 0.02; },
      onStep(throughDoor) { if (!master) return; footstep(0, -1); footstep(0.42, 1); footstep(0.84, -1); if (throughDoor) creak(); },
    };
  }

  function initPOV() {
    const host = document.getElementById('povStage');
    const vignette = document.getElementById('povVignette');
    const overlay = document.getElementById('povOverlay');
    const phaseEl = document.getElementById('povPhase');
    const stepsEl = document.getElementById('povSteps');
    const startBtn = document.getElementById('povStart');
    const stepBtn = document.getElementById('povStep');
    const intensity = document.getElementById('povIntensity');
    const intensityOut = document.getElementById('povIntensityOut');
    const audioToggle = document.getElementById('povAudio');
    const resetBtn = document.getElementById('povReset');
    const audio = createPOVAudio();
    const PHASES = { home: 'בתוך הבית', door: 'על סף הדלת', street: 'ברחוב' };
    let scene = null;

    if (reducedMotion) { intensity.value = 20; intensityOut.value = 20; }

    const callbacks = {
      onPhase(p) { phaseEl.textContent = PHASES[p] || ''; },
      onStep(index, total, throughDoor) {
        Array.from(stepsEl.children).forEach((bar, i) => bar.classList.toggle('is-done', i < index));
        stepBtn.textContent = index >= total ? 'הגעתם לרחוב' : index === 0 ? 'צעד אל מחוץ לדלת' : 'צעד נוסף';
        stepBtn.disabled = index >= total;
        audio.onStep(throughDoor);
      },
    };
    function ensureScene() {
      if (scene) return scene;
      scene = window.THREE ? createPOVScene(host, vignette, callbacks) : create2DScene(host, vignette, callbacks);
      scene.setIntensity(intensity.value / 100);
      return scene;
    }
    startBtn.addEventListener('click', () => { overlay.hidden = true; ensureScene().start(); });
    stepBtn.addEventListener('click', () => { overlay.hidden = true; ensureScene().start(); scene.step(); });
    intensity.addEventListener('input', () => {
      intensityOut.value = intensity.value; const v = intensity.value / 100;
      if (scene) scene.setIntensity(v); audio.setIntensity(v);
    });
    audioToggle.addEventListener('change', () => {
      if (audioToggle.checked) { audio.setIntensity(intensity.value / 100); if (!audio.start()) audioToggle.checked = false; }
      else audio.stop();
    });
    resetBtn.addEventListener('click', () => {
      intensity.value = reducedMotion ? 10 : 15; intensityOut.value = intensity.value;
      audio.stop(); audioToggle.checked = false;
      if (scene) { scene.setIntensity(intensity.value / 100); scene.reset(); }
      phaseEl.textContent = PHASES.home;
    });
    document.addEventListener('visibilitychange', () => {
      if (!scene) return;
      if (document.hidden) scene.stop(); else if (current === SIM_SLIDE - 1 && overlay.hidden) scene.start();
    });
    hooks.onEnter[SIM_SLIDE] = () => { if (scene && overlay.hidden) scene.start(); };
    hooks.onLeave[SIM_SLIDE] = () => { if (scene) scene.stop(); if (audio.active) { audio.stop(); audioToggle.checked = false; } };
  }

  /* ------------------------------------------------------------------ */
  /* Neuro-Sim visuals (slides 16–18)                                    */
  /* ------------------------------------------------------------------ */
  const SVG_NS = 'http://www.w3.org/2000/svg';
  const tooltip = document.getElementById('tooltip');
  function svgEl(name, attrs = {}, text) {
    const el = document.createElementNS(SVG_NS, name);
    Object.entries(attrs).forEach(([k, v]) => el.setAttribute(k, v));
    if (text !== undefined) el.textContent = text;
    return el;
  }
  function el(tag, cls, html) { const e = document.createElement(tag); if (cls) e.className = cls; if (html !== undefined) e.innerHTML = html; return e; }
  function showTooltip(html, x, y) {
    tooltip.innerHTML = html; tooltip.hidden = false;
    const r = tooltip.getBoundingClientRect();
    tooltip.style.left = `${Math.min(window.innerWidth - r.width - 8, Math.max(8, x - r.width / 2))}px`;
    tooltip.style.top = `${y - r.height - 14 < 8 ? y + 18 : y - r.height - 14}px`;
  }
  const hideTooltip = () => { tooltip.hidden = true; };
  const fmt = (v) => Math.round(v);
  const stateByKey = (m, key) => m.states.find((s) => s.key === key);

  /* ------------------------------------------------------------------ */
  /* Slide 5 – horizontal interactive flowchart                          */
  /* ------------------------------------------------------------------ */
  function initFlowchart() {
    const nodes = Array.from(document.querySelectorAll('#dopamineFlow .flow-node'));
    nodes.forEach((node, i) => {
      if (i > 0) { const line = document.createElement('span'); line.className = 'flow-line'; node.appendChild(line); }
      const activate = () => {
        nodes.forEach((n) => n.classList.toggle('is-active', n === node));
        nodes.forEach((n, k) => n.classList.toggle('is-lit', k <= i));
      };
      node.addEventListener('click', activate);
      node.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); activate(); } });
    });
    const list = document.getElementById('dopamineFlow');
    if (list) list.addEventListener('mouseleave', () => nodes.forEach((n) => { if (!n.classList.contains('is-active')) n.classList.remove('is-lit'); }));
  }


  /* ------------------------------------------------------------------ */
  /* Medical micro-animations: floating nodes, stagger indices, ECG,     */
  /* and the brain bridge between slides 19 and 20                       */
  /* ------------------------------------------------------------------ */
  const ECG_PATH = 'M0 40 H120 L140 40 L152 18 L166 64 L180 30 L190 40 H300 L320 40 L332 14 L346 66 L360 32 L370 40 H480 L500 40 L512 18 L526 62 L540 30 L550 40 H600';

  function initDecorations() {
    // Stagger indices for entry animations.
    const groups = '.cols, .grid-cards, .criteria, .timeline, .takeaways, .flowchart, .stat-row, .symptom-list, .chips, .meta-bar, .presenters, .pov, .finale, .chat__suggest';
    document.querySelectorAll(groups).forEach((group) => {
      Array.from(group.children).forEach((child, i) => child.style.setProperty('--i', i));
    });
    // Floating biological nodes on the title, neurobiology and Neuro-Sim slides.
    const seeded = (() => { let s = 7; return () => (s = (s * 16807) % 2147483647) / 2147483647; })();
    [1, 5, 6, 7, 16, 17].forEach((n) => {
      const slide = slides[n - 1]; if (!slide) return;
      const bg = document.createElement('div'); bg.className = 'bio-bg'; bg.setAttribute('aria-hidden', 'true');
      for (let i = 0; i < 9; i++) {
        const node = document.createElement('span'); node.className = 'bio-node';
        const size = 10 + seeded() * 34;
        node.style.cssText = `left:${(seeded() * 96).toFixed(1)}%;top:${(seeded() * 90).toFixed(1)}%;width:${size.toFixed(0)}px;height:${size.toFixed(0)}px;--dur:${(14 + seeded() * 14).toFixed(1)}s;--delay:${(-seeded() * 20).toFixed(1)}s;--node-color:${i % 3 === 0 ? 'rgba(13,148,136,0.5)' : 'rgba(14,165,233,0.55)'};--node-glow:${i % 3 === 0 ? 'rgba(13,148,136,0.3)' : 'rgba(14,165,233,0.35)'}`;
        bg.appendChild(node);
      }
      for (let i = 0; i < 4; i++) {
        const link = document.createElement('span'); link.className = 'bio-link';
        link.style.cssText = `left:${(seeded() * 90).toFixed(1)}%;top:${(seeded() * 90).toFixed(1)}%;width:${(80 + seeded() * 160).toFixed(0)}px;rotate:${(seeded() * 360).toFixed(0)}deg`;
        bg.appendChild(link);
      }
      slide.insertBefore(bg, slide.firstChild);
    });
    // Heartbeat waveform inside the suicide-risk card (slide 10).
    const alertCard = document.querySelector('.card--alert h3');
    if (alertCard) {
      const ecg = svgEl('svg', { class: 'ecg ecg--inline', viewBox: '0 0 600 80', preserveAspectRatio: 'none', 'aria-hidden': 'true' });
      ecg.appendChild(svgEl('path', { d: ECG_PATH, pathLength: 1 }));
      alertCard.insertAdjacentElement('afterend', ecg);
    }
  }

  function initBrainBridge() {
    const bridge = document.getElementById('brainBridge');
    if (!bridge) return;
    const DURATION = 4200;
    let timer = null;
    const hide = () => {
      if (bridge.hidden) return;
      clearTimeout(timer); bridge.hidden = true; bridge.classList.remove('is-on');
    };
    const show = () => {
      bridge.hidden = false; bridge.style.setProperty('--bridge-ms', `${DURATION}ms`);
      requestAnimationFrame(() => bridge.classList.add('is-on'));
      timer = setTimeout(hide, DURATION);
    };
    bridge.addEventListener('click', hide);
    document.addEventListener('keydown', (e) => { if (!bridge.hidden && e.key !== 'Shift') { hide(); } }, true);
    const prevEnter = hooks.onEnter[FINALE_SLIDE];
    hooks.onEnter[FINALE_SLIDE] = (from) => {
      if (prevEnter) prevEnter(from);
      if (from === FINALE_SLIDE - 1 && !reducedMotion) show();
    };
  }


  /* ------------------------------------------------------------------ */
  /* Slide 16 – live clinical AI simulation (chat with the patient agent)*/
  /* ------------------------------------------------------------------ */
  const API_BASE = (() => {
    // Served by the FastAPI backend itself → same origin; otherwise the local server.
    if (location.protocol.startsWith('http') && /localhost:8000|127\.0\.0\.1:8000/.test(location.host)) return '';
    return 'http://localhost:8000';
  })();
  const STATE_LABELS = { untreated: 'ללא טיפול – אפיזודה פסיכוטית פעילה', treated: 'תחת טיפול תרופתי – שישה חודשים של ריספרידון' };
  const OPENERS = {
    untreated: 'אה… שלום. אתה… אתה מהמרפאה? לא משנה. אפשר לדבר, רק בשקט. הם מקשיבים.',
    treated: 'שלום, אני דני. חצי שנה עכשיו עם הטיפול. אפשר לשאול אותי כל דבר – גם על איך שהיה קודם.',
  };
  // Scripted fallback when the backend is unreachable (mirrors python/main.py demo mode).
  const OFFLINE = {
    untreated: [
      'רגע… רגע. אתה שומע את זה? לא, בסדר. מה שאלת? הם אמרו עכשיו שלא כדאי שאדבר איתך, אבל אני מדבר. הטלפון שלך דולק? תכבה אותו רגע.',
      'אני לא ישן טוב. השכנים מלמעלה יודעים משהו, אני שומע אותם מדברים עליי דרך הצינורות. זה לא בראש שלי, זה בקיר.',
      'קשה לי להסביר, המילים… מילה אחת מושכת מילה אחרת וזה בורח לי. הקולות אומרים שאני מבזבז לך את הזמן.',
    ],
    treated: [
      'כן, אפשר לדבר. חצי שנה עם הטיפול, ובסך הכול יותר יציב. יש ימים שאני עייף מאוד בבוקר, אבל הקולות כמעט ולא חוזרים.',
      'לפני חצי שנה הייתי בטוח שהשכנים מאזינים לי דרך הקירות. היום אני יודע שזה היה חלק מהמחלה.',
      'התרופה עוזרת, זה ברור לי. המחיר הוא עלייה של כמה קילו ועייפות. אני לא מפסיק בלי הרופאה שלי.',
    ],
  };

  function initChat() {
    const root = document.getElementById('chat');
    if (!root) return;
    const messagesEl = document.getElementById('chatMessages');
    const form = document.getElementById('chatForm');
    const input = document.getElementById('chatInput');
    const sendBtn = document.getElementById('chatSend');
    const statusEl = document.getElementById('chatStatus');
    const modeEl = document.getElementById('chatMode');
    const endpointEl = document.getElementById('chatEndpoint');
    const toggle = root.querySelector('.state-toggle');
    const options = Array.from(toggle.querySelectorAll('.state-toggle__opt'));
    const history = { untreated: [], treated: [] };
    const offlineIndex = { untreated: 0, treated: 0 };
    let state = 'untreated';
    let busy = false;
    let serverMode = null; // 'llm' | 'demo' | null (unreachable)
    endpointEl.textContent = API_BASE ? API_BASE.replace(/^https?:\/\//, '') : location.host;

    function setStatus(kind, text) {
      statusEl.className = `chat__status is-${kind}`;
      statusEl.innerHTML = `<i class="chat__dot"></i>${text}`;
    }
    function addMessage(role, text, meta) {
      const wrap = el('div', `msg msg--${role}${role === 'agent' ? ` is-${state}` : ''}`);
      if (role === 'agent') wrap.appendChild(el('span', 'msg__avatar', 'ד'));
      const bubble = el('div', 'msg__bubble');
      bubble.appendChild(document.createTextNode(text));
      if (meta) bubble.appendChild(el('span', 'msg__meta', meta));
      wrap.appendChild(bubble);
      messagesEl.appendChild(wrap);
      messagesEl.scrollTop = messagesEl.scrollHeight;
      return wrap;
    }
    function addLoading() {
      const wrap = el('div', 'msg msg--agent msg--loading');
      wrap.appendChild(el('span', 'msg__avatar', 'ד'));
      wrap.innerHTML += '<div class="msg__bubble"><span class="glass-spinner" aria-hidden="true"></span><span class="typing-dots" aria-label="דני מקליד"><i></i><i></i><i></i></span></div>';
      messagesEl.appendChild(wrap); messagesEl.scrollTop = messagesEl.scrollHeight;
      return wrap;
    }
    function renderHistory() {
      messagesEl.innerHTML = '';
      addMessage('system', STATE_LABELS[state]);
      if (!history[state].length) addMessage('agent', OPENERS[state]);
      history[state].forEach((m) => addMessage(m.role === 'user' ? 'user' : 'agent', m.content, m.meta));
    }
    function setState(next) {
      state = next;
      toggle.classList.toggle('is-treated', state === 'treated');
      options.forEach((o) => { const on = o.dataset.state === state; o.classList.toggle('is-active', on); o.setAttribute('aria-checked', on); });
      renderHistory();
    }
    options.forEach((o) => o.addEventListener('click', () => { if (!busy) setState(o.dataset.state); }));

    async function checkHealth() {
      try {
        const res = await fetch(`${API_BASE}/api/health`, { cache: 'no-store' });
        if (!res.ok) throw new Error(res.statusText);
        const data = await res.json();
        serverMode = data.mode;
        if (data.mode === 'llm') { setStatus('live', `מחובר · מודל ${data.model}`); modeEl.textContent = 'מצב LLM'; }
        else { setStatus('demo', 'מחובר · מצב הדגמה (ללא מפתח API)'); modeEl.textContent = 'תשובות כתובות מראש מהשרת'; }
      } catch (err) {
        serverMode = null;
        setStatus('off', 'השרת לא זמין – תשובות הדגמה מקומיות');
        modeEl.textContent = 'הריצו: uvicorn main:app --port 8000';
      }
    }

    function offlineReply(message) {
      const bank = OFFLINE[state];
      const reply = bank[offlineIndex[state] % bank.length];
      offlineIndex[state] += 1;
      return new Promise((resolve) => setTimeout(() => resolve({ reply, mode: 'offline' }), 700 + Math.random() * 600));
    }
    async function ask(message) {
      const payload = { message, clinical_state: state, history: history[state].slice(-20).map(({ role, content }) => ({ role, content })) };
      const controller = new AbortController(); const timer = setTimeout(() => controller.abort(), 45000);
      try {
        const res = await fetch(`${API_BASE}/api/chat`, {
          method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload), signal: controller.signal,
        });
        if (!res.ok) { const detail = await res.json().catch(() => ({})); throw new Error(detail.detail || res.statusText); }
        const data = await res.json();
        if (serverMode === null) checkHealth();
        return data;
      } catch (err) {
        if (serverMode !== null && !(err.name === 'TypeError')) throw err;   // server up but answered with an error
        serverMode = null; setStatus('off', 'השרת לא זמין – תשובות הדגמה מקומיות');
        return offlineReply(message);
      } finally { clearTimeout(timer); }
    }

    async function send(message) {
      const text = (message || '').trim();
      if (!text || busy) return;
      busy = true; sendBtn.disabled = true; input.value = '';
      history[state].push({ role: 'user', content: text });
      addMessage('user', text);
      const loading = addLoading();
      try {
        const data = await ask(text);
        loading.remove();
        const meta = data.mode === 'llm' ? `${data.model}` : data.mode === 'demo' ? 'הדגמה (שרת)' : 'הדגמה (מקומי)';
        history[state].push({ role: 'assistant', content: data.reply, meta });
        addMessage('agent', data.reply, meta);
      } catch (err) {
        loading.remove();
        addMessage('system', `שגיאה מהשרת: ${err.message}`);
      } finally { busy = false; sendBtn.disabled = false; input.focus(); }
    }

    form.addEventListener('submit', (e) => { e.preventDefault(); send(input.value); });
    document.querySelectorAll('#chatSuggest [data-q]').forEach((b) => b.addEventListener('click', () => send(b.dataset.q)));
    hooks.onEnter[CHAT_SLIDE] = () => { if (serverMode === null) checkHealth(); setTimeout(() => input.focus({ preventScroll: true }), 400); };
    setState('untreated');
    checkHealth();
  }

  /* ------------------------------------------------------------------ */
  initDecorations();
  initBrainBridge();
  initFlowchart();
  initPOV();
  initChat();
  goTo(readHash());
})();
