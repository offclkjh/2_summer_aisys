# notetakings (origin in Notion)
https://missing.csail.mit.edu/?utm_source=chatgpt.com

- topic 1: the shell
    - notetaking
        
        terminal&shell
        
        shell: beyond the interface(GUI), textual interface to the computer
        
        ←run by terhminal (win + r → cmd)
        
        linux shell : Bash, most common. (Mac → Zsh command by human rather than program)
        
        window → Batch or PowerShell
        
        kind of PL → write to bash program file
        
        - + : combining programs, open source community
            
            → continuous integrations for projects
            
        
        what is shell?
        
        prompt: main interface.
        
        username@host location (~ ← /home/username)
        
        comands
        
        name of program (source file → .py, built-in → only name)
        
        arguments of program
        
        argument parsing by white space boundaries
        
        !image.png
        
        escaping uses “\@”
        
        !image.png
        
        program “man” (manual) (apocalypse → man bash)
        
        !image.png
        
        or program —help
        
        cd (change directory)
        
        !image.png
        
        reletive path
        
        !image.png
        
        cd . → current directory, cd .. → parent directory 
        
        !image.png
        
        ZOxide: efficient to navigate
        
        Tab → rapid navigate, Tab Tab → show options
        
        what can we execute?
        
        name → path (environmental variable → value mapping (names → strings))
        
        ⇒ meta infomation
        
        $PATH ⇒ lists of directory
        
        !image.png
        
        which ⇒ traverse path list and print out path directory where it first finds a given program
        
        !image.png
        
        !image.png
        
        ls ⇒ lists the contents of a directory
        
        !image.png
        
        cat “file” ⇒ print out the content of a file
        
        sort “data” ⇒ print out with sorted order
        
        uniq “data” ⇒ 3 4 4 4 3 3 4 → 3 4 3 4
        
        sort -u “data” ⇒ no dup & sorted
        
        head “file” ⇒ print out n lines / tail “file”
        
        !image.png
        
        grep “file” ⇒ search in file with certain pattern → complicated searching
        
        !image.png
        
        (-r for recursive)
        
        !image.png
        
        sed file ⇒ edit file lines (sed PL) (-i for in-place replacement, g for global, across entire line)
        
        !image.png
        
        (glob argument & glob regular expressions regex)
        
        find “directory” pattern ⇒ find files (-type f  → is file -name “*.zip” → name ends with .zip, -mtime +30 last modified at least 30 days ago.
        
        !image.png
        
        !image.png
        
        !image.png
        
        (-exec “arguments” {} \ → execute program for that file, find seperates regex by ;)
        
        rm “file” ⇒ remove
        
        !image.png
        
        (-l → print the name of the file, -maxdepth)
        
        FD ⇒ less misuse & convi. find
        
        awk ⇒ parsing files (has own PL)
        
        split by white spaces & lines → let user write expressions over the result of parsing
        
        !image.png
        
        !image.png
        
        (for every line print second field(col))
        
        !image.png
        
        seperate field by comma (SCV)
        
        ssh ⇒ remote connecting tool
        
        !image.png
        
        the shell language (bash)
        
        | ⇒ right pipe output → left pipe input
        
        > ⇒ write to the file, not terminal (create or overwrite)
        
        >> ⇒ append to the file
        
        < ⇒ take input from the location
        
        !image.png
        
        !image.png
        
        !image.png
        
        !image.png
        
        !image.png
        
        !image.png
        
        $() ⇒ run the program inside the parentheses, and replace the output of the program
        
        program test == program 
        
        ![image.png
        
        !image.png
        
        cd, if, pipe, etc are not program, but bash PL ( [ ⇒ built-in test )
        
        bash program
        
        ![image.png
        
        hash bang ( #!/bin/sh )
        
        ⇒ tells the shell when it runs this file, execute the program at that path, and give that program the contents of this file as input.
        
        target program does not have to be a bash program. (python, Ruby, … )
        
        !image.png
        
        without ./, shell will search path program
        
        ls -l ⇒ check detailed file info.
        
    - lecture slides
        
        ## **What is the shell?**
        
        Computers these days have a variety of interfaces for giving them commands; fanciful graphical user interfaces, voice interfaces, AR/VR, and more recently: LLMs. These are great for 80% of use-cases, but they are often fundamentally restricted in what they allow you to do — you cannot press a button that isn’t there or give a voice command that hasn’t been programmed. To take full advantage of the tools your computer provides, we have to go old-school and drop down to a textual interface: The Shell.
        
        Nearly all platforms you can get your hands on have a shell in one form or another, and many of them have several shells for you to choose from. While they may vary in the details, at their core they are all roughly the same: they allow you to run programs, give them input, and inspect their output in a semi-structured way.
        
        To open a shell *prompt* (where you can type commands), you first need a *terminal*, which is the visual interface to a shell. Your device probably shipped with one installed, or you can install one fairly easily:
        
        - **Linux:** Press `Ctrl + Alt + T` (works on most distributions). Or search for “Terminal” in your applications menu.
        - **Windows:** Press `Win + R`, type `cmd` or `powershell`, and press Enter. Alternatively, search “Terminal” or “Command Prompt” in the Start menu.
        - **macOS:** Press `Cmd + Space` to open Spotlight, type “Terminal”, and press Enter. Or find it in Applications → Utilities → Terminal.
        
        On Linux and macOS, this will usually open the Bourne Again SHell, or “bash” for short. This is one of the most widely used shells, and its syntax is similar to what you will see in many other shells. On Windows, you’ll be greeted by the “batch” or “powershell” shells, depending on which command you ran. These are Windows-specific, and not what we’ll be focusing on in this class, although it has analogues for most of what we’ll be teaching. You’ll instead want the Windows Subsystem for Linux or a Linux virtual machine.
        
        Other shells exist, often with many ergonomic improvements over bash (fish and zsh are among the most common). While these are very popular (all the instructors use one), they’re nowhere near as ubiquitous as bash, and lean on many of the same concepts, so we won’t be focusing on those in this lecture.
        
        ## **Why should you care about it?**
        
        The shell is not just (usually) much faster than “clicking around”, it also comes with expressive power you can’t easily find in any one graphical program. As we’ll see, the shell gives you the ability to *combine* programs in creative ways to automate nearly any task.
        
        Knowing your way around a shell is also very useful to navigate the world of open-source software (which often come with install instructions that require the shell), building continuous integration for your software projects (as described in the Code Quality lecture), and debugging errors when other programs fail.
        
        ## **Navigating in the shell**
        
        When you launch your terminal, you will see a *prompt* that often looks a little like this:
        
        ```
        missing:~$
        ```
        
        This is the main textual interface to the shell. It tells you that you are on the machine `missing` and that your “current working directory”, or where you currently are, is `~` (short for “home”). The `$` tells you that you are not the root user (more on that later). At this prompt you can type a *command*, which will then be interpreted by the shell. The most basic command is to execute a program:
        
        ```
        missing:~$date
        Fri 10 Jan 2020 11:49:31 AM ESTmissing:~$
        ```
        
        Here, we executed the `date` program, which (perhaps unsurprisingly) prints the current date and time. The shell then asks us for another command to execute. We can also execute a command with *arguments*:
        
        ```
        missing:~$echohello
        hello
        ```
        
        In this case, we told the shell to execute the program `echo` with the argument `hello`. The `echo` program simply prints out its arguments. The shell parses the command by splitting it by whitespace, and then runs the program indicated by the first word, supplying each subsequent word as an argument that the program can access. If you want to provide an argument that contains spaces or other special characters (e.g., a directory named “My Photos”), you can either quote the argument with `'` or `"` (`"My Photos"`), or escape just the relevant characters with `\` (`My\ Photos`).
        
        Perhaps the most important command when you’re starting out is `man`, short for “manual”. The `man` program, among other things, lets you look up more information about any command on your system. For example, if you run `man date`, it’ll explain what `date` is, and all of the various arguments you can pass it to alter its behavior. You can also usually get a short version of the help by passing `--help` as an argument to most commands.
        
        > Consider installing and using `tldr` in addition to `man`, as it shows you common usage examples right there in the terminal. LLMs are also usually very good at explaining how commands work and how you can call them to achieve what you want to accomplish.
        > 
        
        After `man`, the most important command to learn is `cd`, or “change directory”. This command is actually built into the shell, and isn’t a separate program (i.e., `which cd` will say “no cd found”). You pass it a path, and that path becomes your current working directory. You’ll also see the working directory reflected in the shell prompt:
        
        ```
        missing:~$cd /bin
        missing:/bin$cd /
        missing:/$cd ~
        missing:~$
        ```
        
        > Note that the shell comes with auto-completion, so you can often complete paths faster by pressing `<TAB>`!
        > 
        
        A lot of commands operate on the current working directory if nothing else is specified. If you’re ever unsure where you are, you can run `pwd` or print the `$PWD` environment variable (with `echo $PWD`), both of which produce the current working directory.
        
        The current working directory also comes in handy in that it allows us to use *relative* paths. All the paths we’ve seen so far have been *absolute* — they start with `/` and give the full set of directories needed to navigate to some location from the root of the file system (`/`). In practice, you’ll more commonly work with relative paths; so called because they are relative to the current working directory. In a relative path (anything *not* starting with `/`), the first path component is looked up in the current working directory, and subsequent components traverse as usual. For example:
        
        ```
        missing:~$cd /
        missing:/$cdbin
        missing:/bin$
        ```
        
        There are also two “special” components that exist in every directory: `.` and `..`. `.` is “this directory”, and `..` is “the parent directory”. So:
        
        ```
        missing:~$cd /
        missing:/$cdbin/../bin/../bin/././../bin/..
        missing:/$
        ```
        
        You can usually use absolute and relative paths interchangeably for any command argument, just keep in mind what your current working directory is when using a relative one!
        
        > Consider installing and using `zoxide` to speed up your `cd`ing — `z` will remember the paths you frequently visit and let you access with less typing.
        > 
        
        ## **What is available in the shell?**
        
        But how does the shell know how to find programs like `date` or `echo`? If the shell is asked to execute a command, it consults an *environment variable* called `$PATH` that lists which directories the shell should search for programs when it is given a command:
        
        ```
        missing:~$echo $PATH
        /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/binmissing:~$which echo
        /bin/echomissing:~$/bin/echo $PATH
        /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
        ```
        
        When we run the `echo` command, the shell sees that it should execute the program `echo`, and then searches through the `:`-separated list of directories in `$PATH` for a file by that name. When it finds it, it runs it (assuming the file is *executable*; more on that later). We can find out which file is executed for a given program name using the `which` program. We can also bypass `$PATH` entirely by giving the *path* to the file we want to execute.
        
        This also gives a clue for how we can determine *all* the programs we’re able to execute in the shell: by listing the contents of all the directories on `$PATH`. We can do this by passing a given directory path to the `ls` program, which lists files:
        
        ```
        missing:~$ls /bin
        ```
        
        > Consider installing and using `eza` for a more human-friendly `ls`.
        > 
        
        This will, on most computers, print a *lot* of programs, but we’ll only focus on some of the most important ones here. First, some simple ones:
        
        - `cat file`, which prints the contents of `file`.
        - `sort file`, which prints out the lines of `file` in sorted order.
        - `uniq file`, which eliminates consecutive duplicate lines from `file`.
        - `head file` and `tail file`, which respectively print the first and last few lines of `file`.
        
        > Consider installing and using `bat` over `cat` for syntax highlighting and scrolling.
        > 
        
        There’s also `grep pattern file`, which finds lines matching `pattern` in `file`. This one deserves slightly more attention as it’s both *very* useful and sports a wider array of features than one may expect. `pattern` is actually a *regular expression* which can express very complex patterns — we’ll cover those in the code quality lecture. You can also specify a directory instead of a file (or leave it off for `.`) and pass `-r` to recursively search all the files in a directory.
        
        > Consider installing and using `ripgrep` over `grep` for a faster and more human-friendly (but less portable) alternative. `ripgrep` will also recursively search the current working directory by default!
        > 
        
        There are also some very useful tools with a slightly more complicated interface. First among those is `sed`, which is a programmatic file editor. It has its own programming language for making automated edits to files, but the most common use of it is:
        
        ```
        missing:~$sed -i 's/pattern/replacement/g' file
        ```
        
        This replaces all instances of `pattern` with `replacement` in `file`. The `-i` indicates that we want the substitutions to happen inline (as opposed to leaving `file` unmodified and printing the substituted contents). The `s/` is the way to express in the sed programming language that we want to do a substitution. The `/` separates the pattern from the replacement. And the trailing `/g` indicates that we want to replace *all* occurrences on each line rather than just the first. As with `grep`, `pattern` here is a regular expression, which gives you significant expressive power. Regular expression substitutions also allow `replacement` to refer back to parts of the matched pattern; we’ll see an example of that in a second.
        
        Next, we have `find`, which lets you find files (recursively) that match certain conditions. For example:
        
        ```
        missing:~$find ~/Downloads -type f -name "*.zip" -mtime +30
        ```
        
        Finds ZIP files in the download directory that are older than 30 days.
        
        ```
        missing:~$find ~ -type f -size +100M -exec ls -lh {} \;
        ```
        
        Finds files larger than 100M in your home directory and lists them. Note that `-exec` takes a *command* terminated with a stand-alone `;` (which we need to escape much like a space) where `{}` is replaced with each matching file path by `find`.
        
        ```
        missing:~$find . -name "*.py" -exec grep -l "TODO" {} \;
        ```
        
        Finds any `.py` files with TODO items in them.
        
        The syntax of `find` can be a little daunting, but hopefully this gives you a sense of how useful it can be!
        
        > Consider installing and using `fd` instead of `find` for a more human-friendly (but less portable!) experience.
        > 
        
        Next on the docket is `awk`, which, like `sed`, has its own programming language. Where `sed` is built for editing files, `awk` is built for parsing them. By far the most common use of `awk` is for data files with a regular syntax (like CSV files) where you want to extract only certain parts of every record (i.e., line):
        
        ```
        missing:~$awk '{print $2}' file
        ```
        
        Prints the second whitespace-separated column of every line of `file`. If you add `-F,`, it’ll print the second comma-separated column of every line. `awk` can do much more — filtering rows, computing aggregates, and more — see the exercises for a taste.
        
        Putting these tools together, we can do fancy things like:
        
        ```
        missing:~$ssh myserver 'journalctl -u sshd -b-1 | grep "Disconnected from"' \
          | sed -E 's/.*Disconnected from .* user (.*) [^ ]+ port.*/\1/' \
          | sort | uniq -c \
          | sort -nk1,1 | tail -n10 \  | awk '{print $2}' | paste -sd,postgres,mysql,oracle,dell,ubuntu,inspur,test,admin,user,root
        ```
        
        This grabs SSH logs from a remote server (we’ll talk more about `ssh` in the next lecture), searches for disconnect messages, extracts the username from each such message, and prints the top 10 usernames comma-separated. All in one command! We’ll leave dissecting each step as an exercise.
        
        ## **The shell language (bash)**
        
        The previous example introduced a new concept: pipes (`|`). These let you string together the output of one program with the input of another. This works because most command-line programs will operate on their “standard input” (where your keystrokes normally go) if no `file` argument is given. `|` takes the “standard output” (what normally gets printed to your terminal) of the program before the `|` and makes it be the standard input of the program after the `|`. This allows you to *compose* shell programs, and it’s part of what makes the shell such a productive environment to work in!
        
        In fact, most shells implement a full programming language (like bash), just like Python or Ruby. It has variables, conditionals, loops, and functions. When you run commands in your shell, you are really writing a small bit of code that your shell interprets. We won’t teach you all of bash today, but there are some bits you’ll find particularly useful:
        
        First, redirects: `>file` lets you take the standard output of a program and write it to `file` instead of to your terminal. This makes it easier to analyze after the fact. `>>file` will append to `file` rather than overwrite it. There’s also `<file` which tells the shell to read from `file` instead of from your keyboard as the standard input to a program.
        
        > This is a good time to mention the `tee` program. `tee` will print standard input to standard output (just like `cat`!), but will *also* write it to a file. So `verbose cmd | tee verbose.log | grep CRITICAL` will preserve the full verbose log to a file while keeping your terminal clean!
        > 
        
        Next, conditionals: `if command1; then command2; command3; fi` will execute `command1`, and if it doesn’t result in an error, will run `command2` and `command3`. You can also have an `else` branch if you wish. The most common command to use as `command1` is the `test` command, often abbreviated simply as `[`, which lets you evaluate conditions like “does a file exist” (`test -f file` / `[ -f file ]`) or “does a string equal another” (`[ "$var" = "string" ]`). In bash, there’s also `[[ ]]`, which is a “safer” built-in version of `test` that has fewer odd behaviours around quoting.
        
        Bash also has two forms of loops, `while` and `for`. `while command1; do command2; command3; done` functions just like the equivalent `if` command, except that it will re-execute the whole thing over and over for as long as `command1` does not error. `for varname in a b c d; do command; done` executes `command` four times, each time with `$varname` set to one of `a`, `b`, `c`, and `d`. Instead of listing the items explicitly, you’ll often use “command substitution”, such as:
        
        ```
        fori in $(seq1 10); do
        ```
        
        This executes the command `seq 1 10` (which prints the numbers from 1 to 10 inclusive) and then replaces the whole `$()` with that command’s output, giving you a 10-iteration for loop. In older code you’ll sometimes see literal backticks (like `for i in `seq 1 10`; do`) instead of `$()`, but you should strongly prefer the `$()` form as it can be nested.
        
        While you *can* write long shell scripts directly in your prompt, you’ll usually want to write them into a `.sh` file instead. For example, here’s a script that will run a program in a loop until it fails, printing the output only of the failed run, while stressing your CPU in the background (useful to reproduce flaky tests for example):
        
        ```
        #!/bin/bash
        set -euo pipefail
        
        # Start CPU stress in background
        stress --cpu 8 &
        STRESS_PID=$!
        
        # Setup log file
        LOGFILE="test_runs_$(date +%s).log"
        echo "Logging to$LOGFILE"
        
        # Run tests until one fails
        RUN=1
        whilecargo testmy_test > "$LOGFILE" 2>&1; doecho "Run$RUN passed"
            ((RUN++))
        done
        
        # Cleanup and report
        kill $STRESS_PID
        echo "Test failed on run$RUN"
        echo "Last 20 lines of output:"
        tail -n 20 "$LOGFILE"
        echo "Full log:$LOGFILE"
        ```
        
        This has a number of new things in it that I recommend you spend some time diving into, as they’re very useful in crafting useful shell invocations like background jobs (`&`) to run programs concurrently, trickier shell redirections, and arithmetic expansion.
        
        It’s worth spending a second on the first two lines of the program though. The first is the “shebang” – you’ll see this at the top of other files than shell scripts too. When a file that starts with the magic incantation `#!/path` is executed, the shell will start the program at `/path`, and pass it the contents of the file as input. In the case of a shell script, this means passing the contents of the shell script to `/bin/bash`, but you can also write Python scripts with a shebang line of `/usr/bin/python`!
        
        The second line is a way to make bash “stricter”, and mitigate a number of footguns when writing shell scripts. `set` can take a whole lot of arguments, but briefly: `-e` makes it so that if any command fails, the script exits early; `-u` makes it so that use of undefined variables crashes the script rather than just using an empty string; and `-o pipefail` makes it so that if programs in a `|` sequence fail, the shell script as a whole also exits early.
        
        > Shell programming is a deep topic, just as any programming language is, but be warned: bash has an unusual number of gotchas, to the point that there are multiple websites dedicated to listing them. I highly recommend making heavy use of shellcheck when writing them. LLMs are also great at writing and debugging shell scripts, as well as translating them to a “real” programming language (like Python) when they’ve grown too unwieldy for bash (100+ lines).
        > 
        
        # **Next steps**
        
        At this point you know your way around a shell enough to accomplish basic tasks. You should be able to navigate around to find files of interest and use the basic functionality of most programs. In the next lecture, we will talk about how to perform and automate more complex tasks using the shell and the many handy command-line programs out there.
        
        # **Exercises**
        
        All classes in this course are accompanied by a series of exercises. Some give you a specific task to do, while others are open-ended, like “try using X and Y programs”. We highly encourage you to try them out.
        
        We have not written solutions for the exercises. If you are stuck on anything in particular, feel free to post in `#missing-semester-forum` on Discord or send us an email describing what you’ve tried so far, and we will try to help you out. These exercises will also likely work well as initial prompts in a conversation with an LLM where you can interactively dive into the topic. The real value in these exercises is the journey of discovering the answers, not the answer itself. We encourage you to follow tangents and ask “why” as you work through them, rather than just looking for the shortest path to the solution.
        
    - exercises
        1. For this course, you need to be using a Unix shell like Bash or ZSH. If you are on Linux or macOS, you don’t have to do anything special. If you are on Windows, you need to make sure you are not running cmd.exe or PowerShell; you can use Windows Subsystem for Linux or a Linux virtual machine to use Unix-style command-line tools. To make sure you’re running an appropriate shell, you can try the command `echo $SHELL`. If it says something like `/bin/bash` or `/usr/bin/zsh`, that means you’re running the right program.
        2. What does the `l` flag to `ls` do? Run `ls -l /` and examine the output. What do the first 10 characters of each line mean? (Hint: `man ls`)
        3. In the command `find ~/Downloads -type f -name "*.zip" -mtime +30`, the `.zip` is a “glob”. What is a glob? Create a test directory with some files and experiment with patterns like `ls *.txt`, `ls file?.txt`, and `ls {a,b,c}.txt`. See Pattern Matching in the Bash manual.
        4. What’s the difference between `'single quotes'`, `"double quotes"`, and `$'ANSI quotes'`? Write a command that echoes a string containing a literal `$`, a `!`, and a newline character. See Quoting.
        5. The shell has three standard streams: stdin (0), stdout (1), and stderr (2). Run `ls /nonexistent /tmp` and redirect stdout to one file and stderr to another. How would you redirect both to the same file? See Redirections.
        6. `$?` holds the exit status of the last command (0 = success). `&&` runs the next command only if the previous succeeded; `||` runs it only if the previous failed. Write a one-liner that creates `/tmp/mydir` only if it doesn’t already exist. See Exit Status.
        7. Why does `cd` have to be built into the shell itself rather than a standalone program? (Hint: think about what a child process can and cannot affect in its parent.)
        8. Write a script that takes a filename as an argument (`$1`) and checks whether the file exists using `test -f` or `[ -f ... ]`. It should print different messages depending on whether the file exists. See Bash Conditional Expressions.
        9. Save the script from the previous exercise to a file (e.g., `check.sh`). Try running it with `./check.sh somefile`. What happens? Now run `chmod +x check.sh` and try again. Why is this step necessary? (Hint: look at `ls -l check.sh` before and after the `chmod`.)
        10. What happens if you add `x` to the `set` flags in a script? Try it with a simple script and observe the output. See The Set Builtin.
        11. Write a command that copies a file to a backup with today’s date in the filename (e.g., `notes.txt` → `notes_2026-01-12.txt`). (Hint: `$(date +%Y-%m-%d)`). See Command Substitution.
        12. Modify the flaky test script from the lecture to accept the test command as an argument instead of hardcoding `cargo test my_test`. (Hint: `$1` or `$@`). See Special Parameters.
        13. Use pipes to find the 5 most common file extensions in your home directory. (Hint: combine `find`, `grep` or `sed` or `awk`, `sort`, `uniq -c`, and `head`.)
        14. `xargs` converts lines from stdin into command arguments. Use `find` and `xargs` together (not `find -exec`) to find all `.sh` files in a directory and count the lines in each with `wc -l`. Bonus: make it handle filenames with spaces. (Hint: `print0` and `0`). See `man xargs`.
        15. Use `curl` to fetch the HTML of the course website (`https://missing.csail.mit.edu/`) and pipe it to `grep` to count how many lectures are listed. (Hint: look for a pattern that appears once per lecture; use `curl -s` to silence the progress output.)
        16. `jq` is a powerful tool for processing JSON data. Fetch the sample data at `https://microsoftedge.github.io/Demos/json-dummy-data/64KB.json` with `curl` and use `jq` to extract just the names of people whose version is greater than 6. (Hint: pipe to `jq .` first to see the structure; then try `jq '.[] | select(...) | .name'`)
        17. `awk` can filter lines based on column values and manipulate output. For example, `awk '$3 ~ /pattern/ {$4=""; print}'` prints only lines where the third column matches `pattern`, while omitting the fourth column. Write an `awk` command that prints only lines where the second column is greater than 100, and swaps the first and third columns. Test with: `printf 'a 50 x\nb 150 y\nc 200 z\n'`
        18. Dissect the SSH log pipeline from the lecture: what does each step do? Then build something similar to find your most-used shell commands from `~/.bash_history` (or `~/.zsh_history`).
    
    https://missing.csail.mit.edu/2026/course-shell/
    
- topic 2: command-line environment
    - notetaking
        
        ### Arguments
        
        input&output of program usually very clear, but not shell scripts
        
        !image.png
        
        !image.png
        
        ‘program name’, arguments
        
        flags : arguments with - or — → options, usually order doesn’t matter, can be combined (-al)
        
        *** shell does not offer these features. program parses.
        
        *** globs are not arguments.
        
        !image.png
        
        !image.png
        
        !image.png
        
        !image.png
        
        Z shell, not Bourne-again shell → more complicated globs
        
        !image.png
        
        ### Streams
        
        in pipelines, we are actually running all these programs in parallel.
        
        !image.png
        
        !image.png
        
        not suddenly 13579.
        
        !image.png
        
        !image.png
        
        - : stdin, get input from pipeline (can be omitted)
        
        actually we have 2 outputs: standard output stream (stdout), standard input stream (stderr)
        
        !image.png
        
        !image.png
        
        use /dev/null to abandoning
        
        ### Environment Variables
        
        !image.png
        
        !image.png
        
        !image.png
        
        other shell cannot access DEBUG since it’s local variable
        
        !image.png
        
        environment variable ← useful because convention to name of varables (ex HOME TZ=ASIA/TOKYO)
        
        !image.png
        
        by export, children shells & succeeding processes can use environmental variable without reference
        
        ### Return Codes
        
        signal which indicates that the run was successful or not.
        
        0 → success,  others → error
        
        !image.png
        
        most of the operators in the shell language will rely on return code. (ex &&, || …)
        
        ### Signals
        
        a type of software interrupts. the shell is sending a signal to the program with a specific code. if the program has a way to deal with it, it will run that code, else exit.
        
        !image.png
        
        signal.singal() → interrupt
        
        !image.png
        
        SIGINT: ctrl + C, SIGQUIT: ctrl + backslash, SIGKILL, etc.
        
        !image.png
        
        trap ⇒ signal SIGINT or SIGTERM → cleanup
        
        SIGTSTP: ctrl + Z ⇒ pause program (jobs ⇒ suspended program, fg ⇒ continue)
        
        !image.png
        
        kill -SIGCONT ⇒ run program at background, not terminal (can write terminal codes)
        
        ### Remote machines
        
        !image.png
        
        IP ⇒ remote server
        
        SSH keys ⇒ public key & private key
        
        !image.png
        
        !image.png
        
        public key : show others who the user is ( id_ed25519.pub )
        
        !image.png
        
        private key : only in computer, never spoil
        
        !image.png
        
        !image.png
        
        ⇒ interactive sessions, executing commands
        
        !image.png
        
        wc is running in the local computer
        
        !image.png
        
        wc is running in the remote server
        
        !image.png
        
        scp ⇒ copy file local to remote
        
        !image.png
        
        but cannot do anything else in remote machine
        
        challange: many things running in parallel
        
        ### Terminal Multiplexer
        
        tmux ⇒ program that makes easy to run many other programs within the same environment.
        
        !image.png
        
        create windows ( ctrl + B, released by other key, C to create window, 0 to go to window number 0, D for detouch )
        
        if user disconnects during program, shell sends a special type of signal called the hangup signal “SIGHUP”, kill all the processes that were running.
        
        tmux decides to capture that signal and actually doesn’t propagate it. So if user connects to the server again and does tmux attach, everything is still running.
        
        ⇒ not tied to the connection between the two servers.
        
        ### Customizing the Shell
        
        !image.png
        
        path update is not persisted when reconnecting
        
        bashrc or bash_profile ⇒ whenever a shell process is created, shell reads this file
        
        !image.png
        
        in practice, people upload such plug-ins as dot file to online.
        
        actually bashrc could be not file ← symlinks: a notion in many oss which is whenever anyone tries to read this file just go somewhere else, read other file 
        
        ( .bashrc → .dotfiles/bash/.bashrc )
        
        autocomplete, etc. ← not built into the shell but it can be convenient
        
        ### AI tool in the Shell
        
        CLI tools ⇒ interact with AI
        
        !image.png
        
        !image.png
        
        claude ⇒ shell program but pl is english
        
        !image.png
        
        !image.png
        
        !image.png
        
        ### Terminal Emulator
        
        :GUI program that is running the shell and just presenting it in our computer.
        
    - lecture slides
        
        As we covered in the previous lecture, most shells are not a mere launcher to start up other programs, but in practice they provide an entire programming language full of common patterns and abstractions. However, unlike the majority of programming languages, in shell scripting everything is designed around running programs and getting them to communicate with each other simply and efficiently.
        
        In particular, shell scripting is tightly bound by *conventions*. For a command line interface (CLI) program to play nicely within the broader shell environment there are some common patterns that it needs to follow. We will now cover many of the concepts required to understand how command line programs work as well as ubiquitous conventions on how to use and configure them.
        
        # **The Command Line Interface**
        
        Writing a function in most programming languages looks something like:
        
        ```
        def add(x: int, y: int) -> int:
            return x + y
        ```
        
        Here we can explicitly see the inputs and the outputs of the program. In contrast, shell scripts can look quite different at first glance.
        
        ```
        #!/usr/bin/env bash
        
        if [[ -f $1 ]]; thenecho "Target file already exists"
            exit1
        else
            if $DEBUG; thengrep 'error' - | tee $1
            elsegrep 'error' - > $1
            fiexit0
        fi
        ```
        
        To properly understand what is going in scripts like this one we first need to introduce a few concepts that appear often when shell programs communicate with each other or with the shell environment:
        
        - Arguments
        - Streams
        - Environment variables
        - Return codes
        - Signals
        
        ## **Arguments**
        
        Shell programs receive a list of arguments when they are executed. Arguments are plain strings in shell, and it is up to the program how to interpret them. For instance when we do `ls -l folder/`, we are executing the program `/bin/ls` with arguments `['-l', 'folder/']`.
        
        From within a shell script we access these via special shell syntax. To access the first argument we access the variable `$1`, second argument `$2` and so on and so forth until `$9`. To access all arguments as a list we use `$@` and to retrieve the number of arguments `$#`. Additionally we can also access the name of the program with `$0`.
        
        For most programs the arguments will consist of a mixture of *flags* and regular strings. Flags can be identified because they are preceded by a dash (`-`) or double-dash (`--`). Flags are usually optional and their role is to modify the behavior of the program. For example `ls -l` changes how `ls` formats its output.
        
        You will see double dash flags with long names like `--all`, and single dash flags like `-a`, which are most often followed by a single letter. The same option might be specified in both formats, `ls -a` and `ls --all` are equivalent. Single dash flags are often grouped, so `ls -l -a` and `ls -la` are also equivalent. The order of flags usually doesn’t matter either, `ls -la` and `ls -al` produce the same result. Some flags are quite prevalent and as you get more familiar with the shell environment you’ll intuitively reach for them, for example (`--help`, `--verbose`, `--version`).
        
        > Flags are a first good example of shell conventions. The shell language does not require that our program uses `-` or `--` in this particular way. Nothing prevents us from writing a program with syntax `myprogram +myoption myfile`, but it would lead to confusion since the expectation is that we use dashes. In practice, most programming languages provide CLI flag parsing libraries (e.g. `argparse` in python to parse arguments with the dash syntax).
        > 
        
        Another common convention in CLI programs is for programs to accept a variable number of arguments of the same type. When given arguments in this way the command performs the same operation on each one of them.
        
        ```
        mkdirsrc
        mkdirdocs
        # is equivalent to
        mkdirsrc docs
        ```
        
        This syntax sugar might seem unnecessary at first, but it becomes really powerful when combined with *globbing*. Globbing or globs are special patterns that the shell will expand before calling the program.
        
        Say we wanted to delete all .py files in the current folder nonrecursively. From what we learned in the previous lecture we could achieve this by running
        
        ```
        forfile in $(ls | grep -P '\.py$'); dorm "$file"
        done
        ```
        
        But we can replace that with just `rm *.py`!
        
        When we type `rm *.py` into the terminal, the shell will not call the `/bin/rm` program with arguments `['*.py']`. Instead, the shell will search for files in the current folder matching the pattern `*.py` where `*` can match any string of zero or more characters of any type. So if our folder has `main.py` and `utils.py` then the `rm` program will receive arguments `['main.py', 'utils.py']`.
        
        The most common globs you will find are wildcards `*` (zero or more of anything), `?` (exactly one of anything) and curly braces. Curly braces `{}` expand a comma-separated list of patterns into multiple arguments.
        
        In practice, globs are best understood with motivating examples.
        
        ```
        touchfolder/{a,b,c}.py
        # Will expand to
        touchfolder/a.py folder/b.py folder/c.py
        
        convert image.{png,jpg}
        # Will expand to
        convert image.png image.jpg
        
        cp /path/to/project/{setup,build,deploy}.sh /newpath
        # Will expand to
        cp /path/to/project/setup.sh /path/to/project/build.sh /path/to/project/deploy.sh /newpath
        
        # Globbing techniques can also be combined
        mv *{.py,.sh} folder
        # Will move all *.py and *.sh files
        ```
        
        > Some shells (e.g. zsh) support even more advanced forms of globbing such as `**` that will expand to include recursive paths. So `rm **/*.py` will delete all .py files recursively.
        > 
        
        ## **Streams**
        
        Whenever we execute a program pipeline like
        
        ```
        catmyfile | grep -P '\d+' | uniq -c
        ```
        
        we see that the `grep` program is communicating with both the `cat` and `uniq` programs.
        
        An important observation here is that all three programs are executing at once. Namely, the shell is not first calling cat, then grep, and then uniq. Instead, all three programs are being spawned and the shell is connecting the output of cat to the input of grep and the output of grep to the input of uniq. When using the pipe operator `|`, the shell operates on streams of data that flow from one program to the next in the chain.
        
        We can demonstrate this concurrency, all commands in a pipeline start immediately:
        
        ```
        $(sleep15 && catnumbers.txt) | grep -P '^\d$' | sort | uniq  &
        [1] 12345$ps | grep -P '(sleep|cat|grep|sort|uniq)'
          32930 pts/1    00:00:00 sleep
          32931 pts/1    00:00:00 grep
          32932 pts/1    00:00:00 sort
          32933 pts/1    00:00:00 uniq
          32948 pts/1    00:00:00 grep
        ```
        
        We can see that all processes but `cat` are running right away. The shell spawns all processes and connects their streams before any of them finish. `cat` will only get started once sleep finishes, and the output of `cat` will be sent to grep and so on and so forth.
        
        Every program has an input stream, labeled stdin (for standard input). When piping, stdin is connected automatically. Within a script, many programs accept `-` as a filename to mean “read from stdin”:
        
        ```
        # These are equivalent when data comes from a pipe
        echo "hello" | grep "hello"
        echo "hello" | grep "hello" -
        ```
        
        Similarly, every program has two output streams: stdout and stderr. The standard output is the one most commonly encountered and it is the one that is used for piping the output of the program to the next command in the pipeline. The standard error is an alternative stream that is intended for programs to report warnings and other types of issues, without that output getting parsed by the next command in the chain.
        
        ```
        $ls /nonexistent
        ls: cannot access '/nonexistent': No such file or directory$ls /nonexistent | grep "pattern"
        ls: cannot access '/nonexistent': No such file or directory#The error message still appears because stderr is not piped
        $ls /nonexistent 2>/dev/null
        #No output - stderr was redirected to /dev/null
        ```
        
        The shell provides syntax for redirecting these streams. Here are some illustrative examples.
        
        ```
        # Redirect stdout to a file (overwrite)
        echo "hello" > output.txt
        
        # Redirect stdout to a file (append)
        echo "world" >> output.txt
        
        # Redirect stderr to a file
        lsfoobar 2> errors.txt
        
        # Redirect both stdout and stderr to the same file
        lsfoobar &> all_output.txt
        
        # Redirect stdin from a file
        grep "pattern" < input.txt
        
        # Discard output by redirecting to /dev/null
        cmd > /dev/null 2>&1
        ```
        
        Another powerful tool that exemplifies the Unix philosophy is `fzf`, a fuzzy finder. It reads lines from stdin and provides an interactive interface to filter and select:
        
        ```
        $ls | fzf
        $cat ~/.bash_history | fzf
        ```
        
        `fzf` can be integrated with many shell operations. We’ll see more uses of it when we discuss shell customization.
        
        ## **Environment variables**
        
        To assign variables in bash we use the syntax `foo=bar`, and then access the value of the variable with the `$foo` syntax. Note that `foo = bar` is invalid syntax as the shell will parse it as calling the program `foo` with arguments `['=', 'bar']`. In shell scripting the role of the space character is to perform argument splitting. This behavior can be confusing and tricky to get used to, so keep it in mind.
        
        Shell variables do not have types, they are all strings. Note that when writing string expressions in the shell single and double quotes are not interchangeable. Strings delimited with `'` are literal strings and will not expand variables, perform command substitution, or process escape sequences, whereas `"` delimited strings will.
        
        ```
        foo=bar
        echo "$foo"
        # prints bar
        echo '$foo'
        # prints $foo
        ```
        
        To capture the output of a command into a variable we use *command substitution*. When we execute
        
        ```
        files=$(ls)
        echo "$files" | grepREADME
        echo "$files" | grep ".py"
        ```
        
        the output (concretely the stdout) of ls is placed into the variable `$files` which we can access later. The content of the `$files` variable does include the newlines from the ls output, which is how programs like `grep` know to operate on each item independently.
        
        A lesser known similar feature is *process substitution*, `<( CMD )` will execute `CMD` and place the output in a temporary file and substitute the `<()` with that file’s name. This is useful when commands expect values to be passed by file instead of by STDIN. For example, `diff <(ls src) <(ls docs)` will show differences between files in dirs `src` and `docs`.
        
        Whenever a shell program calls another program it passes along a set of variables that are often referred to as *environment variables*. From within a shell we can find the current environment variables by running `printenv`. To pass an environment variable explicitly we can prepend a command with a variable assignment
        
        > Environment variables are conventionally written in ALL_CAPS (e.g., `HOME`, `PATH`, `DEBUG`). This is a convention, not a technical requirement, but following it helps distinguish environment variables from local shell variables which are typically lowercase.
        > 
        
        ```
        TZ=Asia/Tokyo date  # prints the current time in Tokyo
        echo $TZ  # this will be empty, since TZ was only set for the child command
        ```
        
        Alternatively, we can use the `export` built-in function that will modify our current environment and thus all child processes will inherit the variable:
        
        ```
        exportDEBUG=1
        # All programs from this point onwards will have DEBUG=1 in their environment
        bash -c 'echo $DEBUG'
        # prints 1
        ```
        
        To delete a variable use the `unset` built-in command, e.g. `unset DEBUG`.
        
        > Environment variables are another shell convention. They can be used to modify the behavior of many programs implicitly rather than explicitly. For example, the shell sets the `$HOME` environment variable with the path of the home folder of the current user. Then programs can access this variable to get this information instead of requiring an explicit `--home /home/alice`. Another common example is `$TZ`, which many programs use to format dates and times according to the specified timezone.
        > 
        
        ## **Return codes**
        
        As we saw earlier, the main output of a shell program is conveyed through the stdout/stderr streams and filesystem side effects.
        
        By default a shell script will return exit code zero. The convention is that zero means everything went well whereas nonzero means some issues were encountered. To return a nonzero exit code we have to use the `exit NUM` shell built-in. We can access the return code of the last command that was run by accessing the special variable `$?`.
        
        The shell has boolean operators `&&` and `||` for performing AND and OR operations respectively. Unlike those encountered in regular programming languages, the ones in the shell operate on the return code of programs. Both of these are short-circuiting operators. This means that they can be used to conditionally run commands based on the success or failure of previous commands, where success is determined based on whether the return code is zero or not. Some examples:
        
        ```
        # echo will only run if grep succeeds (finds a match)
        grep -q "pattern" file.txt && echo "Pattern found"
        
        # echo will only run if grep fails (no match)
        grep -q "pattern" file.txt || echo "Pattern not found"
        
        # true is a shell program that always succeeds
        true && echo "This will always print"
        
        # and false is a shell program that always fails
        false || echo "This will always print"
        ```
        
        The same principle applies to `if` and `while` statements, they both use return codes to make decisions:
        
        ```
        # if uses the return code of the condition command (0 = true, nonzero = false)
        ifgrep -q "pattern" file.txt; thenecho "Found"
        fi
        
        # while loops continue as long as the command returns 0
        whilereadline; doecho "$line"
        done < file.txt
        ```
        
        ## **Signals**
        
        In some cases you will need to interrupt a program while it is executing, for instance if a command is taking too long to complete. The simplest way to interrupt a program is to press `Ctrl-C` and the command will probably stop. But how does this actually work and why does it sometimes fail to stop the process?
        
        ```
        $sleep100
        ^C$
        ```
        
        > Note, here `^C` is how `Ctrl-C` is displayed when typed in the terminal.
        > 
        
        Under the hood, what happened here is the following:
        
        1. We pressed `Ctrl-C`
        2. The shell identified the special combination of characters
        3. The shell process sent a SIGINT signal to the `sleep` process
        4. The signal interrupted the execution of the `sleep` process
        
        Signals are a special communication mechanism. When a process receives a signal it stops its execution, deals with the signal and potentially changes the flow of execution based on the information that the signal delivered. For this reason, signals are *software interrupts*.
        
        In our case, when typing `Ctrl-C` this prompts the shell to deliver a `SIGINT` signal to the process. Here’s a minimal example of a Python program that captures `SIGINT` and ignores it, no longer stopping. To kill this program we can now use the `SIGQUIT` signal instead, by typing `Ctrl-\`.
        
        ```
        #!/usr/bin/env pythonimport signal, time
        
        def handler(signum, time):
            print("\nI got a SIGINT, but I am not stopping")
        
        signal.signal(signal.SIGINT, handler)
        i = 0
        while True:
            time.sleep(.1)
            print("\r{}".format(i), end="")
            i += 1
        ```
        
        Here’s what happens if we send `SIGINT` twice to this program, followed by `SIGQUIT`. Note that `^` is how `Ctrl` is displayed when typed in the terminal.
        
        ```
        $python sigint.py
        24^C
        I got a SIGINT, but I am not stopping
        26^C
        I got a SIGINT, but I am not stopping
        30^\[1]    39913 quit       python sigint.py
        ```
        
        While `SIGINT` and `SIGQUIT` are both usually associated with terminal related requests, a more generic signal for asking a process to exit gracefully is the `SIGTERM` signal. To send this signal we can use the `kill` command, with the syntax `kill -TERM <PID>`.
        
        Signals can do other things beyond killing a process. For instance, `SIGSTOP` pauses a process. In the terminal, typing `Ctrl-Z` will prompt the shell to send a `SIGTSTP` signal, short for Terminal Stop (i.e. the terminal’s version of `SIGSTOP`).
        
        We can then continue the paused job in the foreground or in the background using `fg` or `bg`, respectively.
        
        The `jobs` command lists the unfinished jobs associated with the current terminal session. You can refer to those jobs using their pid (you can use `pgrep` to find that out). More intuitively, you can also refer to a process using the percent symbol followed by its job number (displayed by `jobs`). To refer to the last backgrounded job you can use the `$!` special parameter.
        
        One more thing to know is that the `&` suffix in a command will run the command in the background, giving you the prompt back, although it will still use the shell’s STDOUT which can be annoying (use shell redirections in that case). Equivalently, to background an already running program you can do `Ctrl-Z` followed by `bg`.
        
        Note that backgrounded processes are still children processes of your terminal and will die if you close the terminal (this will send yet another signal, `SIGHUP`). To prevent that from happening you can run the program with `nohup` (a wrapper to ignore `SIGHUP`), or use `disown` if the process has already been started. Alternatively, you can use a terminal multiplexer as we will see in the next section.
        
        Below is a sample session to showcase some of these concepts.
        
        ```
        $ sleep 1000
        ^Z
        [1]  + 18653 suspended  sleep 1000
        
        $ nohup sleep 2000 &
        [2] 18745
        appending output to nohup.out
        
        $ jobs
        [1]  + suspended  sleep 1000
        [2]  - running    nohup sleep 2000
        
        $ kill -SIGHUP %1
        [1]  + 18653 hangup     sleep 1000
        
        $ kill -SIGHUP %2   # nohup protects from SIGHUP
        
        $ jobs
        [2]  + running    nohup sleep 2000
        
        $ kill %2
        [2]  + 18745 terminated  nohup sleep 2000
        ```
        
        A special signal is `SIGKILL` since it cannot be captured by the process and it will always terminate it immediately. However, it can have bad side effects such as leaving orphaned children processes.
        
        You can learn more about these and other signals here) or typing `man signal` or `kill -l`.
        
        Within shell scripts, you can use the `trap` built-in to execute commands when signals are received. This is useful for cleanup operations:
        
        ```
        #!/usr/bin/env bash
        cleanup() {
            echo "Cleaning up temporary files..."
            rm -f /tmp/mytemp.*
        }
        trapcleanup EXIT  # Run cleanup when script exits
        trapcleanup SIGINT SIGTERM  # Also on Ctrl-C or kill
        ```
        
        # **Remote Machines**
        
        It has become more and more common for programmers to work with remote servers in their everyday work. The most common tool for the job here is SSH (Secure Shell) which will help us connect to a remote server and provide the now familiar shell interface. We connect to a server with a command like:
        
        ```
        ssh alice@server.mit.edu
        ```
        
        Here we are trying to ssh as user `alice` in server `server.mit.edu`.
        
        An often overlooked feature of `ssh` is the ability to run commands non-interactively. `ssh` correctly handles sending the stdin and receiving the stdout of the command, so we can combine it with other commands
        
        ```
        # here ls runs in the remote, and wc runs locally
        ssh alice@server ls | wc -l
        
        # here both ls and wc run in the server
        ssh alice@server 'ls | wc -l'
        ```
        
        > Try installing Mosh as a SSH replacement that can handle disconnections, entering/exiting sleep, changing networks and dealing with high latency links.
        > 
        
        For `ssh` to let us run commands in the remote server we need to prove that we are authorized to do so. We can do this via passwords or ssh keys. Key-based authentication utilizes public-key cryptography to prove to the server that the client owns the secret private key without revealing the key. Key based authentication is both more convenient and more secure, so you should prefer it. Note that the private key (often `~/.ssh/id_rsa` and more recently `~/.ssh/id_ed25519`) is effectively your password, so treat it like so and never share its contents.
        
        To generate a pair you can run `ssh-keygen`.
        
        ```
        ssh-keygen -a 100 -t ed25519 -f ~/.ssh/id_ed25519
        ```
        
        If you have ever configured pushing to GitHub using SSH keys, then you have probably done the steps outlined here and have a valid key pair already. To check if you have a passphrase and validate it you can run `ssh-keygen -y -f /path/to/key`.
        
        At the server side `ssh` will look into `.ssh/authorized_keys` to determine which clients it should let in. To copy a public key over you can use:
        
        ```
        cat .ssh/id_ed25519.pub | ssh alice@remote 'cat >> ~/.ssh/authorized_keys'
        
        # or more simply (if ssh-copy-id is available)
        
        ssh-copy-id -i .ssh/id_ed25519 alice@remote
        ```
        
        Beyond running commands, the connection that ssh establishes can be used to transfer files from and to the server securely. `scp` is the most traditional tool and the syntax is `scp path/to/local_file remote_host:path/to/remote_file`. `rsync` improves upon `scp` by detecting identical files in local and remote, and preventing copying them again. It also provides more fine grained control over symlinks, permissions and has extra features like the `--partial` flag that can resume from a previously interrupted copy. `rsync` has a similar syntax to `scp`.
        
        SSH client configuration is located at `~/.ssh/config` and it lets us declare hosts and set default settings for them. This configuration file is not just read by `ssh` but also other programs like `scp`, `rsync`, `mosh`, &c.
        
        ```
        Host vm
            User alice
            HostName 172.16.174.141
            Port 2222
            IdentityFile ~/.ssh/id_ed25519
        
        # Configs can also take wildcards
        Host *.mit.edu
            User alice
        ```
        
        # **Terminal Multiplexers**
        
        When using the command line interface you will often want to run more than one thing at once. For instance, you might want to run your editor and your program side by side. Although this can be achieved by opening new terminal windows, using a terminal multiplexer is a more versatile solution.
        
        Terminal multiplexers like `tmux` allow you to multiplex terminal windows using panes and tabs so you can interact with multiple shell sessions in an efficient manner. Moreover, terminal multiplexers let you detach a current terminal session and reattach at some point later in time. Because of this, terminal multiplexers are really convenient when working with remote machines, as it avoids the need to use `nohup` and similar tricks.
        
        The most popular terminal multiplexer these days is `tmux`. `tmux` is highly configurable and by using the associated keybindings you can create multiple tabs and panes and quickly navigate through them.
        
        `tmux` expects you to know its keybindings, and they all have the form `<C-b> x` where that means (1) press `Ctrl+b`, (2) release `Ctrl+b`, and then (3) press `x`. `tmux` has the following hierarchy of objects:
        
        - **Sessions** - a session is an independent workspace with one or more windows
            - `tmux` starts a new session.
            - `tmux new -s NAME` starts it with that name.
            - `tmux ls` lists the current sessions
            - Within `tmux` typing `<C-b> d` detaches the current session
            - `tmux a` attaches the last session. You can use `t` flag to specify which
        - **Windows** - Equivalent to tabs in editors or browsers, they are visually separate parts of the same session
            - `<C-b> c` Creates a new window. To close it you can just terminate the shells doing `<C-d>`
            - `<C-b> N` Go to the *N* th window. Note they are numbered
            - `<C-b> p` Goes to the previous window
            - `<C-b> n` Goes to the next window
            - `<C-b> ,` Rename the current window
            - `<C-b> w` List current windows
        - **Panes** - Like vim splits, panes let you have multiple shells in the same visual display.
            - `<C-b> "` Split the current pane horizontally
            - `<C-b> %` Split the current pane vertically
            - `<C-b> <direction>` Move to the pane in the specified *direction*. Direction here means arrow keys.
            - `<C-b> z` Toggle zoom for the current pane
            - `<C-b> ` Start scrollback. You can then press `<space>` to start a selection and `<enter>` to copy that selection.
            - `<C-b> <space>` Cycle through pane arrangements.
        
        > To learn more about tmux, consider reading [this quick tutorial and this more detailed explanation.
        > 
        
        With tmux and SSH in your toolkit, you’ll want to make your environment feel like home on any machine. That’s where shell customization comes in.
        
        # **Customizing the Shell**
        
        A wide array of command line programs are configured using plain-text files known as *dotfiles* (because the file names begin with a `.`, e.g. `~/.vimrc`, so that they are hidden in the directory listing `ls` by default).
        
        > Dotfiles are yet another shell convention. The dot in the front is to “hide” them when listing (yes, another convention).
        > 
        
        Shells are one example of programs configured with such files. On startup, your shell will read many files to load its configuration. Depending on the shell and whether you are starting a login and/or interactive session, the entire process can be quite complex. Here is an excellent resource on the topic.
        
        For `bash`, editing your `.bashrc` or `.bash_profile` will work in most systems. Some other examples of tools that can be configured through dotfiles are:
        
        - `bash` - `~/.bashrc`, `~/.bash_profile`
        - `git` - `~/.gitconfig`
        - `vim` - `~/.vimrc` and the `~/.vim` folder
        - `ssh` - `~/.ssh/config`
        - `tmux` - `~/.tmux.conf`
        
        A common configuration change is adding new locations for the shell to find programs. You will encounter this pattern when installing software:
        
        ```
        exportPATH="$PATH:path/to/append"
        ```
        
        Here, we are telling the shell to set the value of the $PATH variable to its current value plus a new path, and have all children processes inherit this new value for PATH. This will allow children processes to find programs located under `path/to/append`.
        
        Customizing your shell often means installing new command-line tools. Package managers make this easy. They handle downloading, installing, and updating software. Different operating systems have different package managers: macOS uses Homebrew, Ubuntu/Debian use `apt`, Fedora uses `dnf`, and Arch uses `pacman`. We’ll cover package managers in more depth in the shipping code lecture.
        
        Here’s how to install two useful tools using Homebrew on macOS:
        
        ```
        # ripgrep: a faster grep with better defaults
        brew installripgrep
        
        # fd: a faster, user-friendly find
        brew installfd
        ```
        
        With these installed, you can use `rg` instead of `grep` and `fd` instead of `find`.
        
        > **Warning about `curl | bash`**: You’ll often see installation instructions like `curl -fsSL https://example.com/install.sh | bash`. This pattern downloads a script and immediately executes it, which is convenient but risky; you’re running code you haven’t inspected. A safer approach is to download first, review, then execute:
        > 
        > 
        > ```
        > curl -fsSL https://example.com/install.sh -o install.sh
        > less install.sh  # review the script
        > bash install.sh
        > ```
        > 
        > Some installers use a slightly safer variant: `/bin/bash -c "$(curl -fsSL https://url)"` which at least ensures bash interprets the script rather than your current shell.
        > 
        
        When you try to run a command that isn’t installed, your shell will show `command not found`. The website command-not-found.com is a helpful resource you can use to search for any command to find out how to install it across different package managers and distributions.
        
        Another useful tool is `tldr`, which provides simplified, example-focused man pages. Instead of reading through lengthy documentation, you can quickly see common usage patterns:
        
        ```
        $tldr fd
          An alternative to find.
          Aims to be faster and easier to use than find.
        
          Recursively find files matching a pattern in the current directory:
              fd "pattern"
        
          Find files that begin with "foo":
              fd "^foo"
        
          Find files with a specific extension:
              fd --extension txt
        ```
        
        Sometimes you don’t need a whole new program, but rather just a shortcut for an existing command with specific flags. That’s where aliases come in.
        
        We can also create our own command aliases using the `alias` shell built-in. A shell alias is a short form for another command that your shell will replace automatically before evaluating the expression. For instance, an alias in bash has the following structure:
        
        ```
        aliasalias_name="command_to_alias arg1 arg2"
        ```
        
        > Note that there is no space around the equal sign `=`, because `alias` is a shell command that takes a single argument.
        > 
        
        Aliases have many convenient features:
        
        ```
        # Make shorthands for common flags
        aliasll="ls -lh"
        
        # Save a lot of typing for common commands
        aliasgs="git status"
        aliasgc="git commit"
        
        # Save you from mistyping
        aliassl=ls
        
        # Overwrite existing commands for better defaults
        alias mv="mv -i"           # -i prompts before overwrite
        alias mkdir="mkdir -p"     # -p make parent dirs as needed
        alias df="df -h"           # -h prints human readable format
        
        # Alias can be composed
        aliasla="ls -A"
        aliaslla="la -l"
        
        # To ignore an alias run it prepended with \
        \ls
        # Or disable an alias altogether with unalias
        unaliasla
        
        # To get an alias definition just call it with alias
        aliasll
        # Will print ll='ls -lh'
        ```
        
        Aliases have limitations: they cannot take arguments in the middle of a command. For more complex behavior, you should use shell functions instead.
        
        Most shells support `Ctrl-R` for reverse history search. Type `Ctrl-R` and start typing to search through previous commands. Earlier we introduced `fzf` as a fuzzy finder; with fzf’s shell integration configured, `Ctrl-R` becomes an interactive fuzzy search through your entire history, far more powerful than the default.
        
        How should you organize your dotfiles? They should be in their own folder, under version control, and **symlinked** into place using a script. This has the benefits of:
        
        - **Easy installation**: if you log in to a new machine, applying your customizations will only take a minute.
        - **Portability**: your tools will work the same way everywhere.
        - **Synchronization**: you can update your dotfiles anywhere and keep them all in sync.
        - **Change tracking**: you’re probably going to be maintaining your dotfiles for your entire programming career, and version history is nice to have for long-lived projects.
        
        What should you put in your dotfiles? You can learn about your tool’s settings by reading online documentation or man pages. Another great way is to search the internet for blog posts about specific programs, where authors will tell you about their preferred customizations. Yet another way to learn about customizations is to look through other people’s dotfiles: you can find tons of dotfiles repositories on GitHub — see the most popular one here (we advise you not to blindly copy configurations though). Here is another good resource on the topic.
        
        All of the class instructors have their dotfiles publicly accessible on GitHub: Anish, Jon, Jose.
        
        **Frameworks and plugins** can improve your shell as well. Some popular general frameworks are prezto or oh-my-zsh, and smaller plugins that focus on specific features:
        
        - zsh-syntax-highlighting - colors valid/invalid commands as you type
        - zsh-autosuggestions - suggests commands from history as you type
        - zsh-completions - additional completion definitions
        - zsh-history-substring-search - fish-like history search
        - powerlevel10k - fast, customizable prompt theme
        
        Shells like fish include many of these features by default.
        
        > You don’t need a massive framework like oh-my-zsh to get these features. Installing individual plugins is often faster and gives you more control. Large frameworks can significantly slow down shell startup time, so consider installing only what you actually use.
        > 
        
        # **AI in the Shell**
        
        There are many ways to incorporate AI tooling in the shell. Here are a few examples at different levels of integration:
        
        **Command generation**: Tools like `simonw/llm` can help generate shell commands from natural language descriptions:
        
        ```
        $llm cmd "find all python files modified in the last week"
        find . -name "*.py" -mtime -7
        ```
        
        **Pipeline integration**: LLMs can be integrated into shell pipelines to process and transform data. They’re particularly useful when you need to extract information from inconsistent formats where regex would be painful:
        
        ```
        $catusers.txt
        Contact: john.doe@example.com
        User 'alice_smith' logged in at 3pm
        Posted by: @bob_jones on Twitter
        Author: Jane Doe (jdoe)
        Message from mike_wilson yesterday
        Submitted by user: sarah.connor$INSTRUCTIONS="Extract just the username from each line, one per line, nothing else"
        $llm "$INSTRUCTIONS" < users.txt
        john.doe
        alice_smith
        bob_jones
        jdoe
        mike_wilson
        sarah.connor
        ```
        
        Note how we use `"$INSTRUCTIONS"` (quoted) because the variable contains spaces, and `< users.txt` to redirect the file’s content to stdin.
        
        **AI shells**: Tools like Claude Code act as a meta-shell that accepts English commands and translates them into shell operations, file edits, and more complex multi-step tasks.
        
        # **Terminal Emulators**
        
        Along with customizing your shell, it is worth spending some time figuring out your choice of **terminal emulator** and its settings. A terminal emulator is a GUI program that provides the text-based interface where your shell runs. There are many terminal emulators out there.
        
        Since you might be spending hundreds to thousands of hours in your terminal it pays off to look into its settings. Some of the aspects that you may want to modify in your terminal include:
        
        - Font choice
        - Color Scheme
        - Keyboard shortcuts
        - Tab/Pane support
        - Scrollback configuration
        - Performance (some newer terminals like Alacritty or Ghostty offer GPU acceleration).
    - exercises
        
        ## **Arguments and Globs**
        
        1. You might see commands like `cmd --flag -- --notaflag`. The `-` is a special argument that tells the program to stop parsing flags. Everything after `-` is treated as a positional argument. Why might this be useful? Try running `touch -- -myfile` and then removing it without `-`.
        2. Read `man ls` and write an `ls` command that lists files in the following manner:
            - Includes all files, including hidden files
            - Sizes are listed in human readable format (e.g. 454M instead of 454279954)
            - Files are ordered by recency
            - Output is colorized
            
            A sample output would look like this:
            
            ```
             -rw-r--r--   1 user group 1.1M Jan 14 09:53 baz
             drwxr-xr-x   5 user group  160 Jan 14 09:53 .
             -rw-r--r--   1 user group  514 Jan 14 06:42 bar
             -rw-r--r--   1 user group 106M Jan 13 12:12 foo
             drwx------+ 47 user group 1.5K Jan 12 18:08 ..
            ```
            
        3. Process substitution `<(command)` lets you use a command’s output as if it were a file. Use `diff` with process substitution to compare the output of `printenv` and `export`. Why are they different? (Hint: try `diff <(printenv | sort) <(export | sort)`).
        
        ## **Environment Variables**
        
        1. Write bash functions `marco` and `polo` that do the following: whenever you execute `marco` the current working directory should be saved in some manner, then when you execute `polo`, no matter what directory you are in, `polo` should `cd` you back to the directory where you executed `marco`. For ease of debugging you can write the code in a file `marco.sh` and (re)load the definitions to your shell by executing `source marco.sh`.
        
        ## **Return Codes**
        
        1. Say you have a command that fails rarely. In order to debug it you need to capture its output but it can be time consuming to get a failure run. Write a bash script that runs the following script until it fails and captures its standard output and error streams to files and prints everything at the end. Bonus points if you can also report how many runs it took for the script to fail.
            
            ```
             #!/usr/bin/env bash
            
             n=$(( RANDOM % 100 ))
            
             if [[ $n -eq 42 ]]; thenecho "Something went wrong"
                >&2 echo "The error was using magic numbers"
                exit1
             fiecho "Everything went according to plan"
            ```
            
        
        ## **Signals and Job Control**
        
        1. Start a `sleep 10000` job in a terminal, background it with `Ctrl-Z` and continue its execution with `bg`. Now use `pgrep` to find its pid and `pkill` to kill it without ever typing the pid itself. (Hint: use the `lf` flags).
        2. Say you don’t want to start a process until another completes. How would you go about it? In this exercise, our limiting process will always be `sleep 60 &`. One way to achieve this is to use the `wait` command. Try launching the sleep command and having an `ls` wait until the background process finishes.
            
            However, this strategy will fail if we start in a different bash session, since `wait` only works for child processes. One feature we did not discuss in the notes is that the `kill` command’s exit status will be zero on success and nonzero otherwise. `kill -0` does not send a signal but will give a nonzero exit status if the process does not exist. Write a bash function called `pidwait` that takes a pid and waits until the given process completes. You should use `sleep` to avoid wasting CPU unnecessarily.
            
        
        ## **Files and Permissions**
        
        1. (Advanced) Write a command or script to recursively find the most recently modified file in a directory. More generally, can you list all files by recency?
        
        ## **Terminal Multiplexers**
        
        1. Follow this `tmux` tutorial and then learn how to do some basic customizations following these steps.
        
        ## **Aliases and Dotfiles**
        
        1. Create an alias `dc` that resolves to `cd` for when you type it wrong.
        2. Run `history | awk '{$1="";print substr($0,2)}' | sort | uniq -c | sort -n | tail -n 10` to get your top 10 most used commands and consider writing shorter aliases for them. Note: this works for Bash; if you’re using ZSH, use `history 1` instead of just `history`.
        3. Create a folder for your dotfiles and set up version control.
        4. Add a configuration for at least one program, e.g. your shell, with some customization (to start off, it can be something as simple as customizing your shell prompt by setting `$PS1`).
        5. Set up a method to install your dotfiles quickly (and without manual effort) on a new machine. This can be as simple as a shell script that calls `ln -s` for each file, or you could use a specialized utility.
        6. Test your installation script on a fresh virtual machine.
        7. Migrate all of your current tool configurations to your dotfiles repository.
        8. Publish your dotfiles on GitHub.
        
        ## **Remote Machines (SSH)**
        
        Install a Linux virtual machine (or use an already existing one) for these exercises. If you are not familiar with virtual machines check out this tutorial for installing one.
        
        1. Go to `~/.ssh/` and check if you have a pair of SSH keys there. If not, generate them with `ssh-keygen -a 100 -t ed25519`. It is recommended that you use a password and use `ssh-agent`, more info here.
        2. Edit `.ssh/config` to have an entry as follows:
            
            ```
             Host vm
                 User username_goes_here
                 HostName ip_goes_here
                 IdentityFile ~/.ssh/id_ed25519
                 LocalForward 9999 localhost:8888
            ```
            
        3. Use `ssh-copy-id vm` to copy your ssh key to the server.
        4. Start a webserver in your VM by executing `python -m http.server 8888`. Access the VM webserver by navigating to `http://localhost:9999` in your machine.
        5. Edit your SSH server config by doing `sudo vim /etc/ssh/sshd_config` and disable password authentication by editing the value of `PasswordAuthentication`. Disable root login by editing the value of `PermitRootLogin`. Restart the `ssh` service with `sudo service sshd restart`. Try sshing in again.
        6. (Challenge) Install `mosh` in the VM and establish a connection. Then disconnect the network adapter of the server/VM. Can mosh properly recover from it?
        7. (Challenge) Look into what the `N` and `f` flags do in `ssh` and figure out a command to achieve background port forwarding.
    
    https://missing.csail.mit.edu/2026/command-line-environment/
    
- topic 3: development environment and tools
    - notetaking
        
        terminal based develop environment vs vscode development environment ( AI functionality tends to be better integrated into graphical integrated development environment, IDEs )
        
        ### Text Editing in Vims
        
        when editing codes, we only write on snippets with many files (like cursor)
        
        vim works with only keyboard inputs. ( modal editior )
        
        modal editor has many operating modes for doing different classes of things.
        
        vim ⇒ pressing esc → normal mode →
        
        pressing i : insert mode
        
        pressing R : replace mode
        
        pressing v: plain visual mode
        
        pressing V : visual line mode
        
        pressing ctrl v : visual block mode
        
        pressing ; : command mode
        
        ### Vim’s interface is a programming language
        
        normal mode - movement, selection, edits, counts, modifiers
        
        many key bindings.. 
        
        ### Code intelligence and language servers
        
        LSP: protocol to IDE → language server
        
        language server has semantic understanding of code that cn enable IDE to offer many functions ( like “go to definition”, or catch errors with red lines )
        
        ### AI-powered development
        
        (1) autocomplete
        
        write comments!, exact function name.
        
        (2) inline ai chat
        
    - lecture slides
        
        A *development environment* is a set of tools for developing software. At the heart of a development environment is text editing functionality, along with accompanying features such as syntax highlighting, type checking, code formatting, and autocomplete. *Integrated development environments* (IDEs) such as VS Code bring together all of this functionality into a single application. Terminal-based development workflows combine tools such as tmux (a terminal multiplexer), Vim (a text editor), Zsh (a shell), and language-specific command-line tools, such as Ruff (a Python linter and code formatter) and Mypy (a Python type checker).
        
        IDEs and terminal-based workflows each have their strengths and weaknesses. For example, graphical IDEs can be easier to learn, and today’s IDEs generally have better out-of-the-box AI integrations like AI autocomplete; on the other hand, terminal-based workflows are lightweight, and they may be your only option in environments where you don’t have a GUI or can’t install software. We recommend you develop basic familiarity with both and develop mastery of at least one. If you don’t already have a preferred IDE, we recommend starting with VS Code.
        
        In this lecture, we’ll cover:
        
        - Text editing and Vim
        - Code intelligence and language servers
        - AI-powered development
        - Extensions and other IDE functionality
        
        # **Text editing and Vim**
        
        When programming, you spend most of your time navigating through code, reading snippets of code, and making edits to code, rather than writing long streams or reading files top-to-bottom. Vim is a text editor that is optimized for this distribution of tasks.
        
        **The philosophy of Vim.** Vim has a beautiful idea as its foundation: its interface is itself a programming language, designed for navigating and editing text. Keystrokes (with mnemonic names) are commands, and these commands are composable. Vim avoids the use of the mouse, because it’s too slow; Vim even avoids use of the arrow keys because it requires too much movement. The result: an editor that feels like a brain-computer interface and matches the speed at which you think.
        
        **Vim support in other software.** You don’t have to use Vim itself to benefit from the ideas at its core. Many programs that involve any kind of text editing support “Vim mode”, either as built-in functionality or as a plugin. For example, VS Code has the VSCodeVim plugin, Zsh has built-in support for Vim emulation, and even Claude Code has built-in support for Vim editor mode. Chances are that any tool you use that involves text editing supports Vim mode in one way or another.
        
        ## **Modal editing**
        
        Vim is a *modal editor*: it has different operating modes for different classes of tasks.
        
        - **Normal**: for moving around a file and making edits
        - **Insert**: for inserting text
        - **Replace**: for replacing text
        - **Visual** (plain, line, or block): for selecting blocks of text
        - **Command-line**: for running a command
        
        Keystrokes have different meanings in different operating modes. For example, the letter `x` in Insert mode will just insert a literal character “x”, but in Normal mode, it will delete the character under the cursor, and in Visual mode, it will delete the selection.
        
        In its default configuration, Vim shows the current mode in the bottom left. The initial/default mode is Normal mode. You’ll generally spend most of your time between Normal mode and Insert mode.
        
        You change modes by pressing `<ESC>` (the escape key) to switch from any mode back to Normal mode. From Normal mode, enter Insert mode with `i`, Replace mode with `R`, Visual mode with `v`, Visual Line mode with `V`, Visual Block mode with `<C-v>` (Ctrl-V, sometimes also written `^V`), and Command-line mode with `:`.
        
        You use the `<ESC>` key a lot when using Vim: consider remapping Caps Lock to Escape (macOS instructions) or create an alternative mapping for `<ESC>` with a simple key sequence.
        
        ## **Basics: inserting text**
        
        From Normal mode, press `i` to enter Insert mode. Now, Vim behaves like any other text editor, until you press `<ESC>` to return to Normal mode. This, along with the basics explained above, are all you need to start editing files using Vim (though not particularly efficiently, if you’re spending all your time editing from Insert mode).
        
        ## **Vim’s interface is a programming language**
        
        Vim’s interface is a programming language. Keystrokes (with mnemonic names) are commands, and these commands *compose*. This enables efficient movement and edits, especially once the commands become muscle memory, just like typing becomes super efficient once you’ve learned your keyboard layout.
        
        ### **Movement**
        
        You should spend most of your time in Normal mode, using movement commands to navigate the file. Movements in Vim are also called “nouns”, because they refer to chunks of text.
        
        - Basic movement: `hjkl` (left, down, up, right)
        - Words: `w` (next word), `b` (beginning of word), `e` (end of word)
        - Lines: `0` (beginning of line), `^` (first non-blank character), `$` (end of line)
        - Screen: `H` (top of screen), `M` (middle of screen), `L` (bottom of screen)
        - Scroll: `Ctrl-u` (up), `Ctrl-d` (down)
        - File: `gg` (beginning of file), `G` (end of file)
        - Line numbers: `:{number}<CR>` or `{number}G` (line {number})
            - `<CR>` refers to the carriage return / enter key
        - Misc: `%` (matching item, like parenthesis or brace)
        - Find: `f{character}`, `t{character}`, `F{character}`, `T{character}`
            - find/to forward/backward {character} on the current line
            - `,` / `;` for navigating matches
        - Search: `/{regex}`, `n` / `N` for navigating matches
        
        ### **Selection**
        
        Visual modes:
        
        - Visual: `v`
        - Visual Line: `V`
        - Visual Block: `Ctrl-v`
        
        Can use movement keys to make selection.
        
        ### **Edits**
        
        Everything that you used to do with the mouse, you now do with the keyboard using editing commands that compose with movement commands. Here’s where Vim’s interface starts to look like a programming language. Vim’s editing commands are also called “verbs”, because verbs act on nouns.
        
        - `i` enter Insert mode
            - but for manipulating/deleting text, want to use something more than backspace
        - `o` / `O` insert line below / above
        - `d{motion}` delete {motion}
            - e.g. `dw` is delete word, `d$` is delete to end of line, `d0` is delete to beginning of line
        - `c{motion}` change {motion}
            - e.g. `cw` is change word
            - like `d{motion}` followed by `i`
        - `x` delete character (equivalent to `dl`)
        - `s` substitute character (equivalent to `cl`)
        - Visual mode + manipulation
            - select text, `d` to delete it or `c` to change it
        - `u` to undo, `<C-r>` to redo
        - `y` to copy / “yank” (some other commands like `d` also copy)
        - `p` to paste
        - Lots more to learn: for example, `~` flips the case of a character, and `J` joins together lines
        
        ### **Counts**
        
        You can combine nouns and verbs with a count, which will perform a given action a number of times.
        
        - `3w` move 3 words forward
        - `5j` move 5 lines down
        - `7dw` delete 7 words
        
        ### **Modifiers**
        
        You can use modifiers to change the meaning of a noun. Some modifiers are `i`, which means “inner” or “inside”, and `a`, which means “around”.
        
        - `ci(` change the contents inside the current pair of parentheses
        - `ci` change the contents inside the current pair of square brackets
        - `da'` delete a single-quoted string, including the surrounding single quotes
        
        ## **Putting it all together**
        
        Here is a broken [fizz buzz implementation:
        
        ```
        def fizz_buzz(limit):
            for i in range(limit):
                if i % 3 == 0:
                    print("fizz", end="")
                if i % 5 == 0:
                    print("fizz", end="")
                if i % 3 and i % 5:
                    print(i, end="")
                print()
        
        def main():
            fizz_buzz(20)
        ```
        
        We use the following sequence of commands to fix the issues, beginning in Normal mode:
        
        - Main is never called
            - `G` to jump to the end of the file
            - `o` to **o**pen a new line below
            - Type in `if __name__ == "__main__": main()`
                - If your editor has Python language support, it might do some auto-indentation for you in Insert mode
            - `<ESC>` to go back to Normal mode
        - Starts at 0 instead of 1
            - `/` followed by `range` and `<CR>` to search for “range”
            - `ww` to move forward two **w**ords (you could also use `2w`, but in practice, for small counts it’s common to repeat the key instead of using the count functionality)
            - `i` to switch to **i**nsert mode, and add `1,`
            - `<ESC>` to go back to Normal mode
            - `e` to jump to the **e**nd of the next word
            - `a` to start **a**ppending text, and add `+ 1`
            - `<ESC>` to go back to Normal mode
        - Prints “fizz” for multiples of 5
            - `:6<CR>` to go to line 6
            - `ci"` to **c**hange **i**nside the ‘**“**’, change to `"buzz"`
            - `<ESC>` to go back to Normal mode
        
        ## **Learning Vim**
        
        The best way to learn Vim is to learn the fundamentals (what we’ve covered so far) and then just enable Vim mode in all your software and start using it in practice. Avoid the temptation to use the mouse or the arrow keys; in some editors, you can unbind the arrow keys to force yourself to build good habits.
        
        ### **Additional resources**
        
        - The Vim lecture from the previous iteration of this class — we have covered Vim in more depth there
        - `vimtutor` is a tutorial that comes installed with Vim — if Vim is installed, you should be able to run `vimtutor` from your shell
        - Vim Adventures is a game to learn Vim
        - Vim Tips Wiki
        - Vim Advent Calendar has various Vim tips
        - VimGolf is code golf, but where the programming language is Vim’s UI
        - Vi/Vim Stack Exchange
        - Vim Screencasts
        - Practical Vim (book)
        
        # **Code intelligence and language servers**
        
        IDEs generally offer language-specific support that requires semantic understanding of the code through IDE extensions that connect to *language servers* that implement Language Server Protocol. For example, the Python extension for VS Code relies on Pylance, and the Go extension for VS Code relies on the first-party gopls. By installing the extension and language server for the languages you work with, you can enable many language-specific features in your IDE, such as:
        
        - **Code completion.** Better autocomplete and autosuggest, such as being able to see an object’s fields and methods after typing `object.`.
        - **Inline documentation.** Seeing documentation on hover and autosuggest.
        - **Jump-to-definition.** Jumping from a use site to the definition, such as being able to go from a field reference `object.field` to the definition of the field.
        - **Find references.** The inverse of the above, find all sites where a particular item such as a field or type is referenced.
        - **Help with imports.** Organizing imports, removing unused imports, flagging missing imports.
        - **Code quality.** These tools can be used standalone, but this functionality is often provided by language servers as well. Code formatting auto-indents and auto-formats code, and type checkers and linters find errors in your code, as you type. We will cover this class of functionality in greater depth in the lecture on code quality.
        
        ## **Configuring language servers**
        
        For some languages, all you need to do is install the extension and language server, and you’ll be all set. For others, to get the maximum benefit from the language server, you need to tell the IDE about your environment. For example, pointing VS Code to your Python environment will enable the language server to see your installed packages. Environments are covered in more depth in our lecture on packaging and shipping code.
        
        Depending on the language, there might be some settings you can configure for your language server. For example, using the Python support in VS Code, you can disable static type checking for projects that don’t make use of Python’s optional type annotations.
        
        # **AI-powered development**
        
        Since the introduction of GitHub Copilot using OpenAI’s Codex model in mid 2021, LLMs have become widely adopted in software engineering. There are three main form factors in use right now: autocomplete, inline chat, and coding agents.
        
        ## **Autocomplete**
        
        AI-powered autocomplete has the same form factor as traditional autocomplete in your IDE, suggesting completions at your cursor position as you type. Sometimes, it’s used as a passive feature that “just works”. Beyond that, AI autocomplete is generally prompted using code comments.
        
        For example, let’s write a script to download the contents of these lecture notes and extract all the links. We can start with:
        
        ```
        import requests
        
        def download_contents(url: str) -> str:
        ```
        
        The model will autocomplete the body of the function:
        
        ```
            response = requests.get(url)
            return response.text
        ```
        
        We can further guide completions using comments. For example, if we start writing a function to extract all Markdown links, but it doesn’t have a particularly descriptive name:
        
        ```
        def extract(contents: str) -> list[str]:
        ```
        
        The model will autocomplete something like this:
        
        ```
            lines = contents.splitlines()
            return [line for line in lines if line.strip()]
        ```
        
        We can guide the completion through code comments:
        
        ```
        def extract(content: str) -> list[str]:
            # extract all Markdown links from the content
        ```
        
        This time, the model gives a better completion:
        
        ```
            import re
            pattern = r'\[.*?\]\((.*?)\)'
            return re.findall(pattern, content)
        ```
        
        Here, we see one downside of this AI coding tool: it can only provide completions at the cursor. In this case, it would be better practice to put the `import re` at the module level, rather than inside the function.
        
        The example above used a poorly-named function to demonstrate how code completion can be steered using comments; in practice, you’d want to write code with functions named more descriptively, like `extract_links`, and you’d want to write docstrings (and based on this, the model should generate a completion analogous to the one above).
        
        For demonstration purposes, we can complete the script:
        
        ```
        print(extract(download_contents("https://raw.githubusercontent.com/missing-semester/missing-semester/refs/heads/master/_2026/development-environment.md")))
        ```
        
        ## **Inline chat**
        
        Inline chat lets you select a line or block and then directly prompt the AI model to propose an edit. In this interaction mode, the model can make changes to existing code (which differs from autocomplete, which only completes code beyond the cursor).
        
        Continuing the example from above, suppose we decided not to use the third-party `requests` library. We could select the relevant three lines of code, invoke inline chat, and say something like:
        
        ```
        use built-in libraries instead
        ```
        
        The model proposes:
        
        ```
        from urllib.request import urlopen
        
        def download_contents(url: str) -> str:
            with urlopen(url) as response:
                return response.read().decode('utf-8')
        ```
        
        ## **Coding agents**
        
        Coding agents are covered in depth in the Agentic Coding lecture.
        
        ## **Recommended software**
        
        Some popular AI IDEs are VS Code with the GitHub Copilot extension and Cursor. GitHub Copilot is currently available for free for students, teachers, and maintainers of popular open source projects. This is a rapidly evolving space. Many of the leading products have roughly equivalent functionality.
        
        # **Extensions and other IDE functionality**
        
        IDEs are powerful tools, made even more powerful by *extensions*. We can’t cover all of these features in a single lecture, but here we provide some pointers to a couple popular extensions. We encourage you to explore this space on your own; there are many lists of popular IDE extensions available online, such as Vim Awesome for Vim plugins and VS Code extensions sorted by popularity.
        
        - Development containers: supported by popular IDEs (e.g., supported by VS Code), dev containers let you use a container to run development tools. This can be helpful for portability or isolation. The lecture on packaging and shipping code covers containers in more depth.
        - Remote development: do development on a remote machine using SSH (e.g., with the Remote SSH plugin for VS Code). This can be handy, for example, if you want to develop and run code on a beefy GPU machine in the cloud.
        - Collaborative editing: edit the same file, Google Docs style (e.g., with the Live Share plugin for VS Code).
    - exercises
        1. Enable Vim mode in all the software you use that supports it, such as your editor and your shell, and use Vim mode for all your text editing for the next month. Whenever something seems inefficient, or when you think “there must be a better way”, try Googling it, there probably is a better way.
        2. Complete a challenge from VimGolf.
        3. Configure an IDE extension and language server for a project that you’re working on. Ensure that all the expected functionality, such as jump-to-definition for library dependencies, works as expected. If you don’t have code that you can use for this exercise, you can use some open-source project from GitHub (such as this one).
        4. Browse a list of IDE extensions and install one that seems useful to you.
    
    https://missing.csail.mit.edu/2026/development-environment/
    
- topic 5: version control and git
    - notetaking
        
        version control → saves changes & metadata(account, time, commit messege,)
        
        ### Git’s data model
        
        snapshots: refer to state of directory
        
        blob == file
        
        tree == folder
        
        foo == subtree
        
        , files
        
        history == directed acyclic graph of snapshots.
        
        each snapshot refers to a set of parents
        
        !image.png
        
        commits & merge commit
        
        append only, immutable
        
    - lecture slides
        
        Version control systems (VCSs) are tools used to track changes to source code (or other collections of files and folders). As the name implies, these tools help maintain a history of changes; furthermore, they facilitate collaboration. Logically, VCSs track changes to a folder and its contents in a series of *snapshots*, where each snapshot encapsulates the entire state of files/folders within a top-level directory. VCSs also maintain metadata like who created each snapshot, messages associated with each snapshot, and so on.
        
        Why is version control useful? Even when you’re working by yourself, it can let you look at old snapshots of a project, keep a log of why certain changes were made, work on parallel branches of development, and much more. When working with others, it’s an invaluable tool for seeing what other people have changed, as well as resolving conflicts in concurrent development.
        
        Modern VCSs also let you easily (and often automatically) answer questions like:
        
        - Who wrote this module?
        - When was this particular line of this particular file edited? By whom? Why was it edited?
        - Over the last 1000 revisions, when/why did a particular unit test stop working?
        
        While other VCSs exist, **Git** is the de facto standard for version control. This XKCD comic captures Git’s reputation:
        
        !xkcd 1597
        
        Because Git’s interface is a leaky abstraction, learning Git top-down (starting with its interface / command-line interface) can lead to a lot of confusion. It’s possible to memorize a handful of commands and think of them as magic incantations, and follow the approach in the comic above whenever anything goes wrong.
        
        While Git admittedly has an ugly interface, its underlying design and ideas are beautiful. While an ugly interface has to be *memorized*, a beautiful design can be *understood*. For this reason, we give a bottom-up explanation of Git, starting with its data model and later covering the command-line interface. Once the data model is understood, the commands can be better understood in terms of how they manipulate the underlying data model.
        
        # **Git’s data model**
        
        Git’s ingenuity is in its well-thought-out data model that enables all the nice features of version control, like maintaining history, supporting branches, and enabling collaboration.
        
        ## **Snapshots**
        
        Git models the history of a collection of files and folders within some top-level directory as a series of snapshots. In Git terminology, a file is called a “blob”, and it’s just a bunch of bytes. A directory is called a “tree”, and it maps names to blobs or trees (so directories can contain other directories). A snapshot is the top-level tree that is being tracked. For example, we might have a tree as follows:
        
        ```
        <root> (tree)
        |
        +- foo (tree)
        |  |
        |  + bar.txt (blob, contents = "hello world")
        |
        +- baz.txt (blob, contents = "git is wonderful")
        ```
        
        The top-level tree contains two elements, a tree “foo” (that itself contains one element, a blob “bar.txt”), and a blob “baz.txt”.
        
        ## **Modeling history: relating snapshots**
        
        How should a version control system relate snapshots? One simple model would be to have a linear history. A history would be a list of snapshots in time-order. For many reasons, Git doesn’t use a simple model like this.
        
        In Git, a history is a directed acyclic graph (DAG) of snapshots. That may sound like a fancy math word, but don’t be intimidated. All this means is that each snapshot in Git refers to a set of “parents”, the snapshots that preceded it. It’s a set of parents rather than a single parent (as would be the case in a linear history) because a snapshot might descend from multiple parents, for example, due to combining (merging) two parallel branches of development.
        
        Git calls these snapshots “commit”s. Visualizing a commit history might look something like this:
        
        ```
        o <-- o <-- o <-- o
                    ^
                     \
                      --- o <-- o
        ```
        
        In the ASCII art above, the `o`s correspond to individual commits (snapshots). The arrows point to the parent of each commit (it’s a “comes before” relation, not “comes after”). After the third commit, the history branches into two separate branches. This might correspond to, for example, two separate features being developed in parallel, independently from each other. In the future, these branches may be merged to create a new snapshot that incorporates both of the features, producing a new history that looks like this, with the newly created merge commit shown in bold:
        
        ```
        
        o <-- o <-- o <-- o <---- o
                    ^            /
                     \          v
                      --- o <-- o
        ```
        
        Commits in Git are immutable. This doesn’t mean that mistakes can’t be corrected, however; it’s just that “edits” to the commit history are actually creating entirely new commits, and references (see below) are updated to point to the new ones.
        
        ## **Data model, as pseudocode**
        
        It may be instructive to see Git’s data model written down in pseudocode:
        
        ```
        // a file is a bunch of bytes
        type blob = array<byte>
        
        // a directory contains named files and directories
        type tree = map<string, tree | blob>
        
        // a commit has parents, metadata, and the top-level tree
        type commit = struct {
            parents: array<commit>
            author: string
            message: string
            snapshot: tree
        }
        ```
        
        It’s a clean, simple model of history.
        
        ## **Objects and content-addressing**
        
        An “object” is a blob, tree, or commit:
        
        ```
        type object = blob | tree | commit
        ```
        
        In Git’s data store, all objects are content-addressed by their SHA-1 hash.
        
        ```
        objects = map<string, object>
        
        def store(object):
            id = sha1(object)
            objects[id] = object
        
        def load(id):
            return objects[id]
        ```
        
        Blobs, trees, and commits are unified in this way: they are all objects. When they reference other objects, they don’t actually *contain* them in their on-disk representation, but have a reference to them by their hash.
        
        For example, the tree for the example directory structure above (visualized using `git cat-file -p 698281bc680d1995c5f4caaf3359721a5a58d48d`), looks like this:
        
        ```
        100644 blob 4448adbf7ecd394f42ae135bbeed9676e894af85    baz.txt
        040000 tree c68d233a33c5c06e0340e4c224f0afca87c8ce87    foo
        ```
        
        The tree itself contains pointers to its contents, `baz.txt` (a blob) and `foo` (a tree). If we look at the contents addressed by the hash corresponding to baz.txt with `git cat-file -p 4448adbf7ecd394f42ae135bbeed9676e894af85`, we get the following:
        
        ```
        git is wonderful
        ```
        
        ## **References**
        
        Now, all snapshots can be identified by their SHA-1 hashes. That’s inconvenient, because humans aren’t good at remembering strings of 40 hexadecimal characters.
        
        Git’s solution to this problem is human-readable names for SHA-1 hashes, called “references”. References are pointers to commits. Unlike objects, which are immutable, references are mutable (can be updated to point to a new commit). For example, the `master` reference usually points to the latest commit in the main branch of development.
        
        ```
        references = map<string, string>
        
        def update_reference(name, id):
            references[name] = id
        
        def read_reference(name):
            return references[name]
        
        def load_reference(name_or_id):
            if name_or_id in references:
                return load(references[name_or_id])
            else:
                return load(name_or_id)
        ```
        
        With this, Git can use human-readable names like “master” to refer to a particular snapshot in the history, instead of a long hexadecimal string.
        
        One detail is that we often want a notion of “where we currently are” in the history, so that when we take a new snapshot, we know what it is relative to (how we set the `parents` field of the commit). In Git, that “where we currently are” is a special reference called “HEAD”.
        
        ## **Repositories**
        
        Finally, we can define what (roughly) is a Git *repository*: it is the data `objects` and `references`.
        
        On disk, all Git stores are objects and references: that’s all there is to Git’s data model. All `git` commands map to some manipulation of the commit DAG by adding objects and adding/updating references.
        
        Whenever you’re typing in any command, think about what manipulation the command is making to the underlying graph data structure. Conversely, if you’re trying to make a particular kind of change to the commit DAG, e.g. “discard uncommitted changes and make the ‘master’ ref point to commit `5d83f9e`”, there’s probably a command to do it (e.g. in this case, `git checkout master; git reset --hard 5d83f9e`).
        
        # **Staging area**
        
        This is another concept that’s orthogonal to the data model, but it’s a part of the interface to create commits.
        
        One way you might imagine implementing snapshotting as described above is to have a “create snapshot” command that creates a new snapshot based on the *current state* of the working directory. Some version control tools work like this, but not Git. We want clean snapshots, and it might not always be ideal to make a snapshot from the current state. For example, imagine a scenario where you’ve implemented two separate features, and you want to create two separate commits, where the first introduces the first feature, and the next introduces the second feature. Or imagine a scenario where you have debugging print statements added all over your code, along with a bugfix; you want to commit the bugfix while discarding all the print statements.
        
        Git accommodates such scenarios by allowing you to specify which modifications should be included in the next snapshot through a mechanism called the “staging area”.
        
        # **Git command-line interface**
        
        To avoid duplicating information, we’re not going to explain the commands below in detail in these lecture notes. See the highly recommended Pro Git for more information, or watch the lecture video.
        
        ## **Basics**
        
        - `git help <command>`: get help for a git command
        - `git init`: creates a new git repo, with data stored in the `.git` directory
        - `git status`: tells you what’s going on
        - `git add <filename>`: adds files to staging area
        - `git commit`: creates a new commit
            - Write good commit messages!
            - Even more reasons to write good commit messages!
        - `git log`: shows a flattened log of history
        - `git log --all --graph --decorate`: visualizes history as a DAG
        - `git diff <filename>`: show changes you made relative to the staging area
        - `git diff <revision> <filename>`: shows differences in a file between snapshots
        - `git checkout <revision>`: updates HEAD (and current branch if checking out a branch)
        
        ## **Branching and merging**
        
        - `git branch`: shows branches
        - `git branch <name>`: creates a branch
        - `git switch <name>`: switches to a branch
        - `git checkout -b <name>`: creates a branch and switches to it
            - same as `git branch <name>; git switch <name>`
        - `git merge <revision>`: merges into current branch
        - `git mergetool`: use a fancy tool to help resolve merge conflicts
        - `git rebase`: rebase set of patches onto a new base
        
        ## **Remotes**
        
        - `git remote`: list remotes
        - `git remote add <name> <url>`: add a remote
        - `git push <remote> <local branch>:<remote branch>`: send objects to remote, and update remote reference
        - `git branch --set-upstream-to=<remote>/<remote branch>`: set up correspondence between local and remote branch
        - `git fetch`: retrieve objects/references from a remote
        - `git pull`: same as `git fetch; git merge`
        - `git clone`: download repository from remote
        
        ## **Undo**
        
        - `git commit --amend`: edit a commit’s contents/message
        - `git reset <file>`: unstage a file
        - `git restore`: discard changes
        
        # **Advanced Git**
        
        - `git config`: Git is highly customizable
        - `git clone --depth=1`: shallow clone, without entire version history
        - `git add -p`: interactive staging
        - `git rebase -i`: interactive rebasing
        - `git blame`: show who last edited which line
        - `git stash`: temporarily remove modifications to working directory
        - `git bisect`: binary search history (e.g. for regressions)
        - `git revert`: create a new commit that reverses the effect of an earlier commit
        - `git worktree`: check out multiple branches at the same time
        - `.gitignore`: specify intentionally untracked files to ignore
        
        # **Miscellaneous**
        
        - **GUIs**: there are many GUI clients out there for Git. We personally don’t use them and use the command-line interface instead.
        - **Shell integration**: it’s super handy to have a Git status as part of your shell prompt (zsh, bash). Often included in frameworks like Oh My Zsh.
        - **Editor integration**: similarly to the above, handy integrations with many features. fugitive.vim is the standard one for Vim.
        - **Workflows**: we taught you the data model, plus some basic commands; we didn’t tell you what practices to follow when working on big projects (and there are many different approaches).
        - **GitHub**: Git is not GitHub. GitHub has a specific way of contributing code to other projects, called pull requests.
        - **Other Git providers**: GitHub is not special: there are many Git repository hosts, like GitLab and BitBucket.
        
        # **Resources**
        
        - Pro Git is **highly recommended reading**. Going through Chapters 1–5 should teach you most of what you need to use Git proficiently, now that you understand the data model. The later chapters have some interesting, advanced material.
        - Oh Shit, Git!?! is a short guide on how to recover from some common Git mistakes.
        - Git for Computer Scientists is a short explanation of Git’s data model, with less pseudocode and more fancy diagrams than these lecture notes.
        - Git from the Bottom Up is a detailed explanation of Git’s implementation details beyond just the data model, for the curious.
        - How to explain git in simple words
        - Learn Git Branching is a browser-based game that teaches you Git.
    - exercises
        1. If you don’t have any past experience with Git, either try reading the first couple chapters of Pro Git or go through a tutorial like Learn Git Branching. As you’re working through it, relate Git commands to the data model.
        2. Clone the repository for the class website.
            1. Explore the version history by visualizing it as a graph.
            2. Who was the last person to modify `README.md`? (Hint: use `git log` with an argument).
            3. What was the commit message associated with the last modification to the `collections:` line of `_config.yml`? (Hint: use `git blame` and `git show`).
        3. One common mistake when learning Git is to commit large files that should not be managed by Git or adding sensitive information. Try adding a file to a repository, making some commits and then deleting that file from *history* (not just the latest commit). You may want to look at this.
        4. Clone some repository from GitHub, and modify one of its existing files. What happens when you do `git stash`? What do you see when running `git log --all --oneline`? Run `git stash pop` to undo what you did with `git stash`. In what scenario might this be useful?
        5. Like many command line tools, Git provides a configuration file (or dotfile) called `~/.gitconfig`. Create an alias in `~/.gitconfig` so that when you run `git graph`, you get the output of `git log --all --graph --decorate --oneline`. You can do this by directly editing the `~/.gitconfig` file, or you can use the `git config` command to add the alias. Information about git aliases can be found here.
        6. You can define global ignore patterns in `~/.gitignore_global` after running `git config --global core.excludesfile ~/.gitignore_global`. This sets the location of the global ignore file that Git will use, but you still need to manually create the file at that path. Set up your global gitignore file to ignore OS-specific or editor-specific temporary files, like `.DS_Store`.
        7. Fork the repository for the class website, find a typo or some other improvement you can make, and submit a pull request on GitHub (you may want to look at this). Please only submit PRs that are useful (don’t spam us, please!). If you can’t find an improvement to make, you can skip this exercise.
        8. Practice resolving merge conflicts by simulating a collaborative scenario:
            1. Create a new repository with `git init` and create a file called `recipe.txt` with a few lines (e.g., a simple recipe).
            2. Commit it, then create two branches: `git branch salty` and `git branch sweet`.
            3. In the `salty` branch, modify a line (e.g., change “1 cup sugar” to “1 cup salt”) and commit.
            4. In the `sweet` branch, modify the same line differently (e.g., change “1 cup sugar” to “2 cups sugar”) and commit.
            5. Now switch to `master` and try `git merge salty`, then `git merge sweet`. What happens? Look at the contents of `recipe.txt` - what do the `<<<<<<<`, `=======`, and `>>>>>>>` markers mean?
            6. Resolve the conflict by editing the file to keep the content you want, removing the conflict markers, and completing the merge with `git add` and `git commit` (or `git merge --continue`). Alternatively, try using `git mergetool` to resolve the conflict with a graphical or terminal-based merge tool.
            7. Use `git log --graph --oneline` to visualize the merge history you just created.
    
    https://missing.csail.mit.edu/2026/version-control/