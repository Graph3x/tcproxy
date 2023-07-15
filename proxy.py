import asyncio
import sys
import json
import re


async def regex2string(data: bytes, case_sens: bool, original: str, change: str):
    if case_sens:
        return re.sub(original.encode(), change.encode(), data)

    return re.sub(original.encode(), change.encode(), data, flags=re.IGNORECASE)


async def intrude(data: bytes, rules: list):

    current = data
    for rule in rules:
        match rule["type"]:
            case "regex2string":
                new_data = await regex2string(current, rule["case_sensitive"].lower() == "true", rule["from"], rule["to"])
            case _:
                print("unkown rule type: " + rule["type"])

        if rule["alert"] != "" and new_data != current:
            alert = rule["alert"]
            if "+" in alert:
                alert = alert.replace("+", f" : {data.decode()}")
            print(alert)
        current = new_data

    return current


async def handle(client_reader: asyncio.StreamReader, client_writer: asyncio.StreamWriter, server_host, server_port, rules: list):
    server_reader, server_writer = await asyncio.open_connection(server_host, server_port)

    async def forward(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, rules):
        while True:
            data = await reader.read(1024)
            data = await intrude(data, rules)
            if not data:
                break
            writer.write(data)
            await writer.drain()

    try:
        await asyncio.gather(
            forward(client_reader, server_writer, rules["client"]),
            forward(server_reader, client_writer, rules["server"])
        )
    finally:
        client_writer.close()
        server_writer.close()


async def run_proxy(proxy_host, proxy_port, server_host, server_port, rules):
    server = await asyncio.start_server(
        lambda r, w: handle(r, w, server_host, server_port, rules),
        proxy_host, proxy_port
    )

    print(f'Proxy running on {proxy_host}:{proxy_port}')

    async with server:
        await server.serve_forever()


async def main():

    conf_file = "config.json"

    if len(sys.argv) > 1:
        conf_file = sys.argv[1]
    else:
        print("No config file specified, defaulting to " + conf_file)

    try:
        with open(conf_file, "r") as f:
            config_data = f.read()
    except Exception as e:
        print("Invalid config file")
        return

    config = json.loads(config_data)

    await run_proxy(config["proxy_host"], config["proxy_port"], config["remote_host"], config["remote_port"], config["rules"])

asyncio.run(main())
