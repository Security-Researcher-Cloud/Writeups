# First Terminal
## Objectives
![](../../../Assets/images/prologue/first-terminal/prologue-first-terminal-objective.png)

## First Terminal
The first terminal was the introduction to the Holiday Hack Challenge. In this challenge, your only objective it to was
to put `answer` in the top part of the window next to the `>` symbol.

![](../../../Assets/images/prologue/first-terminal/prologue-first-terminal-regular 1.png)

**Answer:** `answer`

## There's More?
When you explore the bottom terminal you can see that you can move through the operating system, to which you can explore
or test a few commands. I was not able to identify anything of particular value, such as a hidden flag or achievement in
this terminal

### Finding Binaries
- Look for binaries that have suid `find / -perm -u=s -type f 2>/dev/null`

![](../../..//Assets/images/prologue/first-terminal/prologue-first-terminal-suid-lookup.png)

- run the `/usr/bin/runtoanswer` and provide `answer` to it it will grant the trophy and immediately close

![](../../..//Assets/images/prologue/first-terminal/prologue-first-terminal-runtoanswer.png)

### Finding Trolls
- Looking for trolls using grep `find / -type f -iname "*troll*"` which only shows time zones. So no real trolls this 
time. Must have defeated them in 2023.

![](../../../Assets/images/prologue/first-terminal/prologue-first-terminal-finding-trolls.png)

## What's Next

### Prerequisite For

- [Prologue Elf Connect](./Prologue Elf Connect.md)
- [Prologue Elf Minder 9000](./Prologue Elf Minder 9000.md)

### Awards
![](../../../Assets/images/prologue/first-terminal/prologue-first-terminal-award.png.png)