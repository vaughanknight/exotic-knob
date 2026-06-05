# Flight plan — bluetooth-input-baseline

**Plan**: bluetooth-input-baseline · **Mode**: Simple · **Phases**: 1
**Rail**: `[the-flow] ◆─◆─◆─◆─◆` · **now**: Flow complete · **next**: Commit/push when explicitly requested; real hardware smoke remains follow-up

```mermaid
flowchart TD
    classDef done    fill:#4CAF50,stroke:#388E3C,color:#fff
    classDef wip     fill:#FF9800,stroke:#F57C00,color:#000
    classDef blocked fill:#F44336,stroke:#D32F2F,color:#fff
    classDef known   fill:#90A4AE,stroke:#607D8B,color:#000
    classDef assumed fill:#ECEFF1,stroke:#B0BEC5,color:#90A4AE,stroke-dasharray:4 4
    classDef said    fill:#FFFDE7,stroke:#FBC02D,color:#000
    classDef companion fill:#E0F2F1,stroke:#00897B,color:#000
    classDef worker  fill:#E8EAF6,stroke:#3F51B5,color:#000

    R[Research]:::done --> S[Spec]:::done --> PL[Plan]:::done --> P1[Simple Implementation]:::done --> RV[Review]:::done --> M[Merge]:::done
    R -.->|dig deeper| DR[["Deep research x4"]]:::done
    DR -.-> S
    S -.->|prove it| BP[Backpressure survey?]:::done
    BP -.-> PL
    S -.->|prove it?| BP[Backpressure survey?]:::assumed
    BP -.-> PL

    UR>"🗣 let's create a baseline to get the input from the bluetooth device. we will want to run this on esp32 possibly in future, for now it's on my mac (or a pc) via CLI, we'll need to do some technology choices and simple is best, this is unlikely to be a complex app, but i do want to be mindful of battery consumption etc for when we go to esp32, it won't be running often (when volume is changed) but it will be running all the time. First cut can just be a basic CLI that outputs when it gets the messages from the device, selects the device etc"]:::said
    UR -.- R
    UDR>"🗣 run the deep research prompts, let's get this right from the start; can we do deep research on the anticater knob also, as that is the volume knob we are using and it has LED features and click volume knob also... would be good to know what we can do with it and what we expect from it"]:::said
    UDR -.- DR
    US>"🗣 create a baseline CLI for the Anticater VK-01 Bluetooth volume knob: pair/select the device on macOS first and PC later, enumerate HID interfaces, capture descriptors and raw reports for rotate left/right, click/mute, and long-press+rotate actions, print raw and best-effort normalized events, save JSONL fixtures for replay, use a HID-first Python/HIDAPI approach, defer LED/RGB control unless a vendor-defined feature/output report is discovered, and keep the event model transport-neutral for future ESP32 and BluOS dB volume policy work"]:::said
    US -.- S
    UB>"🗣 yes — run backpressure survey"]:::said
    UB -.- BP
    UP>"🗣 yes"]:::said
    UP -.- PL
```

**Legend**: 🟩 done · 🟧 in progress · 🟥 blocked · 🟦 known future (designed) · ⬜╴assumed future (dashed) · 🟨 🗣 verbatim user input · companion (teal, wraps) · worker (indigo, side)

_Generated from `the-flow.json`. Do not hand-edit this file as the primary; update `the-flow.json` first and regenerate._
