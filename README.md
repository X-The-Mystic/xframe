XFrame: A Comprehensive Framework for Cybersecurity and Penetration Testing
=====================================================================

XFrame is a cutting-edge framework designed to facilitate cybersecurity and penetration testing efforts. This comprehensive toolset is tailored to assist security professionals in identifying vulnerabilities, simulating attacks, and strengthening defenses. XFrame encompasses a wide range of features and tools, making it an invaluable asset for any organization seeking to bolster its cybersecurity posture. I specifically designed it under the philosophy that no knowledge deserves to be censored, and that the world of malware need be no different. Please note that it is still under heavy development, and some parts may be further behind than others.

Key Features and Tools
--------------------

## Exploitation Framework

XFrame includes a robust exploitation framework, allowing users to identify and exploit vulnerabilities in various systems and applications. The exploits covered are:

- **Baron Samedit, CVE-2021-3156:** The Baron Samedit exploit is a well-documented exploit that allows for privelege escalation on systems running the sudo utility. Valid on sudo versions 1.9.5p1 and below.
- **BlueKeep, CVE-2021-1675:** The BlueKeep exploit is an infamous exploit that allows for remote code execution on systems running the Microsoft Remote Desktop Protocol. Valid on versions 7.9 and below.
- **DejaBlue, CVE-2021-26701 & CVE-2021-26702:** The DejaBlue exploit is a remote code execution vulnerability in the Microsoft Remote Desktop Protocol. Valid on versions 10 and below.
- **EternalChampion, CVE-2017-2671:** The EternalChampion exploit is a remote code execution vulnerability in the Apache HTTP Server, affecting versions 2.4.0 to 2.4.49. It was part of the ShadowBrokers dump, a collection of exploits and tools leaked from the NSA. This exploit allows an attacker to execute arbitrary code on a vulnerable Apache HTTP Server without authentication via the SMB protocol.
- **EternalRomance, CVE-2017-0143:** The EternalRomance exploit is a remote code execution vulnerability in the SMBv1 server in Windows operating systems. It was part of the EternalBlue exploit dump by the ShadowBrokers group. This exploit allows an attacker to execute arbitrary code on the target system without authentication. Valid on Windows XP to Windows Server 2016.
- **EternalSynergy, CVE-2019-1040:** The EternalSynergy exploit is a remote code execution vulnerability in the SMBv3 server in Windows operating systems. It was part of the EternalSynergy exploit dump by the ShadowBrokers group. This exploit allows an attacker to execute arbitrary code on the target system without authentication. Valid on Windows Vista to Windows 10.
- **Log4Shell, CVE-2021-44228:** The Log4Shell exploit is a critical remote code execution vulnerability in the Apache Log4j 2 library, a popular Java-based logging utility. This vulnerability allows an attacker to execute arbitrary code on a server by sending a specially crafted request that includes a malicious payload. The exploit leverages the JNDI (Java Naming and Directory Interface) lookup feature in Log4j 2, which can be tricked into loading and executing code from an attacker-controlled server. This vulnerability affects Log4j versions 2.0-beta9 to 2.14.1 and has been widely exploited in the wild, posing a significant threat to any application using the vulnerable versions of Log4j 2.
- **AlpineFire**: This exploit targets web applications by uploading a PHP web shell to gain remote code execution capabilities. It involves authenticating with the target, uploading a malicious script, and interacting with the shell to execute commands on the server.
- **BlackPulse**: A critical remote code execution vulnerability in the OpenSSL library. It exploits a buffer overflow triggered by a malformed certificate, allowing arbitrary code execution on vulnerable servers. This exploit is particularly dangerous due to its potential for widespread impact.
- **EtherSalt**: An exploit targeting specific versions of the Postfix mail server. It involves crafting messages with shellcode to exploit buffer overflows, allowing remote code execution. The exploit is tailored for different platform settings, making it versatile against various Postfix configurations.
- **JewelRunner**: This exploit focuses on uploading and executing files on a target system. It includes options for specifying target OS, IP address, and file paths, making it adaptable for different environments. The exploit is designed to bypass security measures and gain unauthorized access. Affects Apache 2.62
- **MysticTunnel**: A tunneling tool that facilitates secure communication between a client and server. It is used to bypass network restrictions and establish a covert channel for data exfiltration or command execution.
- **PolarWinds**: This exploit leverages path traversal and remote code execution vulnerabilities in web applications. It involves sending crafted requests to execute commands on the server, often used to gain unauthorized access or escalate privileges. Affects Apache 2.41.
- **PseudoEphedrine**: A privilege escalation exploit targeting the Linux kernel. It exploits a race condition to gain root privileges, posing a significant threat to multi-user environments.
- **goldenRAG**: The goldenRAG exploit targets Generative AI (GenAI) ecosystems by leveraging adversarial self-replicating prompts. It is designed to infiltrate GenAI-powered applications, such as email assistants, to perform malicious activities like spamming and data exfiltration. The exploit manipulates the GenAI models to replicate and propagate the malicious prompts across the ecosystem, affecting models like Gemini Pro, ChatGPT 4.0, and LLaVA. This exploit demonstrates the potential risks associated with interconnected GenAI services and highlights the need for robust security measures in AI-driven environments.
- **FlowSteering**: The FlowSteering exploit focuses on manipulating GenAI-powered applications by perturbing images to generate specific text outputs. It targets email applications by sending emails with manipulated images that influence the application's behavior. The exploit involves creating perturbations that steer the application towards specific actions, such as forwarding or classifying emails as spam. This technique showcases the vulnerabilities in GenAI systems when handling multimedia inputs and emphasizes the importance of securing AI models against adversarial attacks.


### MkDoS: Denial-of-Service Attack Toolkit

MkDoS is a powerful toolkit integrated into XFrame, designed to simulate Denial-of-Service (DoS) and Distributed Denial-of-Service (DDoS) attacks. This tool enables users to test network resilience, identify vulnerabilities, and develop strategies for mitigating such attacks. See the mkdos readme for more information. The vectors covered are:

- **SMS**: Sends a massive amount of SMS messages and calls to a single target.
- **EMAIL**: Sends a massive amount of Email messages to a target.
- **NTP**: NTP amplification is a type of Distributed Denial of Service (DDoS) attack in which the attacker exploits publically-accessible Network Time Protocol (NTP) servers to overwhelm the targeted with User Datagram Protocol (UDP) traffic.
- **SYN**: A SYN flood (half-open attack) is a type of denial-of-service (DDoS) attack which aims to make a server unavailable to legitimate traffic by consuming all available server resources.
- **UDP**: A UDP flood is a type of denial-of-service attack in which a large number of User Datagram Protocol (UDP) packets are sent to a targeted server with the aim of overwhelming that device's ability to process and respond. The firewall protecting the targeted server can also become exhausted as a result of UDP flooding, resulting in a denial-of-service to legitimate traffic.
- **POD (Ping of Death)**: Ping of Death (a.k.a. PoD) is a type of Denial of Service (DoS) attack in which an attacker attempts to crash, destabilize, or freeze the targeted computer or service by sending malformed or oversized packets using a simple ping command.
- **ICMP**: Ping flood, also known as ICMP flood, is a common Denial of Service (DoS) attack in which an attacker takes down a victim's computer by overwhelming it with ICMP echo requests, also known as pings.
- **HTTP**: HTTP Flood is a type of Distributed Denial of Service (DDoS) attack in which the attacker manipulates HTTP and POST unwanted requests in order to attack a web server or application. These attacks often use interconnected computers that have been taken over with the aid of malware such as Trojan Horses.
- **Slowloris**: Slowloris is a denial-of-service attack program which allows an attacker to overwhelm a targeted server by opening and maintaining many simultaneous HTTP connections between the attacker and the target.
- **Memcached**: A memcached distributed denial-of-service (DDoS) attack is a type of cyber attack in which an attacker attempts to overload a targeted victim with internet traffic. The attacker spoofs requests to a vulnerable UDP memcached* server, which then floods a targeted victim with internet traffic, potentially overwhelming the victim's resources. While the target's internet infrastructure is overloaded, new requests cannot be processed and regular traffic is unable to access the internet resource, resulting in denial-of-service.
- **Envenom**: EnVenom is a utility that utilizes the msfvenom utility created by Metasploit's rapid7. It is a DoS attack that uses msfvenom to generate a payload, then encrypts it across the TCP protocol with a tag that decrypts it once it reaches its intended target. Once decrypted, it can do numerous things, from wiping data to opening a reverse TCP shell. The sheer number of these payloads should yield an exhaustion of resources. It is still experimental, though.

### Additional Features

- **Vulnerability Scanner**: A comprehensive scanner for identifying vulnerabilities in systems, applications, and networks.
- **Password Cracking**: A suite of tools for password cracking and password strength analysis.
- **Network Mapping**: A feature for mapping network topologies, identifying hosts, and detecting open ports.

Getting Started
---------------

To get started with XFrame, follow these steps:

1. Clone the repository: `git clone https://github.com/X-The-Mystic/xframe.git`
2. Install dependencies: `chmod +x installation.sh && ./installation.sh`
3. CD into the relevant directory (example: `cd malware/exploits/windows/eternalleaks/eternalchampion`)
4. Run the exploit or relevant tool: (example: `python poc1.py`)

Licensing and Disclaimer
-----------------------

XFrame is released under the MIT license. Please note that XFrame is intended for legal and ethical use only. Any misuse or unauthorized use of XFrame may result in severe legal consequences.

Contributing
------------

XFrame is an open-source project, and we welcome contributions from the security community. If you're interested in contributing, please submit a pull request or contact us at <xtm@cerberusdev.com>.

Stay Secure
------------
