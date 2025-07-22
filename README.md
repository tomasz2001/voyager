README SUBJECT TO FURTHER REVISIONS.
THE AUTHOR OF THIS FILE WON’T FORGET THAT.

Project Name: VOYAGER
License: AGPLv3
Public Chat (Telegram): https://t.me/voyager_system

NOTE FOR USING THE VOYAGER SYSTEM:
The uncompiled agent [the panda] requires the installation of the following Python libraries:

asyncio

ic-py

Install them via pip:
pip install asyncio ic-py

VOYAGER SYSTEM – OPERATIONAL OVERVIEW

What is Voyager?

Voyager is an open framework for cataloging services and information, built on the decentralized ICP network.
It is not a single application — it's a modular system composed of components that anyone can use to build their own “agent” for communicating with data or services.

Voyager does not dictate a single app model.
You choose which interfaces to support, and what kind of data to expose.

How does it work?

The system consists of two core elements:

Voyager-DataBox (canister): holds data about Voyager apps, other DataBoxes, and their interfaces (e.g., API specs, commands, availability).

Voyager Applications: connect to those data structures and expose interfaces (e.g., an ASCII chat using the glue interface).

These components interact via an open, simple set of “standards” that anyone can help define.

AI? When and how?

Voyager currently does not include a built-in AI agent.
However, its architecture is designed for future integration of local AI systems that can work with metadata (like connector[], title, conn) — without requiring a graphical interface.

The data is already structured and readable for language models, so building AI-ready tools is straightforward.

For example, a future agent could crawl the Voyager network using keywords from "title" and "connector" fields.

Open, human-driven standards

In Voyager, communication protocols are not created by corporations or foundations — they are written by users.

Every Conn object includes a connector[] field that declares which interfaces are supported.

Example: ["glue", "help"] means the app supports the "glue" standard, which may allow posting messages.

There is no central validator.
If you want to create a new standard like ascii-market:0.1 — define it and publish it. That’s it.

This means:

You can create services that communicate with each other — without API gateways, without Google, without the App Store.

Truly decentralized network

Every Voyager-DataBox is an independent node that:

stores data about other Voyagers (friend buffer),

holds records about services (Conn buffer),

is not controlled by any company — it runs on ICP, but the data is owned by the user (Principal).

You don’t need Google or Amazon’s permission to build your own infrastructure.

Our Goal

To create a living system of information exchange, where:

users build their own service catalogs,

AI can interact with them directly (no frontend needed),

and the data is decentralized, open, and censorship-resistant.

It’s not about building another browser.
It’s about building your own internet.

