// Unit test of the AudioManager in player.js, with fake audio elements and a fake clock.
// Run with: node player/test_audio.js
const fs = require('fs'), vm = require('vm');
let now = 0, timers = [], log = [];
class FakeAudio {
  constructor(id) { this.id = id; this.loop = false; this.currentTime = 0; this.playing = false; this.onended = null; }
  play() { this.playing = true; log.push(`${now/1000}s play ${this.id}`); return Promise.resolve(); }
  pause() { if (this.playing) log.push(`${now/1000}s pause ${this.id}`); this.playing = false; }
  end() { this.playing = false; if (this.onended) this.onended(); }
}
const els = {};
const ctx = {
  document: { getElementById: id => els[id] || (els[id] = new FakeAudio(id)) },
  setTimeout: (f, ms) => { const t = { at: now + ms, f }; timers.push(t); return t; },
  clearTimeout: t => { timers = timers.filter(x => x !== t); },
  Date: { now: () => now }, console,
};
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(process.argv[2] || require('path').join(__dirname, 'player.js'), 'utf8') + '\nthis.AudioManager = AudioManager;', ctx);
const advance = ms => { const end = now + ms; for (;;) { timers.sort((a, b) => a.at - b.at); const t = timers[0]; if (!t || t.at > end) break; timers.shift(); now = t.at; t.f(); } now = end; };
const el = id => ctx.document.getElementById('audio-' + id);
const playingNow = () => Object.values(els).filter(e => e.playing).map(e => e.id).join(',');
function check(name, cond) { console.log((cond ? 'ok   ' : 'FAIL ') + name); if (!cond) process.exitCode = 1; }

// 1. Rush hour of 10 s: on, 7 s noise, off, then the ambient loop
let am = new ctx.AudioManager();
am.setTracks(['comm_down', 'noise7', 'comm_restored']);
advance(1600); el('comm_down').end();
check('noise plays after "rush on"', playingNow() === 'audio-noise' && el('noise').loop);
advance(6900); check('noise still on at 6.9 s', playingNow() === 'audio-noise');
advance(200);  check('noise stopped at 7 s and "rush is over" plays', playingNow() === 'audio-comm_restored');
advance(2000); el('comm_restored').end(); check('ambient loop afterwards', playingNow() === 'audio-alarm5');

// 2. Pause in the middle of the noise
log = []; am.setTracks(['comm_down', 'noise7', 'comm_restored']); el('comm_down').end();
advance(3000); am.pause(); advance(20000);
check('paused noise does not end', !el('noise').playing && !el('comm_restored').playing);
am.play(); advance(3900); check('resumed noise still on 3.9 s later', playingNow() === 'audio-noise');
advance(200); check('resumed noise ends after the remaining 4 s', playingNow() === 'audio-comm_restored');

// 3. A new event during the noise cancels it
am.setTracks(['comm_down', 'noise7', 'comm_restored']); el('comm_down').end(); advance(2000);
am.setTracks(['alert', 'time3']);
check('new event stops the noise', !el('noise').playing && playingNow() === 'audio-alert');
advance(10000); check('old noise timer does not fire later', playingNow() === 'audio-alert');
