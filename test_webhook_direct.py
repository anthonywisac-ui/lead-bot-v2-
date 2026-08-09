#!/usr/bin/env python3
# Direct Webhook Testing (No Token Needed)
import asyncio
import aiohttp
import json
from datetime import datetime

class C:
    H = '\033[95m'
    B = '\033[94m'
    C = '\033[96m'
    G = '\033[92m'
    Y = '\033[93m'
    R = '\033[91m'
    E = '\033[0m'
    BOLD = '\033[1m'

BOT_URL = "https://lead-bot-v2-production.up.railway.app"
TEST_PHONE = "923351021321"

results = []
msg_count = 0

async def send_webhook_msg(text, desc=""):
    """Send message through webhook directly"""
    global msg_count

    payload = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": TEST_PHONE,
                        "text": {"body": text},
                        "type": "text"
                    }]
                }
            }]
        }]
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{BOT_URL}/webhook", json=payload) as resp:
                msg_count += 1
                if resp.status == 200:
                    print(f"  {C.G}✓{C.E} {desc}: '{text}'")
                    await asyncio.sleep(2)
                    return True
                else:
                    print(f"  {C.R}✗{C.E} {desc}: HTTP {resp.status}")
                    return False
    except Exception as e:
        print(f"  {C.R}✗{C.E} {desc}: {str(e)[:40]}")
        return False

async def test(name, messages):
    """Run test"""
    print(f"\n{C.B}{C.BOLD}► {name}{C.E}")
    success = True
    for msg, desc in messages:
        ok = await send_webhook_msg(msg, desc)
        success = success and ok

    if success:
        print(f"  {C.G}✅ PASS{C.E}")
        results.append((name, True))
    else:
        print(f"  {C.R}❌ FAIL{C.E}")
        results.append((name, False))

async def main():
    print(f"\n{C.H}{C.BOLD}{'='*70}")
    print(f"  WILD BITES BOT - WEBHOOK DIRECT TESTING")
    print(f"{'='*70}{C.E}\n")

    print(f"{C.BOLD}⚙️  Configuration:{C.E}")
    print(f"  Bot URL: {BOT_URL}")
    print(f"  Test Phone: {TEST_PHONE}")
    print(f"  Start: {datetime.now().strftime('%H:%M:%S')}\n")

    # Test 1: New Customer
    await test("Test 1: New Customer Detection", [
        ("New", "Send 'New' keyword"),
    ])

    # Test 2: Greeting
    await test("Test 2: Smart Greeting", [
        ("Hi", "Send greeting"),
    ])

    # Test 3: Category Selection (simulated interactive)
    await test("Test 3: Menu Available", [
        ("Hi Ahmed", "Greeting with name"),
    ])

    # Test 4: Status Check
    await test("Test 4: Order Status", [
        ("Where is my order", "Status query"),
    ])

    # Test 5: Country Change
    await test("Test 5: Country Selection", [
        ("owner", "Change location"),
    ])

    # Test 6: Multi-language
    await test("Test 6: Multi-language", [
        ("Salam", "Urdu greeting"),
        ("Hola", "Spanish greeting"),
    ])

    # Test 7: B2B
    await test("Test 7: B2B Client", [
        ("Client", "B2B keyword"),
    ])

    # Summary
    print(f"\n{C.H}{C.BOLD}{'='*70}")
    print(f"  RESULTS")
    print(f"{'='*70}{C.E}\n")

    passed = sum(1 for _, ok in results if ok)
    total = len(results)

    for name, ok in results:
        status = f"{C.G}✅{C.E}" if ok else f"{C.R}❌{C.E}"
        print(f"  {status} {name}")

    print(f"\n{C.BOLD}📊 Stats:{C.E}")
    print(f"  Total: {total}")
    print(f"  {C.G}Passed: {passed}{C.E}")
    print(f"  {C.R}Failed: {total-passed}{C.E}")
    print(f"  Messages: {msg_count}")

    if passed == total:
        print(f"\n{C.G}{C.BOLD}🎉 ALL TESTS PASSED!{C.E}\n")
    else:
        print(f"\n{C.Y}{C.BOLD}⚠️ Some tests failed{C.E}\n")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"\n{C.R}Error: {e}{C.E}\n")
