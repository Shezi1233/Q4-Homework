from fastapi import FastAPI

app = FastAPI()

# Fake database (simple dictionary)
accounts = {
    "shahzad": {"pin": 1111, "balance": 1000},
    "ali": {"pin": 2222, "balance": 500},
    "ahmed": {"pin": 3333, "balance": 1200},
}

# -----------------------
# 1) AUTHENTICATION ROUTE
# -----------------------
@app.post("/authenticate")
def authenticate(name: str, pin_number: int):
    if name not in accounts:
        return {"status": "error", "message": "Account not found"}

    if accounts[name]["pin"] != pin_number:
        return {"status": "error", "message": "Invalid PIN"}

    return {
        "status": "success",
        "message": f"Welcome {name}",
        "bank_balance": accounts[name]["balance"]
    }


# -----------------------
# 2) BANK TRANSFER ROUTE
# -----------------------
@app.post("/bank-transfer")
def bank_transfer(sender: str, sender_pin: int, recipient: str, amount: int):

    # Sender validation
    if sender not in accounts:
        return {"status": "error", "message": "Sender account not found"}

    if accounts[sender]["pin"] != sender_pin:
        return {"status": "error", "message": "Invalid sender PIN"}

    # Recipient validation
    if recipient not in accounts:
        return {"status": "error", "message": "Recipient account not found"}

    # Balance check
    if accounts[sender]["balance"] < amount:
        return {"status": "error", "message": "Insufficient balance"}

    # Transfer process
    accounts[sender]["balance"] -= amount
    accounts[recipient]["balance"] += amount

    return {
        "status": "success",
        "message": f"{amount} transferred to {recipient}",
        "sender_new_balance": accounts[sender]["balance"]
    }
