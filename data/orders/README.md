## Order Ledger

Files:
- `orders.json`: array of orders created by the demo flow.

Order schema (simplified):
- `orderId` (string)
- `items` (array): [{"sku": str, "quantity": int, "unitPriceCents": int}]
- `destinationCity` (string|null)
- `destinationCountry` (string|null)
- `breakdown` (object): price breakdown snapshot
- `status` (string): one of ["received", "packed", "shipped", "delivered"]
- `createdAt` (ISO 8601 string)


