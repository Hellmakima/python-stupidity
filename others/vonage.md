https://www.vonageforhome.com/
Baught Virtual Number: 6179339288
tCognition@7869
User Information
Name: Manoj Shinde
Contact Phone Number: (781) 363-0214
Username: tCognitionUSA
Contact Email: vonage@tcognition.com
Caller ID Display: SHINDE, M

---

https://dashboard.nexmo.com/
vonage@tcognition.com
Dev account No: 6174384819
Linked number: 7325268057
tCog@7869123

API: aQh008GOEYlHfGS0

---

https://login.auth.vonage.com/authenticationendpoint/login.do?amplitude_api_key=80d4ab359b88b06abffba0ea237ef107&client_id=_eWm_iZhM74EDxsWbVlG5HLVAn4a&commonAuthCallerPath=%2Foauth2%2Fauthorize&forceAuth=false&passiveAuth=false&redirect_uri=https%3A%2F%2Fadmin.vonage.com%2Fpreauth%3Fsso%3Dtrue&response_type=code&scope=openid&tenantDomain=vbc.prod&sessionDataKey=94bd442c-3d57-4d03-9b11-988139451922&relyingParty=_eWm_iZhM74EDxsWbVlG5HLVAn4a&type=oidc&sp=Admin%20Portal&isSaaSApp=false
Manoj_Shinde
tCognition@7869

manoj.shinde@tcognition.com

---
## Mail Contents
Sufiyan - We have to create Voice Agent Ai Tel.No.6179339288 and the details are in the first line item and the second line item are the users and their numbers. Call me you have any questions? best of luck
Vonage USA -Residencial 	Telephone charges 	https://www.vonageforhome.com/	A/c No.1013162912 Tel.No.6179339288	6179339288	tCognition@7869			Yes	13th		
Manoj.Shinde@tcognition.com
Vonage USA -Business Acct: 363718/ (866)901-0242 	Telephone charges 	https://login.auth.vonage.com/authenticationendpoint/login.do?amplitude_api_key=80d4ab359b88b06abffba0ea237ef107&client_id=_eWm_iZhM74EDxsWbVlG5HLVAn4a&commonAuthCallerPath=%2Foauth2%2Fauthorize&forceAuth=false&passiveAuth=false&redirect_uri=https%3A%2F%2Fadmin.vonage.com%2Fpreauth%3Fsso%3Dtrue&response_type=code&scope=openid&tenantDomain=vbc.prod&sessionDataKey=94bd442c-3d57-4d03-9b11-988139451922&relyingParty=_eWm_iZhM74EDxsWbVlG5HLVAn4a&type=oidc&sp=Admin%20Portal&isSaaSApp=false	Acct: 363718/ (866)901-0242 	Manoj_Shinde	tCognition@7869				20th	02/20/2025

---

tCognition@7869
Manoj_Shinde

nikhil.mohite@tcognition.com
Pass 765234jjk69420
API FnLI7KgS9jKtpn22

https://www.youtube.com/watch?v=szI_KPYvZs8
local server to handle call events (old version)

[new version](https://www.youtube.com/watch?v=wnE5C_bDbKI)


setup guide node: https://developer.vonage.com/en/tutorials/ivr/introduction/node
setup with python: pip install vonage

```py
from flask import Flask, jsonify, request
from vonage_voice import Talk, Input  # For NCCO actions
from vonage import Vonage, Auth

app = Flask(__name__)
client = Vonage(Auth(api_key="YOUR_API_KEY", api_secret="YOUR_API_SECRET"))

@app.route("/webhooks/answer", methods=["GET", "POST"])
def answer():
    ncco = [
        Talk(text="Press 1 for service, 2 for support", language="en-US"),
        Input(eventUrl=[f"{request.url_root}webhooks/input"], maxDigits=1)
    ]
    return jsonify(ncco)
```
---

## Hostinger
VPS
ssh root@72.60.69.239

---

## Vonage alternatives
you basically want an **IVR (Interactive Voice Response)** system, old-school “press 1, press 2” menus.  

### Tech Options:

**1. Hosted APIs (easy mode)**  
- **Twilio** → dead simple IVR, pay-per-minute.  
- **Vonage Voice API** → same deal, can do IVR + speech recognition.  
- **Plivo** → cheaper Twilio alternative.  

**2. Open Source / Self-hosted (more control, more pain)**  
- **Asterisk** → classic open-source PBX, super customizable, runs on your own server.  
- **FreeSWITCH** → similar to Asterisk, more scalable.  

**3. Cloud Contact Center platforms (enterprise $$$)**  
- **Amazon Connect** (AWS) → serverless IVR/contact center.  
- **Genesys Cloud**, **Five9**, etc.  

### TL;DR  
- If you want something quick, hacky, cheap → **Twilio** or **Vonage Voice API**.  
- If you want full control and don’t mind sysadmin headaches → **Asterisk**.  
- If you’re scaling big or need call center features → **Amazon Connect**.  

Can transfer the phone number from Vonage if it is a business account not if it is a residential number.

---
## DTMF only

Alright, if you only want **DTMF (touch-tone keypress) IVR** — no fancy speech AI — you’ve got a bunch of solid options:

### Cloud APIs (fast + managed)
- **Twilio Programmable Voice** → super common, IVR menus with keypress detection.  
- **Vonage Voice API** → similar, supports DTMF events easily.  
- **Plivo Voice API** → cheaper than Twilio, still does DTMF IVR.  
- **Telnyx** → pay-per-use, supports DTMF menus.  

### Open Source / Self-hosted
- **Asterisk** → OG telephony system, bulletproof for DTMF menus.  
- **FreeSWITCH** → modern, scalable alternative.  
- **FusionPBX** (built on FreeSWITCH) → nice web UI for DTMF call flows.  

### Enterprise Cloud Call Center Platforms (if you’re big corp)
- **Amazon Connect** → supports keypress routing, but overkill unless you want call center stuff.  
- **Genesys / Five9** → $$$, but DTMF menus are baseline features.  

👉 Best call:  
- **Hacky prototype / small-scale** → Twilio or Vonage.  
- **Cheap long-term, DIY** → Asterisk.  
- **Enterprise call center vibe** → Amazon Connect.  

Do you want this for **inbound calls only** (like a support line), or also **outbound IVR campaigns** (like auto-dial + menu)?

---

## Sample code

Got it — you want a **multi-layer IVR in Node.js** where calls get **forwarded to real phone numbers** depending on DTMF input. That’s 100% doable with Vonage Voice API using NCCOs.

Here’s a clean example with **Express** + Vonage:

---

### 1. Install deps

```bash
npm init -y
npm install express body-parser
```

---

### 2. Node.js server (`server.js`)

```js
const express = require("express");
const bodyParser = require("body-parser");

const app = express();
app.use(bodyParser.json());

// Main IVR menu
app.get("/webhooks/answer", (req, res) => {
  const ncco = [
    {
      action: "talk",
      text: "Welcome. Press 1 for Support. Press 2 for Sales."
    },
    {
      action: "input",
      eventUrl: [`${req.protocol}://${req.get("host")}/webhooks/menu`],
      maxDigits: 1,
      timeOut: 5
    }
  ];
  res.json(ncco);
});

// First menu input handler
app.post("/webhooks/menu", (req, res) => {
  const dtmf = req.body.dtmf;

  if (dtmf === "1") {
    // Support sub-menu
    const ncco = [
      { action: "talk", text: "Support. Press 1 for John, 2 for Joseph." },
      {
        action: "input",
        eventUrl: [`${req.protocol}://${req.get("host")}/webhooks/support`],
        maxDigits: 1,
        timeOut: 5
      }
    ];
    res.json(ncco);
  } else if (dtmf === "2") {
    const ncco = [{ action: "talk", text: "Sales team coming soon." }];
    res.json(ncco);
  } else {
    const ncco = [{ action: "talk", text: "Invalid choice." }];
    res.json(ncco);
  }
});

// Support submenu handler
app.post("/webhooks/support", (req, res) => {
  const dtmf = req.body.dtmf;

  if (dtmf === "1") {
    // Forward to John
    const ncco = [
      { action: "talk", text: "Connecting you to John." },
      {
        action: "connect",
        endpoint: [{ type: "phone", number: "15551112222" }]
      }
    ];
    res.json(ncco);
  } else if (dtmf === "2") {
    // Forward to Joseph
    const ncco = [
      { action: "talk", text: "Connecting you to Joseph." },
      {
        action: "connect",
        endpoint: [{ type: "phone", number: "15553334444" }]
      }
    ];
    res.json(ncco);
  } else {
    const ncco = [{ action: "talk", text: "Invalid support option." }];
    res.json(ncco);
  }
});

// Event webhook (Vonage sends call status updates here)
app.post("/webhooks/events", (req, res) => {
  console.log(req.body);
  res.sendStatus(200);
});

app.listen(3000, () => console.log("IVR running on port 3000"));
```

---

### 3. How it works

* Caller dials your Vonage number.
* `/webhooks/answer` plays “Press 1 for Support / 2 for Sales.”
* If Support → goes into submenu `/webhooks/support`.
* Depending on choice → `connect` action forwards the call to John or Joseph’s phone.

---

### 4. Next steps

* Expose your server with **ngrok**:

  ```bash
  ngrok http 3000
  ```
* Put your **ngrok URL** into your Vonage App’s **Answer URL** + **Event URL**.

you’ve got a multi-layer IVR with real call forwarding.

Do you want me to also show you how to **swap the TTS prompts with pre-recorded audio files (MP3/WAV)** so you don’t burn TTS credits?
Yes?
```js
{ 
  action: "stream", 
  streamUrl: ["https://your-server.com/audio/welcome.mp3"] 
}
```