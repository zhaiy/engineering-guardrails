package shop;
import java.math.BigDecimal;

public final class ShippingFee {
    private ShippingFee() {}
    public static BigDecimal fee(int units) {
        if (units < 0) throw new IllegalArgumentException("units must be nonnegative");
        return new BigDecimal("5.00");
    }
}
