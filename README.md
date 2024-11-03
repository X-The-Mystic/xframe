XFrame: A Comprehensive Framework for Cybersecurity and Penetration Testing
=====================================================================

XFrame is a cutting-edge framework designed to facilitate cybersecurity and penetration testing efforts. This comprehensive toolset is tailored to assist security professionals in identifying vulnerabilities, simulating attacks, and strengthening defenses. XFrame encompasses a wide range of features and tools, making it an invaluable asset for any organization seeking to bolster its cybersecurity posture.

Key Features and Tools
--------------------

### Exploitation Framework

XFrame includes a robust exploitation framework, allowing users to identify and exploit vulnerabilities in various systems and applications. The exploits covered are:

- **Baron Samedit, CVE-2021-3156:** The Baron Samedit exploit is a well-documented exploit that allows for privelege escalation on systems running the sudo utility. Valid on sudo versions 1.9.5p1 and below.
- **BlueKeep, CVE-2021-1675:** The BlueKeep exploit is an infamous exploit that allows for remote code execution on systems running the Microsoft Remote Desktop Protocol. Valid on versions 7.9 and below.
- **DejaBlue, CVE-2021-26701 & CVE-2021-26702:** The DejaBlue exploit is a remote code execution vulnerability in the Microsoft Remote Desktop Protocol. Valid on versions 10 and below.
- **EternalChampion, CVE-2017-2671:** The EternalChampion exploit is a remote code execution vulnerability in the Apache HTTP Server, affecting versions 2.4.0 to 2.4.49. It was part of the ShadowBrokers dump, a collection of exploits and tools leaked from the NSA. This exploit allows an attacker to execute arbitrary code on a vulnerable Apache HTTP Server without authentication via the SMB protocol.
- **EternalRomance, CVE-2017-0143:** The EternalRomance exploit is a remote code execution vulnerability in the SMBv1 server in Windows operating systems. It was part of the EternalBlue exploit dump by the ShadowBrokers group. This exploit allows an attacker to execute arbitrary code on the target system without authentication. Valid on Windows XP to Windows Server 2016.
- **EternalSynergy, CVE-2019-1040:** The EternalSynergy exploit is a remote code execution vulnerability in the SMBv3 server in Windows operating systems. It was part of the EternalSynergy exploit dump by the ShadowBrokers group. This exploit allows an attacker to execute arbitrary code on the target system without authentication. Valid on Windows Vista to Windows 10.

### MkDoS: Denial-of-Service Attack Toolkit

MkDoS is a powerful toolkit integrated into XFrame, designed to simulate Denial-of-Service (DoS) and Distributed Denial-of-Service (DDoS) attacks. This tool enables users to test network resilience, identify vulnerabilities, and develop strategies for mitigating such attacks. See the mkdos readme for more information. The vectors covered are:

- **SMS**: Sends a massive amount of SMS messages and calls to a single target.
- **EMAIL**: Sends a massive amount of Email messages to a target.
- **NTP**: NTP amplification is a type of Distributed Denial of Service (DDoS) attack in which the attacker exploits publically-accessible Network Time Protocol (NTP) servers to overwhelm the targeted with User Datagram Protocol (UDP) traffic.
- **SYN**: A SYN flood (half-open attack) is a type of denial-of-service (DDoS) attack which aims to make a server unavailable to legitimate traffic by consuming all available server resources.
- **UDP**: A UDP flood is a type of denial-of-service attack in which a large number of User Datagram Protocol (UDP) packets are sent to a targeted server with the aim of overwhelming that device’s ability to process and respond. The firewall protecting the targeted server can also become exhausted as a result of UDP flooding, resulting in a denial-of-service to legitimate traffic.
- **POD (Ping of Death)**: Ping of Death (a.k.a. PoD) is a type of Denial of Service (DoS) attack in which an attacker attempts to crash, destabilize, or freeze the targeted computer or service by sending malformed or oversized packets using a simple ping command.
- **ICMP**: Ping flood, also known as ICMP flood, is a common Denial of Service (DoS) attack in which an attacker takes down a victim's computer by overwhelming it with ICMP echo requests, also known as pings.
- **HTTP**: HTTP Flood is a type of Distributed Denial of Service (DDoS) attack in which the attacker manipulates HTTP and POST unwanted requests in order to attack a web server or application. These attacks often use interconnected computers that have been taken over with the aid of malware such as Trojan Horses.
- **Slowloris**: Slowloris is a denial-of-service attack program which allows an attacker to overwhelm a targeted server by opening and maintaining many simultaneous HTTP connections between the attacker and the target.
- **Memcached**: A memcached distributed denial-of-service (DDoS) attack is a type of cyber attack in which an attacker attempts to overload a targeted victim with internet traffic. The attacker spoofs requests to a vulnerable UDP memcached* server, which then floods a targeted victim with internet traffic, potentially overwhelming the victim’s resources. While the target’s internet infrastructure is overloaded, new requests cannot be processed and regular traffic is unable to access the internet resource, resulting in denial-of-service.
- **Envenom**: EnVenom is a utility that utilizes the msfvenom utility created by Metasploit's rapid7. It is a DoS attack that uses msfvenom to generate a payload, then encrypts it across the TCP protocol with a tag that decrypts it once it reaches its intended target. Once decrypted, it can do numerous things, from wiping data to opening a reverse TCP shell. The sheer number of these payloads should yield an exhaustion of resources. It is still experimental, though.

### Loki: Network Traffic Analysis and Manipulation

Loki is a sophisticated tool within XFrame, focused on network traffic analysis and manipulation. It allows users to capture, analyze, and modify network traffic in real-time, facilitating the detection of malicious activity and the development of countermeasures.

### Additional Features

* **Vulnerability Scanner**: A comprehensive scanner for identifying vulnerabilities in systems, applications, and networks.
* **Password Cracking**: A suite of tools for password cracking and password strength analysis.
* **Network Mapping**: A feature for mapping network topologies, identifying hosts, and detecting open ports.

Getting Started
---------------

To get started with XFrame, follow these steps:

1. Clone the repository: `git clone https://github.com/X-The-Mystic/xframe.git`
2. Install dependencies: `chmod +x installation.sh && ./installation.sh`
3. CD into the relevant directory (example: `cd exploits/windows/smb_exploits/eternalchampion`)
4. Run the exploit or relevant tool: (example: `python poc1.py`)

Licensing and Disclaimer
-----------------------

XFrame is released under the MIT license. Please note that XFrame is intended for legal and ethical use only. Any misuse or unauthorized use of XFrame may result in severe legal consequences.

Contributing
------------

XFrame is an open-source project, and we welcome contributions from the security community. If you're interested in contributing, please submit a pull request or contact us at xtm@cerberusdev.com.

Stay Secure
------------

XFrame is a powerful tool for cybersecurity professionals. Use it responsibly to strengthen your organization's defenses and contribute to a safer digital world.

