package shop;
import java.math.BigDecimal;

public final class InvoiceAmounts {
    private InvoiceAmounts() {}
    /** Missing amounts cannot be reconciled, including two missing amounts. */
    public static boolean matches(BigDecimal expected, BigDecimal actual) {
        return expected != null && actual != null && expected.equals(actual);
    }
    public static String display(BigDecimal amount) {
        return amount == null ? "--" : amount.toPlainString();
    }
}
