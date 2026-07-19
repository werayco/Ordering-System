import asyncio
import json
import os
from pathlib import Path
from datetime import datetime, timezone
import asyncpg
from dotenv import load_dotenv

load_dotenv()

RAW_DATABASE_URL = os.environ["DATABASE_URL"]
DATABASE_URL = RAW_DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://").replace("@postgres", "@localhost")
INVENTORY_JSON_PATH = Path(__file__).parent / "inventory.json"

UPSERT_QUERY = """
INSERT INTO inventory (name, description, price, sku, quantity, is_active, created_at, updated_at)
VALUES ($1, $2, $3, $4, $5, $6, $7, $7)
ON CONFLICT (sku) DO UPDATE SET
    name        = EXCLUDED.name,
    description = EXCLUDED.description,
    price       = EXCLUDED.price,
    quantity    = EXCLUDED.quantity,
    is_active   = EXCLUDED.is_active,
    updated_at  = EXCLUDED.updated_at;
"""

async def seed() -> None:
    if not INVENTORY_JSON_PATH.exists():
        raise FileNotFoundError(f"Could not find {INVENTORY_JSON_PATH}")
    
    with open(INVENTORY_JSON_PATH, "r", encoding="utf-8") as f:
        items = json.load(f)

    if not isinstance(items, list):
        raise ValueError("inventory.json must contain a JSON array of inventory items")

    conn = await asyncpg.connect(DATABASE_URL)
    try:
        now = datetime.now(timezone.utc)
        inserted, skipped = 0, 0

        for item in items:
            try:
                sku = item["sku"]
                name = item["name"]
                price = item["price"]
                quantity = item["quantity"]
            except KeyError as e:
                print(f"Skipping item, missing required field {e}: {item}")
                skipped += 1
                continue

            description = item.get("description")
            is_active = item.get("is_active", True)

            await conn.execute(
                UPSERT_QUERY,
                name,
                description,
                price,
                sku,
                quantity,
                is_active,
                now,
            )
            inserted += 1

        print(f"Seed complete: {inserted} upserted, {skipped} skipped.")
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(seed())