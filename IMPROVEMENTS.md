# SQL Query Generation Pipeline Improvements

## Problem Statement

The original pipeline had a critical issue: the intent parser returned only `{"intent": "show_balance"}` without any context (e.g., whose balance, what time range), making the SQL generator unable to form correct queries.

**Original Error Example:**
```
USER QUERY: what's bank balance for rahul

INTENT: {'intent': 'show_balance'}

Generated SQL: SELECT balance FROM users WHERE name = 'show_balance';
# ^ WRONG! It's using the intent name as the user's name

RAW DATABASE RESULT: []

FORMATTED RESPONSE: Your current account balance is ₹[
# ^ Incomplete and malformed
```

## Solution Overview

Implemented a hybrid pipeline with:
1. **Structured intent extraction** - Parse both intent AND entities
2. **Deterministic SQL generation** - No LLM-based guessing, pure Python logic
3. **Raw data passing** - Keep database rows in their native format
4. **Smart formatting** - Handle multiple result types correctly

## Changes Made

### 1. Enhanced Intent Parser (`app/intent_parser.py`)

**Before:** Only returned intent name
```python
{"intent": "show_balance"}
```

**After:** Returns structured JSON with entities
```python
{
  "intent": "show_balance",
  "target_name": "Rahul",      # Extracted if mentioned
  "time_range": "this month",  # Extracted if mentioned
  "limit": 5                   # Default or extracted
}
```

**Key improvements:**
- Extract named entities (target_name) from natural language
- Support time_range parsing for temporal queries
- Support limit extraction for transaction counts
- LLM still used for high-level classification (kept reliable part)
- Fallback pattern matching for entity extraction

---

### 2. Deterministic SQL Generator (`app/sql_generator.py`)

**Before:** LLM tried to infer everything
```python
# LLM receives only {"intent":"show_balance"}
# and guesses what user wanted → Wrong SQL
```

**After:** Python-based deterministic logic
```python
def generate_sql(intent_data):
    intent = intent_data.get("intent")
    target_name = intent_data.get("target_name")
    
    if intent == "show_balance":
        if target_name:
            return f"SELECT ... FROM users WHERE name = '{target_name}';"
        else:
            return "SELECT ... FROM users LIMIT 1;"
```

**Supported intents:**
- `show_balance` - Balance for user or named person
- `account_info` - Full account details
- `last_transactions` - Recent N transactions
- `money_sent` - Money sent to target (with target_name)
- `money_received` - Money received from target (with target_name)
- `monthly_spending` - Sum of spending this month

**Benefits:**
- Eliminates hallucination errors
- Consistent, predictable SQL generation
- Faster (no LLM latency)
- Easier to debug

---

### 3. Fixed Query Processing (`app/process_query.py`)

**Before:** Stringified database results
```python
result = run_query(sql)
return str(result)  # Returns "[(1, 'Rahul', 'ACC123456', 50000)]"
```

**After:** Returns raw rows
```python
rows = run_query(sql)
return rows  # Returns raw tuple list for proper parsing
```

**Why this matters:** The formatter needs structured data (tuples/lists), not string representations.

---

### 4. Improved Response Formatter (`app/response_formatter.py`)

**Before:** Assumed specific data structures, would fail on strings
```python
balance = db_result[0][0]  # Fails if db_result was a string
return f"Your current account balance is ₹{balance}"
```

**After:** Handles multiple result types correctly
```python
def format_response(intent_data, db_rows):
    intent = intent_data.get("intent")
    target_name = intent_data.get("target_name")
    
    if not db_rows:
        return "No balance information found."
    
    if intent == "show_balance":
        row = db_rows[0]
        balance = row[3]  # Index into tuple
        name = row[1]
        
        if target_name:
            return f"{name}'s current account balance is ₹{balance}"
        else:
            return f"Your current account balance is ₹{balance}"
```

**Format types handled:**
- Empty results → user-friendly "not found" messages
- Balance queries → User or person-specific responses
- Single transactions → Formatted transaction details
- Multiple transactions → Numbered list of transactions
- Money sent/received → Aggregated summary
- Monthly spending → Total + transaction count
- NULL values → Graceful fallback

---

## Example Flow Comparison

### Before (Broken)
```
User: "What's the balance for Rahul?"
↓
Intent: {"intent": "show_balance"}  ← No target_name!
↓
SQL: SELECT balance FROM users WHERE name = 'show_balance';  ← WRONG
↓
Result: []
↓
Output: "Your current account balance is ₹["  ← BROKEN
```

### After (Fixed)
```
User: "What's the balance for Rahul?"
↓
Intent: {"intent": "show_balance", "target_name": "Rahul"}  ← Entity extracted!
↓
SQL: SELECT id, name, account_number, balance FROM users WHERE name = 'Rahul';  ← CORRECT
↓
Result: [(1, "Rahul", "ACC123456", 50000)]
↓
Output: "Rahul's current account balance is ₹50000"  ← WORKS!
```

---

## Dependencies

Added `python-dateutil` to `requirements.txt` for date range calculations (monthly spending).

---

## Testing

Created validation test suite:
- `test_sql_gen.py` - SQL generation correctness
- `validate_pipeline.py` - Response formatting for all intent types
- `test_new_pipeline.py` - End-to-end pipeline flow

All tests verify:
- Empty result handling
- Correct field extraction from rows
- Proper currency formatting
- Date formatting
- Summary aggregation

---

## Files Modified

| File | Changes |
|------|---------|
| `app/intent_parser.py` | Enhanced to extract entities |
| `app/sql_generator.py` | Replaced LLM with deterministic Python logic |
| `app/process_query.py` | Returns raw rows instead of stringified |
| `app/response_formatter.py` | Handles raw row data correctly |
| `requirements.txt` | Added python-dateutil |

---

## Backward Compatibility

The main.py route `/ask` still returns the same API response format:
```json
{
  "success": true,
  "query": "What's the balance for Rahul?",
  "intent": {"intent": "show_balance", "target_name": "Rahul"},
  "response": "Rahul's current account balance is ₹50000"
}
```

The improvement is internal only - external API contract unchanged.

---

## Next Steps (Optional)

1. **Authentication**: Add user context to distinguish "my balance" from "their balance"
2. **Date parsing**: Enhance time_range extraction for natural language dates
3. **Error handling**: Add SQL injection prevention for production
4. **Caching**: Cache frequently accessed balances/account info
5. **Logging**: Add structured logging for debugging
6. **More intents**: Add support for new query types (recurring payments, budget alerts, etc.)
