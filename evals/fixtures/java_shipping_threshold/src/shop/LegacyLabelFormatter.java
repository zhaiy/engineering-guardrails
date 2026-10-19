package shop;

/** Still used by a warehouse label printer with fixed-width fields. */
public final class LegacyLabelFormatter {
    private LegacyLabelFormatter() {}
    public static String format(String value) {
        if (value == null) return "000000";
        String v = value.trim();
        if (v.length() > 6) return v.substring(0, 6);
        while (v.length() < 6) v = "0" + v;
        return v;
    }
}
