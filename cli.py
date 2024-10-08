# cli.py

import argparse
from core import exploit, attack, utils

def main():
    parser = argparse.ArgumentParser(description="My Framework CLI")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Subcommand: exploit
    parser_exploit = subparsers.add_parser("exploit", help="Run an exploit")
    parser_exploit.add_argument("target", type=str, help="Target for the exploit")
    parser_exploit.add_argument("--type", type=str, choices=["sudoedit", "windows"], required=True, help="Type of exploit")
    
    # Subcommand: attack
    parser_attack = subparsers.add_parser("attack", help="Run an attack")
    parser_attack.add_argument("target", type=str, help="Target for the attack")
    parser_attack.add_argument("--method", type=str, choices=["brute", "dos"], required=True, help="Method of attack")
    
    # Subcommand: utils
    parser_utils = subparsers.add_parser("utils", help="Utility functions")
    parser_utils.add_argument("--info", action="store_true", help="Get system info")
    
    args = parser.parse_args()
    
    if args.command == "exploit":
        run_exploit(args)
    elif args.command == "attack":
        run_attack(args)
    elif args.command == "utils":
        run_utils(args)
    else:
        parser.print_help()

def run_exploit(args):
    if args.type == "sudoedit":
        exploit.sudoedit_exploit.run(args.target)
    elif args.type == "windows":
        exploit.windows_exploit.run(args.target)

def run_attack(args):
    if args.method == "brute":
        attack.brute_force.run(args.target)
    elif args.method == "dos":
        attack.dos.run(args.target)

def run_utils(args):
    if args.info:
        utils.system_info()

if __name__ == "__main__":
    main()