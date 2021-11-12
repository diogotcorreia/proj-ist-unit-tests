package ggctests;

import ggctests.utils.PoUILibTest;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class BreakdownTest extends PoUILibTest {

    public BreakdownTest() {
        super(true);
    }

    @Override
    protected void setupWarehouseManager() {

    }

    @Test
    @DisplayName("A-15-01-M-ok - Fazer desagregação de produto inexistente e com Parceiro inexistente")
    void breakdownWithUnknownProductAndPartner() {
        loadFromInputFile("test037.input");
        this.interaction.addMenuOptions(7, 2);
        this.interaction.addFieldValues("M1", "naoExiste", "10");
        this.interaction.addMenuOptions(2);
        this.interaction.addFieldValues("MM1", "garrafa", "10");
        this.interaction.addMenuOptions(1);
        this.interaction.addFieldValues("0");

        this.runApp();

        assertThrownCommandException("UnknownProductKeyException", "O produto 'naoExiste' não existe.");
        assertThrownCommandException("UnknownPartnerKeyException", "O parceiro 'MM1' não existe.");
        assertThrownCommandException("UnknownTransactionKeyException", "A transacção '0' não existe.");
        assertNoMoreExceptions();
        assertEquals("", this.interaction.getResult());
    }

    @Test
    @DisplayName("A-15-02-M-ok - Fazer desagregação de produto simples")
    void breakdownOfSimpleProduct() {
        loadFromInputFile("test037.input");
        this.interaction.addMenuOptions(7, 2, 1, 0);
        this.interaction.addFieldValues("M1", "SAL", "20", "0");
        this.interaction.addMenuOptions(5, 2, 0, 6, 1);
        this.interaction.addFieldValues("M1");

        this.runApp();

        assertThrownCommandException("UnknownTransactionKeyException", "A transacção '0' não existe.");
        assertNoMoreExceptions();
        assertEquals("""
                GARRAFA|S1|1000|500
                HIDROGENIO|S1|200|5000
                ROLHA|M1|30|500
                ROLHA|R1|20|500
                SAL|S1|1000|500
                VIDRO|M1|1000|500
                M1|Rohit Figueiredo|New Delhi, India|NORMAL|0|0|0|0""", this.interaction.getResult());
    }

    @Test
    @DisplayName("A-15-06-M-ok - Fazer desagregação de produto agregado com quantidade insuficiente")
    void breakdownOfDerivedProductWithoutEnoughStock() {
        loadFromInputFile("test038.input");
        this.interaction.addMenuOptions(7, 2, 0);
        this.interaction.addFieldValues("R1", "GARRAFA", "6");
        this.interaction.addMenuOptions(5, 1, 0, 7, 1, 0, 6, 1);
        this.interaction.addFieldValues("0", "R1");

        this.runApp();

        assertThrownCommandException("UnavailableProductException", "Produto 'GARRAFA': pedido=6, existências=5");
        assertThrownCommandException("UnknownTransactionKeyException", "A transacção '0' não existe.");
        assertNoMoreExceptions();
        assertEquals("""
                GARRAFA|200|5|0.1|ROLHA:1#SAL:5#VIDRO:10
                HIDROGENIO|200|5000
                ROLHA|2|500
                SAL|16|500
                VIDRO|10|500
                R1|António Figueiredo|Lisboa|NORMAL|0|0|0|0""", this.interaction.getResult());
    }

    @Test
    @DisplayName("Breakdown of derived product")
    void breakdownOfDerivedProduct() {
        loadFromInputFile("test038.input");
        this.interaction.addMenuOptions(7, 2, 0);
        this.interaction.addFieldValues("R1", "GARRAFA", "5");
        this.interaction.addMenuOptions(5, 1, 0, 7, 1, 0, 6, 1);
        this.interaction.addFieldValues("0", "R1");

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("""
                GARRAFA|200|0|0.1|ROLHA:1#SAL:5#VIDRO:10
                HIDROGENIO|200|5000
                ROLHA|2|505
                SAL|16|525
                VIDRO|10|550
                DESAGREGAÇÃO|0|R1|GARRAFA|5|90|90|0|ROLHA:5:10#SAL:25:400#VIDRO:50:500
                R1|António Figueiredo|Lisboa|NORMAL|900|0|0|0""", this.interaction.getResult());
    }
}
