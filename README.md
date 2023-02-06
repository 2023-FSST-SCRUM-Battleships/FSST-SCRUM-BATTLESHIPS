- Client
- Server
- Networking
- DB-Connection

## Client

- GUI (PyQT6)
- Sends Ship placements to server

## Server

- Receives Ship placement from client
- Handles shots & win checks

## Networking

- JSON strings via sockets:
| FieldName | Description | type |
|---:|:---:|:---|
|type|defines type of packet| string |
| data | the transmitted data | JSON-serializable data |
example:
```
{
	"type" : "ship_placement",
	"data": {<actual data>}
}
```
example for some data:
``[{rotation:0 (x90°), origin:[3, 3]}, {rotation: 1, origin: [6, 8]}]``

## DB-Connection

- ORM 
