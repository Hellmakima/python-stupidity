from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime, time
from zoneinfo import ZoneInfo

app = Flask(__name__)

LOCAL_TZ = ZoneInfo("Asia/Kolkata")

# ---------- Helper function to see if office is open ----------
def is_office_open(dept: str) -> bool:
    now = datetime.now(LOCAL_TZ).time()

    if dept in ("recruitment", "sales", "Executive Manager"):
        return now >= time(18, 0) or now < time(3, 0)  # 6AM–3PM
    else:
        return time(9, 0) <= now < time(21, 0)  # 9AM–9PM


# ---------- Helper function to safely extract DTMF ----------
def get_dtmf_from_request(req):
    """Extract DTMF digits safely from either JSON or form payload."""
    data = req.get_json(silent=True)
    if not data:
        data = req.form.to_dict()

    if isinstance(data.get("dtmf"), dict):
        return data["dtmf"].get("digits")
    return data.get("dtmf") or data.get("digits")


# ---------- Phone directory ----------
DEPARTMENTS = {
    "recruitment": {
        "2": {"name": "Parth", "number": "16176395297"},
        "3": {"name": "Samarsinh", "number": "16179567476"},
        "4": {"name": "Sanket", "number": "16179035789"},
        "5": {"name": "Sakshi", "number": "16174314730"},
        "6": {"name": "Purva", "number": "16179175239"},
        "7": {"name": "Shubham", "number": "16179821636"},
        "8": {"name": "Swapnil", "number": "16176395960"},
        "9": {"name": "Aayushi", "number": "16176395232"}
    },
    "sales": {
        "1": {"name": "Akshata", "number": "16174151543"},
        "3": {"name": "Karan", "number": "16179821831"},
        "4": {"name": "Aishwarya", "number": "16178612984"}
    },
    "it": {
        "1": {"name": "Nikhil", "number": "16179876543"},
        "2": {"name": "Shreyash", "number": "16176395244"}
    },
    "accounts": {
        "1": {"name": "Mahesh", "number": "919860619099"}
    },
    "hr": {
        "1": {"name": "Kiran", "number": "16179821831"}
    },
    "Executive Manager": {
        "1": {"name": "Manoj Shinde", "number": "16174384819"}
    }
}


@app.route("/audio", methods=["GET"])
def audio():
    return send_from_directory(".", "song.mp3")

# ---------- Main IVR menu ----------
@app.route("/answer", methods=["GET"])
def answer_call():
    ncco = [
        {
            "action": "talk",
            "text": (
                "Thank you for calling T Cognition. "
                "Press 1 to speak with our Recruitment team. "
                "Press 2 for Sales. "
                "Press 3 for IT Support. "
                "Press 4 for Accounts and Billing. "
                "Press 5 for HR and Careers."
            ),
            "bargeIn": True,
            "language": "en-IN",
            "style": 1 # Optional 
            # More: https://developer.vonage.com/en/voice/voice-api/concepts/text-to-speech#supported-languages
        },
        # {
        #     "action": "stream",
        #     "streamUrl": [f"{request.url_root}audio"],
        #     "bargeIn": True
        # },
        {
            "action": "input",
            "eventUrl": [f"{request.url_root}menu"],
            "maxDigits": 1,
            "timeOut": 5
        }
    ]
    return jsonify(ncco)


# ---------- Handle main menu input ----------
@app.route("/menu", methods=["POST"])
def handle_menu():
    dtmf = get_dtmf_from_request(request)
    dept_map = {
        "1": "recruitment",
        "2": "sales",
        "3": "it",
        "4": "accounts",
        "5": "h r"
    }

    if dtmf not in dept_map:
        return jsonify([
            {
                "action": "talk",
                "text": "Invalid choice. Please try again."
            },
            {
                "action": "input",
                "eventUrl": [f"{request.url_root}menu"],
                "maxDigits": 1,
                "timeOut": 5
            }
        ])

    dept = dept_map[dtmf]

    # check business hours before showing submenu
    if not is_office_open(dept):
        offshore_working_hours = "9 AM to 5 PM"
        onshore_working_hours = "11 30 AM to 11 30 PM"
        working_hours = offshore_working_hours if dept in ("recruitment", "sales", "Executive Manager") else onshore_working_hours

        time_statement = (
            f"The {dept.title()} team is currently unavailable. "
            f"Please try calling between {working_hours}, "
            "or leave a message after the beep."
        )

        return jsonify([
            {
                "action": "talk",
                "text": time_statement,
                "language": "en-IN",
                "style": 1
            },
            {
                "action": "record",
                "endOnSilence": 3,
                "endOnKey": "#",
                "beepStart": True,
                "eventUrl": [f"{request.url_root}event"]
            }
        ])

    people = DEPARTMENTS[dept]

    # Build dynamic submenu text based on available employees
    employee_text = f"You have selected the {dept.title()} Department. "
    for key, person in people.items():
        employee_text += f"Press {key} to connect with {person['name']}. "

    ncco = [
        {
            "action": "talk",
            "text": employee_text,
            "bargeIn": True,
            "language": "en-IN",
            "style": 1
        },
        {
            "action": "input",
            "eventUrl": [f"{request.url_root}connect/{dept}"],
            "maxDigits": 1,
            "timeOut": 5
        }
    ]
    return jsonify(ncco)


# ---------- Connect caller to the selected person ----------
@app.route("/connect/<dept>", methods=["POST"])
def connect_person(dept):
    dtmf = get_dtmf_from_request(request)
    people = DEPARTMENTS[dept]

    if dtmf in people:
        person = people[dtmf]
        ncco = [
            {
                "action": "talk", 
                "text": f"Connecting you to {person['name']}.",
                "language": "en-IN",
                "style": 1
            },
            {
                "action": "connect",
                "from": "17325268057",
                "endpoint": [{"type": "phone", "number": person['number']}]
            }
        ]
        return jsonify(ncco)
    else:
        return jsonify([
            {
                "action": "talk",
                "text": f"Invalid option in {dept.title()} Department. Please try again.",
                "language": "en-IN",
                "style": 1
            },
            {
                "action": "input",
                "eventUrl": [f"{request.url_root}connect/{dept}"],
                "maxDigits": 1,
                "timeOut": 5
            }
        ])


# ---------- Event webhook ----------
@app.route("/event", methods=["GET", "POST"])
def event():
    payload = request.get_json(silent=True) or request.form.to_dict()
    if payload:
        with open("calls.log", "a") as f:
            f.write(f"EVENT: {payload}\n")
    return "", 200


# ---------- Simple test endpoint ----------
@app.route("/test", methods=["GET"])
def test():
    return {"test": "Working"}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
