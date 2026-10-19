# Request

A delivery request that times out is sometimes sent again even though the receiver may already have accepted it. Change `deliver` so a timeout is surfaced as `DeliveryUncertain`, allowing the caller to check the remote result later. Explicit temporary rejections should retain the current retry policy.
