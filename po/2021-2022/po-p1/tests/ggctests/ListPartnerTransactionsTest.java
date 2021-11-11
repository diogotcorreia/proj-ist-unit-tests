package ggctests;

import ggctests.utils.PoUILibTest;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class ListPartnerTransactionsTest extends PoUILibTest {

    public ListPartnerTransactionsTest() {
      super(true);
    }

    @Override
    protected void setupWarehouseManager() {
    }

    @Test
    @DisplayName("A-17-01-M-ok - Mostrar de parceiro não existente e sem transacções de compra")
    void showAcquisitionsOfUnknownPartnerAndPartnerWithoutAcquisitions() {
        loadFromInputFile("test033.input");
        this.interaction.addMenuOptions(6, 5, 5);
        this.interaction.addFieldValues("M4", "M1");

        this.runApp();

        assertThrownCommandException("UnknownPartnerKeyException", "O parceiro 'M4' não existe.");
        assertNoMoreExceptions();
        assertEquals("", this.interaction.getResult());
    }

    @Test
    @DisplayName("A-17-02-M-ok - Mostrar de parceiro existente e com uma compra")
    void showAcquisitionsOfPartnerWithSingleAcquisition() {
        loadFromInputFile("test033.input");
        this.interaction.addMenuOptions(7, 4, 0);
        this.interaction.addFieldValues("M1", "SAL", "23", "23"); // acquisition
        this.interaction.addMenuOptions(6, 5, 5);
        this.interaction.addFieldValues("M2", "M1");

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("COMPRA|0|M1|SAL|23|529|0", this.interaction.getResult());
    }

    @Test
    @DisplayName("A-17-03-M-ok - Mostrar de parceiros existentes e com várias compras")
    void showAcquisitionsOfPartnerWithMultipleAcquisitions() {
        loadFromInputFile("test033.input");
        this.interaction.addMenuOptions(3, 4);
        this.interaction.addFieldValues("1"); // see and advance date
        this.interaction.addMenuOptions(7, 4, 4, 0);
        this.interaction.addFieldValues("M1", "SAL", "10", "10", "M1", "SAL", "10", "20"); // acquisitions
        this.interaction.addMenuOptions(4);
        this.interaction.addFieldValues("1"); // advance date
        this.interaction.addMenuOptions(7, 4, 0);
        this.interaction.addFieldValues("M2", "VIDRO", "10", "10"); // acquisition
        this.interaction.addMenuOptions(4);
        this.interaction.addFieldValues("3"); // advance date
        this.interaction.addMenuOptions(7, 4, 4, 0);
        this.interaction.addFieldValues("M1", "SAL", "10", "30", "M2", "VIDRO", "10", "40"); // acquisitions
        this.interaction.addMenuOptions(6, 5, 5, 5);
        this.interaction.addFieldValues("S1", "M1", "M2"); // show acquisitions of partner

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("""
                Data actual: 0
                COMPRA|0|M1|SAL|10|100|1
                COMPRA|1|M1|SAL|20|200|1
                COMPRA|3|M1|SAL|30|300|5
                COMPRA|2|M2|VIDRO|10|100|2
                COMPRA|4|M2|VIDRO|40|400|5""", this.interaction.getResult());
    }

    @Test
    @DisplayName("A-18-02-M-ok - Mostrar de parceiro existente e com uma venda")
    void showSalesOfPartnerWithSingleSale() {
        loadFromInputFile("test033.input");
        this.interaction.addMenuOptions(4);
        this.interaction.addFieldValues("9"); // advance date
        this.interaction.addMenuOptions(7, 3, 0);
        this.interaction.addFieldValues("S1", "10", "SAL", "10"); // sale
        this.interaction.addMenuOptions(6, 6, 6);
        this.interaction.addFieldValues("S1", "M1"); // show sales and breakdowns of partner

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("VENDA|0|S1|SAL|10|1000|1000|10", this.interaction.getResult());
    }

    @Test
    @DisplayName("A-18-03-M-ok - Mostrar de parceiro existente e com uma desagregação com valor positivo")
    void showBreakdownsOfPartnerWithPositivelyValuedBreakdown() {
        loadFromInputFile("test042.input");
        this.interaction.addMenuOptions(7, 2, 0);
        this.interaction.addFieldValues("M2", "GARRAFA", "5"); // breakdown
        this.interaction.addMenuOptions(6, 6, 6);
        this.interaction.addFieldValues("M1", "M2"); // show sales and breakdowns of partner

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("DESAGREGAÇÃO|0|M2|GARRAFA|5|30|30|0|ROLHA:5:10#VIDRO:10:10", this.interaction.getResult());
    }

}
