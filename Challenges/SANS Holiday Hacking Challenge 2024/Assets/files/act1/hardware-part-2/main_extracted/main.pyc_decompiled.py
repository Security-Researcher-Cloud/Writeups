# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: main.py
# Bytecode version: 3.10.0rc2 (3439)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import curses
import re
import time
import sys
import random
import textwrap
import cmd
import os
from signal import signal, SIGINT, SIGTSTP
SCREEN_WIDTH = 80
EASTER_EGGS = []
BOOT_STRING = '\nFirmware image loaded!\n\n'
UBOOT_STRINGS = ['U-Boot SPL 2024.08 (Dec 24 2023 - 23:59:59 +0000)', 'Preparing sleigh for takeoff...', '', '', 'U-Boot 2024.08-g1234567-jolly (Dec 25 2023 - 00:00:01 +0000)', '', 'CPU:   North Pole CandyCane v1.0, eco 5', 'Clocks: CPU: 1000MHz, DDR: 1600MHz, Bus: 400MHz, XTAL: 50MHz', "Model: Santa's Magic Access Control Board", 'DRAM:  256 MiB of Magic Memory', 'Loading Environment from SPI Flash... SF: Detected elf32magic with page size 512 Bytes, erase size 128 KiB, total 32 MiB', '*** Warning - bad CRC, using default enchanted environment', '', 'In:    elvenconsole@1e000c00', 'Out:   elvenconsole@1e000c00', 'Err:   elvenconsole@1e000c00', 'Net:   ', 'Warning: eth@1e100000 (eth0) using random MAC address - 5e:69:c8:f8:cf:5b', 'eth0: eth@1e100000', 'Hit any key to stop autoboot:  0 ', 'Reindeer_PCIE_SET: gpio[19]=1', 'Using eth@1e100000 device', 'TFTP from server 192.168.54.25; our IP address is 192.168.54.5', "Filename 'magic_firmware.bin'.", 'Load address: 0x80010000', 'Loading: *', 'North Pole Retry count exceeded; starting again']

class BootloaderCmd(cmd.Cmd):
    prompt = '\n=> '
    magic_count = 0
    undoc_header = None
    ipaddr = '192.168.54.1'
    netmask = '255.255.255.0'
    serverip = '192.168.54.10'
    bootfile = 'C0A80101.img'
    doc_header = 'Commands (type help <topic>):'

    def print_topics(self, header, cmds, cmdlen, maxcol):
        """Override the print_topics method to customize command listing"""
        if header is not None and cmds:
            self.stdout.write('%s\n' % str(header))
            if self.ruler:
                self.stdout.write('%s\n' % str(self.ruler * len(header)))
            self.columnize(cmds, maxcol - 1)
            self.stdout.write('\n')

    def default(self, arg):
        """Default response for unknown commands"""
        print('Unknown command. Type "help" for a list of commands.')

    def boot(self, arg):
        """Simulate booting process"""
        print(BOOT_STRING)
        for i in range(21):
            sys.stdout.write('\r')
            sys.stdout.write('[%-20s] BOOTING' % ('=' * i))
            sys.stdout.flush()
            time.sleep(0.25)
        print('\n\n')

    def do_quit(self, arg):
        """Quit the program"""
        global launch_terminal
        launch_terminal = False
        return True

    def do_base(self, arg):
        """Print address offset"""
        print('\nBase Address: 0x00000000\n')

    def do_bdinfo(self, arg):
        """Print board info"""
        print(f'\nboot_params = 0x87EB1238\nmemstart    = 0x80000000\nmemsize     = 0x08000000\nflashstart  = 0x00000000\nflashsize   = 0x00000000\nflashoffset = 0x00000000\nethaddr     = (not set)\nIP addr     = {self.ipaddr}\nbaudrate    = 115200 bps\nrelocaddr   = 0x87FB0000\nreloc off   = 0x07DB0000\n')

    def do_boot(self, arg):
        """Boot default, i.e., run 'bootcmd'"""
        global launch_terminal
        self.boot(arg)
        launch_terminal = True
        return True

    def do_coninfo(self, arg):
        """Print console devices and information"""
        print('\nList of available devices:\nuartlite0@1e000c00 00000007 IO stdin stdout stderr \nserial   00000003 IO\n              ')

    def do_cp(self, arg):
        """Memory copy"""
        print('\ncp - memory copy\n\nUsage:\ncp [.b, .w, .l] source target count\n')

    def do_echo(self, arg):
        """Echo arguments to console"""
        print(arg)

    def do_envreset(self, arg):
        """Reset environment variables to default settings"""
        self.serverip = '192.168.54.10'
        self.netmask = '255.255.255.0'
        self.ipaddr = '192.168.54.1'
        self.bootfile = 'C0A80101.img'

    def do_ping(self, arg):
        """Ping a network host"""
        if arg == '192.168.54.32':
            for seq, time in enumerate([27.5, 23.4, 25.3, 21.0], start=1):
                print(f'64 bytes from 192.168.54.32: icmp_seq={seq} ttl=58 time={time} ms')
                time.sleep(0.5)
        elif re.match('^(\\d{1,3}\\.){3}\\d{1,3}$', arg):
            print('Not route to hose')
        else:
            print('send ICMP ECHO_REQUEST to network host')

    def do_printenv(self, arg):
        """Print environment variables"""
        print(f'\nbaudrate=115200\nbootcmd=mtkautoboot\nbootdelay=0\nbootmenu_0=Startup system (Default)=mtkboardboot\nbootmenu_1=Upgrade firmware=mtkupgrade fw\nbootmenu_2=Upgrade bootloader=mtkupgrade bl\nbootmenu_3=Upgrade bootloader (advanced mode)=mtkupgrade bladv\nbootmenu_4=Load image=mtkload\nbootfile={self.bootfile}\nethact=eth@1e100000\nfdtcontroladdr=87ff6730\nipaddr={self.ipaddr}\nnetmask={self.netmask}\nserverip={self.serverip}0\nstderr=uartlite0@1e000c00\nstdin=uartlite0@1e000c00\nstdout=uartlite0@1e000c00\n\nEnvironment size: 460/65532 bytes\n')

    def do_setenv(self, arg):
        """Set environment variables"""
        args = arg.split()
        if len(args) == 2 and is_valid_ip(args[1]):
            setattr(self, args[0], args[1])
            print(f'Set {args[0]} to {args[1]}')
        elif len(args) == 2:
            setattr(self, args[0], args[1])
            print(f'Set {args[0]} to {args[1]}')
        else:
            print("\n    set environment variables\n                \n    Usage:\n    setenv [-f] name value ...\n        - [forcibly] set environment variable 'name' to 'value ...'\n    setenv [-f] name\n        - [forcibly] delete environment variable 'name'\n    ")

    def do_tftpboot(self, arg):
        """Boot image via network using TFTP protocol"""
        global launch_terminal
        print("*** Warning: no boot file name; using 'C0A80101.img'")
        print('Using eth@1e100000 device')
        serverip = arg.split()[0] if arg.split() and is_valid_ip(arg.split()[0]) else self.serverip
        print(f'TFTP from server {serverip}; our IP address is {self.ipaddr}')
        print(f"Filename '{self.bootfile}'.")
        print('Load address: 0x80010000')
        print('Loading: ')
        sleep_random()
        if serverip != '192.168.54.32' or self.netmask != '255.255.255.0' or self.ipaddr != '192.168.54.1':
            print('ARP Retry count exceeded; starting again')
            return
        if self.bootfile != 'backup.img':
            print(f'{self.bootfile} not found or invalid.')
            return
        print_asterisks(4)
        self.boot(arg)
        launch_terminal = True
        return True

    def do_version(self, arg):
        """Print monitor version"""
        print('\nU-Boot 2018.09-g8639621-dirty (Mar 03 2022 - 16:13:10 +0800)\n\nmipsel-linux-gcc (Buildroot 2014.11) 4.9.2\nGNU ld (GNU Binutils) 2.24\n')
    do_exit = do_quit
    do_q = do_quit

def handler(signal_received, frame):
    return

def sleep_random():
    random_time = random.uniform(0.01, 0.5)
    time.sleep(random_time)

def is_valid_ip(ip):
    ipv4_pattern = '^(\\d{1,3}\\.){3}\\d{1,3}$'
    return re.match(ipv4_pattern, ip) is not None

def print_asterisks(duration):
    total_asterisks = 100
    interval = duration / total_asterisks
    for _ in range(total_asterisks):
        print('*', end='', flush=True)
        time.sleep(max(0, interval + random.uniform(-0.1, 0.1)))
    print()

def uboot_console():
    global launch_terminal
    mycmd = BootloaderCmd()
    while not os.path.exists('/tmp/tokens'):
        mycmd.cmdloop()
        if launch_terminal:
            os.system('bash')
            if os.path.exists('/usr/share/stuff/tokens'):
                sys.exit()
            launch_terminal = False
        else:
            print('\nThanks for playing!')
            sys.exit()

def menu(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    static_text_before = '*** U-Boot Boot Menu ***'
    static_text_after = 'Press UP/DOWN to move, ENTER to select'
    options = ['1. Startup system (Default)', '2. U-Boot console']
    selected_option = 0
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, static_text_before)
        for i, option in enumerate(options):
            if i == selected_option:
                stdscr.addstr(i + 1, 0, '> ' + option, curses.A_REVERSE)
            else:
                stdscr.addstr(i + 1, 0, '  ' + option)
        stdscr.addstr(len(options) + 1, 0, static_text_after)
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_UP:
            selected_option = (selected_option - 1) % len(options)
        elif key == curses.KEY_DOWN:
            selected_option = (selected_option + 1) % len(options)
        elif key == 10:
            return selected_option
if __name__ == '__main__':
    signal(SIGINT, handler)
    signal(SIGTSTP, handler)
    for line in UBOOT_STRINGS:
        print(line)
        time.sleep(random.uniform(0.08, 0.1))
    while True:
        selected_option = curses.wrapper(menu)
        if selected_option == 0:
            curses.endwin()
            os.system('bash')
        elif selected_option == 1:
            curses.endwin()
            uboot_console()
        else:
            break