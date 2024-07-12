import json
import copy
import base64


plugins = [
    {
        "id": "general",
        "stream": "partial",
        "name": "General",
        "description": "The general settings for the server",
        "version": "0.1",
        "type": "core",
        "method": "manual",
        "page": False,
        "settings": {
            "IS_LOADING": {
                "context": "global",
                "default": "no",
                "help": "Internal use : set to yes when BW is loading.",
                "id": "internal-use-loading",
                "label": "internal use loading",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "NGINX_PREFIX": {
                "context": "global",
                "default": "/etc/nginx/",
                "help": "Where nginx will search for configurations.",
                "id": "nginx-prefix",
                "label": "nginx prefix",
                "regex": "^(\\/[\\-\\w.\\s]+)*\\/$",
                "type": "text",
            },
            "HTTP_PORT": {
                "context": "global",
                "default": "8080",
                "help": "HTTP port number which bunkerweb binds to.",
                "id": "http-port",
                "label": "HTTP port",
                "regex": "^\\d+$",
                "type": "text",
            },
            "HTTPS_PORT": {
                "context": "global",
                "default": "8443",
                "help": "HTTPS port number which bunkerweb binds to.",
                "id": "https-port",
                "label": "HTTPS port",
                "regex": "^\\d+$",
                "type": "text",
            },
            "MULTISITE": {
                "context": "global",
                "default": "no",
                "help": "Multi site activation.",
                "id": "multisite",
                "label": "Multisite",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "SERVER_NAME": {
                "context": "multisite",
                "default": "www.example.com",
                "help": "List of the virtual hosts served by bunkerweb.",
                "id": "server-name",
                "label": "Server name",
                "regex": "^((\\S{1,255})(?!.*\\s\\2(\\s|$)))?(\\s(\\S{1,255})(?!.*\\s\\5(\\s|$)))*$",
                "type": "text",
            },
            "WORKER_PROCESSES": {
                "context": "global",
                "default": "auto",
                "help": "Number of worker processes.",
                "id": "worker-processes",
                "label": "Worker processes",
                "regex": "^(auto|\\d+)$",
                "type": "text",
            },
            "WORKER_RLIMIT_NOFILE": {
                "context": "global",
                "default": "2048",
                "help": "Maximum number of open files for worker processes.",
                "id": "worker-rlimit-nofile",
                "label": "Open files per worker",
                "regex": "^\\d+$",
                "type": "text",
            },
            "WORKER_CONNECTIONS": {
                "context": "global",
                "default": "1024",
                "help": "Maximum number of connections per worker.",
                "id": "worker-connections",
                "label": "Connections per worker",
                "regex": "^\\d+$",
                "type": "text",
            },
            "LOG_FORMAT": {
                "context": "global",
                "default": '$host $remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"',
                "help": "The format to use for access logs.",
                "id": "log-format",
                "label": "Log format",
                "regex": "^.*$",
                "type": "text",
            },
            "LOG_LEVEL": {
                "context": "global",
                "default": "notice",
                "help": "The level to use for error logs.",
                "id": "log-level",
                "label": "Log level",
                "regex": "^(debug|info|notice|warn|error|crit|alert|emerg)$",
                "type": "select",
                "select": [
                    "alert",
                    "crit",
                    "debug",
                    "emerg",
                    "error",
                    "info",
                    "notice",
                    "warn",
                ],
            },
            "DNS_RESOLVERS": {
                "context": "global",
                "default": "127.0.0.11",
                "help": "DNS addresses of resolvers to use.",
                "id": "dns-resolvers",
                "label": "DNS resolvers",
                "regex": "^(?! )(( *[^ ]+)(?!.*\\2))*$",
                "type": "text",
            },
            "DATASTORE_MEMORY_SIZE": {
                "context": "global",
                "default": "64m",
                "help": "Size of the internal datastore.",
                "id": "datastore-memory-size",
                "label": "Datastore memory size",
                "regex": "^\\d+[kKmMgG]?$",
                "type": "text",
            },
            "CACHESTORE_MEMORY_SIZE": {
                "context": "global",
                "default": "64m",
                "help": "Size of the internal cachestore.",
                "id": "cachestore-memory-size",
                "label": "Cachestore memory size",
                "regex": "^\\d+[kKmMgG]?$",
                "type": "text",
            },
            "CACHESTORE_IPC_MEMORY_SIZE": {
                "context": "global",
                "default": "16m",
                "help": "Size of the internal cachestore (ipc).",
                "id": "cachestore-ipc-memory-size",
                "label": "Cachestore ipc memory size",
                "regex": "^\\d+[kKmMgG]?$",
                "type": "text",
            },
            "CACHESTORE_MISS_MEMORY_SIZE": {
                "context": "global",
                "default": "16m",
                "help": "Size of the internal cachestore (miss).",
                "id": "cachestore-miss-memory-size",
                "label": "Cachestore miss memory size",
                "regex": "^\\d+[kKmMgG]?$",
                "type": "text",
            },
            "CACHESTORE_LOCKS_MEMORY_SIZE": {
                "context": "global",
                "default": "16m",
                "help": "Size of the internal cachestore (locks).",
                "id": "cachestore-locks-memory-size",
                "label": "Cachestore locks memory size",
                "regex": "^\\d+[kKmMgG]?$",
                "type": "text",
            },
            "USE_API": {
                "context": "global",
                "default": "yes",
                "help": "Activate the API to control BunkerWeb.",
                "id": "use-api",
                "label": "Activate API",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "API_HTTP_PORT": {
                "context": "global",
                "default": "5000",
                "help": "Listen port number for the API.",
                "id": "api-http-listen",
                "label": "API port number",
                "regex": "^\\d+$",
                "type": "text",
            },
            "API_LISTEN_IP": {
                "context": "global",
                "default": "0.0.0.0",
                "help": "Listen IP address for the API.",
                "id": "api-ip-listen",
                "label": "API listen IP",
                "regex": "^.*$",
                "type": "text",
            },
            "API_SERVER_NAME": {
                "context": "global",
                "default": "bwapi",
                "help": "Server name (virtual host) for the API.",
                "id": "api-server-name",
                "label": "API server name",
                "regex": "^[^ ]{1,255}$",
                "type": "text",
            },
            "API_WHITELIST_IP": {
                "context": "global",
                "default": "127.0.0.0/8",
                "help": "List of IP/network allowed to contact the API.",
                "id": "api-whitelist-ip",
                "label": "API whitelist IP",
                "regex": "^(?! )( *(((\\b25[0-5]|\\b2[0-4]\\d|\\b[01]?\\d\\d?)(\\.(25[0-5]|2[0-4]\\d|[01]?\\d\\d?)){3})(\\/([1-2][0-9]?|3[0-2]?|[04-9]))?|(([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]Z{0,4}){0,4}%[0-9a-zA-Z]+|::(ffff(:0{1,4})?:)?((25[0-5]|(2[0-4]|1?\\d)?\\d)\\.){3}(25[0-5]|(2[0-4]|1?\\d)?\\d)|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1?\\d)?\\d)\\.){3}(25[0-5]|(2[0-4]|1?\\d)?\\d))(\\/(12[0-8]|1[01][0-9]|[0-9][0-9]?))?)(?!.*\\D\\2([^\\d\\/]|$)) *)*$",
                "type": "text",
            },
            "AUTOCONF_MODE": {
                "context": "global",
                "default": "no",
                "help": "Enable Autoconf Docker integration.",
                "id": "autoconf-mode",
                "label": "Autoconf mode",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "SWARM_MODE": {
                "context": "global",
                "default": "no",
                "help": "Enable Docker Swarm integration.",
                "id": "swarm-mode",
                "label": "Swarm mode",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "KUBERNETES_MODE": {
                "context": "global",
                "default": "no",
                "help": "Enable Kubernetes integration.",
                "id": "kubernetes-mode",
                "label": "Kubernetes mode",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "SERVER_TYPE": {
                "context": "multisite",
                "default": "http",
                "help": "Server type : http or stream.",
                "id": "server-type",
                "label": "Server type",
                "regex": "^(http|stream)$",
                "type": "select",
                "select": ["http", "stream"],
            },
            "LISTEN_STREAM": {
                "context": "multisite",
                "default": "yes",
                "help": "Enable listening for non-ssl (passthrough).",
                "id": "listen-stream",
                "label": "Listen stream",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "LISTEN_STREAM_PORT": {
                "context": "multisite",
                "default": "1337",
                "help": "Listening port for non-ssl (passthrough).",
                "id": "listen-stream-port",
                "label": "Listen stream port",
                "regex": "^[0-9]+$",
                "type": "text",
            },
            "LISTEN_STREAM_PORT_SSL": {
                "context": "multisite",
                "default": "4242",
                "help": "Listening port for ssl (passthrough).",
                "id": "listen-stream-port-ssl",
                "label": "Listen stream port ssl",
                "regex": "^[0-9]+$",
                "type": "text",
            },
            "USE_UDP": {
                "context": "multisite",
                "default": "no",
                "help": "UDP listen instead of TCP (stream).",
                "id": "use-udp",
                "label": "Listen UDP",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "USE_IPV6": {
                "context": "global",
                "default": "no",
                "help": "Enable IPv6 connectivity.",
                "id": "use-ipv6",
                "label": "Use IPv6",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "IS_DRAFT": {
                "context": "multisite",
                "default": "no",
                "help": "Internal use : set to yes when the service is in draft mode.",
                "id": "internal-use-draft",
                "label": "internal use draft",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "TIMERS_LOG_LEVEL": {
                "context": "global",
                "default": "debug",
                "help": "Log level for timers.",
                "id": "timers-log-level",
                "label": "Timers log level",
                "regex": "^(debug|info|notice|warn|err|crit|alert|emerg)$",
                "type": "select",
                "select": [
                    "alert",
                    "crit",
                    "debug",
                    "emerg",
                    "err",
                    "info",
                    "notice",
                    "warn",
                ],
            },
            "BUNKERWEB_INSTANCES": {
                "context": "global",
                "default": "127.0.0.1",
                "help": "List of BunkerWeb instances separated with spaces (format : fqdn-or-ip:5000 http://fqdn-or-ip:5000)",
                "id": "bunkerweb-instances",
                "label": "BunkerWeb instances",
                "regex": "^.*$",
                "type": "text",
            },
        },
        "checksum": None,
    },
    {
        "id": "antibot",
        "stream": "no",
        "name": "Antibot",
        "description": "Bot detection by using a challenge.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": True,
        "settings": {
            "USE_ANTIBOT": {
                "context": "multisite",
                "default": "no",
                "help": "Activate antibot feature.",
                "id": "use-antibot",
                "label": "Antibot challenge",
                "regex": "^(no|cookie|javascript|captcha|recaptcha|hcaptcha|turnstile)$",
                "type": "select",
                "select": [
                    "captcha",
                    "cookie",
                    "hcaptcha",
                    "javascript",
                    "no",
                    "recaptcha",
                    "turnstile",
                ],
            },
            "ANTIBOT_URI": {
                "context": "multisite",
                "default": "/challenge",
                "help": "Unused URI that clients will be redirected to to solve the challenge.",
                "id": "antibot-uri",
                "label": "Antibot URL",
                "regex": "^\\/[\\w\\].~:\\/?#\\[@!$\\&'\\(\\)*+,;=\\-]*$",
                "type": "text",
            },
            "ANTIBOT_TIME_RESOLVE": {
                "context": "multisite",
                "default": "60",
                "help": "Maximum time (in seconds) clients have to resolve the challenge. Once this time has passed, a new challenge will be generated.",
                "id": "antibot-time-resolve",
                "label": "Time to resolve",
                "regex": "^[0-9]+$",
                "type": "text",
            },
            "ANTIBOT_TIME_VALID": {
                "context": "multisite",
                "default": "86400",
                "help": "Maximum validity time of solved challenges. Once this time has passed, clients will need to resolve a new one.",
                "id": "antibot-time-valid",
                "label": "Time valid",
                "regex": "^[0-9]+$",
                "type": "text",
            },
            "ANTIBOT_RECAPTCHA_SCORE": {
                "context": "multisite",
                "default": "0.7",
                "help": "Minimum score required for reCAPTCHA challenge.",
                "id": "antibot-recaptcha-score",
                "label": "reCAPTCHA score",
                "regex": "^(0\\.[1-9]|1\\.0)$",
                "type": "text",
            },
            "ANTIBOT_RECAPTCHA_SITEKEY": {
                "context": "multisite",
                "default": "",
                "help": "Sitekey for reCAPTCHA challenge.",
                "id": "antibot-recaptcha-sitekey",
                "label": "reCAPTCHA sitekey",
                "regex": "^[\\w\\-]*$",
                "type": "text",
            },
            "ANTIBOT_RECAPTCHA_SECRET": {
                "context": "multisite",
                "default": "",
                "help": "Secret for reCAPTCHA challenge.",
                "id": "antibot-recaptcha-secret",
                "label": "reCAPTCHA secret",
                "regex": "^[\\w\\-]*$",
                "type": "password",
            },
            "ANTIBOT_HCAPTCHA_SITEKEY": {
                "context": "multisite",
                "default": "",
                "help": "Sitekey for hCaptcha challenge.",
                "id": "antibot-hcaptcha-sitekey",
                "label": "hCaptcha sitekey",
                "regex": "^[a-zA-Z0-9\\-]*$",
                "type": "text",
            },
            "ANTIBOT_HCAPTCHA_SECRET": {
                "context": "multisite",
                "default": "",
                "help": "Secret for hCaptcha challenge.",
                "id": "antibot-hcaptcha-secret",
                "label": "hCaptcha secret",
                "regex": "^\\w*$",
                "type": "password",
            },
            "ANTIBOT_TURNSTILE_SITEKEY": {
                "context": "multisite",
                "default": "",
                "help": "Sitekey for Turnstile challenge.",
                "id": "antibot-turnstile-sitekey",
                "label": "Turnstile sitekey",
                "regex": "^(0x[\\w\\-]+)?$",
                "type": "text",
            },
            "ANTIBOT_TURNSTILE_SECRET": {
                "context": "multisite",
                "default": "",
                "help": "Secret for Turnstile challenge.",
                "id": "antibot-turnstile-secret",
                "label": "Turnstile secret",
                "regex": "^(0x[\\w\\-]+)?$",
                "type": "password",
            },
        },
        "checksum": None,
    },
    {
        "id": "authbasic",
        "stream": "no",
        "name": "Auth basic",
        "description": "Enforce login before accessing a resource or the whole site using HTTP basic auth method.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": False,
        "settings": {
            "USE_AUTH_BASIC": {
                "context": "multisite",
                "default": "no",
                "help": "Use HTTP basic auth",
                "id": "use-auth-basic",
                "label": "Use HTTP basic auth",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "AUTH_BASIC_LOCATION": {
                "context": "multisite",
                "default": "sitewide",
                "help": "URL of the protected resource or sitewide value.",
                "id": "auth-basic-location",
                "label": "Auth basic Location",
                "regex": "^(sitewide|/[a-zA-Z0-9.\\/\\-]*)$",
                "type": "text",
            },
            "AUTH_BASIC_USER": {
                "context": "multisite",
                "default": "changeme",
                "help": "Username",
                "id": "auth-basic-user",
                "label": "Auth basic Username",
                "regex": "^[\\w\\-]+",
                "type": "text",
            },
            "AUTH_BASIC_PASSWORD": {
                "context": "multisite",
                "default": "changeme",
                "help": "Password",
                "id": "auth-basic-password",
                "label": "Password",
                "regex": "^.+",
                "type": "password",
            },
            "AUTH_BASIC_TEXT": {
                "context": "multisite",
                "default": "Restricted area",
                "help": "Text to display",
                "id": "auth-basic-text",
                "label": "Text",
                "regex": "^.+",
                "type": "text",
            },
        },
        "checksum": None,
    },
    {
        "id": "backup",
        "stream": "yes",
        "name": "Backup",
        "description": "Backup your data to a custom location. Ensure the safety and availability of your important files by creating regular backups.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": True,
        "settings": {
            "USE_BACKUP": {
                "context": "global",
                "default": "yes",
                "help": "Enable or disable the backup feature",
                "id": "use-backup",
                "label": "Activate automatic backup",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "BACKUP_SCHEDULE": {
                "context": "global",
                "default": "daily",
                "help": "The frequency of the backup (daily, weekly or monthly)",
                "id": "backup-schedule",
                "label": "Backup schedule",
                "regex": "^(daily|weekly|monthly)$",
                "type": "select",
                "select": ["daily", "monthly", "weekly"],
            },
            "BACKUP_ROTATION": {
                "context": "global",
                "default": "7",
                "help": "The number of backups to keep",
                "id": "backup-rotation",
                "label": "Backup rotation",
                "regex": "^[1-9][0-9]*$",
                "type": "text",
            },
            "BACKUP_DIRECTORY": {
                "context": "global",
                "default": "/var/lib/bunkerweb/backups",
                "help": "The directory where the backup will be stored",
                "id": "backup-directory",
                "label": "Backup directory",
                "regex": "^.*$",
                "type": "text",
            },
        },
        "checksum": None,
        "bwcli": {"list": "list.py", "restore": "restore.py", "save": "save.py"},
    },
    {
        "id": "badbehavior",
        "stream": "yes",
        "name": "Bad behavior",
        "description": "Ban IP generating too much 'bad' HTTP status code in a period of time.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": True,
        "settings": {
            "USE_BAD_BEHAVIOR": {
                "context": "multisite",
                "default": "yes",
                "help": "Activate Bad behavior feature.",
                "id": "use-bad-behavior",
                "label": "Activate bad behavior",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "BAD_BEHAVIOR_STATUS_CODES": {
                "context": "multisite",
                "default": "400 401 403 404 405 429 444",
                "help": "List of HTTP status codes considered as 'bad'.",
                "id": "bad-behavior-status-code",
                "label": "Bad status codes",
                "regex": "^( *([1-5]\\d{2})(?!.*\\2) *)+$",
                "type": "text",
            },
            "BAD_BEHAVIOR_THRESHOLD": {
                "context": "multisite",
                "default": "10",
                "help": "Maximum number of 'bad' HTTP status codes within the period of time before IP is banned.",
                "id": "bad-behavior-threshold",
                "label": "Threshold",
                "regex": "^[1-9][0-9]*",
                "type": "text",
            },
            "BAD_BEHAVIOR_COUNT_TIME": {
                "context": "multisite",
                "default": "60",
                "help": "Period of time (in seconds) during which we count 'bad' HTTP status codes.",
                "id": "bad-behavior-period",
                "label": "Period (in seconds)",
                "regex": "^\\d+",
                "type": "text",
            },
            "BAD_BEHAVIOR_BAN_TIME": {
                "context": "multisite",
                "default": "86400",
                "help": "The duration time (in seconds) of a ban when the corresponding IP has reached the threshold.",
                "id": "bad-behavior-ban-time",
                "label": "Ban duration (in seconds)",
                "regex": "^\\d+",
                "type": "text",
            },
        },
        "checksum": None,
    },
    {
        "id": "blacklist",
        "stream": "partial",
        "name": "Blacklist",
        "description": "Deny access based on internal and external IP/network/rDNS/ASN blacklists.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": True,
        "settings": {
            "USE_BLACKLIST": {
                "context": "multisite",
                "default": "yes",
                "help": "Activate blacklist feature.",
                "id": "use-blacklist",
                "label": "Activate blacklisting",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "BLACKLIST_IP": {
                "context": "multisite",
                "default": "",
                "help": "List of IP/network, separated with spaces, to block.",
                "id": "blacklist-ip",
                "label": "Blacklist IP/network",
                "regex": "^(?! )( *(((\\b25[0-5]|\\b2[0-4]\\d|\\b[01]?\\d\\d?)(\\.(25[0-5]|2[0-4]\\d|[01]?\\d\\d?)){3})(\\/([1-2][0-9]?|3[0-2]?|[04-9]))?|(([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]Z{0,4}){0,4}%[0-9a-zA-Z]+|::(ffff(:0{1,4})?:)?((25[0-5]|(2[0-4]|1?\\d)?\\d)\\.){3}(25[0-5]|(2[0-4]|1?\\d)?\\d)|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1?\\d)?\\d)\\.){3}(25[0-5]|(2[0-4]|1?\\d)?\\d))(\\/(12[0-8]|1[01][0-9]|[0-9][0-9]?))?)(?!.*\\D\\2([^\\d\\/]|$)) *)*$",
                "type": "text",
            },
            "BLACKLIST_RDNS": {
                "context": "multisite",
                "default": ".shodan.io .censys.io",
                "help": "List of reverse DNS suffixes, separated with spaces, to block.",
                "id": "blacklist-rdns",
                "label": "Blacklist reverse DNS",
                "regex": "^( *(([^ ]+)(?!.*\\3( |$))) *)*$",
                "type": "text",
            },
            "BLACKLIST_RDNS_GLOBAL": {
                "context": "multisite",
                "default": "yes",
                "help": "Only perform RDNS blacklist checks on global IP addresses.",
                "id": "blacklist-rdns-global",
                "label": "Blacklist reverse DNS global IPs",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "BLACKLIST_ASN": {
                "context": "multisite",
                "default": "",
                "help": "List of ASN numbers, separated with spaces, to block.",
                "id": "blacklist-asn",
                "label": "Blacklist ASN",
                "regex": "^^( *((ASN?)?(\\d+)\\b(?!.*[SN ]\\4\\b)) *)*$",
                "type": "text",
            },
            "BLACKLIST_USER_AGENT": {
                "context": "multisite",
                "default": "",
                "help": "List of User-Agent (PCRE regex), separated with spaces, to block.",
                "id": "blacklist-user-agent",
                "label": "Blacklist User-Agent",
                "regex": "^.*$",
                "type": "text",
            },
            "BLACKLIST_URI": {
                "context": "multisite",
                "default": "",
                "help": "List of URI (PCRE regex), separated with spaces, to block.",
                "id": "blacklist-uri",
                "label": "Blacklist URI",
                "regex": "^( *(.*)(?!.*\\2(?!.)) *)*$",
                "type": "text",
            },
            "BLACKLIST_IGNORE_IP": {
                "context": "multisite",
                "default": "",
                "help": "List of IP/network, separated with spaces, to ignore in the blacklist.",
                "id": "blacklist-ignore-ip",
                "label": "Blacklist ignore IP/network",
                "regex": "^(?! )( *(((\\b25[0-5]|\\b2[0-4]\\d|\\b[01]?\\d\\d?)(\\.(25[0-5]|2[0-4]\\d|[01]?\\d\\d?)){3})(\\/([1-2][0-9]?|3[0-2]?|[04-9]))?|(([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]Z{0,4}){0,4}%[0-9a-zA-Z]+|::(ffff(:0{1,4})?:)?((25[0-5]|(2[0-4]|1?\\d)?\\d)\\.){3}(25[0-5]|(2[0-4]|1?\\d)?\\d)|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1?\\d)?\\d)\\.){3}(25[0-5]|(2[0-4]|1?\\d)?\\d))(\\/(12[0-8]|1[01][0-9]|[0-9][0-9]?))?)(?!.*\\D\\2([^\\d\\/]|$)) *)*$",
                "type": "text",
            },
            "BLACKLIST_IGNORE_RDNS": {
                "context": "multisite",
                "default": "",
                "help": "List of reverse DNS suffixes, separated with spaces, to ignore in the blacklist.",
                "id": "blacklist-ignore-rdns",
                "label": "Blacklist ignore reverse DNS",
                "regex": "^( *(([^ ]+)(?!.*\\3( |$))) *)*$",
                "type": "text",
            },
            "BLACKLIST_IGNORE_ASN": {
                "context": "multisite",
                "default": "",
                "help": "List of ASN numbers, separated with spaces, to ignore in the blacklist.",
                "id": "blacklist-ignore-asn",
                "label": "Blacklist ignore ASN",
                "regex": "^^( *((ASN?)?(\\d+)\\b(?!.*[SN ]\\4\\b)) *)*$",
                "type": "text",
            },
            "BLACKLIST_IGNORE_USER_AGENT": {
                "context": "multisite",
                "default": "",
                "help": "List of User-Agent (PCRE regex), separated with spaces, to ignore in the blacklist.",
                "id": "blacklist-ignore-user-agent",
                "label": "Blacklist ignore User-Agent",
                "regex": "^.*$",
                "type": "text",
            },
            "BLACKLIST_IGNORE_URI": {
                "context": "multisite",
                "default": "",
                "help": "List of URI (PCRE regex), separated with spaces, to ignore in the blacklist.",
                "id": "blacklist-ignore-uri",
                "label": "Blacklist ignore URI",
                "regex": "^( *(.*)(?!.*\\2(?!.)) *)*$",
                "type": "text",
            },
            "BLACKLIST_IP_URLS": {
                "context": "global",
                "default": "https://www.dan.me.uk/torlist/?exit",
                "help": "List of URLs, separated with spaces, containing bad IP/network to block.",
                "id": "blacklist-ip-urls",
                "label": "Blacklist IP/network URLs",
                "regex": "^( *((https?:\\/\\/|file:\\/\\/\\/)[\\-\\w@:%.+~#=]+[\\-\\w\\(\\)!@:%+.~#?&\\/=$]*)(?!.*\\2(?!.)) *)*$",
                "type": "text",
            },
            "BLACKLIST_RDNS_URLS": {
                "context": "global",
                "default": "",
                "help": "List of URLs, separated with spaces, containing reverse DNS suffixes to block.",
                "id": "blacklist-rdns-urls",
                "label": "Blacklist reverse DNS URLs",
                "regex": "^( *((https?:\\/\\/|file:\\/\\/\\/)[\\-\\w@:%.+~#=]+[\\-\\w\\(\\)!@:%+.~#?&\\/=$]*)(?!.*\\2(?!.)) *)*$",
                "type": "text",
            },
            "BLACKLIST_ASN_URLS": {
                "context": "global",
                "default": "",
                "help": "List of URLs, separated with spaces, containing ASN to block.",
                "id": "blacklist-asn-urls",
                "label": "Blacklist ASN URLs",
                "regex": "^( *((https?:\\/\\/|file:\\/\\/\\/)[\\-\\w@:%.+~#=]+[\\-\\w\\(\\)!@:%+.~#?&\\/=$]*)(?!.*\\2(?!.)) *)*$",
                "type": "text",
            },
            "BLACKLIST_USER_AGENT_URLS": {
                "context": "global",
                "default": "https://raw.githubusercontent.com/mitchellkrogza/nginx-ultimate-bad-bot-blocker/master/_generator_lists/bad-user-agents.list",
                "help": "List of URLs, separated with spaces, containing bad User-Agent to block.",
                "id": "blacklist-user-agent-urls",
                "label": "Blacklist User-Agent URLs",
                "regex": "^( *((https?:\\/\\/|file:\\/\\/\\/)[\\-\\w@:%.+~#=]+[\\-\\w\\(\\)!@:%+.~#?&\\/=$]*)(?!.*\\2(?!.)) *)*$",
                "type": "text",
            },
            "BLACKLIST_URI_URLS": {
                "context": "global",
                "default": "",
                "help": "List of URLs, separated with spaces, containing bad URI to block.",
                "id": "blacklist-uri-urls",
                "label": "Blacklist URI URLs",
                "regex": "^( *((https?:\\/\\/|file:\\/\\/\\/)[\\-\\w@:%.+~#=]+[\\-\\w\\(\\)!@:%+.~#?&\\/=$]*)(?!.*\\2(?!.)) *)*$",
                "type": "text",
            },
            "BLACKLIST_IGNORE_IP_URLS": {
                "context": "global",
                "default": "",
                "help": "List of URLs, separated with spaces, containing IP/network to ignore in the blacklist.",
                "id": "blacklist-ignore-ip-urls",
                "label": "Blacklist ignore IP/network URLs",
                "regex": "^( *((https?:\\/\\/|file:\\/\\/\\/)[\\-\\w@:%.+~#=]+[\\-\\w\\(\\)!@:%+.~#?&\\/=$]*)(?!.*\\2(?!.)) *)*$",
                "type": "text",
            },
            "BLACKLIST_IGNORE_RDNS_URLS": {
                "context": "global",
                "default": "",
                "help": "List of URLs, separated with spaces, containing reverse DNS suffixes to ignore in the blacklist.",
                "id": "blacklist-ignore-rdns-urls",
                "label": "Blacklist ignore reverse DNS URLs",
                "regex": "^( *((https?:\\/\\/|file:\\/\\/\\/)[\\-\\w@:%.+~#=]+[\\-\\w\\(\\)!@:%+.~#?&\\/=$]*)(?!.*\\2(?!.)) *)*$",
                "type": "text",
            },
            "BLACKLIST_IGNORE_ASN_URLS": {
                "context": "global",
                "default": "",
                "help": "List of URLs, separated with spaces, containing ASN to ignore in the blacklist.",
                "id": "blacklist-ignore-asn-urls",
                "label": "Blacklist ignore ASN URLs",
                "regex": "^( *((https?:\\/\\/|file:\\/\\/\\/)[\\-\\w@:%.+~#=]+[\\-\\w\\(\\)!@:%+.~#?&\\/=$]*)(?!.*\\2(?!.)) *)*$",
                "type": "text",
            },
            "BLACKLIST_IGNORE_USER_AGENT_URLS": {
                "context": "global",
                "default": "",
                "help": "List of URLs, separated with spaces, containing User-Agent to ignore in the blacklist.",
                "id": "blacklist-ignore-user-agent-urls",
                "label": "Blacklist ignore User-Agent URLs",
                "regex": "^( *((https?:\\/\\/|file:\\/\\/\\/)[\\-\\w@:%.+~#=]+[\\-\\w\\(\\)!@:%+.~#?&\\/=$]*)(?!.*\\2(?!.)) *)*$",
                "type": "text",
            },
            "BLACKLIST_IGNORE_URI_URLS": {
                "context": "global",
                "default": "",
                "help": "List of URLs, separated with spaces, containing URI to ignore in the blacklist.",
                "id": "blacklist-ignore-uri-urls",
                "label": "Blacklist ignore URI URLs",
                "regex": "^( *((https?:\\/\\/|file:\\/\\/\\/)[\\-\\w@:%.+~#=]+[\\-\\w\\(\\)!@:%+.~#?&\\/=$]*)(?!.*\\2(?!.)) *)*$",
                "type": "text",
            },
        },
        "checksum": None,
    },
    {
        "id": "brotli",
        "stream": "no",
        "name": "Brotli",
        "description": "Compress HTTP requests with the brotli algorithm.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": False,
        "settings": {
            "USE_BROTLI": {
                "context": "multisite",
                "default": "no",
                "help": "Use brotli",
                "id": "use-brotli",
                "label": "Use brotli",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "BROTLI_TYPES": {
                "context": "multisite",
                "default": "application/atom+xml application/javascript application/json application/rss+xml application/vnd.ms-fontobject application/x-font-opentype application/x-font-truetype application/x-font-ttf application/x-javascript application/xhtml+xml application/xml font/eot font/opentype font/otf font/truetype image/svg+xml image/vnd.microsoft.icon image/x-icon image/x-win-bitmap text/css text/javascript text/plain text/xml",
                "help": "List of MIME types that will be compressed with brotli.",
                "id": "brotli-types",
                "label": "MIME types",
                "regex": "^(?! )( ?([\\-\\w.]+/[\\-\\w.+]+)(?!.*\\2(?!.)))+$",
                "type": "text",
            },
            "BROTLI_MIN_LENGTH": {
                "context": "multisite",
                "default": "1000",
                "help": "Minimum length for brotli compression.",
                "id": "brotli-min-length",
                "label": "Minimum length",
                "regex": "^\\d+",
                "type": "text",
            },
            "BROTLI_COMP_LEVEL": {
                "context": "multisite",
                "default": "6",
                "help": "The compression level of the brotli algorithm.",
                "id": "brotli-comp-level",
                "label": "Compression level",
                "regex": "^([02-9]|1[01]?)$",
                "type": "select",
                "select": [
                    "0",
                    "1",
                    "10",
                    "11",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                ],
            },
        },
        "checksum": None,
    },
    {
        "id": "bunkernet",
        "stream": "yes",
        "name": "BunkerNet",
        "description": "Share threat data with other BunkerWeb instances via BunkerNet.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": True,
        "settings": {
            "USE_BUNKERNET": {
                "context": "multisite",
                "default": "yes",
                "help": "Activate BunkerNet feature.",
                "id": "use-bunkernet",
                "label": "Activate BunkerNet",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "BUNKERNET_SERVER": {
                "context": "global",
                "default": "https://api.bunkerweb.io",
                "help": "Address of the BunkerNet API.",
                "id": "bunkernet-server",
                "label": "BunkerNet server",
                "regex": "^https?:\\/\\/[\\-\\w@:%.+~#=]+[\\-\\w\\(\\)!@:%+.~#?&\\/=$]*$",
                "type": "text",
            },
        },
        "checksum": None,
    },
    {
        "id": "cors",
        "stream": "no",
        "name": "CORS",
        "description": "Cross-Origin Resource Sharing.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": True,
        "settings": {
            "USE_CORS": {
                "context": "multisite",
                "default": "no",
                "help": "Use CORS",
                "id": "use-cors",
                "label": "Use CORS",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "CORS_ALLOW_ORIGIN": {
                "context": "multisite",
                "default": "*",
                "help": "Allowed origins to make CORS requests : PCRE regex or *.",
                "id": "cors-allow-origin",
                "label": "Allowed origins",
                "regex": "^.*$",
                "type": "text",
            },
            "CORS_ALLOW_METHODS": {
                "context": "multisite",
                "default": "GET, POST, OPTIONS",
                "help": "Value of the Access-Control-Allow-Methods header.",
                "id": "cors-allow-methods",
                "label": "Access-Control-Allow-Methods value",
                "regex": "^(\\*|(?![, ])(,? ?(GET|HEAD|POST|PUT|DELETE|CONNECT|OPTIONS|TRACE|PATCH)(?!.*\\3))*)?$",
                "type": "text",
            },
            "CORS_ALLOW_HEADERS": {
                "context": "multisite",
                "default": "DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range",
                "help": "Value of the Access-Control-Allow-Headers header.",
                "id": "cors-allow-headers",
                "label": "Access-Control-Allow-Headers value",
                "regex": "^(\\*|(?![, ])(,? ?([\\w\\-]+)(?!.*\\3(?!.)))*)?$",
                "type": "text",
            },
            "CORS_ALLOW_CREDENTIALS": {
                "context": "multisite",
                "default": "no",
                "help": "Send the Access-Control-Allow-Credentials header.",
                "id": "cors-allow-credentials",
                "label": "Send Access-Control-Allow-Credentials",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "CORS_EXPOSE_HEADERS": {
                "context": "multisite",
                "default": "Content-Length,Content-Range",
                "help": "Value of the Access-Control-Expose-Headers header.",
                "id": "cors-expose-headers",
                "label": "Access-Control-Expose-Headers value",
                "regex": "^(\\*|(?![, ]+)(,? ?([\\w\\-]+)(?!.*\\3(?!.)))*)?$",
                "type": "text",
            },
            "CROSS_ORIGIN_OPENER_POLICY": {
                "context": "multisite",
                "default": "",
                "help": "Value for the Cross-Origin-Opener-Policy header.",
                "id": "cross-origin-opener-policy",
                "label": "Cross-Origin-Opener-Policy",
                "regex": "^(unsafe-none|same-origin-allow-popups|same-origin)?$",
                "type": "select",
                "select": [
                    "",
                    "same-origin",
                    "same-origin-allow-popups",
                    "unsafe-none",
                ],
            },
            "CROSS_ORIGIN_EMBEDDER_POLICY": {
                "context": "multisite",
                "default": "",
                "help": "Value for the Cross-Origin-Embedder-Policy header.",
                "id": "cross-origin-embedder-policy",
                "label": "Cross-Origin-Embedder-Policy",
                "regex": "^(unsafe-none|require-corp|credentialless)?$",
                "type": "select",
                "select": ["", "credentialless", "require-corp", "unsafe-none"],
            },
            "CROSS_ORIGIN_RESOURCE_POLICY": {
                "context": "multisite",
                "default": "",
                "help": "Value for the Cross-Origin-Resource-Policy header.",
                "id": "cross-origin-resource-policy",
                "label": "Cross-Origin-Resource-Policy",
                "regex": "^(same-site|same-origin|cross-origin)?$",
                "type": "select",
                "select": ["", "cross-origin", "same-origin", "same-site"],
            },
            "CORS_MAX_AGE": {
                "context": "multisite",
                "default": "86400",
                "help": "Value of the Access-Control-Max-Age header.",
                "id": "cors-max-age",
                "label": "Access-Control-Max-Age value",
                "regex": "^\\d+$",
                "type": "text",
            },
            "CORS_DENY_REQUEST": {
                "context": "multisite",
                "default": "yes",
                "help": "Deny request and don't send it to backend if Origin is not allowed.",
                "id": "cors-deny-request",
                "label": "Deny request",
                "regex": "^(yes|no)$",
                "type": "check",
            },
        },
        "checksum": None,
    },
    {
        "id": "clientcache",
        "stream": "no",
        "name": "Client cache",
        "description": "Manage caching for clients.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": False,
        "settings": {
            "USE_CLIENT_CACHE": {
                "context": "multisite",
                "default": "no",
                "help": "Tell client to store locally static files.",
                "id": "use-client-cache",
                "label": "Use client cache",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "CLIENT_CACHE_EXTENSIONS": {
                "context": "global",
                "default": "jpg|jpeg|png|bmp|ico|svg|tif|css|js|otf|ttf|eot|woff|woff2",
                "help": "List of file extensions, separated with pipes that should be cached.",
                "id": "client-cache-extensions",
                "label": "Extensions that should be cached by the client",
                "regex": "^(?!\\|)(\\|?([a-z0-9]+)(?!.*\\2(?!.)))+$",
                "type": "text",
            },
            "CLIENT_CACHE_ETAG": {
                "context": "multisite",
                "default": "yes",
                "help": "Send the HTTP ETag header for static resources.",
                "id": "client-cache-etag",
                "label": "ETag",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "CLIENT_CACHE_CONTROL": {
                "context": "multisite",
                "default": "public, max-age=15552000",
                "help": "Value of the Cache-Control HTTP header.",
                "id": "client-cache-control",
                "label": "Cache-Control header",
                "regex": "^(?!(, ?| ))((, )?(((max-age|s-maxage|stale-while-revalidate|stale-if-error)=\\d+(?!.*\\6))|((?!.*public)private|(?!.*private)public)|(must|proxy)-revalidate|must-understand|immutable|no-(cache|store|transform))(?!.*\\4))+$",
                "type": "text",
            },
        },
        "checksum": None,
    },
    {
        "id": "country",
        "stream": "yes",
        "name": "Country",
        "description": "Deny access based on the country of the client IP.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": True,
        "settings": {
            "BLACKLIST_COUNTRY": {
                "context": "multisite",
                "default": "",
                "help": "Deny access if the country of the client is in the list (ISO 3166-1 alpha-2 format separated with spaces).",
                "id": "country-blacklist",
                "label": "Country blacklist",
                "regex": "^(?! )( *([A-Z]{2})(?!.*\\2) *)*$",
                "type": "text",
            },
            "WHITELIST_COUNTRY": {
                "context": "multisite",
                "default": "",
                "help": "Deny access if the country of the client is not in the list (ISO 3166-1 alpha-2 format separated with spaces).",
                "id": "country-whitelist",
                "label": "Country whitelist",
                "regex": "^(?! )( *([A-Z]{2})(?!.*\\2) *)*$",
                "type": "text",
            },
        },
        "checksum": None,
    },
    {
        "id": "customcert",
        "stream": "yes",
        "name": "Custom HTTPS certificate",
        "description": "Choose custom certificate for HTTPS.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": False,
        "settings": {
            "USE_CUSTOM_SSL": {
                "context": "multisite",
                "default": "no",
                "help": "Use custom HTTPS certificate.",
                "id": "use-custom-https",
                "label": "Use custom certificate",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "CUSTOM_SSL_CERT": {
                "context": "multisite",
                "default": "",
                "help": "Full path of the certificate or bundle file (must be readable by the scheduler).",
                "id": "custom-https-cert",
                "label": "Certificate path",
                "regex": "^(/[\\w. \\-]+)*/?$",
                "type": "text",
            },
            "CUSTOM_SSL_KEY": {
                "context": "multisite",
                "default": "",
                "help": "Full path of the key file (must be readable by the scheduler).",
                "id": "custom-https-key",
                "label": "Key path",
                "regex": "^(/[\\w. \\-]+)*/?$",
                "type": "text",
            },
            "CUSTOM_SSL_CERT_DATA": {
                "context": "multisite",
                "default": "",
                "help": "Certificate data encoded in base64.",
                "id": "custom-https-cert-data",
                "label": "Certificate data (base64)",
                "regex": "^.*$",
                "type": "text",
            },
            "CUSTOM_SSL_KEY_DATA": {
                "context": "multisite",
                "default": "",
                "help": "Key data encoded in base64.",
                "id": "custom-https-key-data",
                "label": "Key data (base64)",
                "regex": "^.*$",
                "type": "text",
            },
        },
        "checksum": None,
    },
    {
        "id": "db",
        "stream": "yes",
        "name": "DB",
        "description": "Integrate easily the Database.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": False,
        "settings": {
            "DATABASE_URI": {
                "context": "global",
                "default": "sqlite:////var/lib/bunkerweb/db.sqlite3",
                "help": "The database URI, following the sqlalchemy format.",
                "id": "database-uri",
                "label": "The database URI",
                "regex": "^((postgresql|mysql|mariadb|sqlite)(\\+[\\w\\-]+)?:.+)?$",
                "type": "text",
            },
            "DATABASE_URI_READONLY": {
                "context": "global",
                "default": "",
                "help": "The database URI for read-only operations, it can also serve as a fallback if the main database is down. Following the sqlalchemy format.",
                "id": "database-uri-readonly",
                "label": "The database URI for read-only operations",
                "regex": "^((postgresql|mysql|mariadb|sqlite)(\\+[\\w\\-]+)?:.+)?$",
                "type": "text",
            },
            "DATABASE_LOG_LEVEL": {
                "context": "global",
                "default": "warning",
                "help": "The level to use for database logs.",
                "id": "database-log-level",
                "label": "Database log level",
                "regex": "^(debug|info|warn|warning|error)$",
                "type": "select",
                "select": ["debug", "error", "info", "warn", "warning"],
            },
        },
        "checksum": None,
    },
    {
        "id": "dnsbl",
        "stream": "yes",
        "name": "DNSBL",
        "description": "Deny access based on external DNSBL servers.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": True,
        "settings": {
            "USE_DNSBL": {
                "context": "multisite",
                "default": "yes",
                "help": "Activate DNSBL feature.",
                "id": "use-dnsbl",
                "label": "Activate DNSBL",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "DNSBL_LIST": {
                "context": "global",
                "default": "bl.blocklist.de problems.dnsbl.sorbs.net sbl.spamhaus.org xbl.spamhaus.org",
                "help": "List of DNSBL servers.",
                "id": "dnsbl-list",
                "label": "DNSBL list",
                "regex": "^(?! )( ?((?!\\.)[\\w.]+)(?!.*\\2(?!.)))*$",
                "type": "text",
            },
        },
        "checksum": None,
    },
    {
        "id": "errors",
        "stream": "no",
        "name": "Errors",
        "description": "Manage default error pages",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": True,
        "settings": {
            "ERRORS": {
                "context": "multisite",
                "default": "",
                "help": "List of HTTP error code and corresponding error pages, separated with spaces (404=/my404.html 403=/errors/403.html ...).",
                "id": "errors",
                "label": "Errors",
                "regex": "^(?! )( ?([1-5]\\d{2})(?!.*\\2(?![^=]))=(\\/[\\w\\].~:\\/?#\\[@!$\\&'\\(\\)*+,;=\\-]*)(?!.*\\3(?!.)))*$",
                "type": "text",
            },
            "INTERCEPTED_ERROR_CODES": {
                "context": "multisite",
                "default": "400 401 403 404 405 413 429 500 501 502 503 504",
                "help": "List of HTTP error code intercepted by BunkerWeb",
                "id": "intercepted-error-codes",
                "label": "Intercepted error codes",
                "regex": "^( *([1-5]\\d{2})(?!.*\\2) *)+$",
                "type": "text",
            },
        },
        "checksum": None,
    },
    {
        "id": "greylist",
        "stream": "partial",
        "name": "Greylist",
        "description": "Allow access while keeping security features based on internal and external IP/network/rDNS/ASN greylists.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": True,
        "settings": {
            "USE_GREYLIST": {
                "context": "multisite",
                "default": "no",
                "help": "Activate greylist feature.",
                "id": "use-greylist",
                "label": "Activate greylisting",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "GREYLIST_IP": {
                "context": "multisite",
                "default": "",
                "help": "List of IP/network, separated with spaces, to put into the greylist.",
                "id": "greylist-ip",
                "label": "Greylist IP/network",
                "regex": "^(?! )( *(((\\b25[0-5]|\\b2[0-4]\\d|\\b[01]?\\d\\d?)(\\.(25[0-5]|2[0-4]\\d|[01]?\\d\\d?)){3})(\\/([1-2][0-9]?|3[0-2]?|[04-9]))?|(([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]Z{0,4}){0,4}%[0-9a-zA-Z]+|::(ffff(:0{1,4})?:)?((25[0-5]|(2[0-4]|1?\\d)?\\d)\\.){3}(25[0-5]|(2[0-4]|1?\\d)?\\d)|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1?\\d)?\\d)\\.){3}(25[0-5]|(2[0-4]|1?\\d)?\\d))(\\/(12[0-8]|1[01][0-9]|[0-9][0-9]?))?)(?!.*\\D\\2([^\\d\\/]|$)) *)*$",
                "type": "text",
            },
            "GREYLIST_RDNS": {
                "context": "multisite",
                "default": "",
                "help": "List of reverse DNS suffixes, separated with spaces, to put into the greylist.",
                "id": "greylist-rdns",
                "label": "Greylist reverse DNS",
                "regex": "^( *(([^ ]+)(?!.*\\3( |$))) *)*$",
                "type": "text",
            },
            "GREYLIST_RDNS_GLOBAL": {
                "context": "multisite",
                "default": "yes",
                "help": "Only perform RDNS greylist checks on global IP addresses.",
                "id": "greylist-rdns-global",
                "label": "Greylist reverse DNS global IPs",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "GREYLIST_ASN": {
                "context": "multisite",
                "default": "",
                "help": "List of ASN numbers, separated with spaces, to put into the greylist.",
                "id": "greylist-asn",
                "label": "Greylist ASN",
                "regex": "^^( *((ASN?)?(\\d+)\\b(?!.*[SN ]\\4\\b)) *)*$",
                "type": "text",
            },
            "GREYLIST_USER_AGENT": {
                "context": "multisite",
                "default": "",
                "help": "List of User-Agent (PCRE regex), separated with spaces, to put into the greylist.",
                "id": "greylist-user-agent",
                "label": "Greylist User-Agent",
                "regex": "^.*$",
                "type": "text",
            },
            "GREYLIST_URI": {
                "context": "multisite",
                "default": "",
                "help": "List of URI (PCRE regex), separated with spaces, to put into the greylist.",
                "id": "greylist-uri",
                "label": "Greylist URI",
                "regex": "^.*$",
                "type": "text",
            },
            "GREYLIST_IP_URLS": {
                "context": "global",
                "default": "",
                "help": "List of URLs, separated with spaces, containing good IP/network to put into the greylist.",
                "id": "greylist-ip-urls",
                "label": "Greylist IP/network URLs",
                "regex": "^( *((https?:\\/\\/|file:\\/\\/\\/)[\\-\\w@:%.+~#=]+[\\-\\w\\(\\)!@:%+.~#?&\\/=$]*)(?!.*\\2(?!.)) *)*$",
                "type": "text",
            },
            "GREYLIST_RDNS_URLS": {
                "context": "global",
                "default": "",
                "help": "List of URLs, separated with spaces, containing reverse DNS suffixes to put into the greylist.",
                "id": "greylist-rdns-urls",
                "label": "Greylist reverse DNS URLs",
                "regex": "^( *((https?:\\/\\/|file:\\/\\/\\/)[\\-\\w@:%.+~#=]+[\\-\\w\\(\\)!@:%+.~#?&\\/=$]*)(?!.*\\2(?!.)) *)*$",
                "type": "text",
            },
            "GREYLIST_ASN_URLS": {
                "context": "global",
                "default": "",
                "help": "List of URLs, separated with spaces, containing ASN to put into the greylist.",
                "id": "greylist-asn-urls",
                "label": "Greylist ASN URLs",
                "regex": "^( *((https?:\\/\\/|file:\\/\\/\\/)[\\-\\w@:%.+~#=]+[\\-\\w\\(\\)!@:%+.~#?&\\/=$]*)(?!.*\\2(?!.)) *)*$",
                "type": "text",
            },
            "GREYLIST_USER_AGENT_URLS": {
                "context": "global",
                "default": "",
                "help": "List of URLs, separated with spaces, containing good User-Agent to put into the greylist.",
                "id": "greylist-user-agent-urls",
                "label": "Greylist User-Agent URLs",
                "regex": "^( *((https?:\\/\\/|file:\\/\\/\\/)[\\-\\w@:%.+~#=]+[\\-\\w\\(\\)!@:%+.~#?&\\/=$]*)(?!.*\\2(?!.)) *)*$",
                "type": "text",
            },
            "GREYLIST_URI_URLS": {
                "context": "global",
                "default": "",
                "help": "List of URLs, separated with spaces, containing bad URI to put into the greylist.",
                "id": "greylist-uri-urls",
                "label": "Greylist URI URLs",
                "regex": "^( *((https?:\\/\\/|file:\\/\\/\\/)[\\-\\w@:%.+~#=]+[\\-\\w\\(\\)!@:%+.~#?&\\/=$]*)(?!.*\\2(?!.)) *)*$",
                "type": "text",
            },
        },
        "checksum": None,
    },
    {
        "id": "gzip",
        "stream": "no",
        "name": "Gzip",
        "description": "Compress HTTP requests with the gzip algorithm.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": False,
        "settings": {
            "USE_GZIP": {
                "context": "multisite",
                "default": "no",
                "help": "Use gzip",
                "id": "use-gzip",
                "label": "Use gzip",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "GZIP_TYPES": {
                "context": "multisite",
                "default": "application/atom+xml application/javascript application/json application/rss+xml application/vnd.ms-fontobject application/x-font-opentype application/x-font-truetype application/x-font-ttf application/x-javascript application/xhtml+xml application/xml font/eot font/opentype font/otf font/truetype image/svg+xml image/vnd.microsoft.icon image/x-icon image/x-win-bitmap text/css text/javascript text/plain text/xml",
                "help": "List of MIME types that will be compressed with gzip.",
                "id": "gzip-types",
                "label": "MIME types",
                "regex": "^(?! )( ?([\\-\\w.]+/[\\-\\w.+]+)(?!.*\\2(?!.)))+$",
                "type": "text",
            },
            "GZIP_MIN_LENGTH": {
                "context": "multisite",
                "default": "1000",
                "help": "Minimum length for gzip compression.",
                "id": "gzip-min-length",
                "label": "Minimum length",
                "regex": "^\\d+$",
                "type": "text",
            },
            "GZIP_COMP_LEVEL": {
                "context": "multisite",
                "default": "5",
                "help": "The compression level of the gzip algorithm.",
                "id": "gzip-comp-level",
                "label": "Compression level",
                "regex": "^[1-9]$",
                "type": "select",
                "select": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
            },
            "GZIP_PROXIED": {
                "context": "multisite",
                "default": "no-cache no-store private expired auth",
                "help": "Which kind of proxied requests we should compress.",
                "id": "gzip-proxied",
                "label": "Proxied requests",
                "regex": "^.*$",
                "type": "text",
            },
        },
        "checksum": None,
    },
    {
        "id": "inject",
        "stream": "no",
        "name": "HTML injection",
        "description": "Inject custom HTML code before the </body> tag.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": False,
        "settings": {
            "INJECT_BODY": {
                "context": "multisite",
                "default": "",
                "help": "The HTML code to inject.",
                "id": "inject-body",
                "label": "HTML code",
                "regex": "^.*$",
                "type": "text",
            }
        },
        "checksum": None,
    },
    {
        "id": "headers",
        "stream": "no",
        "name": "Headers",
        "description": "Manage HTTP headers sent to clients.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": False,
        "settings": {
            "CUSTOM_HEADER": {
                "context": "multisite",
                "default": "",
                "help": "Custom header to add (HeaderName: HeaderValue).",
                "id": "custom-header",
                "label": "Custom header (HeaderName: HeaderValue)",
                "regex": "^([\\w\\-]+: .+)?$",
                "type": "text",
                "multiple": "custom-headers",
            },
            "REMOVE_HEADERS": {
                "context": "multisite",
                "default": "Server Expect-CT X-Powered-By X-AspNet-Version X-AspNetMvc-Version",
                "help": "Headers to remove (Header1 Header2 Header3 ...)",
                "id": "remove-headers",
                "label": "Remove headers",
                "regex": "^(?! )( ?[\\w\\-]+)*$",
                "type": "text",
            },
            "KEEP_UPSTREAM_HEADERS": {
                "context": "multisite",
                "default": "Content-Security-Policy Permissions-Policy Feature-Policy X-Frame-Options",
                "help": "Headers to keep from upstream (Header1 Header2 Header3 ... or * for all).",
                "id": "keep-upstream-headers",
                "label": "Keep upstream headers",
                "regex": "^((?! )( ?[\\w\\-]+)+|\\*)?$",
                "type": "text",
            },
            "STRICT_TRANSPORT_SECURITY": {
                "context": "multisite",
                "default": "max-age=31536000",
                "help": "Value for the Strict-Transport-Security header.",
                "id": "strict-transport-security",
                "label": "Strict-Transport-Security",
                "regex": "^max-age=\\d+(; includeSubDomains(; preload)?)?$",
                "type": "text",
            },
            "COOKIE_FLAGS": {
                "context": "multisite",
                "default": "* HttpOnly SameSite=Lax",
                "help": "Cookie flags automatically added to all cookies (value accepted for nginx_cookie_flag_module).",
                "id": "cookie-flags",
                "label": "Cookie flags",
                "regex": "^(\\*|[^;]+)( (HttpOnly|(SameSite)(?!.*\\4)(=(Lax|Strict))?)(?!.*\\3))*$",
                "type": "text",
                "multiple": "cookie-flags",
            },
            "COOKIE_AUTO_SECURE_FLAG": {
                "context": "multisite",
                "default": "yes",
                "help": "Automatically add the Secure flag to all cookies.",
                "id": "cookie-auto-secure-flag",
                "label": "Cookie auto Secure flag",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "CONTENT_SECURITY_POLICY": {
                "context": "multisite",
                "default": "object-src 'none'; form-action 'self'; frame-ancestors 'self';",
                "help": "Value for the Content-Security-Policy header.",
                "id": "content-security-policy",
                "label": "Content-Security-Policy",
                "regex": "^.*$",
                "type": "text",
            },
            "CONTENT_SECURITY_POLICY_REPORT_ONLY": {
                "context": "multisite",
                "default": "no",
                "help": "Send reports for violations of the Content-Security-Policy header instead of blocking them.",
                "id": "content-security-policy-report-only",
                "label": "Content-Security-Policy-Report-Only",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "REFERRER_POLICY": {
                "context": "multisite",
                "default": "strict-origin-when-cross-origin",
                "help": "Value for the Referrer-Policy header.",
                "id": "referrer-policy",
                "label": "Referrer-Policy",
                "regex": "^(?!^(,| ))((, )?(no-referrer-when-downgrade|no-referrer|origin-when-cross-origin|same-origin|strict-origin-when-cross-origin|strict-origin|origin|unsafe-url)(?!\\b.*, \\4\\b))*$",
                "type": "text",
            },
            "PERMISSIONS_POLICY": {
                "context": "multisite",
                "default": "accelerometer=(), ambient-light-sensor=(), autoplay=(), battery=(), camera=(), cross-origin-isolated=(), display-capture=(), document-domain=(), encrypted-media=(), execution-while-not-rendered=(), execution-while-out-of-viewport=(), fullscreen=(), geolocation=(), gyroscope=(), hid=(), idle-detection=(), magnetometer=(), microphone=(), midi=(), navigation-override=(), payment=(), picture-in-picture=(), publickey-credentials-get=(), screen-wake-lock=(), serial=(), usb=(), web-share=(), xr-spatial-tracking=()",
                "help": "Value for the Permissions-Policy header.",
                "id": "permissions-policy",
                "label": "Permissions-Policy",
                "regex": "^(?![, ])(,? ?([a-z\\-]+)(?!.*[^\\-]\\2=)=(\\*|\\(( ?(self|\\u0022https?:\\/\\/[\\-\\w@:%.+~#=]+[\\-\\w\\(\\)!@:%+.~#?&\\/=$]*\\u0022)(?=[ \\)]))*\\)))*$",
                "type": "text",
            },
            "FEATURE_POLICY": {
                "context": "multisite",
                "default": "accelerometer 'none'; ambient-light-sensor 'none'; autoplay 'none'; battery 'none'; camera 'none'; display-capture 'none'; document-domain 'none'; encrypted-media 'none'; execution-while-not-rendered 'none'; execution-while-out-of-viewport 'none'; fullscreen 'none'; geolocation 'none'; gyroscope 'none'; layout-animation 'none'; legacy-image-formats 'none'; magnetometer 'none'; microphone 'none'; midi 'none'; navigation-override 'none'; payment 'none'; picture-in-picture 'none'; publickey-credentials-get 'none'; speaker-selection 'none'; sync-xhr 'none'; unoptimized-images 'none'; unsized-media 'none'; usb 'none'; screen-wake-lock 'none'; web-share 'none'; xr-spatial-tracking 'none';",
                "help": "Value for the Feature-Policy header.",
                "id": "feature-policy",
                "label": "Feature-Policy",
                "regex": "^(?![; ])( ?([\\w\\-]+)(?!.*[^\\-]\\2 )( ('(none|self|strict-dynamic|report-sample|unsafe-inline|unsafe-eval|unsafe-hashes|unsafe-allow-redirects)'|https?:\\/\\/[\\w@:%.+~#=\\-]+[\\w\\(\\)!@:%+.~#?&\\/=$\\-]*))+;)*$",
                "type": "text",
            },
            "X_FRAME_OPTIONS": {
                "context": "multisite",
                "default": "SAMEORIGIN",
                "help": "Value for the X-Frame-Options header.",
                "id": "x-frame-options",
                "label": "X-Frame-Options",
                "regex": "^(DENY|SAMEORIGIN)?$",
                "type": "select",
                "select": ["", "DENY", "SAMEORIGIN"],
            },
            "X_CONTENT_TYPE_OPTIONS": {
                "context": "multisite",
                "default": "nosniff",
                "help": "Value for the X-Content-Type-Options header.",
                "id": "x-content-type-options",
                "label": "X-Content-Type-Options",
                "regex": "^(nosniff)?$",
                "type": "select",
                "select": ["", "nosniff"],
            },
            "X_XSS_PROTECTION": {
                "context": "multisite",
                "default": "1; mode=block",
                "help": "Value for the X-XSS-Protection header.",
                "id": "x-xss-protection",
                "label": "X-XSS-Protection",
                "regex": "^0|1(; (mode=block|report=https?:\\/\\/[\\-\\w@:%.+~#=]+[\\-\\w\\(\\)!@:%+.~#?&\\/=$]*))?$",
                "type": "text",
            },
        },
        "checksum": None,
    },
    {
        "id": "jobs",
        "stream": "yes",
        "name": "Jobs",
        "description": "Fake core plugin for internal jobs.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": False,
        "settings": {},
        "checksum": None,
    },
    {
        "id": "letsencrypt",
        "stream": "yes",
        "name": "Let's Encrypt",
        "description": "Automatic creation, renewal and configuration of Let's Encrypt certificates.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": False,
        "settings": {
            "AUTO_LETS_ENCRYPT": {
                "context": "multisite",
                "default": "no",
                "help": "Activate automatic Let's Encrypt mode.",
                "id": "auto-lets-encrypt",
                "label": "Automatic Let's Encrypt",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "EMAIL_LETS_ENCRYPT": {
                "context": "multisite",
                "default": "",
                "help": "Email used for Let's Encrypt notification and in certificate.",
                "id": "email-lets-encrypt",
                "label": "Email Let's Encrypt",
                "regex": "^([^@ \\t\\r\\n]+@[^@ \\t\\r\\n]+\\.[^@ \\t\\r\\n]+)?$",
                "type": "text",
            },
            "USE_LETS_ENCRYPT_STAGING": {
                "context": "multisite",
                "default": "no",
                "help": "Use the staging environment for Let’s Encrypt certificate generation. Useful when you are testing your deployments to avoid being rate limited in the production environment.",
                "id": "use-lets-encrypt-staging",
                "label": "Use Let's Encrypt Staging",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "LETS_ENCRYPT_CLEAR_OLD_CERTS": {
                "context": "global",
                "default": "no",
                "help": "Clear old certificates when renewing.",
                "id": "lets-encrypt-clear-old-certs",
                "label": "Clear old certificates when they are no longer needed",
                "regex": "^(yes|no)$",
                "type": "check",
            },
        },
        "checksum": None,
    },
    {
        "id": "limit",
        "stream": "partial",
        "name": "Limit",
        "description": "Limit maximum number of requests and connections.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": True,
        "settings": {
            "USE_LIMIT_REQ": {
                "context": "multisite",
                "default": "yes",
                "help": "Activate limit requests feature.",
                "id": "use-limit-req",
                "label": "Activate limit requests",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "LIMIT_REQ_URL": {
                "context": "multisite",
                "default": "/",
                "help": "URL (PCRE regex) where the limit request will be applied or special value / for all requests.",
                "id": "limit-req-url",
                "label": "Limit request URL",
                "regex": "^.+$",
                "type": "text",
                "multiple": "limit-req",
            },
            "LIMIT_REQ_RATE": {
                "context": "multisite",
                "default": "2r/s",
                "help": "Rate to apply to the URL (s for second, m for minute, h for hour and d for day).",
                "id": "limit-req-rate",
                "label": "Limit request Rate",
                "regex": "^\\d+r/[smhd]$",
                "type": "text",
                "multiple": "limit-req",
            },
            "USE_LIMIT_CONN": {
                "context": "multisite",
                "default": "yes",
                "help": "Activate limit connections feature.",
                "id": "use-limit-conn",
                "label": "Activate limit connections",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "LIMIT_CONN_MAX_HTTP1": {
                "context": "multisite",
                "default": "10",
                "help": "Maximum number of connections per IP when using HTTP/1.X protocol.",
                "id": "limit-conn-max-http1",
                "label": "Maximum number of HTTP/1.X connections",
                "regex": "^\\d+$",
                "type": "text",
            },
            "LIMIT_CONN_MAX_HTTP2": {
                "context": "multisite",
                "default": "100",
                "help": "Maximum number of streams per IP when using HTTP/2 protocol.",
                "id": "limit-conn-max-http2",
                "label": "Maximum number of HTTP/2 streams",
                "regex": "^\\d+$",
                "type": "text",
            },
            "LIMIT_CONN_MAX_STREAM": {
                "context": "multisite",
                "default": "10",
                "help": "Maximum number of connections per IP when using stream.",
                "id": "limit-conn-max-stream",
                "label": "Maximum number of stream connections",
                "regex": "^\\d+$",
                "type": "text",
            },
        },
        "checksum": None,
    },
    {
        "id": "metrics",
        "stream": "partial",
        "name": "Metrics",
        "description": "Metrics collection and retrieve.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": False,
        "settings": {
            "USE_METRICS": {
                "context": "multisite",
                "default": "yes",
                "help": "Enable collection and retrieval of internal metrics.",
                "id": "use-metrics",
                "label": "Use metrics",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "METRICS_MEMORY_SIZE": {
                "context": "global",
                "default": "16m",
                "help": "Size of the internal storage for metrics.",
                "id": "metrics-memory-size",
                "label": "Metrics memory size",
                "regex": "^\\d+[kKmMgG]?$",
                "type": "text",
            },
            "METRICS_MAX_BLOCKED_REQUESTS": {
                "context": "global",
                "default": "100",
                "help": "Maximum number of blocked requests to store (per worker).",
                "id": "metrics-max-blocked-requests",
                "label": "Metrics max blocked requests",
                "regex": "^\\d+$",
                "type": "text",
            },
        },
        "checksum": None,
    },
    {
        "id": "misc",
        "stream": "partial",
        "name": "Miscellaneous",
        "description": "Miscellaneous settings.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": True,
        "settings": {
            "DISABLE_DEFAULT_SERVER": {
                "context": "global",
                "default": "no",
                "help": "Deny HTTP request if the request vhost is unknown.",
                "id": "disable-default-server",
                "label": "Disable default server",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "DISABLE_DEFAULT_SERVER_STRICT_SNI": {
                "context": "global",
                "default": "no",
                "help": "Close SSL/TLS connection if the SNI is unknown.",
                "id": "disable-default-server-strict-sni",
                "label": "Disable default server strict SNI",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "REDIRECT_HTTP_TO_HTTPS": {
                "context": "multisite",
                "default": "no",
                "help": "Redirect all HTTP request to HTTPS.",
                "id": "redirect-http-to-https",
                "label": "Redirect HTTP to HTTPS",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "AUTO_REDIRECT_HTTP_TO_HTTPS": {
                "context": "multisite",
                "default": "yes",
                "help": "Try to detect if HTTPS is used and activate HTTP to HTTPS redirection if that's the case.",
                "id": "auto-redirect-http-to-https",
                "label": "Auto redirect HTTP to HTTPS",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "ALLOWED_METHODS": {
                "context": "multisite",
                "default": "GET|POST|HEAD",
                "help": "Allowed HTTP and WebDAV methods, separated with pipes to be sent by clients.",
                "id": "allowed-methods",
                "label": "Allowed methods",
                "regex": "^(?!\\|)(\\|?([A-Z]{3,})(?!.*(^|\\|)\\2))+$",
                "type": "text",
            },
            "MAX_CLIENT_SIZE": {
                "context": "multisite",
                "default": "10m",
                "help": "Maximum body size (0 for infinite).",
                "id": "max-client-size",
                "label": "Maximum body size",
                "regex": "^\\d+[kKmMgG]?$",
                "type": "text",
            },
            "SERVE_FILES": {
                "context": "multisite",
                "default": "yes",
                "help": "Serve files from the local folder.",
                "id": "serve-files",
                "label": "Serve files",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "ROOT_FOLDER": {
                "context": "multisite",
                "default": "",
                "help": "Root folder containing files to serve (/var/www/html/{server_name} if unset).",
                "id": "root-folder",
                "label": "Root folder",
                "regex": "^(/[\\w. \\-]+)*/?$",
                "type": "text",
            },
            "SSL_PROTOCOLS": {
                "context": "multisite",
                "default": "TLSv1.2 TLSv1.3",
                "help": "The supported version of TLS. We recommend the default value TLSv1.2 TLSv1.3 for compatibility reasons.",
                "id": "https-protocols",
                "label": "HTTPS protocols",
                "regex": "^(?! )( ?TLSv1\\.[0-3])*$",
                "type": "text",
            },
            "HTTP2": {
                "context": "multisite",
                "default": "yes",
                "help": "Support HTTP2 protocol when HTTPS is enabled.",
                "id": "http2",
                "label": "HTTP2",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "HTTP3": {
                "context": "multisite",
                "default": "no",
                "help": "Support HTTP3 protocol when HTTPS is enabled.",
                "id": "http3",
                "label": "HTTP3",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "HTTP3_ALT_SVC_PORT": {
                "context": "multisite",
                "default": "443",
                "help": "HTTP3 alternate service port. This value will be used as part of the Alt-Svc header.",
                "id": "http3-alt-svc-port",
                "label": "HTTP3 Alt-Svc port",
                "regex": "^\\d+$",
                "type": "text",
            },
            "LISTEN_HTTP": {
                "context": "multisite",
                "default": "yes",
                "help": "Respond to (insecure) HTTP requests.",
                "id": "http-listen",
                "label": "HTTP listen",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "USE_OPEN_FILE_CACHE": {
                "context": "multisite",
                "default": "no",
                "help": "Enable open file cache feature",
                "id": "use-open-file-cache",
                "label": "Use open file cache",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "OPEN_FILE_CACHE": {
                "context": "multisite",
                "default": "max=1000 inactive=20s",
                "help": "Open file cache directive",
                "id": "open-file-cache",
                "label": "Use open file cache",
                "regex": "^(off|max=\\d+( inactive=\\d+(ms?|[shdwMy]))?)$",
                "type": "text",
            },
            "OPEN_FILE_CACHE_ERRORS": {
                "context": "multisite",
                "default": "yes",
                "help": "Enable open file cache for errors",
                "id": "open-file-cache-errors",
                "label": "Open file cache errors",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "OPEN_FILE_CACHE_MIN_USES": {
                "context": "multisite",
                "default": "2",
                "help": "Enable open file cache minimum uses",
                "id": "open-file-cache-min-uses",
                "label": "Open file cache min uses",
                "regex": "^[1-9]\\d*$",
                "type": "text",
            },
            "OPEN_FILE_CACHE_VALID": {
                "context": "multisite",
                "default": "30s",
                "help": "Open file cache valid time",
                "id": "open-file-cache-valid",
                "label": "Open file cache valid time",
                "regex": "^\\d+(ms?|[shdwMy])$",
                "type": "text",
            },
            "EXTERNAL_PLUGIN_URLS": {
                "context": "global",
                "default": "",
                "help": "List of external plugins URLs (direct download to .zip or .tar file) to download and install (URLs are separated with space).",
                "id": "external-plugin-urls",
                "label": "External plugin URLs",
                "regex": "^( *((https?:\\/\\/|file:\\/\\/\\/)[\\-\\w@:%.+~#=]+[\\-\\w\\(\\)!@:%+.~#?&\\/=$]*)(?!.*\\2(?!.)) *)*$",
                "type": "text",
            },
            "DENY_HTTP_STATUS": {
                "context": "global",
                "default": "403",
                "help": "HTTP status code to send when the request is denied (403 or 444). When using 444, BunkerWeb will close the connection.",
                "id": "deny-http-status",
                "label": "Deny HTTP status",
                "regex": "^(403|444)$",
                "type": "select",
                "select": ["403", "444"],
            },
            "SEND_ANONYMOUS_REPORT": {
                "context": "global",
                "default": "yes",
                "help": "Send anonymous report to BunkerWeb maintainers.",
                "id": "send-anonymous-report",
                "label": "Send anonymous report",
                "regex": "^(yes|no)$",
                "type": "check",
            },
        },
        "checksum": None,
    },
    {
        "id": "modsecurity",
        "stream": "no",
        "name": "ModSecurity",
        "description": "Management of the ModSecurity WAF.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": False,
        "settings": {
            "USE_MODSECURITY": {
                "context": "multisite",
                "default": "yes",
                "help": "Enable ModSecurity WAF.",
                "id": "use-modsecurity",
                "label": "Use ModSecurity",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "USE_MODSECURITY_CRS": {
                "context": "multisite",
                "default": "yes",
                "help": "Enable OWASP Core Rule Set.",
                "id": "use-modsecurity-crs",
                "label": "Use Core Rule Set",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "MODSECURITY_CRS_VERSION": {
                "context": "multisite",
                "default": "3",
                "help": "Version of the OWASP Core Rule Set to use with ModSecurity (3, 4 or nightly).",
                "id": "modsecurity-crs-version",
                "label": "Core Rule Set Version",
                "regex": "^(3|4|nightly)$",
                "type": "select",
                "select": ["3", "4", "nightly"],
            },
            "MODSECURITY_SEC_AUDIT_ENGINE": {
                "context": "multisite",
                "default": "RelevantOnly",
                "help": "SecAuditEngine directive of ModSecurity.",
                "id": "modsecurity-sec-audit-engine",
                "label": "SecAuditEngine",
                "regex": "^(On|RelevantOnly|Off)$",
                "type": "select",
                "select": ["Off", "On", "RelevantOnly"],
            },
            "MODSECURITY_SEC_RULE_ENGINE": {
                "context": "multisite",
                "default": "On",
                "help": "SecRuleEngine directive of ModSecurity.",
                "id": "modsecurity-sec-rule-engine",
                "label": "SecRuleEngine",
                "regex": "^(On|DetectionOnly|Off)$",
                "type": "select",
                "select": ["DetectionOnly", "Off", "On"],
            },
            "MODSECURITY_SEC_AUDIT_LOG_PARTS": {
                "context": "multisite",
                "default": "ABCFHZ",
                "help": "SecAuditLogParts directive of ModSecurity.",
                "id": "modsecurity-sec-audit-log-parts",
                "label": "SecAuditLogParts",
                "regex": "^A(([B-K])(?!.*\\2))+Z$",
                "type": "text",
            },
        },
        "checksum": None,
    },
    {
        "id": "php",
        "stream": "no",
        "name": "PHP",
        "description": "Manage local or remote PHP-FPM.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": False,
        "settings": {
            "REMOTE_PHP": {
                "context": "multisite",
                "default": "",
                "help": "Hostname of the remote PHP-FPM instance.",
                "id": "remote-php",
                "label": "Remote PHP",
                "regex": "^((?=.{1,255}$)[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?(?:\\.[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?)*\\.?)?$",
                "type": "text",
            },
            "REMOTE_PHP_PATH": {
                "context": "multisite",
                "default": "",
                "help": "Root folder containing files in the remote PHP-FPM instance.",
                "id": "remote-php-path",
                "label": "Remote PHP path",
                "regex": "^(/[\\w. \\-]+)*/?$",
                "type": "text",
            },
            "LOCAL_PHP": {
                "context": "multisite",
                "default": "",
                "help": "Path to the PHP-FPM socket file.",
                "id": "local",
                "label": "Local PHP",
                "regex": "^(/[\\w. \\-]+)*/?$",
                "type": "text",
            },
            "LOCAL_PHP_PATH": {
                "context": "multisite",
                "default": "",
                "help": "Root folder containing files in the local PHP-FPM instance.",
                "id": "local-php-path",
                "label": "Local PHP path",
                "regex": "^(/[\\w. \\-]+)*/?$",
                "type": "text",
            },
        },
        "checksum": None,
    },
    {
        "id": "pro",
        "stream": "no",
        "name": "Pro",
        "description": "Pro settings for the Pro version of BunkerWeb.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": False,
        "settings": {
            "PRO_LICENSE_KEY": {
                "context": "global",
                "default": "",
                "help": "The License Key for the Pro version of BunkerWeb.",
                "id": "pro-license-key",
                "label": "Pro License Key",
                "regex": "^.*$",
                "type": "password",
            }
        },
        "checksum": None,
    },
    {
        "id": "realip",
        "stream": "partial",
        "name": "Real IP",
        "description": "Get real IP of clients when BunkerWeb is behind a reverse proxy / load balancer.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": False,
        "settings": {
            "USE_REAL_IP": {
                "context": "multisite",
                "default": "no",
                "help": "Retrieve the real IP of client.",
                "id": "use-real-ip",
                "label": "Use real ip",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "USE_PROXY_PROTOCOL": {
                "context": "multisite",
                "default": "no",
                "help": "Enable PROXY protocol communication.",
                "id": "use-proxy-protocol",
                "label": "Use PROXY protocol",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "REAL_IP_FROM": {
                "context": "multisite",
                "default": "192.168.0.0/16 172.16.0.0/12 10.0.0.0/8",
                "help": "List of trusted IPs / networks, separated with spaces, where proxied requests come from.",
                "id": "real-ip-from",
                "label": "Real IP from",
                "regex": "^(?! )( *(((\\b25[0-5]|\\b2[0-4]\\d|\\b[01]?\\d\\d?)(\\.(25[0-5]|2[0-4]\\d|[01]?\\d\\d?)){3})(\\/([1-2][0-9]?|3[0-2]?|[04-9]))?|(([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]Z{0,4}){0,4}%[0-9a-zA-Z]+|::(ffff(:0{1,4})?:)?((25[0-5]|(2[0-4]|1?\\d)?\\d)\\.){3}(25[0-5]|(2[0-4]|1?\\d)?\\d)|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1?\\d)?\\d)\\.){3}(25[0-5]|(2[0-4]|1?\\d)?\\d))(\\/(12[0-8]|1[01][0-9]|[0-9][0-9]?))?)(?!.*\\D\\2([^\\d\\/]|$)) *)*$",
                "type": "text",
            },
            "REAL_IP_HEADER": {
                "context": "multisite",
                "default": "X-Forwarded-For",
                "help": "HTTP header containing the real IP or special value proxy_protocol for PROXY protocol.",
                "id": "real-ip-header",
                "label": "Real IP header",
                "regex": "^(?! )(( ?(?!proxy_protocol)[\\w\\-]+)*|proxy_protocol)$",
                "type": "text",
            },
            "REAL_IP_RECURSIVE": {
                "context": "multisite",
                "default": "yes",
                "help": "Perform a recursive search in the header container IP address.",
                "id": "real-ip-recursive",
                "label": "Real IP recursive",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "REAL_IP_FROM_URLS": {
                "context": "global",
                "default": "",
                "help": "List of URLs containing trusted IPs / networks, separated with spaces, where proxied requests come from.",
                "id": "real-ip-from-urls",
                "label": "Real IP from URLs",
                "regex": "^( *((https?:\\/\\/|file:\\/\\/\\/)[\\-\\w@:%.+~#=]+[\\-\\w\\(\\)!@:%+.~#?&\\/=$]*)(?!.*\\2(?!.)) *)*$",
                "type": "text",
            },
        },
        "checksum": None,
    },
    {
        "id": "redirect",
        "stream": "no",
        "name": "Redirect",
        "description": "Manage HTTP redirects.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": False,
        "settings": {
            "REDIRECT_TO": {
                "context": "multisite",
                "default": "",
                "help": "Redirect a whole site to another one.",
                "id": "redirect-to",
                "label": "Redirect to",
                "regex": "^(https?:\\/\\/[\\-\\w@:%.+~#=]+[\\-\\w\\(\\)!@:%+.~#?&\\/=$]*)?$",
                "type": "text",
            },
            "REDIRECT_TO_REQUEST_URI": {
                "context": "multisite",
                "default": "no",
                "help": "Append the requested URI to the redirect address.",
                "id": "redirect-to-request-uri",
                "label": "Append request URI",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "REDIRECT_TO_STATUS_CODE": {
                "context": "multisite",
                "default": "301",
                "help": "Status code to send to client when redirecting.",
                "id": "redirect-to-status-code",
                "label": "Append request URI",
                "regex": "^(301|302)$",
                "type": "select",
                "select": ["301", "302"],
            },
        },
        "checksum": None,
    },
    {
        "id": "redis",
        "stream": "yes",
        "name": "Redis",
        "description": "Redis server configuration when using BunkerWeb in cluster mode.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": True,
        "settings": {
            "USE_REDIS": {
                "context": "global",
                "default": "no",
                "help": "Activate Redis.",
                "id": "use-redis",
                "label": "Activate Redis",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "REDIS_HOST": {
                "context": "global",
                "default": "",
                "help": "Redis server IP or hostname.",
                "id": "redis-host",
                "label": "Redis server",
                "regex": "^((?!-)[a-zA-Z0-9\\-]{1,63}(.[a-zA-Z]{2,})+|(\\b25[0-5]|\\b2[0-4]\\d|\\b[01]?\\d\\d?)(\\.(25[0-5]|2[0-4]\\d|[01]?\\d\\d?)){3}|(([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]Z{0,4}){0,4}%[0-9a-zA-Z]+|::(ffff(:0{1,4})?:)?((25[0-5]|(2[0-4]|1?\\d)?\\d)\\.){3}(25[0-5]|(2[0-4]|1?\\d)?\\d)|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1?\\d)?\\d)\\.){3}(25[0-5]|(2[0-4]|1?\\d)?\\d)))?$",
                "type": "text",
            },
            "REDIS_PORT": {
                "context": "global",
                "default": "6379",
                "help": "Redis server port.",
                "id": "redis-port",
                "label": "Redis port",
                "regex": "^[0-9]+$",
                "type": "text",
            },
            "REDIS_DATABASE": {
                "context": "global",
                "default": "0",
                "help": "Redis database number.",
                "id": "redis-database",
                "label": "Redis database",
                "regex": "^[0-9]+$",
                "type": "text",
            },
            "REDIS_SSL": {
                "context": "global",
                "default": "no",
                "help": "Use SSL/TLS connection with Redis server.",
                "id": "redis-ssl",
                "label": "Redis SSL/TLS",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "REDIS_SSL_VERIFY": {
                "context": "global",
                "default": "no",
                "help": "Verify the certificate of Redis server.",
                "id": "redis-ssl-verify",
                "label": "Redis SSL/TLS verify",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "REDIS_TIMEOUT": {
                "context": "global",
                "default": "1000",
                "help": "Redis server timeout (in ms) for connect, read and write.",
                "id": "redis-timeout",
                "label": "Redis timeout (ms)",
                "regex": "^[0-9]+$",
                "type": "text",
            },
            "REDIS_USERNAME": {
                "context": "global",
                "default": "",
                "help": "Redis username used in AUTH command.",
                "id": "redis-username",
                "label": "Redis username",
                "regex": "^.*$",
                "type": "text",
            },
            "REDIS_PASSWORD": {
                "context": "global",
                "default": "",
                "help": "Redis password used in AUTH command.",
                "id": "redis-password",
                "label": "Redis password",
                "regex": "^.*$",
                "type": "password",
            },
            "REDIS_SENTINEL_HOSTS": {
                "context": "global",
                "default": "",
                "help": "Redis sentinel hosts with format host:[port] separated with spaces.",
                "id": "redis-sentinel-hosts",
                "label": "Redis sentinel hosts",
                "regex": "^.*$",
                "type": "text",
            },
            "REDIS_SENTINEL_USERNAME": {
                "context": "global",
                "default": "",
                "help": "Redis sentinel username.",
                "id": "redis-sentinel-username",
                "label": "Redis sentinel username",
                "regex": "^.*$",
                "type": "text",
            },
            "REDIS_SENTINEL_PASSWORD": {
                "context": "global",
                "default": "",
                "help": "Redis sentinel password.",
                "id": "redis-sentinel-password",
                "label": "Redis sentinel password",
                "regex": "^.*$",
                "type": "password",
            },
            "REDIS_SENTINEL_MASTER": {
                "context": "global",
                "default": "",
                "help": "Redis sentinel master name.",
                "id": "redis-sentinel-master",
                "label": "Redis sentinel master",
                "regex": "^.*$",
                "type": "text",
            },
            "REDIS_KEEPALIVE_IDLE": {
                "context": "global",
                "default": "30000",
                "help": "Max idle time (in ms) before closing redis connection in the pool.",
                "id": "redis-keepalive-idle",
                "label": "Redis keepalive idle (ms)",
                "regex": "^[0-9]+$",
                "type": "text",
            },
            "REDIS_KEEPALIVE_POOL": {
                "context": "global",
                "default": "10",
                "help": "Max number of redis connection(s) kept in the pool.",
                "id": "redis-keepalive-pool",
                "label": "Redis keepalive pool",
                "regex": "^[0-9]+$",
                "type": "text",
            },
        },
        "checksum": None,
    },
    {
        "id": "reverseproxy",
        "stream": "partial",
        "name": "Reverse proxy",
        "description": "Manage reverse proxy configurations.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": False,
        "settings": {
            "USE_REVERSE_PROXY": {
                "context": "multisite",
                "default": "no",
                "help": "Activate reverse proxy mode.",
                "id": "use-reverse-proxy",
                "label": "Use reverse proxy",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "REVERSE_PROXY_INTERCEPT_ERRORS": {
                "context": "multisite",
                "default": "yes",
                "help": "Intercept and rewrite errors.",
                "id": "reverse-proxy-intercept-errors",
                "label": "Intercept errors",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "REVERSE_PROXY_CUSTOM_HOST": {
                "context": "multisite",
                "default": "",
                "help": "Override Host header sent to upstream server.",
                "id": "reverse-proxy-custom-host",
                "label": "Reverse proxy custom host",
                "regex": "^.*$",
                "type": "text",
            },
            "REVERSE_PROXY_HOST": {
                "context": "multisite",
                "default": "",
                "help": "Full URL of the proxied resource (proxy_pass).",
                "id": "reverse-proxy-host",
                "label": "Reverse proxy host",
                "regex": "^.*$",
                "type": "text",
                "multiple": "reverse-proxy",
            },
            "REVERSE_PROXY_URL": {
                "context": "multisite",
                "default": "/",
                "help": "Location URL that will be proxied.",
                "id": "reverse-proxy-url",
                "label": "Reverse proxy url",
                "regex": "^.*$",
                "type": "text",
                "multiple": "reverse-proxy",
            },
            "REVERSE_PROXY_WS": {
                "context": "multisite",
                "default": "no",
                "help": "Enable websocket on the proxied resource.",
                "id": "reverse-proxy-ws",
                "label": "Reverse proxy WS",
                "regex": "^(yes|no)$",
                "type": "check",
                "multiple": "reverse-proxy",
            },
            "REVERSE_PROXY_HEADERS": {
                "context": "multisite",
                "default": "",
                "help": "List of HTTP headers to send to proxied resource separated with semicolons (values for proxy_set_header directive).",
                "id": "reverse-proxy-headers",
                "label": "Reverse proxy headers",
                "regex": "^(?![; ])(;? ?([\\w\\-]+)(?!.*\\2 ) [^;]+)*$",
                "type": "text",
                "multiple": "reverse-proxy",
            },
            "REVERSE_PROXY_HEADERS_CLIENT": {
                "context": "multisite",
                "default": "",
                "help": "List of HTTP headers to send to client separated with semicolons (values for add_header directive).",
                "id": "reverse-proxy-headers-client",
                "label": "Reverse proxy headers-client",
                "regex": "^(?![; ])(;? ?([\\w\\-]+)(?!.*\\2 ) [^;]+)*$",
                "type": "text",
                "multiple": "reverse-proxy",
            },
            "REVERSE_PROXY_BUFFERING": {
                "context": "multisite",
                "default": "yes",
                "help": "Enable or disable buffering of responses from proxied resource.",
                "id": "reverse-proxy-buffering",
                "label": "Reverse proxy buffering",
                "regex": "^(yes|no)$",
                "type": "check",
                "multiple": "reverse-proxy",
            },
            "REVERSE_PROXY_KEEPALIVE": {
                "context": "multisite",
                "default": "no",
                "help": "Enable or disable keepalive connections with the proxied resource.",
                "id": "reverse-proxy-keepalive",
                "label": "Reverse proxy keepalive",
                "regex": "^(yes|no)$",
                "type": "check",
                "multiple": "reverse-proxy",
            },
            "REVERSE_PROXY_AUTH_REQUEST": {
                "context": "multisite",
                "default": "",
                "help": "Enable authentication using an external provider (value of auth_request directive).",
                "id": "reverse-proxy-auth-request",
                "label": "Reverse proxy auth request",
                "regex": "^(\\/[\\w\\].~:\\/?#\\[@!$\\&'\\(\\)*+,;=\\-]*|off)?$",
                "type": "text",
                "multiple": "reverse-proxy",
            },
            "REVERSE_PROXY_AUTH_REQUEST_SIGNIN_URL": {
                "context": "multisite",
                "default": "",
                "help": "Redirect clients to sign-in URL when using REVERSE_PROXY_AUTH_REQUEST (used when auth_request call returned 401).",
                "id": "reverse-proxy-auth-request-signin-url",
                "label": "Auth request signin URL",
                "regex": "^(https?:\\/\\/[\\-\\w@:%.+~#=]+[\\-\\w\\(\\)!@:%+.~#?&\\/=$]*)?$",
                "type": "text",
                "multiple": "reverse-proxy",
            },
            "REVERSE_PROXY_AUTH_REQUEST_SET": {
                "context": "multisite",
                "default": "",
                "help": "List of variables to set from the authentication provider, separated with semicolons (values of auth_request_set directives).",
                "id": "reverse-proxy-auth-request-set",
                "label": "Reverse proxy auth request set",
                "regex": "^(?! ;)(;? ?(\\$[a-z_\\-]+)(?!.*\\2 ) [^;]+)*$",
                "type": "text",
                "multiple": "reverse-proxy",
            },
            "REVERSE_PROXY_CONNECT_TIMEOUT": {
                "context": "multisite",
                "default": "60s",
                "help": "Timeout when connecting to the proxied resource.",
                "id": "reverse-proxy-connect-timeout",
                "label": "Reverse proxy connect timeout",
                "regex": "^\\d+(ms?|[shdwMy])$",
                "type": "text",
                "multiple": "reverse-proxy",
            },
            "REVERSE_PROXY_READ_TIMEOUT": {
                "context": "multisite",
                "default": "60s",
                "help": "Timeout when reading from the proxied resource.",
                "id": "reverse-proxy-read-timeout",
                "label": "Reverse proxy read timeout",
                "regex": "^\\d+(ms?|[shdwMy])$",
                "type": "text",
                "multiple": "reverse-proxy",
            },
            "REVERSE_PROXY_SEND_TIMEOUT": {
                "context": "multisite",
                "default": "60s",
                "help": "Timeout when sending to the proxied resource.",
                "id": "reverse-proxy-send-timeout",
                "label": "Reverse proxy send timeout",
                "regex": "^\\d+(ms?|[shdwMy])$",
                "type": "text",
                "multiple": "reverse-proxy",
            },
            "REVERSE_PROXY_INCLUDES": {
                "context": "multisite",
                "default": "",
                "help": "Additional configuration to include in the location block, separated with spaces.",
                "id": "reverse-proxy-includes",
                "label": "Reverse proxy includes",
                "regex": "^(?! )( ?(\\w+)(?!.*\\b\\2\\b))*$",
                "type": "text",
                "multiple": "reverse-proxy",
            },
            "USE_PROXY_CACHE": {
                "context": "multisite",
                "default": "no",
                "help": "Enable or disable caching of the proxied resources.",
                "id": "use-proxy-cache",
                "label": "Reverse proxy cache",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "PROXY_CACHE_PATH_LEVELS": {
                "context": "global",
                "default": "1:2",
                "help": "Hierarchy levels of the cache.",
                "id": "proxy-cache-path-levels",
                "label": "Hierarchy levels",
                "regex": "^(:?[12]){1,3}$",
                "type": "text",
            },
            "PROXY_CACHE_PATH_ZONE_SIZE": {
                "context": "global",
                "default": "10m",
                "help": "Maximum size of cached metadata when caching proxied resources.",
                "id": "proxy-cache-path-zone-size",
                "label": "Reverse proxy cache zone size",
                "regex": "^\\d+[kKmMgG]?$",
                "type": "text",
            },
            "PROXY_CACHE_PATH_PARAMS": {
                "context": "global",
                "default": "max_size=100m",
                "help": "Additional parameters to add to the proxy_cache directive.",
                "id": "proxy-cache-path-params",
                "label": "Reverse proxy cache params",
                "regex": "^.*$",
                "type": "text",
            },
            "PROXY_CACHE_METHODS": {
                "context": "multisite",
                "default": "GET HEAD",
                "help": "HTTP methods that should trigger a cache operation.",
                "id": "proxy-cache-methods",
                "label": "Reverse proxy cache methods",
                "regex": "^(?! )( ?(GET|HEAD|POST|PUT|DELETE|CONNECT|OPTIONS|TRACE|PATCH)(?!.*\\2))+$",
                "type": "text",
            },
            "PROXY_CACHE_MIN_USES": {
                "context": "multisite",
                "default": "2",
                "help": "The minimum number of requests before a response is cached.",
                "id": "proxy-cache-min-uses",
                "label": "Reverse proxy cache minimum uses",
                "regex": "^[1-9]\\d*$",
                "type": "text",
            },
            "PROXY_CACHE_KEY": {
                "context": "multisite",
                "default": "$scheme$host$request_uri",
                "help": "The key used to uniquely identify a cached response.",
                "id": "proxy-cache-key",
                "label": "Reverse proxy cache key",
                "regex": "^(?! )( ?(\\$[a-z_]+)(?!.*\\2))+$",
                "type": "text",
            },
            "PROXY_CACHE_VALID": {
                "context": "multisite",
                "default": "200=24h 301=1h 302=24h",
                "help": "Define the caching time depending on the HTTP status code (list of status=time), separated with spaces.",
                "id": "proxy-cache-valid",
                "label": "Reverse proxy cache valid",
                "regex": "^(?! )( ?([1-5]\\d{2})(?!.*\\2=)=\\d+(ms?|[shdwMy]))*$",
                "type": "text",
            },
            "PROXY_NO_CACHE": {
                "context": "multisite",
                "default": "$http_pragma $http_authorization",
                "help": "Conditions to disable caching of responses.",
                "id": "proxy-no-cache",
                "label": "Reverse proxy no cache",
                "regex": "^.*$",
                "type": "text",
            },
            "PROXY_CACHE_BYPASS": {
                "context": "multisite",
                "default": "0",
                "help": "Conditions to bypass caching of responses.",
                "id": "proxy-cache-bypass",
                "label": "Reverse proxy bypass",
                "regex": "^.*$",
                "type": "text",
            },
        },
        "checksum": None,
    },
    {
        "id": "reversescan",
        "stream": "yes",
        "name": "Reverse scan",
        "description": "Scan clients ports to detect proxies or servers.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": True,
        "settings": {
            "USE_REVERSE_SCAN": {
                "context": "multisite",
                "default": "no",
                "help": "Enable scanning of clients ports and deny access if one is opened.",
                "id": "use-reverse-scan",
                "label": "Reverse scan",
                "regex": "^(no|yes)$",
                "type": "check",
            },
            "REVERSE_SCAN_PORTS": {
                "context": "multisite",
                "default": "22 80 443 3128 8000 8080",
                "help": "List of port to scan when using reverse scan feature.",
                "id": "reverse-scan-ports",
                "label": "Reverse scan ports",
                "regex": "^.*$",
                "type": "text",
            },
            "REVERSE_SCAN_TIMEOUT": {
                "context": "multisite",
                "default": "500",
                "help": "Specify the maximum timeout (in ms) when scanning a port.",
                "id": "reverse-scan-timeout",
                "label": "Reverse scan timeout",
                "regex": "^.*$",
                "type": "text",
            },
        },
        "checksum": None,
    },
    {
        "id": "selfsigned",
        "stream": "yes",
        "name": "Self-signed certificate",
        "description": "Generate self-signed certificate.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": False,
        "settings": {
            "GENERATE_SELF_SIGNED_SSL": {
                "context": "multisite",
                "default": "no",
                "help": "Generate and use self-signed certificate.",
                "id": "generate-self-signed-ssl",
                "label": "Activate self-signed certificate",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "SELF_SIGNED_SSL_EXPIRY": {
                "context": "multisite",
                "default": "365",
                "help": "Self-signed certificate expiry in days.",
                "id": "self-signed-ssl-expiry",
                "label": "Certificate expiry",
                "regex": "^\\d+$",
                "type": "text",
            },
            "SELF_SIGNED_SSL_SUBJ": {
                "context": "multisite",
                "default": "/CN=www.example.com/",
                "help": "Self-signed certificate subject.",
                "id": "self-signed-ssl-subj",
                "label": "Certificate subject",
                "regex": "^/CN=[^,]+$",
                "type": "text",
            },
        },
        "checksum": None,
    },
    {
        "id": "sessions",
        "stream": "yes",
        "name": "Sessions",
        "description": "Management of session used by other plugins.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": False,
        "settings": {
            "SESSIONS_SECRET": {
                "context": "global",
                "default": "random",
                "help": "Secret used to encrypt sessions variables for storing data related to challenges.",
                "id": "session-secret",
                "label": "Sessions secret",
                "regex": "^\\w+$",
                "type": "password",
            },
            "SESSIONS_NAME": {
                "context": "global",
                "default": "random",
                "help": "Name of the cookie given to clients.",
                "id": "sessions-name",
                "label": "Sessions name",
                "regex": "^\\w+$",
                "type": "text",
            },
            "SESSIONS_IDLING_TIMEOUT": {
                "context": "global",
                "default": "1800",
                "help": "Maximum time (in seconds) of inactivity before the session is invalidated.",
                "id": "sessions-idling-timeout",
                "label": "Sessions idling timeout",
                "regex": "^\\d+$",
                "type": "text",
            },
            "SESSIONS_ROLLING_TIMEOUT": {
                "context": "global",
                "default": "3600",
                "help": "Maximum time (in seconds) before a session must be renewed.",
                "id": "sessions-rolling-timeout",
                "label": "Sessions rolling timeout",
                "regex": "^\\d+$",
                "type": "text",
            },
            "SESSIONS_ABSOLUTE_TIMEOUT": {
                "context": "global",
                "default": "86400",
                "help": "Maximum time (in seconds) before a session is destroyed.",
                "id": "sessions-absolute-timeout",
                "label": "Sessions absolute timeout",
                "regex": "^\\d+$",
                "type": "text",
            },
            "SESSIONS_CHECK_IP": {
                "context": "global",
                "default": "yes",
                "help": "Destroy session if IP address is different than original one.",
                "id": "sessions-check-ip",
                "label": "Sessions check IP",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "SESSIONS_CHECK_USER_AGENT": {
                "context": "global",
                "default": "yes",
                "help": "Destroy session if User-Agent is different than original one.",
                "id": "sessions-user-agent",
                "label": "Sessions check User-Agent",
                "regex": "^(yes|no)$",
                "type": "check",
            },
        },
        "checksum": None,
    },
    {
        "id": "ui",
        "stream": "no",
        "name": "UI",
        "description": "Integrate easily the BunkerWeb UI.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": False,
        "settings": {
            "USE_UI": {
                "context": "multisite",
                "default": "no",
                "help": "Use UI",
                "id": "use-ui",
                "label": "Use UI",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "UI_HOST": {
                "context": "global",
                "default": "",
                "help": "Address of the web UI used for initial setup",
                "id": "ui-host",
                "label": "UI host",
                "regex": "^.*$",
                "type": "text",
            },
        },
        "checksum": None,
    },
    {
        "id": "whitelist",
        "stream": "partial",
        "name": "Whitelist",
        "description": "Allow access based on internal and external IP/network/rDNS/ASN whitelists.",
        "version": "1.0",
        "type": "core",
        "method": "manual",
        "page": True,
        "settings": {
            "USE_WHITELIST": {
                "context": "multisite",
                "default": "yes",
                "help": "Activate whitelist feature.",
                "id": "use-whitelist",
                "label": "Activate whitelisting",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "WHITELIST_IP": {
                "context": "multisite",
                "default": "20.191.45.212 40.88.21.235 40.76.173.151 40.76.163.7 20.185.79.47 52.142.26.175 20.185.79.15 52.142.24.149 40.76.162.208 40.76.163.23 40.76.162.191 40.76.162.247",
                "help": "List of IP/network, separated with spaces, to put into the whitelist.",
                "id": "whitelist-ip",
                "label": "Whitelist IP/network",
                "regex": "^(?! )( *(((\\b25[0-5]|\\b2[0-4]\\d|\\b[01]?\\d\\d?)(\\.(25[0-5]|2[0-4]\\d|[01]?\\d\\d?)){3})(\\/([1-2][0-9]?|3[0-2]?|[04-9]))?|(([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]Z{0,4}){0,4}%[0-9a-zA-Z]+|::(ffff(:0{1,4})?:)?((25[0-5]|(2[0-4]|1?\\d)?\\d)\\.){3}(25[0-5]|(2[0-4]|1?\\d)?\\d)|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1?\\d)?\\d)\\.){3}(25[0-5]|(2[0-4]|1?\\d)?\\d))(\\/(12[0-8]|1[01][0-9]|[0-9][0-9]?))?)(?!.*\\D\\2([^\\d\\/]|$)) *)*$",
                "type": "text",
            },
            "WHITELIST_RDNS": {
                "context": "multisite",
                "default": ".google.com .googlebot.com .yandex.ru .yandex.net .yandex.com .search.msn.com .baidu.com .baidu.jp .crawl.yahoo.net .fwd.linkedin.com .twitter.com .twttr.com .discord.com",
                "help": "List of reverse DNS suffixes, separated with spaces, to whitelist.",
                "id": "whitelist-rdns",
                "label": "Whitelist reverse DNS",
                "regex": "^( *(([^ ]+)(?!.*\\3( |$))) *)*$",
                "type": "text",
            },
            "WHITELIST_RDNS_GLOBAL": {
                "context": "multisite",
                "default": "yes",
                "help": "Only perform RDNS whitelist checks on global IP addresses.",
                "id": "whitelist-rdns-global",
                "label": "Whitelist reverse DNS global IPs",
                "regex": "^(yes|no)$",
                "type": "check",
            },
            "WHITELIST_ASN": {
                "context": "multisite",
                "default": "32934",
                "help": "List of ASN numbers, separated with spaces, to whitelist.",
                "id": "whitelist-asn",
                "label": "Whitelist ASN",
                "regex": "^^( *((ASN?)?(\\d+)\\b(?!.*[SN ]\\4\\b)) *)*$",
                "type": "text",
            },
            "WHITELIST_USER_AGENT": {
                "context": "multisite",
                "default": "",
                "help": "List of User-Agent (PCRE regex), separated with spaces, to whitelist.",
                "id": "whitelist-user-agent",
                "label": "Whitelist User-Agent",
                "regex": "^.*$",
                "type": "text",
            },
            "WHITELIST_URI": {
                "context": "multisite",
                "default": "",
                "help": "List of URI (PCRE regex), separated with spaces, to whitelist.",
                "id": "whitelist-uri",
                "label": "Whitelist URI",
                "regex": "^( *(.*)(?!.*\\2(?!.)) *)*$",
                "type": "text",
            },
            "WHITELIST_IP_URLS": {
                "context": "global",
                "default": "",
                "help": "List of URLs, separated with spaces, containing good IP/network to whitelist.",
                "id": "whitelist-ip-urls",
                "label": "Whitelist IP/network URLs",
                "regex": "^( *((https?:\\/\\/|file:\\/\\/\\/)[\\-\\w@:%.+~#=]+[\\-\\w\\(\\)!@:%+.~#?&\\/=$]*)(?!.*\\2(?!.)) *)*$",
                "type": "text",
            },
            "WHITELIST_RDNS_URLS": {
                "context": "global",
                "default": "",
                "help": "List of URLs, separated with spaces, containing reverse DNS suffixes to whitelist.",
                "id": "whitelist-rdns-urls",
                "label": "Whitelist reverse DNS URLs",
                "regex": "^( *((https?:\\/\\/|file:\\/\\/\\/)[\\-\\w@:%.+~#=]+[\\-\\w\\(\\)!@:%+.~#?&\\/=$]*)(?!.*\\2(?!.)) *)*$",
                "type": "text",
            },
            "WHITELIST_ASN_URLS": {
                "context": "global",
                "default": "",
                "help": "List of URLs, separated with spaces, containing ASN to whitelist.",
                "id": "whitelist-asn-urls",
                "label": "Whitelist ASN URLs",
                "regex": "^( *((https?:\\/\\/|file:\\/\\/\\/)[\\-\\w@:%.+~#=]+[\\-\\w\\(\\)!@:%+.~#?&\\/=$]*)(?!.*\\2(?!.)) *)*$",
                "type": "text",
            },
            "WHITELIST_USER_AGENT_URLS": {
                "context": "global",
                "default": "",
                "help": "List of URLs, separated with spaces, containing good User-Agent to whitelist.",
                "id": "whitelist-user-agent-urls",
                "label": "Whitelist User-Agent URLs",
                "regex": "^( *((https?:\\/\\/|file:\\/\\/\\/)[\\-\\w@:%.+~#=]+[\\-\\w\\(\\)!@:%+.~#?&\\/=$]*)(?!.*\\2(?!.)) *)*$",
                "type": "text",
            },
            "WHITELIST_URI_URLS": {
                "context": "global",
                "default": "",
                "help": "List of URLs, separated with spaces, containing bad URI to whitelist.",
                "id": "whitelist-uri-urls",
                "label": "Whitelist URI URLs",
                "regex": "^( *((https?:\\/\\/|file:\\/\\/\\/)[\\-\\w@:%.+~#=]+[\\-\\w\\(\\)!@:%+.~#?&\\/=$]*)(?!.*\\2(?!.)) *)*$",
                "type": "text",
            },
        },
        "checksum": None,
    },
]

template_settings = {
    "ERRORS": "",
    "USE_UI": "no",
    "USE_CORS": "no",
    "REVERSE_PROXY_HOST_1": "template1",
    "REVERSE_PROXY_HOST_2": "template2",
}

# Service settings
service_settings = {
    "ERRORS": {"value": "", "global": True, "method": "scheduler"},
    "USE_UI": {"value": "yes", "global": True, "method": "ui"},
    "USE_CORS": {"value": "yes", "global": True, "method": "scheduler"},
    "REVERSE_PROXY_HOST_1": {"value": "yes", "global": True, "method": "scheduler"},
    "REVERSE_PROXY_HOST": {"value": "no", "global": True, "method": "ui"},
}


# Default template
default_template = {
    "name": "default",
    "steps": [
        {
            "title": "Title 1",
            "subtitle": "subtitle 1",
            "settings": ["USE_UI", "USE_CORS"],
        },
        {
            "title": "Title 2",
            "subtitle": "subtitle 2",
            "settings": ["USE_UI", "USE_CORS"],
        },
    ],
    "configs": {},
    "settings": {
        "USE_UI": "no",
        "USE_CORS": "no",
        "USE_GZIP": "dsfrgrdgrdgrdhgd",
        "REVERSE_PROXY_HOST_1": "template1",
        "REVERSE_PROXY_HOST_2": "template2",
        "REVERSE_PROXY_HOST": "template",
    },
}


def get_service_forms(templates=[], plugins=[], service_settings={}):

    forms = {"advanced": {}, "easy": {}, "raw": {}}

    for template in templates:
        forms["advanced"][template.get("name")] = set_advanced(template, plugins, service_settings)
        forms["raw"][template.get("name")] = set_raw(template, plugins, service_settings)
        forms["easy"][template.get("name")] = set_easy(template, plugins, service_settings)

    return forms


def set_easy(template, plugins_base, service_settings):
    """
    Prepare the easy form based on the template and plugins data.
    We need to loop on each steps and prepare settings and configs for each step.
    """
    template_settings = template.get("settings")
    plugins = copy.deepcopy(plugins_base)
    configs = template.get("configs")
    steps = template.get("steps")

    for step in steps:
        step_settings = step.get("settings", {})
        step_configs = step.get("configs", {})
        # Loop on step settings to set the settings value
        loop_id = 0
        step_settings_output = {}
        for setting in step_settings:
            loop_id += 1
            # Get relate setting from plugins using setting name
            plugin = next(
                (plugin for plugin in plugins if setting in plugin.get("settings")),
                None,
            )

            if not plugin:
                continue

            if not plugin.get("settings").get(setting):
                continue

            plugin_setting = copy.deepcopy(plugin.get("settings").get(setting))

            plugin_setting = format_setting(
                setting,
                plugin_setting,
                len(step_settings),
                loop_id,
                template_settings,
                service_settings,
            )

            step_settings_output[setting] = plugin_setting

        step["settings"] = step_settings_output

    return steps


def set_raw(template, plugins_base, service_settings):
    """
    Set the raw form based on the template and plugins data.
    It consists of keeping only the value or default value for each plugin settings.
    """
    template_settings = template.get("settings")
    settings = template.get("settings")
    raw_settings = {}
    # Copy of the plugins base
    plugins = copy.deepcopy(plugins_base)
    # Update settings with global config data
    for plugin in plugins:
        for setting, value in plugin.get("settings").items():
            # avoid some methods from services_settings
            if setting in service_settings and service_settings[setting].get("method", "ui") not in ("ui", "default", "manual"):
                continue

            raw_value = False

            # Start by setting template value if exists
            if setting in template_settings:
                # Update value or set default as value
                raw_value = template_settings.get(setting, value.get("default"))

            # Then override by service settings
            if setting in service_settings:
                raw_value = service_settings[setting].get("value", value.get("value", value.get("default")))

            # Add value only if exists
            if raw_value:
                raw_settings[setting] = raw_value

    return raw_settings


def set_advanced(template, plugins_base, service_settings):
    """
    Set the advanced form based on the template and plugins data.
    It consists of formatting each plugin settings to be used in the advanced form.
    """
    template_settings = template.get("settings")
    # Copy of the plugins base data
    plugins = copy.deepcopy(plugins_base)
    # Update settings with global config data
    for plugin in plugins:
        loop_id = 0
        total_settings = len(plugin.get("settings"))
        for setting, value in plugin.get("settings").items():
            loop_id += 1
            value = format_setting(
                setting,
                value,
                total_settings,
                loop_id,
                template_settings,
                service_settings,
            )

    set_multiples(template, plugins, service_settings)

    return plugins


def get_multiple_from_template(template, multiples):
    """
    We are gonna loop on each plugins multiples group, in case a setting is matching a template setting,
    we will create a group using the prefix as key (or "0" if no prefix) with default settings at first.
    Then we will override by the template value in case there is one.
    This will return something of this type :
    {'0' : {'setting' : value, 'setting2': value2}, '1' : {'setting_1': value, 'setting2_1': value}} }
    """
    # Loop on each plugin and loop on multiples key
    # Check if the name us matching a template key
    multiple_plugin = copy.deepcopy(multiples)

    multiple_template = {}
    for setting, value in template.get("settings").items():
        # Sanitize setting name to remove prefix of type _1 if exists
        # Slipt by _ and check if last element is a digit
        format_setting = setting
        setting_split = setting.split("_")
        prefix = "0"
        if setting_split[-1].isdigit():
            prefix = setting_split[-1]
            format_setting = "_".join(setting_split[:-1])
        # loop on settings of a multiple group
        for mult_name, mult_settings in multiple_plugin.items():
            # Check if at least one multiple plugin setting is matching the template setting
            if format_setting in mult_settings:
                if not mult_name in multiple_template:
                    multiple_template[mult_name] = {}
                # Case it is, we will check if already a group with the right prefix exists
                # If not, we will create it
                if not prefix in multiple_template[mult_name]:
                    # We want each settings to have the prefix if exists
                    # We will get the value of the setting without the prefix and create a prefix key with the same value
                    # And after that we can delete the original setting
                    new_multiple_group = {}
                    for multSett, multValue in mult_settings.items():
                        new_multiple_group[f"{multSett}{f'_{prefix}' if prefix != '0' else ''}"] = multValue

                    new_multiple_group = copy.deepcopy(new_multiple_group)

                    # Update id for each settings
                    for multSett, multValue in new_multiple_group.items():
                        multValue["id"] = f"{multValue['id']}{f'-{prefix}' if prefix != '0' else ''}"

                    multiple_template[mult_name][prefix] = new_multiple_group

                # We can now add the template value to setting using the same setting name with prefix
                multiple_template[mult_name][prefix][setting]["value"] = value

                # Sort key incrementally
                for mult_name, mult_settings in multiple_template.items():
                    multiple_template[mult_name] = dict(sorted(mult_settings.items(), key=lambda item: int(item[0])))
    return multiple_template


def get_multiple_from_settings(settings, multiples):
    """
    We are gonna loop on each plugins multiples group, in case a setting is matching a service / global config setting,
    we will create a group using the prefix as key (or "0" if no prefix) with default settings at first.
    Then we will override by the service / global config value in case there is one.
    This will return something of this type :
    {'0' : {'setting' : value, 'setting2': value2}, '1' : {'setting_1': value, 'setting2_1': value}} }
    """

    # Loop on each plugin and loop on multiples key
    # Check if the name us matching a template key
    multiple_plugins = copy.deepcopy(multiples)

    multiple_settings = {}
    for setting, value in settings.items():
        # Sanitize setting name to remove prefix of type _1 if exists
        # Slipt by _ and check if last element is a digit
        format_setting = setting
        setting_split = setting.split("_")
        prefix = "0"
        if setting_split[-1].isdigit():
            prefix = setting_split[-1]
            format_setting = "_".join(setting_split[:-1])
        # loop on settings of a multiple group
        for mult_name, mult_settings in multiple_plugins.items():
            # Check if at least one multiple plugin setting is matching the template setting
            if format_setting in mult_settings:

                if not mult_name in multiple_settings:
                    multiple_settings[mult_name] = {}
                # Case it is, we will check if already a group with the right prefix exists
                # If not, we will create it
                if not prefix in multiple_settings:
                    # We want each settings to have the prefix if exists
                    # We will get the value of the setting without the prefix and create a prefix key with the same value
                    # And after that we can delete the original setting
                    new_multiple_group = {}
                    for multSett, multValue in mult_settings.items():
                        new_multiple_group[f"{multSett}{f'_{prefix}' if prefix != '0' else ''}"] = multValue

                    new_multiple_group = copy.deepcopy(new_multiple_group)

                    # Update id for each settings
                    for multSett, multValue in new_multiple_group.items():
                        multValue["id"] = f"{multValue['id']}{f'-{prefix}' if prefix != '0' else ''}"

                    multiple_settings[mult_name][prefix] = new_multiple_group

                # We can now add the template value to setting using the same setting name with prefix
                multiple_settings[mult_name][prefix][setting]["value"] = value.get("value", multiple_settings[mult_name][prefix][setting]["value"])
                multiple_settings[mult_name][prefix][setting]["method"] = value.get("method", "ui")
                multiple_settings[mult_name][prefix][setting]["disabled"] = False if value.get("method", "ui") in ("ui", "default", "manual") else True
                if multiple_settings[mult_name][prefix][setting].get("disabled", False):
                    multiple_settings[mult_name][prefix][setting]["popovers"] = [
                        {
                            "iconName": "trespass",
                            "text": "inp_popover_method_disabled",
                        }
                    ] + multiple_settings[mult_name][prefix][setting].get("popovers", [])
    return multiple_settings


def set_multiples(template, format_plugins, service_settings):
    """
    Set the multiples settings for each plugin.
    """
    # copy of format plugins
    for plugin in format_plugins:
        # Get multiples
        multiples = {}
        settings_to_delete = []
        total_settings = len(plugin.get("settings"))
        zindex = 0
        for setting, value in plugin.get("settings").items():

            if not value.get("multiple"):
                continue

            zindex += 1

            value["containerClass"] = f"z-{total_settings - zindex}"

            mult_name = value.get("multiple")
            # Get the multiple value and set it as key if not in multiples dict
            if mult_name not in multiples:
                multiples[mult_name] = {}

            multiples[mult_name][setting] = value
            settings_to_delete.append(setting)

        # Delete multiple settings from regular settings
        for setting in settings_to_delete:
            del plugin["settings"][setting]

        if len(multiples):
            # Now that we have for each plugin the multiples settings, we need to do the following
            # Get all settings from template that are multiples
            template_multiples = get_multiple_from_template(template, multiples)
            # Get all settings from service settings / global config that are multiples
            service_multiples = get_multiple_from_settings(service_settings, multiples)
            # Get service multiples if at least one, else use template multiples
            plugin["multiples"] = service_multiples if len(service_multiples) else template_multiples

    return format_plugins


def format_setting(
    setting_name,
    setting_value,
    total_settings,
    loop_id,
    template_settings,
    service_settings,
):
    """
    Format a setting in order to be used with form builder.
    This will only set value for none multiple settings.
    Additionnel set_multiples function will handle multiple settings.
    """
    # add zindex for field in case not a multiple
    # Case multiple, this will be set on the group level
    if not "multiple" in setting_value:
        setting_value["containerClass"] = f"z-{total_settings - loop_id}"

    # regex by pattern
    setting_value["pattern"] = setting_value.get("regex", "")

    # set inpType based on type define for each settings
    inpType = (
        "checkbox"
        if setting_value.get("type") == "check"
        else ("select" if setting_value.get("type") == "select" else "datepicker" if setting_value.get("type") == "date" else "input")
    )
    setting_value["inpType"] = inpType

    # set name using the label
    setting_value["name"] = setting_value.get("label")

    # case select
    if inpType == "select":
        # replace "select" key by "values"
        setting_value["values"] = setting_value.pop("select")

    # add columns
    setting_value["columns"] = {"pc": 4, "tablet": 6, "mobile": 12}

    # By default, the input is enabled unless specific method
    setting_value["disabled"] = False

    setting_value["value"] = setting_value.get("default")

    # Start by setting template value if exists
    if setting_name in template_settings and not "multiple" in setting_value:
        # Update value or set default as value
        setting_value["value"] = template_settings.get(setting_name, setting_value.get("default"))

    # Then override by service settings if not a multiple
    # Case multiple, we need to keep the default value and override only each multiple group
    if setting_name in service_settings and not "multiple" in setting_value:
        setting_value["value"] = service_settings[setting_name].get("value", setting_value.get("value", setting_value.get("default")))
        setting_value["method"] = service_settings[setting_name].get("method", "ui")

    # Then override by service settings
    if setting_name in service_settings:
        setting_value["disabled"] = False if service_settings[setting_name].get("method", "ui") in ("ui", "default", "manual") else True

    # Prepare popover checking "help", "context"
    popovers = []

    if (setting_value.get("disabled", False)) and service_settings[setting_name].get("method", "ui") not in ("ui", "default", "manual"):
        popovers.append(
            {
                "iconName": "trespass",
                "text": "inp_popover_method_disabled",
            }
        )

    if setting_value.get("context"):
        popovers.append(
            {
                "iconName": ("disk" if setting_value.get("context") == "multisite" else "globe"),
                "text": ("inp_popover_multisite" if setting_value.get("context") == "multisite" else "inp_popover_global"),
            }
        )

    if setting_value.get("help"):
        popovers.append(
            {
                "iconName": "info",
                "text": setting_value.get("help"),
            }
        )

    setting_value["popovers"] = popovers
    return setting_value


templates = [default_template]


def global_config_builder():
    builder = [
        {
            "type": "card",
            "containerColumns": {"pc": 12, "tablet": 12, "mobile": 12},
            "widgets": [
                {
                    "type": "Title",
                    "data": {"title": "global_config_title", "type": "container"},
                },
                {
                    "type": "Subtitle",
                    "data": {"subtitle": "global_config_subtitle", "type": "container"},
                },
                {
                    "type": "Templates",
                    "data": {
                        "templates": get_service_forms(templates, plugins, service_settings),
                    },
                },
            ],
        }
    ]

    return builder


output = global_config_builder()
with open("globalconfig.json", "w") as f:
    json.dump(output, f, indent=4)

output_base64_bytes = base64.b64encode(bytes(json.dumps(output), "utf-8"))
output_base64_string = output_base64_bytes.decode("ascii")
with open("globalconfig64.txt", "w") as f:
    f.write(output_base64_string)
