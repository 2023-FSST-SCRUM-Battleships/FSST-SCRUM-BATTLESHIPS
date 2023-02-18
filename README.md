# Getting started with Battleships

[Jira](https://atlassian.net/) is an implementation of Scrum.
We use a `BS-{random-id}`-tag to connect Jira with Github-Repositories & Github-Commits.
To install the requirements, type in your commandline `pip install -r requirements.txt`.

## Week 1

- [x] <font size="4">`BS-3`</font>: fundamental GUI

- [x] <font size="4">`BS-4`</font>: fundamental network-communication - client

- [ ] <font size="4">`BS-9`</font>: place ships on field

- [ ] <font size="4">`BS-10`</font>: rotate ships

- [ ] <font size="4">`BS-11`</font>: collision detection for ships

- [ ] <font size="4">`BS-16`</font>: set up database

## Week 2

- [ ] <font size="4">`BS-5`</font>: connection with database

- [ ] <font size="4">`BS-12`</font>: render ships

- [ ] <font size="4">`BS-17`</font>: set up automatic deployment

- [ ] <font size="4">`BS-18`</font>: fundamental network-communication - server

- [ ] <font size="4">`BS-18`</font>: fundamental network-communication - server

- [ ] <font size="4">`BS-19`</font>: ships fleet manager (layout)

- [ ] <font size="4">`BS-20`</font>: send ships fleet layout to server

- [ ] <font size="4">`BS-21`</font>: set up shots

## Week 3

- [ ] <font size="4">`BS-7`</font>: matchmaking

- [ ] <font size="4">`BS-13`</font>: login GUI

- [ ] <font size="4">`BS-14`</font>: databank accounts

- [ ] <font size="4">`BS-15`</font>: login network

- [ ] <font size="4">`BS-22`</font>: display shots in GUI

## Week 4

- [ ] <font size="4">`BS-23`</font>: win condition

- [ ] <font size="4">`BS-24`</font>: display stats in GUI

- [ ] <font size="4">`BS-25`</font>: GUI picture

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
