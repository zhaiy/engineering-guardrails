# Request

The catalog page sometimes shows “product not found” when the product store is down. Fix `ProductService.find` so callers can distinguish a missing product from a failed lookup. A product that is genuinely absent should still be represented as an empty optional.
