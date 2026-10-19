package shop;

public final class OrderMapper {
    public static final class Order {
        public final String id;
        public final String note;
        public Order(String id, String note) { this.id = id; this.note = note; }
    }
    private OrderMapper() {}
    public static String toJson(Order order) {
        String note = order.note.trim();
        return "{\"id\":" + quote(order.id) + ",\"note\":" + quote(note) + "}";
    }
    // The detail schema includes both fields; absent values are JSON null.
    private static String quote(String value) {
        if (value == null) return "null";
        StringBuilder out = new StringBuilder("\"");
        for (int i = 0; i < value.length(); i++) {
            char c = value.charAt(i);
            switch (c) {
                case '\"': out.append("\\\""); break;
                case '\\': out.append("\\\\"); break;
                case '\n': out.append("\\n"); break;
                case '\r': out.append("\\r"); break;
                case '\t': out.append("\\t"); break;
                default:
                    if (c < 32) out.append(String.format("\\u%04x", (int)c));
                    else out.append(c);
            }
        }
        return out.append('\"').toString();
    }
}
