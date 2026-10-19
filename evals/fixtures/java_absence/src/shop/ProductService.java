package shop;
import java.util.Optional;

public final class ProductService {
    public interface Store { String read(String sku); }
    private final Store store;
    public ProductService(Store store) { this.store = store; }
    public Optional<String> find(String sku) {
        try {
            return Optional.ofNullable(store.read(sku));
        } catch (RuntimeException failure) {
            return Optional.empty();
        }
    }
}
