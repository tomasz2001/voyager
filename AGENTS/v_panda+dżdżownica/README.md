voyager-dżdżownica

This README describes the dżdżownica ecosystem. It does not cover the agent or Voyager itself – to learn more, please refer to the main Voyager README.

Dżdżownica is an ecosystem for creating transparent records of databoxes within the Voyager system. It was designed to preserve Voyager’s decentralized nature. It uses external records stored on independent blockchains, which enables:

fully decentralized discovery of databoxes by any user,

decentralized promotion of one’s own databoxes,

avoiding situations where users become “trapped” in a centralized cluster of databoxes within so-called Voyager micro-networks.

The core mechanism relies on storing three values:

index / canister-id / last-save

index – a unique identifier that allows records to be found and correctly recognized in the dżdżownica system,

canister-id – the databox identifier; canisters are part of the ICP (Internet Computer Protocol) ecosystem,

last-save – the location of the most recent record about a databox. This allows the voyager-agent to efficiently trace earlier entries, optimizing the search process.

Hackathon deliverables

As part of this hackathon, two programs were delivered:

An updated experimental version of the Panda agent

A tool for adding records about databoxes

Everything runs on the ICP blockchain and the testnet provided by golem-DB.