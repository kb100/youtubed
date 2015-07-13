youtubed - A bash daemon for controlling youtube-dl



Development copy, expect bugs.

- [INSTALLATION] (#installation)
- [USE] (#use)
- [USE WITH TOR] (#use-with-tor)
- [OPTIONS] (#options)
- [BUGS] (#bugs)

# INSTALLATION

These scripts were written to be used with [i3](http://www.i3wm.org) and [i3blocks](https://github.com/vivien/i3blocks), so we assume you have a working installation of each.
It is possible to use youtubed with other status line displayers besides i3blocks, but we will not go into detail about how to do so.
With that in mind, let's get started.

Install the dependencies:

```ShellSession
sudo aptitude install youtube-dl inotify-tools xclip
```

Clone the repo:

```ShellSession
git clone https://github.com/kb100/youtubed.git
```

No need to compile anything, just put the scripts somewhere in your path:

```ShellSession
sudo cp youtubed/{youtubed,youtubed_controller,youtubed_validate-url.py} /usr/local/bin
```

You only need the url validator if you plan on using the `--domain-whitelist` option.


Edit your i3blocks config (e.g. `$HOME/.config/i3blocks/config`):

```INI
[youtube_controller]
command=$SCRIPT_DIR/youtubed_controller
interval=once
markup=pango
signal=1
# use pkill -RTMIN+1 i3blocks to trigger a block update
```

Run the youtubed script:

```ShellSession
youtubed --download-dir=$HOME/.youtubed --media-cmd="i3-msg exec mpv"
```

where you can replace mpv with your favorite media player, or use `--media-cmd=""` to disable automatic opening of files after download completes. 
If you specify `--daemon-dir`, you must also specify the same directory in the i3blocks blocklet command:

```INI
command=$SCRIPT_DIR/youtubed_controller $DAEMON_DIR
```

After you have setup your i3blocks configuration, restart i3 inplace:

```ShellSession
i3-msg restart
```

Your youtubed setup is now running!
You should now see `[DL]` in your status line.

![DL](https://cloud.githubusercontent.com/assets/1966710/7039499/741102cc-dd88-11e4-8a8e-999efb8ebb32.gif)

# USE

Left click the blocklet to trigger a download of the video from your clipboard.
Right click the blocklet to cancel a download of the video from your clipboard.

![leftclick](https://cloud.githubusercontent.com/assets/1966710/7052700/d5022f94-ddf5-11e4-81f0-f9d934ad6a1d.gif)

These can also be done by sending SIGUSR1 and SIGUSR2 respectively, e.g.:

```ShellSession
pkill -SIGUSR1 youtubed
```

or by sending commands directly to youtubed's command fifo:

```ShellSession
echo "download $URL" > $DAEMON_DIR/youtubed.fifo
```

A simple "download" or "cancel" command with no other arguments will use the clipboard's content's
as the URL to download or cancel.
You can specify alternative download and cancel signals with `--download-signal` and `--cancel-signal`.
If youtubed is in the middle of a download, left clicking will either begin downloading the next video in parallel,
or gracefully restart youtube-dl and resume the download if the video URL matches one that is already downloading.
This is useful because sometimes youtube decides to throttle your download speed, and simply restarting the download
may significantly increase your speeds.
Multiple simultaneous downloads are supported, just copy URL, click, copy URL, click.
Terminating youtubed can be done with a SIGTERM, with a SIGINT (CTRL-C) if youtubed is running in the foreground, or by sending the message "die" to the fifo.

By default, youtubed will tell youtube-dl to get the best quality video and audio to download.
You can use your mouse wheel and scroll  up over the blocklet to change between: bestvideo+bestaudio, bestaudio, worstvideo+worstaudio, and worstaudio.
You can also specify a custom quality with the `--default-quality` flag or by sending "quality FORMAT" to the fifo.
The format must be a valid youtube-dl format string (see the `--format` option in youtube-dl's man page).
You can also send "toggle_quality" to the fifo to automatically switch between the formats listed above.

# USE WITH TOR

Due to an unknown change in youtube-dl, torsocks no longer works with youtube-dl on some systems.
In the event that your system is not compatible, attempting to run youtube-dl with torsocks will cause your cpus to max out and ram will be malloced at over 1GB per second.

If compatible, we recommend the use of [tor](https://www.torproject.org/) and torsocks in combination with youtubed.
Of course you will need to install them first:

```ShellSession
sudo aptitude install tor torsocks
```

Prepending `torsocks` to your youtubed call should allow you to use youtubed over tor:

```ShellSession
torsocks youtubed [usual options] [--default-quality="worstvideo+worstaudio"] [--domain-whitelist="domain-whitelist.conf"]
```

Please be mindful that the tor network is not (yet) equipped for high bandwidth users, so be considerate and set the download quality to worstvideo+worstaudio or worstaudio when using tor.
This can be accomplished with the `--default-quality` option as above.

**WARNING: by nature of how youtubed works, the contents of your clipboard may be sent over the tor network upon executing a youtubed command. If your clipboard contains sensitive or identifying information, this could be a serious problem for you. We strongly suggest using the `--domain whitelist` option as above to prevent yourself from revealing your clipboard should you accidentally click the blocklet.**

Whitelist files should be lines with domain names one per line. Lines beginning with '#' are ignored.

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

    --default-quality   Set the default quality of videos to download.
                        Default: bestvideo+bestaudio

    --media-cmd         Use "media-cmd file" to open a file after download.
                        Default: i3-msg exec mpv

    --domain-whitelist  Reject url unless its domain is in the given file.
                        Default: 

    --run-in-foreground Tells youtubed to stay in the foreground.

# BUGS

Report bugs and suggestions at the [issues](https://github.com/kb100/youtubed/issues) page.
Try running youtubed with the `--run-in-foreground` flag for some helpful output, and be sure to include this output when reporting a bug.
Fixes and other contributions are welcome.
