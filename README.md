youtubed - A bash daemon for controlling youtube-dl



Development copy. MINIMALLY TESTED, UNFINISHED, EXPECT SYSTEM CRASHING BUGS.

- [INSTALLATION] (#installation)
- [OPTIONS] (#options)
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

Restart `i3`:

    i3-msg restart

Your `youtubed` is now running!

# OPTIONS

    -h --help           Print this help message.
    --download-signal   The signal that will trigger a download.
                        Default: SIGUSR1
    --cancel-signal     The signal that will cancel a download.
                        Default: SIGUSR2
    --download-dir      The directory to save downloads in.
                        Default: $XDG_DATA_DIR
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
Fixes and other contributions are welcome.
