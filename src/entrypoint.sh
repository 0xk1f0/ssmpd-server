#!/usr/bin/env bash

# "bash strict mode"
set -uo pipefail

# /etc/snapserver.conf
SNAP_CONFFILE="/etc/snapserver.conf"
MPD_PATH="/etc/"

# make sure paths are there
/bin/mkdir -p /etc/mpd/
/bin/mkdir -p /var/lib/mpd/database/

log_notify_user() {
    echo "$(date) setup: ${1}"
}

# check envvars
ENVVARS=("ENDPOINTS")
for var in "${ENVVARS[@]}"; do
    if [[ ! -v $var ]]; then
        log_notify_user "${var} is unset, exiting"
        exit 1
    fi
done

# Add the common configuration
log_notify_user "Creating snapserver config.."
> "${SNAP_CONFFILE}"
cat << EOF >> "${SNAP_CONFFILE}"
[http]
enabled = true
bind_to_address = 0.0.0.0
port = 1780
doc_root = /usr/share/snapserver/snapweb/

[stream]
EOF

# Add the "source" lines based on the number of endpoints
for ((i=1; i<=$ENDPOINTS; i++)); do
    cat << EOF >> "${SNAP_CONFFILE}"
# Endpoint ${i}
source = spotify:///librespot?name=Spotify${i}&bitrate=320&devicename=Snapcast${i}&volume=25&normalize=true
source = pipe:///tmp/snapfifo${i}?name=MPD${i}
EOF
done
log_notify_user "Done!"

# Create mpd configs for each endpoints
log_notify_user "Creating mpd configs.."
for ((i=1; i<=$ENDPOINTS; i++)); do
    > "${MPD_PATH}mpd${i}.conf"
    if [ $i -eq 1 ]; then
        cat << EOF >> "${MPD_PATH}mpd${i}.conf"
music_directory     "/var/lib/mpd/music"
playlist_directory  "/var/lib/mpd/playlists"
db_file             "/var/lib/mpd/database/database"
port "6600"

EOF
    else
	PORT=$((i - 1))
        cat << EOF >> "${MPD_PATH}mpd${i}.conf"
music_directory     "/var/lib/mpd/music"
playlist_directory  "/var/lib/mpd/playlists"
port                "660${PORT}"

database {
    plugin  "proxy"
    host    "localhost"
    port    "6600"
}

EOF
    fi
    cat << EOF >> "${MPD_PATH}mpd${i}.conf"
user                "root"
zeroconf_enabled    "no"
bind_to_address     "localhost"

audio_output {
    type            "fifo"
    name            "snapcast"
    path            "/tmp/snapfifo${i}"
    format          "48000:16:2"
    mixer_type      "software"
}
EOF
done
log_notify_user "Done!"

# start mpd daemons
log_notify_user "Ready to Rock!"
log_notify_user "Starting MPD instances.."
for ((i=1; i<=$ENDPOINTS; i++)); do
    mpd /etc/mpd${i}.conf
done

# start snapserver
log_notify_user "Starting Snapcast Server.."
snapserver
