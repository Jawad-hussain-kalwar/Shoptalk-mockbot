## Inventory Schema

File: `inventory.json`

Represents stock by SKU (variant-level). Intended for `CheckInventory` tool.

Schema (per entry):
- `sku` (string): Variant SKU from the product catalog.
- `stock` (integer): Units available.
- `restockEtaDays` (integer|null): Estimated days to restock if currently 0; null if unknown/not applicable.

Notes:
- Entries may be omitted for discontinued SKUs (treated as unavailable).
- `stock` is a snapshot for the demo; real systems would lock/re-validate during order creation.


