# Getting started with Battleships

[Jira](https://aetherialkilix.atlassian.net/) is an implementation of Scrum.
We use a `BS-{random-id}`-tag to connect Jira with Github-Repositories & Github-Commits.

## Week 1

- [ ] <font size="4">`BS-3`</font>: fundamental GUI

- [ ] <font size="4">`BS-4`</font>: place ships on field

- [ ] <font size="4">`BS-10`</font>: rotate ships

## Week 2

- [ ] <font size="4">`BS-11`</font>: collision detection for ships

- [ ] <font size="4">`BS-12`</font>: render ships

## Week 3

## Week 4

## Tasks to assign for

- [ ] <font size="4">`BS-4`</font>: fundamental networkcommunication

- [ ] <font size="4">`BS-5`</font>: connection with database

- [ ] <font size="4">`BS-7`</font>: matchmaking

- [ ] <font size="4">`BS-13`</font>: login GUI

- [ ] <font size="4">`BS-14`</font>: databank

- [ ] <font size="4">`BS-15`</font>: login network

---

## Details

### Client

- GUI (PyQT6)
- Sends Ship placements to server

### Server

- Receives Ship placement from client
- Handles shots & win checks

### Networking

- JSON strings via sockets:

| FieldName |      Description       | type                   |
| --------: | :--------------------: | :--------------------- |
|      type | defines type of packet | string                 |
|      data |  the transmitted data  | JSON-serializable data |

example:

```
{
	"type" : "ship_placement",
	"data": {<actual data>}
}
```

example for some data:
`[{rotation:0 (x90°), origin:[3, 3]}, {rotation: 1, origin: [6, 8]}]`

### DB-Connection

- ORM
