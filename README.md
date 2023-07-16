# ssmpd-server

[![Docker](https://github.com/0xk1f0/ssmpd-server/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/0xk1f0/ssmpd-server/actions/workflows/docker-publish.yml)

***S***napcast***S***potify***MPD***

This is project aims to unify:

- [Snapcast](https://github.com/badaix/snapcast)
- [MPD](https://github.com/MusicPlayerDaemon/MPD)
- [LibreSpot](https://github.com/librespot-org/librespot) (Spotify Connect)

It runs in a single Docker Container and aims to have a unified API
endpoint that can be accessed by different clients.

## Why does this exist

There are many configurations and setups concerning my use case which
can be summed up as

- The Ability to use Spotify Connect on all Speakers in my home
- Also play from a local Music Collection
- Be able to play from Internet Radio Stations

But I find most of them either don't work right for me or are to cluttered
with other stuff that I don't really need.

*So I decided to do my own thing.*

Local Music and Internet Radio playback can be done with MPD, while Spotify 
Connect one can be implemented with Librespot. To unify these two we can 
use Snapcast.

## How to run

Docker Images are automatically built, get the image from this repo's container
registry using:

```bash
docker pull ghcr.io/0xk1f0/ssmpd-server:master
```

There is an example docker-compose file located in this repo also, should be self
explanatory if you've done some docker stuff before. You can control the whole thing
like this:

```bash
# start
docker-compose up -d
# stop
docker-compose down
```

Make sure to check out the list below to get a general idea of what is implemented
yet and what isn't.

## Checklist

- [x] Server Docker Container with all needed integrations
- [ ] Generic API Interface that can control all involved services (some Python Flask combo)
- [ ] Web Frontend (probably Astro.js)
- [ ] Desktop/Mobile App (probably either Tauri or React Native if i feel like it)
