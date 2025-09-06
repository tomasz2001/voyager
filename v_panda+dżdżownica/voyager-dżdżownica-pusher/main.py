import asyncio
from golem_base_sdk import GolemBaseClient, GolemBaseCreate, Annotation

HTTP_RPC = "https://ethwarsaw.holesky.golemdb.io/rpc"
WS_RPC = "wss://ethwarsaw.holesky.golemdb.io/rpc/ws"
PRIVATE_KEY = "bfcb7d6bf916cc6fbf48f35c2cbc61989297d8d95cb08e461494411ab69af979"

async def main():
    databox = input("gif me voyager data/box or data pripical to push dżdżownica ekosystem: ")

    receipts = None
    client = None
    try:
        # RW client (obsługuje create_entities)
        client = await GolemBaseClient.create_rw_client(HTTP_RPC, WS_RPC, PRIVATE_KEY)

        # query też działa na RW
        vd_entities = await client.query_entities('type="vd"')
        entity = vd_entities[0]  # index = 0
        old = entity.entity_key

        # entity_key może być str lub bytes
        old_bytes = old.encode() if isinstance(old, str) else old

        entity = GolemBaseCreate(
            data=f"vd/{databox}/{old}".encode(),  # 👈 przecinek!
            btl=21370000,
            string_annotations=[
                Annotation(key="type", value="vd"),
                Annotation(key="language", value="python"),
            ],
            numeric_annotations=[
                Annotation(key="priority", value=1),
                Annotation(key="version", value=3),
            ],
        )

        receipts = await client.create_entities([entity])
        print("entity created successfully")

    except Exception as e:
        print("error plesse try later:", e)

    finally:
        if receipts:
            print("Entity key:", receipts[0].entity_key)
            print("save info on this databox is enjoy")
        if client:
            await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
