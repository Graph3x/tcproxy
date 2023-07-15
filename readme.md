A basic Python 3 TCP proxy for filtering traffic, mainly intended for AD CTFs

Usage: ./proxy.py config_file
default config file is ./config.json

test_server.py and test_client.py are only basic scripts to test the functionality

Config example:
{
    "remote_host": "127.0.0.1", //self-explanatory
    "remote_port": "9000", //self-explanatory
    "proxy_host": "127.0.0.1", //self-explanatory
    "proxy_port": "9001", //self-explanatory
    "rules":
    {
        "client":       //rules applied to traffic from client
        [
            {
                "name": "Adore is better than like", //name is not actually used, just organizational
                "type": "regex2string", //type of the rule - currently just regex2string
                "case_sensitive": "false", //self-explanatory
                "from": "like", //the filtered regex
                "to": "adore", //what should the matches be replaced with
                "alert": "" //empty means no alert
            }
        ],
        "server":       //rules applied to responses from server
        [
            {
                "name": "I dont like flags",
                "type": "regex2string",
                "case_sensitive": "true",
                "from": "FLAG{[^}]+}",
                "to": "not_today_crocodile",
                "alert": "FLAG OUT+"        //on every rule break, prints FLAG OUT, "+" gets replaced with the traffic that broke the rule
            }
        ]
    }

}
