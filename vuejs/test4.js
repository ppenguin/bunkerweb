const tableData = {
  title: "Table title",
  minWidth: "lg",
  header: [
    "Name",
    "Plugin id",
    "Interval",
    "Last run",
    "Success",
    "last run date",
    "Cache",
  ],
  positions: [2, 2, 1, 1, 1, 3, 2],
  items: [
    [
      {
        name: "anonymous-report",
        type: "Text",
        data: {
          text: "anonymous-report",
        },
      },
      {
        plugin_id: "misc",
        type: "Text",
        data: {
          text: "misc",
        },
      },
      {
        every: "day",
        type: "Text",
        data: {
          text: "day",
        },
      },
      {
        reload: "no",
        type: "Icons",
        data: {
          iconColor: "error",
          iconName: "cross",
        },
      },
      {
        success: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        last_run: "2024/06/14, 01:33:11 PM",
        type: "Text",
        data: {
          text: "2024/06/14, 01:33:11 PM",
        },
      },
      {
        cache: [],
        type: "Text",
        data: {
          text: "No cache",
        },
      },
    ],
    [
      {
        name: "backup-data",
        type: "Text",
        data: {
          text: "backup-data",
        },
      },
      {
        plugin_id: "backup",
        type: "Text",
        data: {
          text: "backup",
        },
      },
      {
        every: "day",
        type: "Text",
        data: {
          text: "day",
        },
      },
      {
        reload: "no",
        type: "Icons",
        data: {
          iconColor: "error",
          iconName: "cross",
        },
      },
      {
        success: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        last_run: "2024/06/14, 01:33:10 PM",
        type: "Text",
        data: {
          text: "2024/06/14, 01:33:10 PM",
        },
      },
      {
        cache: [],
        type: "Text",
        data: {
          text: "No cache",
        },
      },
    ],
    [
      {
        name: "blacklist-download",
        type: "Text",
        data: {
          text: "blacklist-download",
        },
      },
      {
        plugin_id: "blacklist",
        type: "Text",
        data: {
          text: "blacklist",
        },
      },
      {
        every: "hour",
        type: "Text",
        data: {
          text: "hour",
        },
      },
      {
        reload: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        success: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        last_run: "2024/06/14, 01:33:09 PM",
        type: "Text",
        data: {
          text: "2024/06/14, 01:33:09 PM",
        },
      },
      {
        cache: [],
        type: "Text",
        data: {
          text: "No cache",
        },
      },
    ],
    [
      {
        name: "bunkernet-data",
        type: "Text",
        data: {
          text: "bunkernet-data",
        },
      },
      {
        plugin_id: "bunkernet",
        type: "Text",
        data: {
          text: "bunkernet",
        },
      },
      {
        every: "day",
        type: "Text",
        data: {
          text: "day",
        },
      },
      {
        reload: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        success: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        last_run: "2024/06/14, 01:33:11 PM",
        type: "Text",
        data: {
          text: "2024/06/14, 01:33:11 PM",
        },
      },
      {
        cache: [],
        type: "Text",
        data: {
          text: "No cache",
        },
      },
    ],
    [
      {
        name: "bunkernet-register",
        type: "Text",
        data: {
          text: "bunkernet-register",
        },
      },
      {
        plugin_id: "bunkernet",
        type: "Text",
        data: {
          text: "bunkernet",
        },
      },
      {
        every: "hour",
        type: "Text",
        data: {
          text: "hour",
        },
      },
      {
        reload: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        success: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        last_run: "2024/06/14, 01:33:09 PM",
        type: "Text",
        data: {
          text: "2024/06/14, 01:33:09 PM",
        },
      },
      {
        cache: [],
        type: "Text",
        data: {
          text: "No cache",
        },
      },
    ],
    [
      {
        name: "certbot-new",
        type: "Text",
        data: {
          text: "certbot-new",
        },
      },
      {
        plugin_id: "letsencrypt",
        type: "Text",
        data: {
          text: "letsencrypt",
        },
      },
      {
        every: "once",
        type: "Text",
        data: {
          text: "once",
        },
      },
      {
        reload: "no",
        type: "Icons",
        data: {
          iconColor: "error",
          iconName: "cross",
        },
      },
      {
        success: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        last_run: "2024/06/14, 01:33:08 PM",
        type: "Text",
        data: {
          text: "2024/06/14, 01:33:08 PM",
        },
      },
      {
        cache: [],
        type: "Text",
        data: {
          text: "No cache",
        },
      },
    ],
    [
      {
        name: "certbot-renew",
        type: "Text",
        data: {
          text: "certbot-renew",
        },
      },
      {
        plugin_id: "letsencrypt",
        type: "Text",
        data: {
          text: "letsencrypt",
        },
      },
      {
        every: "day",
        type: "Text",
        data: {
          text: "day",
        },
      },
      {
        reload: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        success: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        last_run: "2024/06/14, 01:33:09 PM",
        type: "Text",
        data: {
          text: "2024/06/14, 01:33:09 PM",
        },
      },
      {
        cache: [],
        type: "Text",
        data: {
          text: "No cache",
        },
      },
    ],
    [
      {
        name: "coreruleset-nightly",
        type: "Text",
        data: {
          text: "coreruleset-nightly",
        },
      },
      {
        plugin_id: "modsecurity",
        type: "Text",
        data: {
          text: "modsecurity",
        },
      },
      {
        every: "day",
        type: "Text",
        data: {
          text: "day",
        },
      },
      {
        reload: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        success: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        last_run: "2024/06/14, 01:33:09 PM",
        type: "Text",
        data: {
          text: "2024/06/14, 01:33:09 PM",
        },
      },
      {
        cache: [],
        type: "Text",
        data: {
          text: "No cache",
        },
      },
    ],
    [
      {
        name: "custom-cert",
        type: "Text",
        data: {
          text: "custom-cert",
        },
      },
      {
        plugin_id: "customcert",
        type: "Text",
        data: {
          text: "customcert",
        },
      },
      {
        every: "day",
        type: "Text",
        data: {
          text: "day",
        },
      },
      {
        reload: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        success: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        last_run: "2024/06/14, 01:33:10 PM",
        type: "Text",
        data: {
          text: "2024/06/14, 01:33:10 PM",
        },
      },
      {
        cache: [],
        type: "Text",
        data: {
          text: "No cache",
        },
      },
    ],
    [
      {
        name: "default-server-cert",
        type: "Text",
        data: {
          text: "default-server-cert",
        },
      },
      {
        plugin_id: "misc",
        type: "Text",
        data: {
          text: "misc",
        },
      },
      {
        every: "once",
        type: "Text",
        data: {
          text: "once",
        },
      },
      {
        reload: "no",
        type: "Icons",
        data: {
          iconColor: "error",
          iconName: "cross",
        },
      },
      {
        success: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        last_run: "2024/06/14, 01:33:10 PM",
        type: "Text",
        data: {
          text: "2024/06/14, 01:33:10 PM",
        },
      },
      {
        cache: "none default-server-cert.pem default-server-cert.key",
        type: "Fields",
        data: {
          setting: {
            id: "default-server-cert_cache",
            label: "default-server-cert_cache",
            hideLabel: true,
            inpType: "select",
            name: "default-server-cert_cache",
            value: "none",
            values: [
              "none",
              "default-server-cert.pem",
              "default-server-cert.key",
            ],
            columns: {
              pc: 12,
              tablet: 12,
              mobile: 12,
            },
            overflowAttrEl: "data-table-body",
            containerClass: "table",
            maxBtnChars: 12,
            popovers: [
              {
                iconColor: "info",
                iconName: "info",
                text: "jobs_download_cache_file",
              },
            ],
          },
        },
      },
    ],
    [
      {
        name: "download-plugins",
        type: "Text",
        data: {
          text: "download-plugins",
        },
      },
      {
        plugin_id: "misc",
        type: "Text",
        data: {
          text: "misc",
        },
      },
      {
        every: "once",
        type: "Text",
        data: {
          text: "once",
        },
      },
      {
        reload: "no",
        type: "Icons",
        data: {
          iconColor: "error",
          iconName: "cross",
        },
      },
      {
        success: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        last_run: "2024/06/14, 01:33:13 PM",
        type: "Text",
        data: {
          text: "2024/06/14, 01:33:13 PM",
        },
      },
      {
        cache: [],
        type: "Text",
        data: {
          text: "No cache",
        },
      },
    ],
    [
      {
        name: "download-pro-plugins",
        type: "Text",
        data: {
          text: "download-pro-plugins",
        },
      },
      {
        plugin_id: "pro",
        type: "Text",
        data: {
          text: "pro",
        },
      },
      {
        every: "day",
        type: "Text",
        data: {
          text: "day",
        },
      },
      {
        reload: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        success: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        last_run: "2024/06/14, 01:33:10 PM",
        type: "Text",
        data: {
          text: "2024/06/14, 01:33:10 PM",
        },
      },
      {
        cache: [],
        type: "Text",
        data: {
          text: "No cache",
        },
      },
    ],
    [
      {
        name: "failover-backup",
        type: "Text",
        data: {
          text: "failover-backup",
        },
      },
      {
        plugin_id: "jobs",
        type: "Text",
        data: {
          text: "jobs",
        },
      },
      {
        every: "once",
        type: "Text",
        data: {
          text: "once",
        },
      },
      {
        reload: "no",
        type: "Icons",
        data: {
          iconColor: "error",
          iconName: "cross",
        },
      },
      {
        success: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        last_run: "2024/06/14, 01:33:16 PM",
        type: "Text",
        data: {
          text: "2024/06/14, 01:33:16 PM",
        },
      },
      {
        cache: "none folder:/var/tmp/bunkerweb/failover.tgz",
        type: "Fields",
        data: {
          setting: {
            id: "failover-backup_cache",
            label: "failover-backup_cache",
            hideLabel: true,
            inpType: "select",
            name: "failover-backup_cache",
            value: "none",
            values: ["none", "folder:/var/tmp/bunkerweb/failover.tgz"],
            columns: {
              pc: 12,
              tablet: 12,
              mobile: 12,
            },
            overflowAttrEl: "data-table-body",
            containerClass: "table",
            maxBtnChars: 12,
            popovers: [
              {
                iconColor: "info",
                iconName: "info",
                text: "jobs_download_cache_file",
              },
            ],
          },
        },
      },
    ],
    [
      {
        name: "greylist-download",
        type: "Text",
        data: {
          text: "greylist-download",
        },
      },
      {
        plugin_id: "greylist",
        type: "Text",
        data: {
          text: "greylist",
        },
      },
      {
        every: "hour",
        type: "Text",
        data: {
          text: "hour",
        },
      },
      {
        reload: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        success: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        last_run: "2024/06/14, 01:33:09 PM",
        type: "Text",
        data: {
          text: "2024/06/14, 01:33:09 PM",
        },
      },
      {
        cache: [],
        type: "Text",
        data: {
          text: "No cache",
        },
      },
    ],
    [
      {
        name: "mmdb-asn",
        type: "Text",
        data: {
          text: "mmdb-asn",
        },
      },
      {
        plugin_id: "jobs",
        type: "Text",
        data: {
          text: "jobs",
        },
      },
      {
        every: "day",
        type: "Text",
        data: {
          text: "day",
        },
      },
      {
        reload: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        success: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        last_run: "2024/06/14, 01:33:14 PM",
        type: "Text",
        data: {
          text: "2024/06/14, 01:33:14 PM",
        },
      },
      {
        cache: "none asn.mmdb",
        type: "Fields",
        data: {
          setting: {
            id: "mmdb-asn_cache",
            label: "mmdb-asn_cache",
            hideLabel: true,
            inpType: "select",
            name: "mmdb-asn_cache",
            value: "none",
            values: ["none", "asn.mmdb"],
            columns: {
              pc: 12,
              tablet: 12,
              mobile: 12,
            },
            overflowAttrEl: "data-table-body",
            containerClass: "table",
            maxBtnChars: 12,
            popovers: [
              {
                iconColor: "info",
                iconName: "info",
                text: "jobs_download_cache_file",
              },
            ],
          },
        },
      },
    ],
    [
      {
        name: "mmdb-country",
        type: "Text",
        data: {
          text: "mmdb-country",
        },
      },
      {
        plugin_id: "jobs",
        type: "Text",
        data: {
          text: "jobs",
        },
      },
      {
        every: "day",
        type: "Text",
        data: {
          text: "day",
        },
      },
      {
        reload: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        success: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        last_run: "2024/06/14, 01:33:12 PM",
        type: "Text",
        data: {
          text: "2024/06/14, 01:33:12 PM",
        },
      },
      {
        cache: "none country.mmdb",
        type: "Fields",
        data: {
          setting: {
            id: "mmdb-country_cache",
            label: "mmdb-country_cache",
            hideLabel: true,
            inpType: "select",
            name: "mmdb-country_cache",
            value: "none",
            values: ["none", "country.mmdb"],
            columns: {
              pc: 12,
              tablet: 12,
              mobile: 12,
            },
            overflowAttrEl: "data-table-body",
            containerClass: "table",
            maxBtnChars: 12,
            popovers: [
              {
                iconColor: "info",
                iconName: "info",
                text: "jobs_download_cache_file",
              },
            ],
          },
        },
      },
    ],
    [
      {
        name: "realip-download",
        type: "Text",
        data: {
          text: "realip-download",
        },
      },
      {
        plugin_id: "realip",
        type: "Text",
        data: {
          text: "realip",
        },
      },
      {
        every: "hour",
        type: "Text",
        data: {
          text: "hour",
        },
      },
      {
        reload: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        success: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        last_run: "2024/06/14, 01:33:09 PM",
        type: "Text",
        data: {
          text: "2024/06/14, 01:33:09 PM",
        },
      },
      {
        cache: [],
        type: "Text",
        data: {
          text: "No cache",
        },
      },
    ],
    [
      {
        name: "self-signed",
        type: "Text",
        data: {
          text: "self-signed",
        },
      },
      {
        plugin_id: "selfsigned",
        type: "Text",
        data: {
          text: "selfsigned",
        },
      },
      {
        every: "day",
        type: "Text",
        data: {
          text: "day",
        },
      },
      {
        reload: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        success: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        last_run: "2024/06/14, 01:33:10 PM",
        type: "Text",
        data: {
          text: "2024/06/14, 01:33:10 PM",
        },
      },
      {
        cache: "none www.example.com/cert.pem www.example.com/key.pem",
        type: "Fields",
        data: {
          setting: {
            id: "self-signed_cache",
            label: "self-signed_cache",
            hideLabel: true,
            inpType: "select",
            name: "self-signed_cache",
            value: "none",
            values: [
              "none",
              "www.example.com/cert.pem",
              "www.example.com/key.pem",
            ],
            columns: {
              pc: 12,
              tablet: 12,
              mobile: 12,
            },
            overflowAttrEl: "data-table-body",
            containerClass: "table",
            maxBtnChars: 12,
            popovers: [
              {
                iconColor: "info",
                iconName: "info",
                text: "jobs_download_cache_file",
              },
            ],
          },
        },
      },
    ],
    [
      {
        name: "update-check",
        type: "Text",
        data: {
          text: "update-check",
        },
      },
      {
        plugin_id: "jobs",
        type: "Text",
        data: {
          text: "jobs",
        },
      },
      {
        every: "day",
        type: "Text",
        data: {
          text: "day",
        },
      },
      {
        reload: "no",
        type: "Icons",
        data: {
          iconColor: "error",
          iconName: "cross",
        },
      },
      {
        success: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        last_run: "2024/06/14, 01:33:15 PM",
        type: "Text",
        data: {
          text: "2024/06/14, 01:33:15 PM",
        },
      },
      {
        cache: [],
        type: "Text",
        data: {
          text: "No cache",
        },
      },
    ],
    [
      {
        name: "whitelist-download",
        type: "Text",
        data: {
          text: "whitelist-download",
        },
      },
      {
        plugin_id: "whitelist",
        type: "Text",
        data: {
          text: "whitelist",
        },
      },
      {
        every: "hour",
        type: "Text",
        data: {
          text: "hour",
        },
      },
      {
        reload: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        success: "yes",
        type: "Icons",
        data: {
          iconColor: "success",
          iconName: "check",
        },
      },
      {
        last_run: "2024/06/14, 01:33:09 PM",
        type: "Text",
        data: {
          text: "2024/06/14, 01:33:09 PM",
        },
      },
      {
        cache: [],
        type: "Text",
        data: {
          text: "No cache",
        },
      },
    ],
  ],
};

const intervals = [];
// Loop on items
for (let i = 0; i < tableData.items.length; i++) {
  // Loop on items[i]
  for (let j = 0; j < tableData.items[i].length; j++) {
    // Loop on object keys and
    for (const key in tableData.items[i][j]) {
      // Check if key is 'every'
      if (key === "every" && !intervals.includes(tableData.items[i][j][key])) {
        // Push the value to intervals array
        intervals.push(tableData.items[i][j][key]);
      }
    }
  }
}

console.log(intervals);
