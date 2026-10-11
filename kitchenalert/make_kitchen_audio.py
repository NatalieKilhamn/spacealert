# -*- coding: utf-8 -*-
"""Build the English announcements for Kitchen Alert.

The voices come from macOS text-to-speech (`say`), the bell, the ticking timer and the
kitchen noise are synthesised here, and ffmpeg encodes everything to MP3 in audio/.
Run this on a Mac with ffmpeg installed:

    python3 make_kitchen_audio.py [--voice Daniel] [--rate 175]

Countdowns are assembled word by word, so "five ... one" lands on whole seconds and the
phase ends exactly seven seconds after the countdown clip starts, as in Space Alert.
"""
import argparse, math, os, random, struct, subprocess, tempfile, wave

RATE = 22050
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio')

NUMBERS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight']
ORDINALS = {1: 'First', 2: 'Second', 3: 'Third'}


class Clip:
    """Mono 16-bit samples as a list of ints."""
    def __init__(self, samples=None):
        self.samples = samples or []

    @property
    def seconds(self):
        return len(self.samples) / RATE

    def place(self, other, at):
        """Mix *other* into this clip starting *at* seconds, growing the clip if needed."""
        start = int(round(at * RATE))
        end = start + len(other.samples)
        if end > len(self.samples):
            self.samples.extend([0] * (end - len(self.samples)))
        for i, s in enumerate(other.samples):
            v = self.samples[start + i] + s
            self.samples[start + i] = max(-32768, min(32767, v))
        return self

    def then(self, other, gap=0.0):
        return self.place(other, self.seconds + gap)

    def pad_to_extra(self, seconds):
        return self.pad_to(self.seconds + seconds)

    def pad_to(self, seconds):
        n = int(round(seconds * RATE))
        if len(self.samples) < n:
            self.samples.extend([0] * (n - len(self.samples)))
        return self


def speak(text, voice, rate, tmp):
    path = os.path.join(tmp, 'say.wav')
    subprocess.run(['say', '-v', voice, '-r', str(rate), '-o', path,
                    '--data-format=LEI16@{}'.format(RATE), text], check=True)
    with wave.open(path) as w:
        assert w.getnchannels() == 1 and w.getsampwidth() == 2
        data = w.readframes(w.getnframes())
    samples = list(struct.unpack('<{}h'.format(len(data) // 2), data))
    # trim the silence `say` leaves around the words
    threshold = 300
    first = next((i for i, s in enumerate(samples) if abs(s) > threshold), 0)
    last = next((i for i in range(len(samples) - 1, -1, -1) if abs(samples[i]) > threshold), len(samples) - 1)
    first = max(0, first - int(0.02 * RATE))
    last = min(len(samples), last + int(0.06 * RATE))
    return Clip(samples[first:last])


def bell():
    """Two strikes on a service bell."""
    clip = Clip()
    partials = [(1.0, 1568.0), (0.55, 3951.0), (0.3, 5390.0), (0.15, 2093.0)]
    for strike in (0.0, 0.32):
        n = int(1.1 * RATE)
        s = []
        for i in range(n):
            t = i / RATE
            v = sum(a * math.sin(2 * math.pi * f * t) * math.exp(-t * (3.0 + 2.2 * k))
                    for k, (a, f) in enumerate(partials))
            s.append(int(9000 * v * min(1.0, t * 400)))
        clip.place(Clip(s), strike)
    return clip


def tick_loop(seconds=2.0):
    """A quiet kitchen timer: one tick per second, looped by the player between announcements."""
    clip = Clip().pad_to(seconds)
    rnd = random.Random(1)
    for k in range(int(seconds)):
        n = int(0.012 * RATE)
        s = [int(2600 * rnd.uniform(-1, 1) * math.exp(-i / (0.0025 * RATE))) for i in range(n)]
        clip.place(Clip(s), k * 1.0)
    return clip


def fan_noise(seconds=75.0):
    """Extractor fan: brown noise with a slow wobble, faded in and out."""
    rnd = random.Random(2)
    n = int(seconds * RATE)
    s, v = [], 0.0
    for i in range(n):
        v = 0.985 * v + rnd.uniform(-1, 1) * 0.6
        t = i / RATE
        env = min(1.0, t / 1.5) * min(1.0, (seconds - t) / 1.5) * (0.85 + 0.15 * math.sin(2 * math.pi * 0.23 * t))
        s.append(int(max(-1.0, min(1.0, v / 6.0)) * 9000 * env))
    return Clip(s)


def beep():
    n = int(0.45 * RATE)
    return Clip([int(9000 * math.sin(2 * math.pi * 880 * i / RATE) * min(1.0, i / 200, (n - i) / 200)) for i in range(n)])


def countdown(intro, outro, say_):
    """Intro, then five ... one on whole seconds from 2 s, and the outro exactly at 7 s."""
    clip = say_(intro)
    if clip.seconds > 1.9:
        raise ValueError('Countdown intro too long: {!r} ({:.2f} s)'.format(intro, clip.seconds))
    for k, n in enumerate((5, 4, 3, 2, 1)):
        clip.place(say_(NUMBERS[n].capitalize() + '.'), 2.0 + k)
    clip.place(say_(outro), 7.0)
    return clip


def write(clip, name, tmp):
    wav = os.path.join(tmp, name + '.wav')
    with wave.open(wav, 'w') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
        w.writeframes(struct.pack('<{}h'.format(len(clip.samples)), *clip.samples))
    mp3 = os.path.join(OUT, name + '.mp3')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-c:a', 'libmp3lame', '-q:a', '4', mp3], check=True)
    print('{:<14} {:5.2f} s'.format(name, clip.seconds))


def main():
    parser = argparse.ArgumentParser(description='Build the Kitchen Alert announcements.')
    parser.add_argument('--voice', default='Daniel')
    parser.add_argument('--rate', type=int, default=175)
    args = parser.parse_args()
    os.makedirs(OUT, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        say_ = lambda text: speak(text, args.voice, args.rate, tmp)
        clips = {
            'begin': say_('Doors open. Guests are arriving. Begin first phase.'),
            # parts of an order announcement, played back to back: leave a short pause after each
            'order': say_('New order.').pad_to_extra(0.3),
            'large_order': say_('Large order.').pad_to_extra(0.3),
            'room_red': say_('Red dining room.').pad_to_extra(0.45),
            'room_blue': say_('Blue dining room.').pad_to_extra(0.45),
            'repeat': say_('Repeat.').pad_to_extra(0.35),
            'delivery': say_('Delivery. Each player may draw one card.'),
            'rush_on': say_('Rush hour. No talking.'),
            'rush_off': say_('Rush is over. You may talk again.'),
            'bell': bell(),
            'tick': tick_loop(),
            'fan': fan_noise(),
        }
        for t in range(1, 9):
            clips['time{}'.format(t)] = say_('Time T plus {}.'.format(NUMBERS[t])).pad_to_extra(0.3)
        handover = say_('Handover. Each player may give one card to another player.')
        for k, n in enumerate((3, 2, 1)):
            handover.place(say_(NUMBERS[n].capitalize() + '.'), 9.3 + k)
        clips['handover'] = handover.place(beep(), 12.3)
        for p in (1, 2):
            name, nxt = ORDINALS[p], ORDINALS[p + 1].lower()
            clips['phase{}_60'.format(p)] = say_('{} phase ends in one minute.'.format(name))
            clips['phase{}_20'.format(p)] = say_('{} phase ends in twenty seconds.'.format(name))
            clips['phase{}_7'.format(p)] = countdown('{} phase ends in'.format(name),
                                                     '{} phase has ended. Begin {} phase.'.format(name, nxt), say_)
        clips['phase3_60'] = say_('The kitchen closes in one minute.')
        clips['phase3_20'] = say_('The kitchen closes in twenty seconds.')
        clips['phase3_7'] = countdown('The kitchen closes in', 'The kitchen is closed. Service is over.', say_)
        clips['bell'].pad_to_extra(0.2)
        for name, clip in sorted(clips.items()):
            write(clip, name, tmp)


if __name__ == '__main__':
    main()
