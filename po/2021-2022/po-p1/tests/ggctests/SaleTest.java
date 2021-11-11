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

}
