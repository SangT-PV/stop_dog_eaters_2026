#!/usr/bin/env python3
"""
Fund Data Update Script
Update campaign fund tracking data manually or via API integration

Part of Plan 06-03: Fund Tracking Dashboard
Usage:
    python scripts/update_funds.py add-source "Change.org" 250 --status active
    python scripts/update_funds.py add-expense "Media Production" 150 "Lucky photography session"
    python scripts/update_funds.py update-source "Kickstarter" 1200
    python scripts/update_funds.py recalculate
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Path to funds data file
FUNDS_FILE = Path(__file__).parent.parent.parent / "website" / "data" / "funds.json"


def load_funds():
    """Load current fund data"""
    if not FUNDS_FILE.exists():
        print(f"Error: {FUNDS_FILE} not found")
        sys.exit(1)

    with open(FUNDS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_funds(data):
    """Save updated fund data with timestamp"""
    data['last_updated'] = datetime.utcnow().isoformat() + 'Z'

    with open(FUNDS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[OK] Fund data updated successfully")
    print(f"  Last updated: {data['last_updated']}")


def recalculate_summary(data):
    """Recalculate summary totals from sources and expenses"""
    total_raised = sum(source['amount'] for source in data['sources'])
    total_spent = sum(expense['amount'] for expense in data['expenses'] if expense['amount'] > 0)
    balance = total_raised - total_spent

    data['summary'] = {
        'total_raised': total_raised,
        'total_spent': total_spent,
        'balance': balance
    }

    # Recalculate budgeted amounts based on total raised
    for alloc in data['allocations']:
        alloc['budgeted_amount'] = round(total_raised * (alloc['budgeted_percent'] / 100), 2)

    return data


def cmd_update_source(data, args):
    """Update amount for existing source"""
    if len(args) < 2:
        print("Usage: update-source <source_name> <new_amount>")
        sys.exit(1)

    source_name = args[0]
    try:
        new_amount = float(args[1])
    except ValueError:
        print(f"Error: Invalid amount '{args[1]}'")
        sys.exit(1)

    # Find and update source
    found = False
    for source in data['sources']:
        if source['name'].lower() == source_name.lower():
            old_amount = source['amount']
            source['amount'] = new_amount
            source['status'] = 'active'
            found = True
            print(f"[OK] Updated {source_name}: ${old_amount} -> ${new_amount}")
            break

    if not found:
        print(f"Error: Source '{source_name}' not found")
        print("Available sources:", [s['name'] for s in data['sources']])
        sys.exit(1)

    return recalculate_summary(data)


def cmd_add_expense(data, args):
    """Add new expense"""
    if len(args) < 3:
        print("Usage: add-expense <category> <amount> <description> [--approved-by <name>]")
        sys.exit(1)

    category = args[0]
    try:
        amount = float(args[1])
    except ValueError:
        print(f"Error: Invalid amount '{args[1]}'")
        sys.exit(1)

    description = args[2]
    approved_by = "Siva"  # Default approver

    # Check for --approved-by flag
    if len(args) > 3 and args[3] == '--approved-by' and len(args) > 4:
        approved_by = args[4]

    # Validate category
    valid_categories = [alloc['category'] for alloc in data['allocations']]
    if category not in valid_categories:
        print(f"Error: Invalid category '{category}'")
        print("Valid categories:", valid_categories)
        sys.exit(1)

    # Add expense
    expense = {
        'date': datetime.utcnow().strftime('%Y-%m-%d'),
        'category': category,
        'amount': amount,
        'description': description,
        'approved_by': approved_by,
        'receipt_url': None
    }

    # Remove placeholder if it exists
    if len(data['expenses']) == 1 and data['expenses'][0]['amount'] == 0:
        data['expenses'] = []

    data['expenses'].append(expense)

    # Update category spent amount
    for alloc in data['allocations']:
        if alloc['category'] == category:
            alloc['spent'] += amount
            break

    print(f"[OK] Added expense: ${amount} to {category}")
    print(f"  Description: {description}")
    print(f"  Approved by: {approved_by}")

    return recalculate_summary(data)


def cmd_recalculate(data, args):
    """Recalculate all summary totals"""
    print("Recalculating fund totals...")
    return recalculate_summary(data)


def cmd_status(data, args):
    """Display current fund status"""
    print("\n=== FUND STATUS ===")
    print(f"\nTotal Raised:  ${data['summary']['total_raised']:,.2f}")
    print(f"Total Spent:   ${data['summary']['total_spent']:,.2f}")
    print(f"Balance:       ${data['summary']['balance']:,.2f}")

    print("\n--- Sources ---")
    for source in data['sources']:
        status_icon = "[OK]" if source['status'] == 'active' else "[PENDING]"
        print(f"  {status_icon} {source['name']}: ${source['amount']:,.2f} ({source['status']})")

    print("\n--- Allocations ---")
    for alloc in data['allocations']:
        percent_spent = (alloc['spent'] / alloc['budgeted_amount'] * 100) if alloc['budgeted_amount'] > 0 else 0
        print(f"  {alloc['category']}: ${alloc['spent']:,.2f} / ${alloc['budgeted_amount']:,.2f} ({percent_spent:.1f}%)")

    print(f"\n--- Recent Expenses (last 5) ---")
    recent = data['expenses'][-5:] if data['expenses'] else []
    if not recent or (len(recent) == 1 and recent[0]['amount'] == 0):
        print("  No expenses yet")
    else:
        for expense in reversed(recent):
            print(f"  {expense['date']} | ${expense['amount']:,.2f} | {expense['category']} | {expense['description']}")

    print(f"\nLast Updated: {data['last_updated']}")
    print()


def main():
    if len(sys.argv) < 2:
        print("Fund Data Update Script")
        print("\nCommands:")
        print("  status                           - Show current fund status")
        print("  update-source <name> <amount>    - Update funding source amount")
        print("  add-expense <cat> <amt> <desc>   - Add new expense")
        print("  recalculate                      - Recalculate all totals")
        print("\nExamples:")
        print("  python scripts/update_funds.py status")
        print("  python scripts/update_funds.py update-source 'Change.org' 250")
        print("  python scripts/update_funds.py add-expense 'Media Production' 150 'Lucky photography'")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    # Load current data
    data = load_funds()

    # Route to command handler
    commands = {
        'update-source': cmd_update_source,
        'add-expense': cmd_add_expense,
        'recalculate': cmd_recalculate,
        'status': cmd_status,
    }

    if command not in commands:
        print(f"Error: Unknown command '{command}'")
        print("Run without arguments to see usage")
        sys.exit(1)

    # Execute command
    result = commands[command](data, args)

    # Save if data was modified (status doesn't modify)
    if command != 'status' and result is not None:
        save_funds(result)


if __name__ == '__main__':
    main()
