## Product Catalog Schema

This directory contains mock data for the product catalog used by the terminal demo.

File: `products.json`

Schema (per product):
- `id` (string): Stable product identifier.
- `name` (string): Display name.
- `category` (string): High-level category (e.g., "Headphones").
- `shortDescription` (string): Brief marketing copy.
- `specs` (object): Key-value specs (e.g., batteryLifeHours, weightGrams, connectivity).
- `variants` (array): Variant objects with:
  - `sku` (string): Unique variant identifier.
  - `attributes` (object): Variant attributes (e.g., color, size/capacity).
  - `listPrice` (number): Base price in USD cents.
  - `currency` (string): ISO 4217 code (e.g., "USD").
- `tags` (array<string>): Keywords for search/recommendations.

Notes:
- Prices use integer minor units (cents) for simplicity.
- Variant `attributes` are flexible to accommodate color/size/capacity.
- Additional fields can be added later (e.g., images) without breaking consumers.


