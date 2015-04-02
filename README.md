youtubed - A bash daemon for controlling youtube-dl



Development copy, expect bugs.

- [INSTALLATION] (#installation)
- [OPTIONS] (#options)
- [USE] (#use)
- [BUGS] (#bugs)

# INSTALLATION

This script was written to be used with [i3](http://www.i3wm.org) and [i3blocks](https://github.com/vivien/i3blocks), so we assume you have a working desktop installation of each.

Install the dependencies:

    sudo aptitude install youtube-dl inotify-tools xclip

Clone the repo:

    git clone https://github.com/kb100/youtubed.git

They are bash scripts, so there is no need to compile, just put them somewhere in your path:

    sudo cp youtubed/{youtubed,youtubed_controller} /usr/local/bin

Edit your `i3blocks` config (e.g. `$HOME/.config/i3blocks/config`):

    [youtube_controller]
    command=$SCRIPT_DIR/youtubed_controller
    interval=once
    signal=1

Run the `youtubed` script:

    youtubed --download-dir=$HOME/.youtubed --media-cmd="i3-msg exec mpv"

where you can replace `mpv` with your favorite media player, or with `""` to disable automatic opening of files after download completes. 
If you specify `--daemon-dir` you must also specify the same directory in the i3blocks blocklet command:

    command=$SCRIPT_DIR/youtubed_controller $DAEMON_DIR

Restart `i3`:

    i3-msg restart

Your `youtubed` is now running!

# USE

Left click to trigger download of the video from your clipboard.
Right click to cancel download of the video from your clipboard.
These can also be done by sending `SIGUSR1` and `SIGUSR2` respectively, e.g.:

    pkill -SIGUSR1 youtubed

or by sending commands directly to `youtubed`'s command fifo:

    echo "download $URL" > $DAEMON_DIR/youtubed.fifo

A simple "download" or "cancel" assumes the clipboard should be used.
Alternatively you can specify  other signals with `--download-signal` and `--cancel-signal`.
If already running, left clicking will gracefully restart youtube-dl
and resume the download.
Multiple simultaneous downloads are supported, just copy URL, click, copy URL, click.
Terminating `youtubed` can be done with a `SIGTERM` or by sending the message "die" to the fifo.

# OPTIONS

    -h --help           Print this help message.
    --download-signal   The signal that will trigger a download.
                        Default: SIGUSR1
    --cancel-signal     The signal that will cancel a download.
                        Default: SIGUSR2
    --download-dir      The directory to save downloads in.
                        Default: $XDG_DATA_DIR/youtubed
    --exec-after-write  A command to execute after youtube-dl writes a status
                        line. 
                        Default: pkill -RTMIN+1 i3blocks
    --daemon-dir        The directory that youtubed keeps its state files 
                        (.pid files, progress files, youtubed-fifo, status text
                        files). 
                        Default: $XDG_RUNTIME_DIR/youtubed
    --format-str        The format string to supply to youtube-dl. 
                        Default: %(title)s.%(id)s.%(resolution)s.%(ext)s
    --media-cmd         Use "media-cmd file" to open a file after download.
                        Default: i3-msg exec mpv
    --run-in-foreground Tells youtubed to stay in the foreground.

# BUGS

Report bugs and suggests at the [issues](https://github.com/kb100/youtubed/issues) page.
Try running `youtubed` with the `--run-in-foreground` flag for some helpful output.
Fixes and other contributions are welcome.
