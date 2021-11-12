package ggctests;

import ggctests.utils.PoUILibTest;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class SaleTest extends PoUILibTest {

    public SaleTest() {
      super(true);
    }

    @Override
    protected void setupWarehouseManager() {
    }

    @Test
    @DisplayName("A-19-02-M-ok - Fazer compra de produto simples com quantidade insuficiente")
    void sellSimpleProductWithInsufficientQuantity() {
        loadFromInputFile("test043.input");
        this.interaction.addMenuOptions(7, 3, 3, 1, 1);
        this.interaction.addFieldValues("M1", "2", "VIDRO", "30", "M1", "2", "VIDRO", "40", "0", "1");

        this.runApp();

        assertThrownCommandException("UnavailableProductException", "Produto 'VIDRO': pedido=40, existências=20");
        assertThrownCommandException("UnknownTransactionKeyException", "A transacção '1' não existe.");
        assertNoMoreExceptions();
        assertEquals("VENDA|0|M1|VIDRO|30|30|30|2", this.interaction.getResult());
    }

    @Test
    @DisplayName("A-19-04-M-ok - Fazer compra de produto agregado com quantidade insuficiente no 2º componente")
    void sellDerivedProductWithUnsufficientQuantityOnSecondComponent() {
        loadFromInputFile("test044.input");
        this.interaction.addMenuOptions(7, 3, 1);
        this.interaction.addFieldValues("m1", "2", "GARRAFA", "20", "0");

        this.runApp();

        assertThrownCommandException("UnavailableProductException", "Produto 'VIDRO': pedido=85, existências=45");
        assertThrownCommandException("UnknownTransactionKeyException", "A transacção '0' não existe.");
        assertNoMoreExceptions();
        assertEquals("", this.interaction.getResult());
    }

    @Test
    @DisplayName("A-19-05-M-ok - Fazer compra de produto agregado com quantidade insuficiente no 1º componente")
    void sellDerivedProductWithUnsufficientQuantityOnFirstComponent() {
        loadFromInputFile("test045.input");
        this.interaction.addMenuOptions(7, 3, 1);
        this.interaction.addFieldValues("S1", "2", "GARRAFA", "10", "0");

        this.runApp();

        assertThrownCommandException("UnavailableProductException", "Produto 'ROLHA': pedido=80, existências=75");
        assertThrownCommandException("UnknownTransactionKeyException", "A transacção '0' não existe.");
        assertNoMoreExceptions();
        assertEquals("", this.interaction.getResult());
    }

    @Test
    @DisplayName("A-19-06-M-ok - Fazer compra de produto agregado com agregação")
    void sellDerivedProductWithAggregation() {
        loadFromInputFile("test046.input");
        this.interaction.addMenuOptions(7, 3, 1, 0);
        this.interaction.addFieldValues("M1", "2", "GARRAFA", "4", "0");
        this.interaction.addMenuOptions(5, 1); // list products

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("""
                VENDA|0|M1|GARRAFA|4|81|81|2
                GARRAFA|28|0|0.1|ROLHA:10#VIDRO:5
                ROLHA|2|55
                SAL|40|500
                VIDRO|1|35""", this.interaction.getResult());
    }

    /**
     * This tests an edge case of selling derived products requiring aggregation, which most likely won't be tested by the official tests.
     * A visualization of the problem can be found here: https://user-images.githubusercontent.com/56204853/141300485-53925ecb-4b1b-4965-8e2f-96abf5e5af1e.png
     * If you're failing this test, it's because the batches were changed even though you didn't have enough stock.
     */
    @Test
    @DisplayName("Attempt sell without stock of derived product composed of derived products that share the same simple product")
    void sellDerivedProductWithNestedDerivedProductSharingTheSameSimpleProductInsufficientQuantity() {
        loadFromInputFile("test047.input");
        this.interaction.addMenuOptions(7, 3, 1, 0);
        this.interaction.addFieldValues("QUI", "2", "H2OOH", "3", "0"); // sale
        this.interaction.addMenuOptions(5, 1); // list products

        this.runApp();

        assertThrownCommandException("UnavailableProductException", "Produto 'H': pedido=3, existências=2");
        assertThrownCommandException("UnknownTransactionKeyException", "A transacção '0' não existe.");
        assertNoMoreExceptions();
        assertEquals("""
                H|10|2
                H2O|30|1|0.1|H:2#O:1
                H2OOH|25|1|0.3|H2O:1#OH:1
                O|50|5
                OH|20|1|0.2|O:1#H:1""", this.interaction.getResult());
    }

}
