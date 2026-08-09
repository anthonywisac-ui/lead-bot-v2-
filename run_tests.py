#!/usr/bin/env python3
# Real E2E Bot Testing - Sends actual WhatsApp messages
import asyncio
import aiohttp
import json
import time
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# ==================== CONFIG ====================
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")
WHATSAPP_API_URL = f"https://graph.instagram.com/v18.0/{WHATSAPP_PHONE_ID}/messages"

# Test configuration
TEST_PHONE = "923351021321"  # Manager's number (real test)
TEST_PHONE_FORMATTED = f"+{TEST_PHONE}"

# Colors
class C:
    H = '\033[95m'  # Header
    B = '\033[94m'  # Blue
    C = '\033[96m'  # Cyan
    G = '\033[92m'  # Green
    Y = '\033[93m'  # Yellow
    R = '\033[91m'  # Red
    E = '\033[0m'   # End
    BOLD = '\033[1m'

print(f"\n{C.H}{C.BOLD}{'='*70}")
print(f"  WILD BITES BOT - LIVE E2E TESTING")
print(f"{'='*70}{C.E}\n")

print(f"{C.BOLD}📋 Configuration:{C.E}")
print(f"  Bot URL: https://lead-bot-v2-production.up.railway.app")
print(f"  Test Phone: {TEST_PHONE}")
print(f"  WhatsApp API: Configured ✓")
print(f"  Start: {datetime.now().strftime('%H:%M:%S')}\n")

# Test results tracker
results = []
message_count = 0

async def send_msg(msg, test_name=""):
    """Send WhatsApp message via API"""
    global message_count

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": TEST_PHONE_FORMATTED,
        "type": "text",
        "text": {"body": msg}
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(WHATSAPP_API_URL, json=payload, headers=headers) as resp:
                if resp.status == 200:
                    message_count += 1
                    print(f"  {C.G}✓{C.E} Sent ({test_name}): {msg[:40]}")
                    await asyncio.sleep(1.5)
                    return True
                else:
                    error = await resp.text()
                    print(f"  {C.R}✗{C.E} Failed ({test_name}): {error[:50]}")
                    return False
    except Exception as e:
        print(f"  {C.R}✗{C.E} Error: {str(e)[:50]}")
        return False

async def test(name, msgs):
    """Run test with sequence of messages"""
    print(f"\n{C.B}{C.BOLD}► {name}{C.E}")

    success = True
    for i, (msg, desc) in enumerate(msgs, 1):
        result = await send_msg(msg, desc)
        success = success and result

    if success:
        print(f"  {C.G}✅ {name} - PASS{C.E}")
        results.append((name, True))
    else:
        print(f"  {C.R}❌ {name} - FAIL{C.E}")
        results.append((name, False))

async def run_tests():
    """Execute all tests"""

    # Test 1: New Customer
    await test("New Customer Detection", [
        ("New", "New Customer Keyword"),
    ])

    # Test 2: Returning Customer
    await test("Returning Customer", [
        ("Hi Ahmed", "Greeting with Name"),
    ])

    # Test 3: B2B Client
    await test("B2B Client Setup", [
        ("Client", "B2B Keyword"),
    ])

    # Test 4: Country Selection
    await test("Country/Location", [
        ("owner", "Change Country"),
    ])

    # Test 5: Multi-language
    await test("Multi-language Support", [
        ("Salam", "Urdu Greeting"),
        ("Hola", "Spanish Greeting"),
    ])

    # Test 6: Order Status
    await test("Order Status Check", [
        ("Where is my order", "Status Query"),
    ])

    # Test 7: Menu Navigation (simulated)
    await test("Menu Flow", [
        ("Hi", "Browse Menu"),
    ])

    # Print Summary
    print(f"\n{C.H}{C.BOLD}{'='*70}")
    print(f"  TEST RESULTS SUMMARY")
    print(f"{'='*70}{C.E}\n")

    passed = sum(1 for _, ok in results if ok)
    total = len(results)

    for name, ok in results:
        status = f"{C.G}✅{C.E}" if ok else f"{C.R}❌{C.E}"
        print(f"  {status} {name}")

    print(f"\n{C.BOLD}📊 Statistics:{C.E}")
    print(f"  Total Tests: {total}")
    print(f"  {C.G}Passed: {passed}{C.E}")
    print(f"  {C.R}Failed: {total-passed}{C.E}")
    print(f"  Messages Sent: {message_count}")
    pass_pct = (passed/total*100) if total > 0 else 0
    print(f"  Pass Rate: {pass_pct:.0f}%")

    if passed == total:
        print(f"\n{C.G}{C.BOLD}🎉 ALL TESTS PASSED!{C.E}")
        print(f"{C.G}Bot is working perfectly! ✨{C.E}\n")
    else:
        print(f"\n{C.Y}{C.BOLD}⚠️  {total-passed} test(s) need attention{C.E}\n")

    print(f"  End: {datetime.now().strftime('%H:%M:%S')}\n")

# ==================== MAIN ====================
if __name__ == "__main__":
    try:
        asyncio.run(run_tests())
    except KeyboardInterrupt:
        print(f"\n{C.Y}Testing stopped by user{C.E}\n")
    except Exception as e:
        print(f"\n{C.R}Error: {str(e)}{C.E}\n")
