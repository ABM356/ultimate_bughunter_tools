"""
Complete registry of all offensive and defensive security tools.
Each tool has: name, category, team (red/blue/both), install method, tier level.
"""

TOOL_REGISTRY = {

    # =========================================================================
    # RED TEAM — OFFENSIVE TOOLS
    # =========================================================================

    # --- Reconnaissance: Subdomain Enumeration ---
    "amass": {
        "team": "red",
        "category": "recon_subdomain",
        "description": "In-depth attack surface mapping and asset discovery",
        "install": "go",
        "install_cmd": "go install -v github.com/owasp-amass/amass/v4/...@master",
        "tier": 1,
    },
    "subfinder": {
        "team": "red",
        "category": "recon_subdomain",
        "description": "Fast passive subdomain enumeration tool",
        "install": "go",
        "install_cmd": "go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
        "tier": 1,
    },
    "assetfinder": {
        "team": "red",
        "category": "recon_subdomain",
        "description": "Find domains and subdomains related to a given domain",
        "install": "go",
        "install_cmd": "go install github.com/tomnomnom/assetfinder@latest",
        "tier": 1,
    },
    "findomain": {
        "team": "red",
        "category": "recon_subdomain",
        "description": "Cross-platform subdomain enumerator",
        "install": "git",
        "repo": "https://github.com/Findomain/Findomain.git",
        "tier": 1,
    },
    "knockpy": {
        "team": "red",
        "category": "recon_subdomain",
        "description": "Subdomain enumeration via wordlist",
        "install": "pip",
        "install_cmd": "pip3 install knockpy",
        "tier": 1,
    },
    "sublist3r": {
        "team": "red",
        "category": "recon_subdomain",
        "description": "Fast subdomains enumeration tool using OSINT",
        "install": "git",
        "repo": "https://github.com/aboul3la/Sublist3r.git",
        "tier": 1,
    },
    "crtndstry": {
        "team": "red",
        "category": "recon_subdomain",
        "description": "Certificate transparency subdomain finder",
        "install": "git",
        "repo": "https://github.com/nahamsec/crtndstry.git",
        "tier": 1,
    },

    # --- Reconnaissance: DNS ---
    "dnsx": {
        "team": "red",
        "category": "recon_dns",
        "description": "Fast and multi-purpose DNS toolkit",
        "install": "go",
        "install_cmd": "go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest",
        "tier": 1,
    },
    "massdns": {
        "team": "red",
        "category": "recon_dns",
        "description": "High-performance DNS stub resolver for bulk lookups",
        "install": "git",
        "repo": "https://github.com/blechschmidt/massdns.git",
        "tier": 1,
    },
    "dnscan": {
        "team": "red",
        "category": "recon_dns",
        "description": "DNS subdomain scanner with zone transfer check",
        "install": "git",
        "repo": "https://github.com/rbsec/dnscan.git",
        "tier": 1,
    },
    "dnsrecon": {
        "team": "red",
        "category": "recon_dns",
        "description": "DNS enumeration and zone transfer testing",
        "install": "pip",
        "install_cmd": "pip3 install dnsrecon",
        "tier": 2,
    },

    # --- Reconnaissance: HTTP Probing ---
    "httpx": {
        "team": "red",
        "category": "recon_http",
        "description": "Fast HTTP probing toolkit",
        "install": "go",
        "install_cmd": "go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest",
        "tier": 1,
    },
    "httprobe": {
        "team": "red",
        "category": "recon_http",
        "description": "Probe for working HTTP/HTTPS servers",
        "install": "go",
        "install_cmd": "go install github.com/tomnomnom/httprobe@latest",
        "tier": 1,
    },

    # --- Reconnaissance: URL & Parameter Discovery ---
    "katana": {
        "team": "red",
        "category": "recon_crawl",
        "description": "Next-gen crawling and spidering framework",
        "install": "go",
        "install_cmd": "go install github.com/projectdiscovery/katana/cmd/katana@latest",
        "tier": 1,
    },
    "gau": {
        "team": "red",
        "category": "recon_crawl",
        "description": "Fetch known URLs from AlienVault, Wayback Machine, Common Crawl",
        "install": "go",
        "install_cmd": "go install github.com/lc/gau/v2/cmd/gau@latest",
        "tier": 1,
    },
    "waybackurls": {
        "team": "red",
        "category": "recon_crawl",
        "description": "Fetch URLs from the Wayback Machine",
        "install": "go",
        "install_cmd": "go install github.com/tomnomnom/waybackurls@latest",
        "tier": 1,
    },
    "photon": {
        "team": "red",
        "category": "recon_crawl",
        "description": "Incredibly fast crawler designed for OSINT",
        "install": "git",
        "repo": "https://github.com/s0md3v/Photon.git",
        "tier": 1,
    },
    "jsparser": {
        "team": "red",
        "category": "recon_crawl",
        "description": "Parse JavaScript files to find API endpoints",
        "install": "git",
        "repo": "https://github.com/nicksanzotta/JSParser.git",
        "tier": 2,
    },
    "arjun": {
        "team": "red",
        "category": "recon_crawl",
        "description": "HTTP parameter discovery suite",
        "install": "pip",
        "install_cmd": "pip3 install arjun",
        "tier": 2,
    },
    "paramspider": {
        "team": "red",
        "category": "recon_crawl",
        "description": "Mining parameters from dark corners of web archives",
        "install": "git",
        "repo": "https://github.com/devanshbatham/ParamSpider.git",
        "tier": 2,
    },

    # --- Reconnaissance: Port Scanning ---
    "naabu": {
        "team": "red",
        "category": "recon_ports",
        "description": "Fast port scanner written in Go",
        "install": "go",
        "install_cmd": "go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest",
        "tier": 1,
    },
    "masscan": {
        "team": "red",
        "category": "recon_ports",
        "description": "TCP port scanner — transmits 10 million packets per second",
        "install": "git",
        "repo": "https://github.com/robertdavidgraham/masscan.git",
        "tier": 2,
    },
    "rustscan": {
        "team": "red",
        "category": "recon_ports",
        "description": "The modern port scanner — fast then passes to nmap",
        "install": "cargo",
        "install_cmd": "cargo install rustscan",
        "tier": 2,
    },

    # --- Reconnaissance: OSINT ---
    "theHarvester": {
        "team": "both",
        "category": "recon_osint",
        "description": "E-mails, subdomains, hosts, names from public sources",
        "install": "pip",
        "install_cmd": "pip3 install theHarvester",
        "tier": 1,
    },
    "datasploit": {
        "team": "red",
        "category": "recon_osint",
        "description": "OSINT framework for various recon techniques",
        "install": "git",
        "repo": "https://github.com/DataSploit/datasploit.git",
        "tier": 2,
    },
    "asnlookup": {
        "team": "red",
        "category": "recon_osint",
        "description": "ASN lookup tool and execute mass scans",
        "install": "git",
        "repo": "https://github.com/yassineaboukir/Asnlookup.git",
        "tier": 2,
    },
    "gitrob": {
        "team": "red",
        "category": "recon_osint",
        "description": "Find sensitive files in public GitHub repos",
        "install": "go",
        "install_cmd": "go install github.com/michenriksen/gitrob@latest",
        "tier": 2,
    },
    "git-secrets": {
        "team": "both",
        "category": "recon_osint",
        "description": "Prevents committing secrets and credentials to git repos",
        "install": "git",
        "repo": "https://github.com/awslabs/git-secrets.git",
        "tier": 1,
    },
    "trufflehog": {
        "team": "both",
        "category": "recon_osint",
        "description": "Find credentials in Git repos, S3 buckets, and more",
        "install": "pip",
        "install_cmd": "pip3 install trufflehog",
        "tier": 2,
    },

    # --- Reconnaissance: Screenshots ---
    "eyewitness": {
        "team": "red",
        "category": "recon_screenshot",
        "description": "Take screenshots of websites and identify default creds",
        "install": "git",
        "repo": "https://github.com/RedSiege/EyeWitness.git",
        "tier": 1,
    },
    "aquatone": {
        "team": "red",
        "category": "recon_screenshot",
        "description": "Visual inspection of websites across large attack surfaces",
        "install": "git",
        "repo": "https://github.com/michenriksen/aquatone.git",
        "tier": 1,
    },
    "gowitness": {
        "team": "red",
        "category": "recon_screenshot",
        "description": "Web screenshot utility using Chrome Headless",
        "install": "go",
        "install_cmd": "go install github.com/sensepost/gowitness@latest",
        "tier": 2,
    },

    # --- Vulnerability Scanning ---
    "nuclei": {
        "team": "red",
        "category": "vuln_scanning",
        "description": "Fast template-based vulnerability scanner",
        "install": "go",
        "install_cmd": "go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest",
        "tier": 1,
    },
    "nikto": {
        "team": "red",
        "category": "vuln_scanning",
        "description": "Web server scanner — tests for dangerous files, outdated software",
        "install": "git",
        "repo": "https://github.com/sullo/nikto.git",
        "tier": 1,
    },
    "wpscan": {
        "team": "red",
        "category": "vuln_scanning",
        "description": "WordPress vulnerability scanner",
        "install": "gem",
        "install_cmd": "gem install wpscan",
        "tier": 1,
    },
    "cmsmap": {
        "team": "red",
        "category": "vuln_scanning",
        "description": "CMS vulnerability scanner (WordPress, Joomla, Drupal)",
        "install": "git",
        "repo": "https://github.com/Dionach/CMSmap.git",
        "tier": 2,
    },
    "retire_js": {
        "team": "both",
        "category": "vuln_scanning",
        "description": "Scanner detecting use of JavaScript libraries with known vulnerabilities",
        "install": "npm",
        "install_cmd": "npm install -g retire",
        "tier": 1,
    },
    "trivy": {
        "team": "both",
        "category": "vuln_scanning",
        "description": "Comprehensive vulnerability scanner for containers, filesystems, repos",
        "install": "script",
        "install_cmd": "curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin",
        "tier": 2,
    },
    "grype": {
        "team": "blue",
        "category": "vuln_scanning",
        "description": "Vulnerability scanner for container images and filesystems",
        "install": "script",
        "install_cmd": "curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin",
        "tier": 3,
    },

    # --- Web Application Testing: SQLi ---
    "sqlmap": {
        "team": "red",
        "category": "web_sqli",
        "description": "Automatic SQL injection and database takeover tool",
        "install": "pip",
        "install_cmd": "pip3 install sqlmap",
        "tier": 1,
    },

    # --- Web Application Testing: XSS ---
    "xsstrike": {
        "team": "red",
        "category": "web_xss",
        "description": "Advanced XSS scanner with fuzzing engine",
        "install": "git",
        "repo": "https://github.com/s0md3v/XSStrike.git",
        "tier": 1,
    },
    "dalfox": {
        "team": "red",
        "category": "web_xss",
        "description": "Fast parameter analysis and XSS scanner",
        "install": "go",
        "install_cmd": "go install github.com/hahwul/dalfox/v2@latest",
        "tier": 2,
    },

    # --- Web Application Testing: SSRF ---
    "ssrfdetector": {
        "team": "red",
        "category": "web_ssrf",
        "description": "Server-side request forgery detection tool",
        "install": "git",
        "repo": "https://github.com/JacobReynolds/ssrfDetector.git",
        "tier": 2,
    },

    # --- Web Application Testing: XXE ---
    "xxeinjector": {
        "team": "red",
        "category": "web_xxe",
        "description": "XXE injection automation tool",
        "install": "git",
        "repo": "https://github.com/enjoiz/XXEinjector.git",
        "tier": 2,
    },
    "oxml_xxe": {
        "team": "red",
        "category": "web_xxe",
        "description": "XXE exploitation in OXML file formats",
        "install": "git",
        "repo": "https://github.com/BuffaloWill/oxml_xxe.git",
        "tier": 3,
    },

    # --- Web Application Testing: LFI/RFI ---
    "lfisuite": {
        "team": "red",
        "category": "web_lfi",
        "description": "Local File Inclusion exploitation and scanner",
        "install": "git",
        "repo": "https://github.com/D35m0nd142/LFISuite.git",
        "tier": 2,
    },

    # --- Web Application Testing: CORS ---
    "corstest": {
        "team": "red",
        "category": "web_cors",
        "description": "CORS misconfiguration scanner",
        "install": "git",
        "repo": "https://github.com/RUB-NDS/CORStest.git",
        "tier": 2,
    },

    # --- Web Application Testing: JWT ---
    "jwt_tool": {
        "team": "red",
        "category": "web_jwt",
        "description": "Toolkit for testing, tweaking and cracking JSON Web Tokens",
        "install": "git",
        "repo": "https://github.com/ticarpi/jwt_tool.git",
        "tier": 2,
    },

    # --- Web Application Testing: Command Injection ---
    "commix": {
        "team": "red",
        "category": "web_cmdi",
        "description": "Automated OS command injection exploitation",
        "install": "pip",
        "install_cmd": "pip3 install commix",
        "tier": 2,
    },

    # --- Web Application Testing: Serialization ---
    "ysoserial": {
        "team": "red",
        "category": "web_deserialization",
        "description": "Java deserialization exploit generation",
        "install": "git",
        "repo": "https://github.com/frohoff/ysoserial.git",
        "tier": 3,
    },
    "phpggc": {
        "team": "red",
        "category": "web_deserialization",
        "description": "PHP unserialize() gadget chains",
        "install": "git",
        "repo": "https://github.com/ambionics/phpggc.git",
        "tier": 3,
    },

    # --- Directory / File Brute-Forcing ---
    "ffuf": {
        "team": "red",
        "category": "brute_dir",
        "description": "Fast web fuzzer written in Go",
        "install": "go",
        "install_cmd": "go install github.com/ffuf/ffuf/v2@latest",
        "tier": 1,
    },
    "feroxbuster": {
        "team": "red",
        "category": "brute_dir",
        "description": "Fast, simple, recursive content discovery tool",
        "install": "cargo",
        "install_cmd": "cargo install feroxbuster",
        "tier": 1,
    },
    "gobuster": {
        "team": "red",
        "category": "brute_dir",
        "description": "Directory/file, DNS and VHost busting tool",
        "install": "go",
        "install_cmd": "go install github.com/OJ/gobuster/v3@latest",
        "tier": 1,
    },
    "dirsearch": {
        "team": "red",
        "category": "brute_dir",
        "description": "Web path discovery via brute-force",
        "install": "pip",
        "install_cmd": "pip3 install dirsearch",
        "tier": 1,
    },
    "wfuzz": {
        "team": "red",
        "category": "brute_dir",
        "description": "Web application fuzzer",
        "install": "pip",
        "install_cmd": "pip3 install wfuzz",
        "tier": 2,
    },
    "bfac": {
        "team": "red",
        "category": "brute_dir",
        "description": "Backup file artifacts checker",
        "install": "git",
        "repo": "https://github.com/mazen160/bfac.git",
        "tier": 2,
    },

    # --- Password / Credential Attacks ---
    "hydra": {
        "team": "red",
        "category": "brute_password",
        "description": "Network logon cracker supporting many protocols",
        "install": "git",
        "repo": "https://github.com/vanhauser-thc/thc-hydra.git",
        "tier": 2,
    },
    "patator": {
        "team": "red",
        "category": "brute_password",
        "description": "Multi-purpose brute-forcer with modular design",
        "install": "git",
        "repo": "https://github.com/lanjelot/patator.git",
        "tier": 3,
    },
    "changeme": {
        "team": "red",
        "category": "brute_password",
        "description": "Default credential scanner",
        "install": "git",
        "repo": "https://github.com/ztgrace/changeme.git",
        "tier": 1,
    },

    # --- Exploitation Frameworks ---
    "searchsploit": {
        "team": "red",
        "category": "exploit",
        "description": "Offline copy of Exploit-DB with search capabilities",
        "install": "git",
        "repo": "https://gitlab.com/exploit-database/exploitdb.git",
        "tier": 2,
    },
    "getsploit": {
        "team": "red",
        "category": "exploit",
        "description": "Search and download exploits from multiple sources",
        "install": "git",
        "repo": "https://github.com/vulnersCom/getsploit.git",
        "tier": 2,
    },
    "findsploit": {
        "team": "red",
        "category": "exploit",
        "description": "Find exploits in local and online databases",
        "install": "git",
        "repo": "https://github.com/1N3/Findsploit.git",
        "tier": 2,
    },
    "sn1per": {
        "team": "red",
        "category": "exploit",
        "description": "Automated pentest recon scanner",
        "install": "git",
        "repo": "https://github.com/1N3/Sn1per.git",
        "tier": 3,
    },

    # --- Network Tools ---
    "ground-control": {
        "team": "red",
        "category": "network",
        "description": "Collection of scripts for SSRF and open redirect testing",
        "install": "git",
        "repo": "https://github.com/jobertabma/ground-control.git",
        "tier": 2,
    },
    "virtual-host-discovery": {
        "team": "red",
        "category": "network",
        "description": "Enumerate virtual hosts on a server",
        "install": "git",
        "repo": "https://github.com/jobertabma/virtual-host-discovery.git",
        "tier": 2,
    },
    "race-the-web": {
        "team": "red",
        "category": "network",
        "description": "Race condition testing in web applications",
        "install": "git",
        "repo": "https://github.com/TheHackerDev/race-the-web.git",
        "tier": 3,
    },

    # --- Cloud Security (Offensive) ---
    "cloudfox": {
        "team": "red",
        "category": "cloud_offensive",
        "description": "Find exploitable attack paths in cloud infrastructure",
        "install": "go",
        "install_cmd": "go install github.com/BishopFox/cloudfox@latest",
        "tier": 3,
    },
    "pacu": {
        "team": "red",
        "category": "cloud_offensive",
        "description": "AWS exploitation framework",
        "install": "pip",
        "install_cmd": "pip3 install pacu",
        "tier": 3,
    },
    "scoutsuite": {
        "team": "both",
        "category": "cloud_offensive",
        "description": "Multi-cloud security auditing tool",
        "install": "pip",
        "install_cmd": "pip3 install scoutsuite",
        "tier": 3,
    },

    # --- Mobile Security ---
    "mobsf": {
        "team": "red",
        "category": "mobile",
        "description": "Mobile Security Framework — automated pen-testing for Android/iOS",
        "install": "git",
        "repo": "https://github.com/MobSF/Mobile-Security-Framework-MobSF.git",
        "tier": 3,
    },

    # --- Subdomain Takeover ---
    "tko-subs": {
        "team": "red",
        "category": "takeover",
        "description": "Detect and report subdomain takeovers",
        "install": "go",
        "install_cmd": "go install github.com/anshumanbh/tko-subs@latest",
        "tier": 2,
    },
    "subjack": {
        "team": "red",
        "category": "takeover",
        "description": "Subdomain takeover vulnerability checker",
        "install": "go",
        "install_cmd": "go install github.com/haccer/subjack@latest",
        "tier": 2,
    },
    "hostilesubbruteforcer": {
        "team": "red",
        "category": "takeover",
        "description": "Brute-force subdomains and check for takeovers",
        "install": "git",
        "repo": "https://github.com/nahamsec/HostileSubBruteforcer.git",
        "tier": 2,
    },

    # --- S3 Bucket Tools ---
    "lazys3": {
        "team": "red",
        "category": "cloud_s3",
        "description": "Brute-force AWS S3 bucket names",
        "install": "git",
        "repo": "https://github.com/nahamsec/lazys3.git",
        "tier": 2,
    },
    "teh_s3_bucketeers": {
        "team": "red",
        "category": "cloud_s3",
        "description": "Discover S3 buckets via certstream",
        "install": "git",
        "repo": "https://github.com/tomdev/teh_s3_bucketeers.git",
        "tier": 2,
    },

    # --- Git Recon ---
    "gittools": {
        "team": "red",
        "category": "git_recon",
        "description": "Find, download, and extract .git repositories",
        "install": "git",
        "repo": "https://github.com/internetwache/GitTools.git",
        "tier": 2,
    },
    "dvcs-ripper": {
        "team": "red",
        "category": "git_recon",
        "description": "Rip web accessible DVCS repositories (.svn, .hg, .bzr)",
        "install": "git",
        "repo": "https://github.com/kost/dvcs-ripper.git",
        "tier": 3,
    },

    # --- Google Dorking ---
    "googd0rker": {
        "team": "red",
        "category": "dorking",
        "description": "Google dorking automation tool",
        "install": "git",
        "repo": "https://github.com/ZephrFish/GoogD0rker.git",
        "tier": 2,
    },

    # --- Wordlists ---
    "seclists": {
        "team": "both",
        "category": "wordlists",
        "description": "Collection of lists used during security assessments",
        "install": "git",
        "repo": "https://github.com/danielmiessler/SecLists.git",
        "tier": 1,
    },

    # --- Automation / Recon Pipelines ---
    "lazyrecon": {
        "team": "red",
        "category": "automation",
        "description": "Automated recon and scanning pipeline",
        "install": "git",
        "repo": "https://github.com/nahamsec/lazyrecon.git",
        "tier": 1,
    },
    "reconftw": {
        "team": "red",
        "category": "automation",
        "description": "Full automated recon pipeline using multiple tools",
        "install": "git",
        "repo": "https://github.com/six2dez/reconftw.git",
        "tier": 2,
    },

    # =========================================================================
    # BLUE TEAM — DEFENSIVE TOOLS
    # =========================================================================

    # --- Host Hardening & Audit ---
    "lynis": {
        "team": "blue",
        "category": "hardening",
        "description": "Security auditing and hardening tool for Linux",
        "install": "git",
        "repo": "https://github.com/CISOfy/lynis.git",
        "tier": 1,
    },
    "linux_exploit_suggester": {
        "team": "blue",
        "category": "hardening",
        "description": "Suggest applicable kernel exploits based on OS version",
        "install": "git",
        "repo": "https://github.com/The-Z-Labs/linux-exploit-suggester.git",
        "tier": 2,
    },
    "openscap": {
        "team": "blue",
        "category": "hardening",
        "description": "NIST-certified SCAP compliance scanner",
        "install": "apt",
        "install_cmd": "apt-get install -y libopenscap8",
        "tier": 3,
    },

    # --- Network Defense / IDS / IPS ---
    "suricata": {
        "team": "blue",
        "category": "ids_ips",
        "description": "High-performance network IDS, IPS and security monitoring engine",
        "install": "apt",
        "install_cmd": "apt-get install -y suricata",
        "tier": 2,
    },
    "zeek": {
        "team": "blue",
        "category": "ids_ips",
        "description": "Powerful network analysis framework (formerly Bro)",
        "install": "apt",
        "install_cmd": "apt-get install -y zeek",
        "tier": 3,
    },

    # --- Log Analysis & SIEM ---
    "wazuh": {
        "team": "blue",
        "category": "siem",
        "description": "Open-source security monitoring — XDR and SIEM capabilities",
        "install": "script",
        "install_cmd": "curl -sO https://packages.wazuh.com/4.7/wazuh-install.sh",
        "tier": 2,
    },
    "ossec": {
        "team": "blue",
        "category": "siem",
        "description": "Host-based intrusion detection system",
        "install": "git",
        "repo": "https://github.com/ossec/ossec-hids.git",
        "tier": 2,
    },

    # --- Incident Response / Forensics ---
    "volatility3": {
        "team": "blue",
        "category": "forensics",
        "description": "Advanced memory forensics framework",
        "install": "pip",
        "install_cmd": "pip3 install volatility3",
        "tier": 3,
    },
    "chainsaw": {
        "team": "blue",
        "category": "forensics",
        "description": "Rapidly search and hunt through Windows forensic artefacts",
        "install": "cargo",
        "install_cmd": "cargo install chainsaw",
        "tier": 3,
    },

    # --- Threat Intelligence ---
    "yara": {
        "team": "blue",
        "category": "threat_intel",
        "description": "Pattern matching for malware researchers",
        "install": "apt",
        "install_cmd": "apt-get install -y yara",
        "tier": 2,
    },
    "sigma": {
        "team": "blue",
        "category": "threat_intel",
        "description": "Generic signature format for SIEM systems",
        "install": "pip",
        "install_cmd": "pip3 install pySigma",
        "tier": 3,
    },

    # --- Container Security ---
    "falco": {
        "team": "blue",
        "category": "container_security",
        "description": "Cloud-native runtime security (threat detection for containers)",
        "install": "script",
        "install_cmd": "curl -fsSL https://falco.org/script/install | bash",
        "tier": 3,
    },

    # --- Cloud Security (Defensive) ---
    "prowler": {
        "team": "blue",
        "category": "cloud_defensive",
        "description": "AWS/Azure/GCP security assessment and compliance tool",
        "install": "pip",
        "install_cmd": "pip3 install prowler",
        "tier": 3,
    },
    "cloudsplaining": {
        "team": "blue",
        "category": "cloud_defensive",
        "description": "AWS IAM security assessment — identifies violations of least privilege",
        "install": "pip",
        "install_cmd": "pip3 install cloudsplaining",
        "tier": 3,
    },

    # --- Malware Analysis ---
    "capa": {
        "team": "blue",
        "category": "malware_analysis",
        "description": "Identify capabilities in executable files",
        "install": "pip",
        "install_cmd": "pip3 install flare-capa",
        "tier": 4,
    },

    # --- Network Monitoring ---
    "ntopng": {
        "team": "blue",
        "category": "network_monitoring",
        "description": "Web-based network traffic monitoring",
        "install": "apt",
        "install_cmd": "apt-get install -y ntopng",
        "tier": 3,
    },

    # --- WAF / Firewall ---
    "modsecurity": {
        "team": "blue",
        "category": "waf",
        "description": "Open-source web application firewall",
        "install": "apt",
        "install_cmd": "apt-get install -y libapache2-mod-security2",
        "tier": 3,
    },

    # --- Secrets Detection (Defensive) ---
    "gitleaks": {
        "team": "blue",
        "category": "secrets_detection",
        "description": "Detect and prevent hardcoded secrets in git repos",
        "install": "go",
        "install_cmd": "go install github.com/gitleaks/gitleaks/v8@latest",
        "tier": 1,
    },
    "detect-secrets": {
        "team": "blue",
        "category": "secrets_detection",
        "description": "Detect secrets in code before they get committed",
        "install": "pip",
        "install_cmd": "pip3 install detect-secrets",
        "tier": 1,
    },

    # --- SSL/TLS Testing ---
    "testssl": {
        "team": "both",
        "category": "ssl_tls",
        "description": "Testing TLS/SSL encryption on any port",
        "install": "git",
        "repo": "https://github.com/drwetter/testssl.sh.git",
        "tier": 1,
    },
    "sslyze": {
        "team": "both",
        "category": "ssl_tls",
        "description": "Fast SSL/TLS server scanning library",
        "install": "pip",
        "install_cmd": "pip3 install sslyze",
        "tier": 2,
    },
}


def get_tools_by_team(team):
    return {k: v for k, v in TOOL_REGISTRY.items() if v["team"] in (team, "both")}


def get_tools_by_tier(max_tier):
    return {k: v for k, v in TOOL_REGISTRY.items() if v["tier"] <= max_tier}


def get_tools_by_category(category):
    return {k: v for k, v in TOOL_REGISTRY.items() if v["category"] == category}


def get_tool_count():
    red = len(get_tools_by_team("red"))
    blue = len(get_tools_by_team("blue"))
    both = len([v for v in TOOL_REGISTRY.values() if v["team"] == "both"])
    return {"total": len(TOOL_REGISTRY), "red_team": red, "blue_team": blue, "shared": both}


CATEGORIES = {
    "red": {
        "recon_subdomain": "Subdomain Enumeration",
        "recon_dns": "DNS Reconnaissance",
        "recon_http": "HTTP Probing",
        "recon_crawl": "URL & Parameter Discovery",
        "recon_ports": "Port Scanning",
        "recon_osint": "OSINT & Intelligence Gathering",
        "recon_screenshot": "Visual Reconnaissance",
        "vuln_scanning": "Vulnerability Scanning",
        "web_sqli": "SQL Injection",
        "web_xss": "Cross-Site Scripting (XSS)",
        "web_ssrf": "Server-Side Request Forgery",
        "web_xxe": "XML External Entity",
        "web_lfi": "Local/Remote File Inclusion",
        "web_cors": "CORS Misconfiguration",
        "web_jwt": "JWT Exploitation",
        "web_cmdi": "Command Injection",
        "web_deserialization": "Deserialization Attacks",
        "brute_dir": "Directory & File Brute-Forcing",
        "brute_password": "Password & Credential Attacks",
        "exploit": "Exploitation Frameworks",
        "network": "Network Testing",
        "cloud_offensive": "Cloud Offensive Security",
        "cloud_s3": "S3 Bucket Enumeration",
        "mobile": "Mobile Application Security",
        "takeover": "Subdomain Takeover",
        "git_recon": "Git Repository Reconnaissance",
        "dorking": "Google Dorking",
        "wordlists": "Wordlists & Payloads",
        "automation": "Automated Recon Pipelines",
    },
    "blue": {
        "hardening": "Host Hardening & Audit",
        "ids_ips": "Intrusion Detection / Prevention",
        "siem": "SIEM & Log Analysis",
        "forensics": "Incident Response & Forensics",
        "threat_intel": "Threat Intelligence",
        "container_security": "Container Security",
        "cloud_defensive": "Cloud Security (Defensive)",
        "malware_analysis": "Malware Analysis",
        "network_monitoring": "Network Monitoring",
        "waf": "Web Application Firewall",
        "secrets_detection": "Secrets Detection",
    },
    "shared": {
        "ssl_tls": "SSL/TLS Testing",
        "vuln_scanning": "Vulnerability Scanning",
    },
}
