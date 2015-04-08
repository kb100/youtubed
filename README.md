youtubed - A bash daemon for controlling youtube-dl



Development copy, expect bugs.

- [INSTALLATION] (#installation)
- [USE] (#use)
- [OPTIONS] (#options)
- [BUGS] (#bugs)

# INSTALLATION

These scripts were written to be used with [i3](http://www.i3wm.org) and [i3blocks](https://github.com/vivien/i3blocks), so we assume you have a working installation of each.
It is possible to use youtubed

Install the dependencies:

    sudo aptitude install youtube-dl inotify-tools xclip

Clone the repo:

    git clone https://github.com/kb100/youtubed.git

Since the executables are bash scripts, there is no need to compile them.
Just put them somewhere in your path:

    sudo cp youtubed/{youtubed,youtubed_controller} /usr/local/bin

Edit your i3blocks config (e.g. `$HOME/.config/i3blocks/config`):

    [youtube_controller]
    command=$SCRIPT_DIR/youtubed_controller
    interval=once
    signal=1

Run the youtubed script:

    youtubed --download-dir=$HOME/.youtubed --media-cmd="i3-msg exec mpv"

where you can replace mpv with your favorite media player, or use `--media-cmd=""` to disable automatic opening of files after download completes. 
If you specify `--daemon-dir`, you must also specify the same directory in the i3blocks blocklet command:

    command=$SCRIPT_DIR/youtubed_controller $DAEMON_DIR

After you have setup your i3blocks configuration, restart i3 inplace:

    i3-msg restart

Your youtubed setup is now running!
You should now see `[DL]` in your status line.

# USE

Left click the blocklet to trigger a download of the video from your clipboard.
Right click the blocklet to cancel a download of the video from your clipboard.
These can also be done by sending SIGUSR1 and SIGUSR2 respectively, e.g.:

    pkill -SIGUSR1 youtubed

or by sending commands directly to youtubed's command fifo:

    echo "download $URL" > $DAEMON_DIR/youtubed.fifo

A simple "download" or "cancel" command with no other arguments will use the clipboard's content's
as the URL to download or cancel.
You can specify alternative download and cancel signals with `--download-signal` and `--cancel-signal`.
If youtubed is in the middle of a download, left clicking will either begin downloading the next video in parallel,
or gracefully restart youtube-dl and resume the download if the video URL matches one that is already downloading.
This is useful because sometimes youtube decides to throttle your download speed, and simply restarting the download
may significantly increase your speeds.
Multiple simultaneous downloads are supported, just copy URL, click, copy URL, click.
Terminating youtubed can be done with a SIGTERM or by sending the message "die" to the fifo.

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

Report bugs and suggestions at the [issues](https://github.com/kb100/youtubed/issues) page.
Try running youtubed with the `--run-in-foreground` flag for some helpful output, and be sure to include this output when reporting a bug.
Fixes and other contributions are welcome.
